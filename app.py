import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title='Stock Variance Analyzer',
    layout='wide'
)

# ==================================================
# STYLE
# ==================================================
st.markdown(
    '''
    <style>
    .stApp {
        background: linear-gradient(180deg,#F8FAFC 0%,#EEF2FF 100%);
    }

    div[data-testid="metric-container"] {
        padding:18px;
        border-radius:18px;
        box-shadow:0 6px 16px rgba(0,0,0,0.08);
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg,#4338CA,#6366F1);
        color:white;
        border:none;
        border-radius:12px;
        font-weight:700;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# ==================================================
# LOGIN SYSTEM
# ==================================================
VALID_USERNAME = 'rachmat79'
VALID_PASSWORD = '591979'

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def do_login():
    input_user = st.session_state.get('login_username', '')
    input_pass = st.session_state.get('login_password', '')

    if input_user == VALID_USERNAME and input_pass == VALID_PASSWORD:
        st.session_state.authenticated = True
        st.session_state.login_error = False
    else:
        st.session_state.authenticated = False
        st.session_state.login_error = True

def do_logout():
    st.session_state.authenticated = False
    st.session_state.login_username = ''
    st.session_state.login_password = ''

if not st.session_state.authenticated:

    st.markdown(
        '''
        <style>
        div[data-testid="stTextInput"] label p {
            font-size:15px;
            font-weight:600;
            color:#1E293B;
        }
        div[data-testid="stTextInput"] input {
            background-color:#EEF2FF;
            border-radius:12px;
            border:1px solid #C7D2FE;
            padding:12px 14px;
            font-size:15px;
        }
        div.stButton > button {
            background: linear-gradient(135deg,#4338CA,#6366F1);
            color:white;
            border:none;
            border-radius:12px;
            font-weight:700;
            padding:10px 0;
            width:100%;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

    col_left, col_center, col_right = st.columns([1, 1.3, 1])

    with col_center:

        st.markdown(
            '''
            <div style="background: linear-gradient(135deg,#312E81,#4338CA,#6366F1);
                        padding:26px;border-radius:22px;color:white;
                        margin-top:40px;margin-bottom:28px;text-align:center;">
                <h2 style="color:white;margin:0;font-size:26px;">🔒 Stock Variance Analyzer</h2>
                <p style="color:#E0E7FF;margin-top:8px;margin-bottom:0;font-size:14px;">
                    Silakan login untuk mengakses aplikasi
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )

        st.markdown(
            'Username <span style="color:#DC2626;">*</span>',
            unsafe_allow_html=True
        )
        st.text_input(
            'Username',
            key='login_username',
            label_visibility='collapsed',
            placeholder='Masukkan username'
        )

        st.markdown(
            'Password <span style="color:#DC2626;">*</span>',
            unsafe_allow_html=True
        )
        st.text_input(
            'Password',
            key='login_password',
            type='password',
            label_visibility='collapsed',
            placeholder='Masukkan password'
        )

        st.write('')
        st.button('Login', on_click=do_login)

        if st.session_state.get('login_error'):
            st.error('Username atau Password salah. Akses ditolak.')

    st.stop()

# ==================================================
# HEADER
# ==================================================
st.markdown(
    '''
    <div style="background: linear-gradient(135deg,#312E81,#4338CA,#6366F1);
                padding:28px;border-radius:22px;color:white;margin-bottom:24px;">
        <h1 style="color:white;margin:0;font-size:36px;">Stock Variance Analyzer</h1>
        <p style="color:#E0E7FF;font-size:18px;margin-top:10px;margin-bottom:6px;">
            Executive Dashboard Analisa Variance Stock Take
        </p>
        <p style="color:#C7D2FE;font-size:14px;margin:0;font-style:italic;">
            Author : Rachmat Hidayat
        </p>
    </div>
    ''',
    unsafe_allow_html=True
)

# ==================================================
# SIDEBAR - USER INFO & LOGOUT
# ==================================================
with st.sidebar:
    st.markdown(f'👤 **Login sebagai:** `{VALID_USERNAME}`')
    st.button('Logout', on_click=do_logout, use_container_width=True)
    st.markdown('---')

# ==================================================
# FORMAT RUPIAH
# ==================================================
def rupiah(x):
    return f'Rp {x:,.0f}'

# ==================================================
# UPLOAD FILE
# ==================================================
uploaded_file = st.file_uploader(
    'Upload file stock take (Excel atau CSV)',
    type=['xlsx', 'csv']
)

if uploaded_file is not None:

    if uploaded_file.name.lower().endswith('.csv'):
        raw_df = pd.read_csv(uploaded_file, sep=None, engine='python')
    else:
        raw_df = pd.read_excel(uploaded_file)

    st.success('File berhasil dibaca')

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
        st.stop()

    numeric_cols = [
        'SOH Qty',
        'Qty Counted',
        'Stock Take Variance Qty',
        'Stock Take Variance Value'
    ]

    for col in numeric_cols:
        raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce').fillna(0)

    tab_dashboard, tab_report = st.tabs([
        'Executive Dashboard',
        'Stock Variance Report'
    ])
    # ==================================================
    # EXECUTIVE DASHBOARD
    # ==================================================
    with tab_dashboard:

        store_option = st.selectbox(
            'Pilih Store',
            ['ALL'] + sorted(raw_df['Store'].dropna().unique().tolist())
        )

        df = raw_df.copy()

        if store_option != 'ALL':
            df = df[df['Store'] == store_option]

        total_variance = df['Stock Take Variance Value'].sum()
        total_loss = df[df['Stock Take Variance Value'] < 0]['Stock Take Variance Value'].sum()
        total_plus = df[df['Stock Take Variance Value'] > 0]['Stock Take Variance Value'].sum()

        st.markdown('## 📊 Ringkasan')

        c1, c2, c3 = st.columns(3)

        c1.metric('Net Variance', rupiah(total_variance))
        c2.metric('Total Loss', rupiah(total_loss))
        c3.metric('Total Plus', rupiah(total_plus))

        st.markdown('---')

        st.markdown('## 📑 Executive Summary by Category')

        summary = (
            df.groupby('Category')
            .agg(
                SOH_Qty=('SOH Qty', 'sum'),
                Counted_Qty=('Qty Counted', 'sum'),
                Diff_Qty=('Stock Take Variance Qty', 'sum'),
                Diff_Value=('Stock Take Variance Value', 'sum')
            )
            .reset_index()
            .sort_values('Diff_Value')
        )

        summary_display = summary.copy()
        summary_display['Diff_Value'] = summary_display['Diff_Value'].apply(rupiah)

        st.dataframe(summary_display, use_container_width=True, height=520)

        st.markdown('### 🧾 Total Summary by Category')

        t1, t2, t3, t4 = st.columns(4)

        t1.metric('Total SOH Qty', f'{summary["SOH_Qty"].sum():,.0f}')
        t2.metric('Total Counted Qty', f'{summary["Counted_Qty"].sum():,.0f}')
        t3.metric('Total Diff Qty', f'{summary["Diff_Qty"].sum():,.0f}')
        t4.metric('Total Diff Value', rupiah(summary['Diff_Value'].sum()))

        st.markdown('---')

        st.markdown('## 📉 Top 15 Loss Category')

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

            fig_loss.update_traces(
                texttemplate='Rp %{x:,.0f}',
                textposition='outside'
            )

            fig_loss.update_layout(
                showlegend=False,
                height=600,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )

            st.plotly_chart(fig_loss, use_container_width=True)

        st.markdown('---')

        st.markdown('## 📈 Top 15 Plus Category')

        top_plus_cat = summary[summary['Diff_Value'] > 0].sort_values(
            'Diff_Value',
            ascending=False
        ).head(15)

        if not top_plus_cat.empty:
            fig_plus = px.bar(
                top_plus_cat,
                x='Diff_Value',
                y='Category',
                orientation='h',
                text='Diff_Value',
                color_discrete_sequence=['#10B981']
            )

            fig_plus.update_traces(
                texttemplate='Rp %{x:,.0f}',
                textposition='outside'
            )

            fig_plus.update_layout(
                showlegend=False,
                height=600,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )

            st.plotly_chart(fig_plus, use_container_width=True)

        st.markdown('---')

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
                'Plus': '#10B981'
            }
        )

        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('---')

        st.markdown('## 🔻 Top 10 Loss')

        top_loss = (
            df[df['Stock Take Variance Value'] < 0]
            .sort_values('Stock Take Variance Value')
            .head(10)
        )

        loss_display = top_loss.copy()
        loss_display['Stock Take Variance Value'] = loss_display[
            'Stock Take Variance Value'
        ].apply(rupiah)

        st.dataframe(
            loss_display[
                [
                    'Store',
                    'Category',
                    'Article',
                    'Article Description',
                    'Stock Take Variance Qty',
                    'Stock Take Variance Value'
                ]
            ],
            use_container_width=True
        )

        st.markdown('---')

        st.markdown('## 🔺 Top 10 Plus')

        top_plus = (
            df[df['Stock Take Variance Value'] > 0]
            .sort_values('Stock Take Variance Value', ascending=False)
            .head(10)
        )

        plus_display = top_plus.copy()
        plus_display['Stock Take Variance Value'] = plus_display[
            'Stock Take Variance Value'
        ].apply(rupiah)

        st.dataframe(
            plus_display[
                [
                    'Store',
                    'Category',
                    'Article',
                    'Article Description',
                    'Stock Take Variance Qty',
                    'Stock Take Variance Value'
                ]
            ],
            use_container_width=True
        )

        st.markdown('---')

        st.markdown('## 📋 Data Lengkap')

        data_lengkap_display = df.copy()
        data_lengkap_display['Stock Take Variance Value'] = (
            data_lengkap_display['Stock Take Variance Value']
            .apply(rupiah)
        )

        st.dataframe(
            data_lengkap_display[
                [
                    'Store',
                    'Category',
                    'Article',
                    'Article Description',
                    'SOH Qty',
                    'Qty Counted',
                    'Stock Take Variance Qty',
                    'Stock Take Variance Value'
                ]
            ],
            use_container_width=True,
            height=500
        )

        st.caption(f'Total data ditampilkan: {len(data_lengkap_display):,} baris')

        st.markdown('---')

        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data Lengkap', index=False)
            summary.to_excel(writer, sheet_name='Summary Category', index=False)
            top_loss.to_excel(writer, sheet_name='Top Loss', index=False)
            top_plus.to_excel(writer, sheet_name='Top Plus', index=False)

        st.download_button(
            label='Download Excel Dashboard',
            data=output.getvalue(),
            file_name='Stock_Variance_Dashboard.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    # ==================================================
    # STOCK VARIANCE REPORT
    # ==================================================
    with tab_report:

        st.markdown(
            '<h2 style="background:#1E40AF;color:white;padding:12px;border-radius:8px;">Stock Variance Report</h2>',
            unsafe_allow_html=True
        )

        st.markdown('### Filter')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            report_store = st.selectbox(
                'Location',
                ['ALL'] + sorted(raw_df['Store'].dropna().unique().tolist()),
                key='report_store'
            )

        temp_df = raw_df.copy()

        if report_store != 'ALL':
            temp_df = temp_df[temp_df['Store'] == report_store]

        with col2:
            report_category = st.selectbox(
                'Select Category',
                ['ALL'] + sorted(temp_df['Category'].dropna().unique().tolist()),
                key='report_category'
            )

        if report_category != 'ALL':
            temp_df = temp_df[temp_df['Category'] == report_category]

        with col3:
            report_article = st.selectbox(
                'Select Article',
                ['ALL'] + sorted(temp_df['Article'].astype(str).unique().tolist()),
                key='report_article'
            )

        with col4:
            top_n = st.selectbox(
                'Top Items Filter',
                [10, 20, 30],
                index=2,
                key='top_n'
            )

        variance_type = st.radio(
            'Variance Type',
            ['Loss', 'Plus', '-+'],
            horizontal=True
        )

        report_df = raw_df.copy()

        if report_store != 'ALL':
            report_df = report_df[report_df['Store'] == report_store]

        if report_category != 'ALL':
            report_df = report_df[report_df['Category'] == report_category]

        if report_article != 'ALL':
            report_df = report_df[
                report_df['Article'].astype(str) == report_article
            ]

        if variance_type == 'Loss':
            report_df = report_df[
                report_df['Stock Take Variance Value'] < 0
            ].sort_values(
                'Stock Take Variance Value',
                ascending=True
            ).head(top_n).copy()

        elif variance_type == 'Plus':
            report_df = report_df[
                report_df['Stock Take Variance Value'] > 0
            ].sort_values(
                'Stock Take Variance Value',
                ascending=False
            ).head(top_n).copy()

        else:
            # Variance Type '-+' -> gabungan Top Loss dan Top Plus
            report_loss = report_df[
                report_df['Stock Take Variance Value'] < 0
            ].sort_values(
                'Stock Take Variance Value',
                ascending=True
            ).head(top_n).copy()

            report_plus = report_df[
                report_df['Stock Take Variance Value'] > 0
            ].sort_values(
                'Stock Take Variance Value',
                ascending=False
            ).head(top_n).copy()

            report_loss['Variance Group'] = 'Loss'
            report_plus['Variance Group'] = 'Plus'

            report_df = pd.concat(
                [report_loss, report_plus],
                ignore_index=True
            )

        report_df.insert(0, 'S/N', range(1, len(report_df) + 1))

        if variance_type == '-+':
            display_df = report_df[
                [
                    'S/N',
                    'Variance Group',
                    'Article',
                    'Article Description',
                    'SOH Qty',
                    'Qty Counted',
                    'Stock Take Variance Qty',
                    'Stock Take Variance Value'
                ]
            ].copy()

            display_df.columns = [
                'S/N',
                'Variance Group',
                'Product No.',
                'Article Description',
                'SOH',
                'Counted Qty',
                'Diff Qty',
                'Diff Value'
            ]
        else:
            display_df = report_df[
                [
                    'S/N',
                    'Article',
                    'Article Description',
                    'SOH Qty',
                    'Qty Counted',
                    'Stock Take Variance Qty',
                    'Stock Take Variance Value'
                ]
            ].copy()

            display_df.columns = [
                'S/N',
                'Product No.',
                'Article Description',
                'SOH',
                'Counted Qty',
                'Diff Qty',
                'Diff Value'
            ]

        display_df['Diff Value'] = display_df['Diff Value'].apply(rupiah)

        st.dataframe(display_df, use_container_width=True, height=650)

        st.markdown('### Total')

        total_soh = report_df['SOH Qty'].sum()
        total_counted = report_df['Qty Counted'].sum()
        total_diff_qty = report_df['Stock Take Variance Qty'].sum()
        total_diff_value = report_df['Stock Take Variance Value'].sum()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric('SOH Qty', f'{total_soh:,.0f}')
        c2.metric('Counted Qty', f'{total_counted:,.0f}')
        c3.metric('Diff Qty', f'{total_diff_qty:,.0f}')
        c4.metric('Diff Value', rupiah(total_diff_value))

        st.markdown('---')

        st.write(f'**Printed By:** Rachmat Hidayat')
        st.write(f'**Printed On:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        st.caption('Internal Use – Sensitive Stock Take Variance By Location Report')

        report_output = BytesIO()

        with pd.ExcelWriter(report_output, engine='openpyxl') as writer:
            display_df.to_excel(
                writer,
                sheet_name='Stock Variance Report',
                index=False
            )

        st.download_button(
            label='Download Stock Variance Report',
            data=report_output.getvalue(),
            file_name='Stock_Variance_Report.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

# ==================================================
# FOOTER
# ==================================================
st.markdown('---')
st.caption('Stock Variance Analyzer | Author : Rachmat Hidayat')