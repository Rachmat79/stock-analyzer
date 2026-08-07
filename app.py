import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title='OPAL Variance Analyzer',
    layout='wide'
)

# ==================================================
# CUSTOM THEME PREMIUM
# ==================================================
st.markdown(
    '''
    <style>

    .stApp {
        background-color: #F5F7FB;
    }

    h1 {
        color: #4338CA !important;
        font-weight: 800;
    }

    h2, h3 {
        color: #1E293B !important;
        font-weight: 700;
    }

    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    div[data-testid="metric-container"] label {
        color: #64748B !important;
        font-size: 14px !important;
        font-weight: 600;
    }

    div[data-testid="metric-container"] div {
        color: #0F172A !important;
        font-weight: 800 !important;
    }

    section[data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #C7D2FE;
        border-radius: 16px;
        padding: 16px;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px;
        border-color: #CBD5E1;
    }

    div[data-testid="stDataFrame"] {
        background: white;
        border-radius: 16px;
        padding: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #4338CA, #6366F1);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 18px;
        font-weight: 700;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #3730A3, #4F46E5);
        color: white;
    }

    hr {
        border-top: 1px solid #E2E8F0;
    }

    footer {
        visibility: hidden;
    }

    </style>
    ''',
    unsafe_allow_html=True
)

# ==================================================
# HEADER
# ==================================================
st.title('📦Stock Variance Analyzer')
st.write('Executive Dashboard Analisa Variance Stock Take')
st.write('Author : Rachmat Hidayat')

st.markdown(
    '''
    <div style="
        background: linear-gradient(135deg,#4338CA,#6366F1);
        padding:20px;
        border-radius:18px;
        color:white;
        margin-bottom:20px;
        box-shadow:0 6px 18px rgba(67,56,202,0.25);
    ">
        <h3 style="margin:0;color:white;">📊 Executive Stock Take Dashboard</h3>
        <p style="margin:6px 0 0 0;font-size:15px;">
            Monitoring shrinkage, loss, plus, dan performa inventory store secara real-time.
        </p>
    </div>
    ''',
    unsafe_allow_html=True
)

# ==================================================
# FORMAT RUPIAH
# ==================================================
def rupiah(x):
    return f'Rp {x:,.0f}'

# ==================================================
# UPLOAD FILE EXCEL / CSV
# ==================================================
uploaded_file = st.file_uploader(
    'Upload file stock take (Excel atau CSV)',
    type=['xlsx', 'csv']
)

if uploaded_file is not None:

    file_name = uploaded_file.name.lower()

    if file_name.endswith('.csv'):
        raw_df = pd.read_csv(
            uploaded_file,
            sep=None,
            engine='python'
        )
        st.success('CSV berhasil dibaca')
    else:
        raw_df = pd.read_excel(uploaded_file)
        st.success('Excel berhasil dibaca')

    # ==================================================
    # VALIDASI KOLOM FILE PERUSAHAAN
    # ==================================================
    required_cols = [
        'Store',
        'Category',
        'Article',
        'Article Description',
        'SOH Qty',
        'Qty Counted',
        'Stock Take Variance Qty',
        'Stock Take Variance Value'
    ]

    missing = [c for c in required_cols if c not in raw_df.columns]

    if missing:

        st.error(f'Kolom belum ditemukan: {missing}')
        st.write(raw_df.columns.tolist())

    else:

        df = raw_df[required_cols].copy()

        df.columns = [
            'Store',
            'Category',
            'Article',
            'Article Description',
            'SOH Qty',
            'Qty Counted',
            'Variance Qty',
            'Variance Value'
        ]

        numeric_cols = [
            'SOH Qty',
            'Qty Counted',
            'Variance Qty',
            'Variance Value'
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(
                df[col],
                errors='coerce'
            ).fillna(0)

        # ==================================================
        # FILTER STORE
        # ==================================================
        store_option = st.selectbox(
            'Pilih Store',
            ['ALL'] + sorted(df['Store'].unique().tolist())
        )

        if store_option != 'ALL':
            df = df[df['Store'] == store_option]

        # ==================================================
        # KPI
        # ==================================================
        total_variance = df['Variance Value'].sum()
        total_loss = df[df['Variance Value'] < 0]['Variance Value'].sum()
        total_plus = df[df['Variance Value'] > 0]['Variance Value'].sum()

        st.markdown('## 📊 Ringkasan')

        c1, c2, c3 = st.columns(3)

        c1.metric('Net Variance', rupiah(total_variance))
        c2.metric('Total Loss', rupiah(total_loss))
        c3.metric('Total Plus', rupiah(total_plus))

        st.markdown('---')

        # ==================================================
        # SUMMARY CATEGORY
        # ==================================================
        st.markdown('## 📑 Executive Summary by Category')

        summary = (
            df.groupby('Category')
            .agg(
                SOH_Qty=('SOH Qty', 'sum'),
                Counted_Qty=('Qty Counted', 'sum'),
                Diff_Qty=('Variance Qty', 'sum'),
                Diff_Value=('Variance Value', 'sum')
            )
            .reset_index()
        )

        minus_df = summary[summary['Diff_Value'] < 0].sort_values('Diff_Value')
        plus_df = summary[summary['Diff_Value'] > 0].sort_values('Diff_Value', ascending=False)

        summary = pd.concat([minus_df, plus_df], ignore_index=True)

        summary.insert(0, 'No', range(1, len(summary) + 1))

        total_row = pd.DataFrame([{
            'No': 'TOTAL',
            'Category': 'TOTAL',
            'SOH_Qty': summary['SOH_Qty'].sum(),
            'Counted_Qty': summary['Counted_Qty'].sum(),
            'Diff_Qty': summary['Diff_Qty'].sum(),
            'Diff_Value': summary['Diff_Value'].sum()
        }])

        summary_display = pd.concat([summary, total_row], ignore_index=True)

        summary_display_fmt = summary_display.copy()
        summary_display_fmt['Diff_Value'] = summary_display_fmt['Diff_Value'].apply(rupiah)

        st.dataframe(summary_display_fmt, use_container_width=True, height=520)

        # ==================================================
        # TOTAL SUMMARY
        # ==================================================
        st.markdown('### 📌 Total Summary by Category')

        t1, t2, t3, t4 = st.columns(4)

        t1.metric('Total SOH Qty', f'{summary["SOH_Qty"].sum():,.0f}')
        t2.metric('Total Counted Qty', f'{summary["Counted_Qty"].sum():,.0f}')
        t3.metric('Total Diff Qty', f'{summary["Diff_Qty"].sum():,.0f}')
        t4.metric('Total Diff Value', rupiah(summary['Diff_Value'].sum()))

        st.markdown('---')

        # ==================================================
        # TOP 15 LOSS CATEGORY
        # ==================================================
        st.markdown('## 🔻 Top 15 Loss Category')

        top_loss_cat = summary[summary['Diff_Value'] < 0].head(15)

        if not top_loss_cat.empty:

            fig_loss = px.bar(
                top_loss_cat,
                x='Diff_Value',
                y='Category',
                orientation='h',
                text='Diff_Value',
                color_discrete_sequence=['#DC2626']
            )

            fig_loss.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1E293B'),
                title='Top 15 Loss Category by Variance Value'
            )

            st.plotly_chart(fig_loss, use_container_width=True)

        # ==================================================
        # TOP 15 PLUS CATEGORY
        # ==================================================
        st.markdown('## 🔺 Top 15 Plus Category')

        top_plus_cat = summary[summary['Diff_Value'] > 0].head(15)

        if not top_plus_cat.empty:

            fig_plus = px.bar(
                top_plus_cat,
                x='Diff_Value',
                y='Category',
                orientation='h',
                text='Diff_Value',
                color_discrete_sequence=['#16A34A']
            )

            fig_plus.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1E293B'),
                title='Top 15 Plus Category by Variance Value'
            )

            st.plotly_chart(fig_plus, use_container_width=True)

        st.markdown('---')

        # ==================================================
        # PIE CHART
        # ==================================================
        st.markdown('## 🥧 Komposisi Loss vs Plus')

        pie_df = pd.DataFrame({
            'Kategori': ['Loss', 'Plus'],
            'Nilai': [abs(total_loss), total_plus]
        })

        fig_pie = px.pie(
            pie_df,
            names='Kategori',
            values='Nilai',
            hole=0.55,
            color='Kategori',
            color_discrete_map={
                'Loss': '#DC2626',
                'Plus': '#16A34A'
            }
        )

        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1E293B'),
            title='Komposisi Loss vs Plus'
        )

        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('---')

        # ==================================================
        # TOP 10 LOSS
        # ==================================================
        st.markdown('## 🔻 Top 10 Loss')

        top_loss = (
            df[df['Variance Value'] < 0]
            .sort_values('Variance Value')
            .head(10)
        )

        loss_display = top_loss.copy()
        loss_display['Variance Value'] = loss_display['Variance Value'].apply(rupiah)

        st.dataframe(
            loss_display[
                [
                    'Store',
                    'Category',
                    'Article',
                    'Article Description',
                    'Variance Qty',
                    'Variance Value'
                ]
            ],
            use_container_width=True
        )

        st.markdown('---')

        # ==================================================
        # TOP 10 PLUS
        # ==================================================
        st.markdown('## 🔺 Top 10 Plus')

        top_plus = (
            df[df['Variance Value'] > 0]
            .sort_values('Variance Value', ascending=False)
            .head(10)
        )

        plus_display = top_plus.copy()
        plus_display['Variance Value'] = plus_display['Variance Value'].apply(rupiah)

        st.dataframe(
            plus_display[
                [
                    'Store',
                    'Category',
                    'Article',
                    'Article Description',
                    'Variance Qty',
                    'Variance Value'
                ]
            ],
            use_container_width=True
        )

        st.markdown('---')

        # ==================================================
        # DATA LENGKAP
        # ==================================================
        st.markdown('## 📄 Data Lengkap')

        data_display = df.copy()
        data_display['Variance Value'] = data_display['Variance Value'].apply(rupiah)

        st.dataframe(
            data_display,
            use_container_width=True,
            height=450
        )

        # ==================================================
        # DOWNLOAD EXCEL
        # ==================================================
        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data Lengkap', index=False)
            summary.to_excel(writer, sheet_name='Summary Category', index=False)
            top_loss.to_excel(writer, sheet_name='Top Loss', index=False)
            top_plus.to_excel(writer, sheet_name='Top Plus', index=False)

        st.download_button(
            label='⬇ Download Excel Report',
            data=output.getvalue(),
            file_name='OPAL_Variance_Report.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

# ==================================================
# FOOTER
# ==================================================
st.markdown('---')
st.caption('Inventory Intelligence | Developed by Rachmat Hidayat')
