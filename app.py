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
# STYLE — Light Purple Glassmorphism Theme
# ==================================================
st.markdown(
    '''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ---------- Base canvas: soft lavender + ambient purple glow ---------- */
    .stApp {
        background:
            radial-gradient(circle at 8% 6%, rgba(147,51,234,0.14) 0%, rgba(147,51,234,0) 42%),
            radial-gradient(circle at 92% 12%, rgba(217,70,239,0.10) 0%, rgba(217,70,239,0) 40%),
            radial-gradient(circle at 85% 92%, rgba(124,58,237,0.12) 0%, rgba(124,58,237,0) 42%),
            linear-gradient(165deg, #FAF9FF 0%, #F3EEFE 50%, #FBF5FF 100%);
        background-attachment: fixed;
    }

    .stApp, .stApp p, .stApp li, .stApp span, .stApp label {
        color: #4B4468;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Manrope', sans-serif !important;
        color: #241F47 !important;
        letter-spacing: -0.01em;
    }
    h1 { font-weight: 800 !important; }
    h2 { font-weight: 700 !important; font-size: 21px !important; }
    h3 { font-weight: 600 !important; font-size: 17px !important; color:#312A5E !important; }

    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, rgba(147,51,234,0) 0%, rgba(147,51,234,0.28) 50%, rgba(147,51,234,0) 100%) !important;
        margin: 26px 0 !important;
    }

    /* ---------- Reusable glass panel ---------- */
    .glass-panel {
        background: rgba(255,255,255,0.55);
        border: 1px solid rgba(147,51,234,0.16);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(124,58,237,0.10), inset 0 1px 0 rgba(255,255,255,0.7);
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(243,238,254,0.96));
        border-right: 1px solid rgba(147,51,234,0.12);
    }
    section[data-testid="stSidebar"] * { color:#4B4468 !important; }

    /* ---------- Buttons ---------- */
    div.stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg,#7C3AED,#A855F7 55%,#D946EF);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        letter-spacing: 0.01em;
        padding: 10px 18px;
        box-shadow: 0 4px 18px rgba(147,51,234,0.30);
        transition: all .2s ease;
    }
    div.stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 26px rgba(147,51,234,0.42);
        filter: brightness(1.06);
    }

    /* ---------- Metric cards ---------- */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.6);
        border: 1px solid rgba(147,51,234,0.15);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-radius: 18px;
        padding: 20px 22px;
        box-shadow: 0 8px 28px rgba(124,58,237,0.08), inset 0 1px 0 rgba(255,255,255,0.7);
        overflow: visible !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8A82AD !important;
        text-transform: uppercase;
        font-size: 11.5px !important;
        letter-spacing: 0.08em;
        font-weight: 700 !important;
    }
    /* Fix: nilai metric (mis. Total Diff Value) tidak lagi terpotong/ellipsis */
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #241F47 !important;
        font-weight: 600 !important;
        font-size: 19px !important;
        line-height: 1.3 !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: break-word !important;
    }
    div[data-testid="stMetricValue"] > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }

    /* ---------- Tabs ---------- */
    button[data-baseweb="tab"] {
        background: rgba(255,255,255,0.45);
        border-radius: 12px !important;
        color: #8A82AD !important;
        font-weight: 600;
        margin-right: 6px;
        border: 1px solid rgba(147,51,234,0.12) !important;
    }
    button[aria-selected="true"][data-baseweb="tab"] {
        background: linear-gradient(135deg,#7C3AED,#D946EF) !important;
        color: #ffffff !important;
        border: none !important;
    }
    [data-baseweb="tab-highlight"] { display:none; }
    [data-baseweb="tab-border"] { display:none; }

    /* ---------- Radio ---------- */
    div[role="radiogroup"] label { color:#4B4468 !important; font-weight:500; }
    input[type="radio"] { accent-color: #7C3AED; }

    /* ---------- Select / Text Input ---------- */
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background: rgba(255,255,255,0.65) !important;
        border: 1px solid rgba(147,51,234,0.18) !important;
        border-radius: 12px !important;
        color: #241F47 !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(168,85,247,0.6) !important;
        box-shadow: 0 0 0 3px rgba(168,85,247,0.15) !important;
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(255,255,255,0.45);
        border: 1px dashed rgba(147,51,234,0.3);
        border-radius: 16px;
    }

    /* ---------- Dataframe ---------- */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(147,51,234,0.14);
        box-shadow: 0 8px 24px rgba(124,58,237,0.08);
    }

    /* ---------- Alerts ---------- */
    div[data-testid="stAlert"] {
        background: rgba(255,255,255,0.6) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(147,51,234,0.16) !important;
        color: #312A5E !important;
    }

    /* ---------- Scrollbar ---------- */
    ::-webkit-scrollbar { width:8px; height:8px; }
    ::-webkit-scrollbar-thumb { background: rgba(147,51,234,0.32); border-radius:8px; }
    ::-webkit-scrollbar-track { background: transparent; }

    /* ---------- Keyboard focus accessibility ---------- */
    button:focus-visible, input:focus-visible, [tabindex]:focus-visible {
        outline: 2px solid #A855F7 !important;
        outline-offset: 2px;
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

    col_left, col_center, col_right = st.columns([1, 1.3, 1])

    with col_center:

        st.markdown(
            '''
            <div class="glass-panel" style="padding:36px 34px;margin-top:64px;
                        margin-bottom:26px;text-align:center;position:relative;overflow:hidden;">
                <div style="position:absolute;top:-32%;left:-14%;width:220px;height:220px;
                            background:radial-gradient(circle,rgba(217,70,239,0.20),transparent 70%);
                            filter:blur(6px);pointer-events:none;"></div>
                <div style="position:absolute;bottom:-30%;right:-14%;width:200px;height:200px;
                            background:radial-gradient(circle,rgba(124,58,237,0.22),transparent 70%);
                            filter:blur(6px);pointer-events:none;"></div>
                <p style="color:#A855F7;font-size:11.5px;font-weight:700;letter-spacing:0.16em;
                          text-transform:uppercase;margin:0 0 10px 0;position:relative;">Secure Access</p>
                <h2 style="margin:0;font-size:24px;font-weight:800;position:relative;
                           background:linear-gradient(135deg,#4C1D95,#7C3AED 55%,#D946EF);
                           -webkit-background-clip:text;background-clip:text;color:transparent;">
                    Stock Variance Analyzer
                </h2>
                <p style="color:#8A82AD;font-size:13.5px;margin-top:8px;margin-bottom:0;position:relative;">
                    Masuk untuk mengakses dashboard
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )

        st.markdown(
            '<p style="color:#4B4468;font-size:13.5px;font-weight:600;margin-bottom:6px;">'
            'Username <span style="color:#DB2777;">*</span></p>',
            unsafe_allow_html=True
        )
        st.text_input(
            'Username',
            key='login_username',
            label_visibility='collapsed',
            placeholder='Masukkan username'
        )

        st.markdown(
            '<p style="color:#4B4468;font-size:13.5px;font-weight:600;'
            'margin-top:16px;margin-bottom:6px;">'
            'Password <span style="color:#DB2777;">*</span></p>',
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
        st.button('Masuk', on_click=do_login, use_container_width=True)

        if st.session_state.get('login_error'):
            st.error('Username atau Password salah. Akses ditolak.')

    st.stop()

# ==================================================
# HEADER
# ==================================================
st.markdown(
    '''
    <div class="glass-panel" style="padding:34px 38px;margin-bottom:28px;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-45%;right:-8%;width:300px;height:300px;
                    background:radial-gradient(circle,rgba(147,51,234,0.22),transparent 70%);
                    filter:blur(8px);pointer-events:none;"></div>
        <div style="position:absolute;bottom:-60%;left:20%;width:260px;height:260px;
                    background:radial-gradient(circle,rgba(217,70,239,0.14),transparent 70%);
                    filter:blur(8px);pointer-events:none;"></div>
        <h1 style="margin:0;font-size:34px;font-weight:800;position:relative;
                   background:linear-gradient(135deg,#4C1D95,#7C3AED 55%,#D946EF);
                   -webkit-background-clip:text;background-clip:text;color:transparent;">
            Stock Variance Analyzer
        </h1>
        <p style="color:#6D6690;font-size:15px;margin-top:10px;margin-bottom:4px;position:relative;">
            Executive Dashboard Analisa Variance Stock Take
        </p>
        <p style="color:#948FB0;font-size:12.5px;margin:0;font-style:italic;position:relative;">
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
    st.markdown(
        f'''
        <div class="glass-panel" style="padding:14px 16px;margin-bottom:14px;">
            <p style="margin:0;font-size:10.5px;color:#8A82AD;text-transform:uppercase;
                      letter-spacing:0.08em;font-weight:700;">Signed in as</p>
            <p style="margin:5px 0 0 0;font-size:14.5px;color:#241F47;font-weight:700;">
                {VALID_USERNAME}
            </p>
        </div>
        ''',
        unsafe_allow_html=True
    )
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

        st.dataframe(
            summary_display,
            use_container_width=True,
            height=520,
            hide_index=True,
            column_config={
                'Category': st.column_config.TextColumn(width=200),
                'SOH_Qty': st.column_config.TextColumn(label='SOH Qty', width=90),
                'Counted_Qty': st.column_config.TextColumn(label='Counted Qty', width=100),
                'Diff_Qty': st.column_config.TextColumn(label='Diff Qty', width=90),
                'Diff_Value': st.column_config.TextColumn(label='Diff Value', width=120)
            }
        )

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
                color_discrete_sequence=['#FB7185']
            )

            fig_loss.update_traces(
                texttemplate='Rp %{x:,.0f}',
                textposition='outside'
            )

            fig_loss.update_layout(
                showlegend=False,
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#4B4468', family='Manrope'),
                xaxis=dict(gridcolor='rgba(147,51,234,0.10)', zerolinecolor='rgba(147,51,234,0.22)'),
                yaxis=dict(gridcolor='rgba(147,51,234,0.05)')
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
                color_discrete_sequence=['#34D399']
            )

            fig_plus.update_traces(
                texttemplate='Rp %{x:,.0f}',
                textposition='outside'
            )

            fig_plus.update_layout(
                showlegend=False,
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#4B4468', family='Manrope'),
                xaxis=dict(gridcolor='rgba(147,51,234,0.10)', zerolinecolor='rgba(147,51,234,0.22)'),
                yaxis=dict(gridcolor='rgba(147,51,234,0.05)')
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
                'Loss': '#FB7185',
                'Plus': '#34D399'
            }
        )

        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#4B4468', family='Manrope'),
            legend=dict(font=dict(color='#4B4468'))
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

        loss_table = loss_display[
            [
                'Store',
                'Category',
                'Article',
                'Article Description',
                'Stock Take Variance Qty',
                'Stock Take Variance Value'
            ]
        ]

        st.dataframe(
            loss_table,
            use_container_width=True,
            hide_index=True,
            height=int(35.2 * (len(loss_table) + 1)) + 3,
            column_config={
                'Store': st.column_config.TextColumn(width=180),
                'Category': st.column_config.TextColumn(width=160),
                'Article': st.column_config.TextColumn(width=70),
                'Article Description': st.column_config.TextColumn(width=220),
                'Stock Take Variance Qty': st.column_config.TextColumn(
                    label='Variance Qty', width=90
                ),
                'Stock Take Variance Value': st.column_config.TextColumn(
                    label='Variance Value', width=120
                )
            }
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

        plus_table = plus_display[
            [
                'Store',
                'Category',
                'Article',
                'Article Description',
                'Stock Take Variance Qty',
                'Stock Take Variance Value'
            ]
        ]

        st.dataframe(
            plus_table,
            use_container_width=True,
            hide_index=True,
            height=int(35.2 * (len(plus_table) + 1)) + 3,
            column_config={
                'Store': st.column_config.TextColumn(width=180),
                'Category': st.column_config.TextColumn(width=160),
                'Article': st.column_config.TextColumn(width=70),
                'Article Description': st.column_config.TextColumn(width=220),
                'Stock Take Variance Qty': st.column_config.TextColumn(
                    label='Variance Qty', width=90
                ),
                'Stock Take Variance Value': st.column_config.TextColumn(
                    label='Variance Value', width=120
                )
            }
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
            height=500,
            hide_index=True,
            column_config={
                'Store': st.column_config.TextColumn(width=170),
                'Category': st.column_config.TextColumn(width=150),
                'Article': st.column_config.TextColumn(width=70),
                'Article Description': st.column_config.TextColumn(width=200),
                'SOH Qty': st.column_config.TextColumn(width=80),
                'Qty Counted': st.column_config.TextColumn(width=90),
                'Stock Take Variance Qty': st.column_config.TextColumn(
                    label='Variance Qty', width=90
                ),
                'Stock Take Variance Value': st.column_config.TextColumn(
                    label='Variance Value', width=120
                )
            }
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
            '''
            <div class="glass-panel" style="padding:18px 24px;margin-bottom:22px;">
                <p style="color:#A855F7;font-size:11px;font-weight:700;letter-spacing:0.14em;
                          text-transform:uppercase;margin:0 0 6px 0;">Detail Report</p>
                <h2 style="margin:0;font-size:22px;font-weight:800;color:#241F47;">
                    Stock Variance Report
                </h2>
            </div>
            ''',
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

        report_column_config = {
            'S/N': st.column_config.TextColumn(width=50),
            'Variance Group': st.column_config.TextColumn(width=90),
            'Product No.': st.column_config.TextColumn(width=80),
            'Article Description': st.column_config.TextColumn(width=220),
            'SOH': st.column_config.TextColumn(width=80),
            'Counted Qty': st.column_config.TextColumn(width=90),
            'Diff Qty': st.column_config.TextColumn(width=80),
            'Diff Value': st.column_config.TextColumn(width=120)
        }

        st.dataframe(
            display_df,
            use_container_width=True,
            height=650,
            hide_index=True,
            column_config=report_column_config
        )

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
st.markdown(
    '''
    <p style="text-align:center;color:#948FB0;font-size:12.5px;letter-spacing:0.02em;">
        Stock Variance Analyzer &nbsp;•&nbsp; Author : Rachmat Hidayat
    </p>
    ''',
    unsafe_allow_html=True
)