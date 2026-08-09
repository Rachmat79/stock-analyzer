import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
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
VALID_USERS = {
    'rachmat79': '591979',
    'stockhrn': '12345'
}

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def do_login():
    input_user = st.session_state.get('login_username', '')
    input_pass = st.session_state.get('login_password', '')

    if input_user in VALID_USERS and VALID_USERS[input_user] == input_pass:
        st.session_state.authenticated = True
        st.session_state.current_user = input_user
        st.session_state.login_error = False
    else:
        st.session_state.authenticated = False
        st.session_state.login_error = True

def do_logout():
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.login_username = ''
    st.session_state.login_password = ''
    st.session_state.pop('last_activity', None)

# --------------------------------------------------
# AUTO-LOGOUT setelah tidak ada aktivitas (idle timeout)
# --------------------------------------------------
SESSION_TIMEOUT_MINUTES = 60

def check_session_timeout():
    '''
    Dipanggil di setiap rerun. Kalau user sudah login dan jeda waktu
    sejak aktivitas terakhir melebihi SESSION_TIMEOUT_MINUTES, user
    otomatis di-logout dan diarahkan kembali ke halaman login dengan
    pesan sesi berakhir.
    '''
    if st.session_state.authenticated:
        last_activity = st.session_state.get('last_activity')

        if last_activity is not None:
            elapsed_minutes = (datetime.now() - last_activity).total_seconds() / 60

            if elapsed_minutes > SESSION_TIMEOUT_MINUTES:
                st.session_state.authenticated = False
                st.session_state.session_expired = True
                st.session_state.pop('last_activity', None)
                return

        st.session_state.last_activity = datetime.now()

check_session_timeout()

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

        if st.session_state.get('session_expired'):
            st.warning(
                f'Sesi Anda berakhir karena tidak ada aktivitas selama '
                f'{SESSION_TIMEOUT_MINUTES} menit. Silakan login kembali.'
            )
            st.session_state.session_expired = False

    st.stop()

# ==================================================
# AUTO-LOGOUT IDLE DETECTOR (client-side)
# ==================================================
# Memantau aktivitas mouse/keyboard/scroll di browser. Kalau tidak ada
# aktivitas sama sekali selama SESSION_TIMEOUT_MINUTES, halaman otomatis
# di-refresh -> memicu pengecekan check_session_timeout() di server yang
# akan mengeluarkan user ke halaman login.
components.html(
    f'''
    <script>
    (function() {{
        var idleLimitMs = {SESSION_TIMEOUT_MINUTES} * 60 * 1000;
        var idleTimer;

        function resetIdleTimer() {{
            clearTimeout(idleTimer);
            idleTimer = setTimeout(function() {{
                window.parent.location.reload();
            }}, idleLimitMs);
        }}

        ['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart'].forEach(
            function(evt) {{
                window.parent.document.addEventListener(evt, resetIdleTimer, true);
            }}
        );

        resetIdleTimer();
    }})();
    </script>
    ''',
    height=0
)

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
                {st.session_state.current_user}
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
# STOCK RECONCILIATION ENGINE
# ==================================================
# Implementasi mengikuti "1. TUJUAN UTAMA PROGRAM.txt" yang dilampirkan.
#
# CATATAN PENTING - baca ini dulu sebelum mengubah logika di bawah:
#
#   [CONFIRMED RULE]  Diambil persis sesuai spesifikasi:
#     - Sign reversal detection (P1>0 & P2<0, atau sebaliknya)
#     - Mirror/opposite value detection (dengan tolerance)
#     - New item / Missing item -> REQUIRES_REVIEW, bukan otomatis error
#     - Duplicate item detection dalam satu periode
#     - Risk scoring 0-100 dengan klasifikasi NORMAL/LOW/MEDIUM/HIGH/CRITICAL
#     - Percentage change = 0 saat Qty_P1 = 0 dihindari (pakai status khusus)
#
#   [ASSUMPTION - karena skema data app ini tidak punya kolom terpisah
#    untuk SKU/Barcode/UOM/Batch]:
#     - "Item Code" memakai kolom `Article` yang sudah ada di data
#     - Matching key = kombinasi (Store + Article), BUKAN Article saja.
#       Alasan: data di app ini per toko, kalau hanya pakai Article maka
#       item yang sama di toko berbeda akan tercampur jadi satu baris.
#       -> Kalau ternyata rekonsiliasi yang diinginkan LINTAS TOKO
#          (agregat semua toko), beri tahu saya, logikanya bisa diubah.
#     - Kolom UOM tidak tersedia -> UOM_MISMATCH TIDAK diimplementasikan
#       di versi ini (lihat REQUIRES USER CONFIRMATION di bawah)
#
#   [CONFIGURABLE RULE - nilai default di bawah, bisa diubah lewat UI
#    "⚙️ Konfigurasi Reconciliation" di dalam tab Stock Reconciliation]:
#     - Threshold variance % (LOW/MEDIUM/HIGH/CRITICAL)
#     - Materiality threshold (variance absolut minimum supaya dianggap
#       signifikan, mencegah item kecil dengan %change besar tapi
#       absolut kecil ikut ditandai CRITICAL)
#     - Mirror tolerance
#     - Bobot risk scoring per jenis flag
#     - Kolom quantity yang direkonsiliasi (Stock Take Variance Qty /
#       SOH Qty / Qty Counted)
#
#   [REQUIRES USER CONFIRMATION / FUTURE DEVELOPMENT - belum
#    diimplementasikan di versi ini, butuh keputusan bisnis dulu]:
#     - UOM control & conversion factor (kolom UOM belum ada di data)
#     - Cross-period 3+ (P3, P4, P5, dst) & Historical Z-Score anomaly
#       (baru bisa jalan kalau ada riwayat >=3 periode tersimpan)
#     - Audit trail permanen ke database (saat ini traceability hanya
#       sebatas nama file + nomor baris asli, disimpan di sesi berjalan)
#     - Export ke PDF & dashboard terpisah (saat ini export ke Excel)
#     - Machine learning anomaly detection
#
RECON_REQUIRED_COLS = [
    'Store', 'Category', 'Article', 'Article Description',
    'SOH Qty', 'Qty Counted',
    'Stock Take Variance Qty', 'Stock Take Variance Value'
]

RECON_NUMERIC_COLS = [
    'SOH Qty', 'Qty Counted',
    'Stock Take Variance Qty', 'Stock Take Variance Value'
]


def load_and_validate_recon_file(uploaded, source_label):
    '''Baca & validasi file (dipakai untuk file periode saat ini maupun
    periode sebelumnya), tanpa mengubah file sumber asli (raw tetap utuh,
    hasil cleaning disimpan di dataframe baru).'''

    if uploaded.name.lower().endswith('.csv'):
        df = pd.read_csv(uploaded, sep=None, engine='python')
    else:
        df = pd.read_excel(uploaded)

    missing = [c for c in RECON_REQUIRED_COLS if c not in df.columns]
    if missing:
        st.error(f'[{source_label}] Kolom belum ditemukan: {missing}')
        st.write('Kolom yang tersedia:', df.columns.tolist())
        st.stop()

    df = df.copy()
    df['__SourceFile__'] = uploaded.name
    df['__SourceRow__'] = df.index + 2  # +2 asumsi row 1 = header di Excel

    for col in RECON_NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def recon_data_quality_report(df, label):
    '''Section 19 - Data Validation, sebelum data masuk perhitungan.'''
    issues = []

    n_missing_article = df['Article'].isna().sum() + (df['Article'].astype(str).str.strip() == '').sum()
    n_missing_desc = df['Article Description'].isna().sum() + (df['Article Description'].astype(str).str.strip() == '').sum()
    n_missing_store = df['Store'].isna().sum() + (df['Store'].astype(str).str.strip() == '').sum()

    for col in RECON_NUMERIC_COLS:
        n_invalid = df[col].isna().sum()
        if n_invalid > 0:
            issues.append({
                'Periode': label,
                'Isu': f'Nilai bukan angka / kosong pada kolom "{col}"',
                'Jumlah Baris': int(n_invalid)
            })

    if n_missing_article > 0:
        issues.append({'Periode': label, 'Isu': 'Article (Item Code) kosong', 'Jumlah Baris': int(n_missing_article)})
    if n_missing_desc > 0:
        issues.append({'Periode': label, 'Isu': 'Article Description kosong', 'Jumlah Baris': int(n_missing_desc)})
    if n_missing_store > 0:
        issues.append({'Periode': label, 'Isu': 'Store kosong', 'Jumlah Baris': int(n_missing_store)})

    dup_key_check = (
        df['Store'].astype(str).str.strip().str.upper() + '||' +
        df['Article'].astype(str).str.strip().str.upper()
    )
    n_dup_rows = dup_key_check.duplicated(keep=False).sum()
    if n_dup_rows > 0:
        issues.append({'Periode': label, 'Isu': 'Baris dengan Store+Article duplikat', 'Jumlah Baris': int(n_dup_rows)})

    return issues


def build_match_key(df):
    return (
        df['Store'].astype(str).str.strip().str.upper() + '||' +
        df['Article'].astype(str).str.strip().str.upper()
    )


def prepare_recon_period(df, period_label, qty_col):
    '''Normalisasi + agregasi duplikat untuk satu periode (Section 3 & 9).'''
    d = df.copy()
    d[RECON_NUMERIC_COLS] = d[RECON_NUMERIC_COLS].fillna(0)
    d['__MatchKey__'] = build_match_key(d)

    dup_counts = d.groupby('__MatchKey__').size()
    dup_keys = set(dup_counts[dup_counts > 1].index)

    agg = d.groupby('__MatchKey__').agg(
        Store=('Store', 'first'),
        Article=('Article', 'first'),
        ArticleDescription=('Article Description', 'first'),
        Category=('Category', 'first'),
        Qty=(qty_col, 'sum'),
        RowCount=(qty_col, 'count'),
        SourceFile=('__SourceFile__', 'first'),
        SourceRow=('__SourceRow__', lambda x: ', '.join(map(str, x)))
    ).reset_index()

    agg['Duplicate'] = agg['__MatchKey__'].isin(dup_keys)
    agg = agg.rename(columns={
        'Qty': f'Qty_{period_label}',
        'RowCount': f'RowCount_{period_label}',
        'Duplicate': f'Duplicate_{period_label}',
        'SourceFile': f'SourceFile_{period_label}',
        'SourceRow': f'SourceRow_{period_label}'
    })

    return agg


def run_reconciliation(df_p1, df_p2, qty_col, config):
    '''Engine utama: matching -> variance calc -> anomaly detection -> risk scoring.
    Mengikuti alur modular Section 24 (Matching -> Reconciliation -> Variance
    -> Anomaly Detection -> Risk Scoring -> Classification).'''

    p1_agg = prepare_recon_period(df_p1, 'P1', qty_col)
    p2_agg = prepare_recon_period(df_p2, 'P2', qty_col)

    merged = pd.merge(
        p1_agg, p2_agg,
        on='__MatchKey__', how='outer', suffixes=('_p1', '_p2')
    )

    for base_col in ['Store', 'Article', 'ArticleDescription', 'Category']:
        merged[base_col] = merged[f'{base_col}_p1'].fillna(merged[f'{base_col}_p2'])

    merged['Status_Exist'] = 'BOTH'
    merged.loc[merged['Qty_P1'].isna(), 'Status_Exist'] = 'NEW_IN_P2'
    merged.loc[merged['Qty_P2'].isna(), 'Status_Exist'] = 'MISSING_IN_P2'

    merged['Qty_P1'] = merged['Qty_P1'].fillna(0)
    merged['Qty_P2'] = merged['Qty_P2'].fillna(0)

    merged['Change'] = merged['Qty_P2'] - merged['Qty_P1']
    merged['Abs_Variance'] = merged['Change'].abs()

    def _pct(row):
        if row['Qty_P1'] == 0:
            return None
        return (row['Change'] / abs(row['Qty_P1'])) * 100

    merged['Pct_Change'] = merged.apply(_pct, axis=1)

    # ---- Section 5: Sign Reversal ----
    merged['Sign_Reversal'] = (
        ((merged['Qty_P1'] > 0) & (merged['Qty_P2'] < 0)) |
        ((merged['Qty_P1'] < 0) & (merged['Qty_P2'] > 0))
    )

    # ---- Section 6: Mirror / Opposite Value ----
    merged['Mirror_Value'] = (
        ((merged['Qty_P1'] + merged['Qty_P2']).abs() <= config['mirror_tolerance']) &
        (merged['Qty_P1'] != 0) & (merged['Qty_P2'] != 0)
    )

    # ---- Section 7: Extreme Variance (percentage + absolute + materiality) ----
    def _bucket(pct):
        if pct is None:
            return 'N/A'
        p = abs(pct)
        if p < config['thr_low']:
            return 'LOW'
        elif p < config['thr_medium']:
            return 'MEDIUM'
        elif p < config['thr_high']:
            return 'HIGH'
        return 'CRITICAL'

    merged['Variance_Bucket'] = merged['Pct_Change'].apply(_bucket)
    merged['Extreme_Variance_Flag'] = (
        merged['Variance_Bucket'].isin(['HIGH', 'CRITICAL']) &
        (merged['Abs_Variance'] >= config['materiality'])
    )

    # ---- Section 9: Duplicate ----
    merged['Duplicate_P1'] = merged['Duplicate_P1'].fillna(False)
    merged['Duplicate_P2'] = merged['Duplicate_P2'].fillna(False)
    merged['Duplicate_Flag'] = merged['Duplicate_P1'] | merged['Duplicate_P2']

    # ---- Section 13: Risk Scoring ----
    def _score_and_reasons(row):
        score = 0
        reasons = []

        if row['Sign_Reversal']:
            score += config['w_sign_reversal']
            reasons.append('Sign reversal — tanda quantity berbalik (+/-) antar periode')

        if row['Mirror_Value']:
            score += config['w_mirror']
            reasons.append('Possible mirror value — P2 mendekati kebalikan dari P1')

        if row['Extreme_Variance_Flag']:
            score += config['w_variance']
            reasons.append(f"Variance ekstrem ({row['Variance_Bucket']}) dan signifikan secara absolut")

        if row['Duplicate_Flag']:
            score += config['w_duplicate']
            reasons.append('Item duplikat terdeteksi (Store+Article muncul lebih dari 1x pada periode yang sama)')

        if row['Status_Exist'] == 'NEW_IN_P2':
            score += config['w_new']
            reasons.append('Item baru — tidak ditemukan pada periode sebelumnya')

        if row['Status_Exist'] == 'MISSING_IN_P2':
            score += config['w_missing']
            reasons.append('Item hilang — ada di periode sebelumnya, tidak ada di periode saat ini')

        score = min(score, 100)

        if not reasons:
            reasons.append('Tidak ada pola tidak normal terdeteksi (normal movement)')

        return pd.Series({'Risk_Score': score, 'Reasons': reasons})

    score_df = merged.apply(_score_and_reasons, axis=1)
    merged = pd.concat([merged, score_df], axis=1)

    def _risk_level(score):
        if score >= 80:
            return 'CRITICAL'
        elif score >= 60:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        elif score >= 20:
            return 'LOW'
        return 'NORMAL'

    merged['Risk_Level'] = merged['Risk_Score'].apply(_risk_level)

    # ---- Section 23: Classification ----
    def _classify(row):
        if row['Status_Exist'] in ('NEW_IN_P2', 'MISSING_IN_P2'):
            return 'BUSINESS_CHANGE (Requires Review)'
        if row['Sign_Reversal'] or row['Mirror_Value']:
            return 'ANOMALY'
        if row['Duplicate_Flag']:
            return 'DATA_QUALITY_ERROR (Duplicate)'
        if row['Extreme_Variance_Flag']:
            return 'ANOMALY (Extreme Variance)'
        return 'NORMAL_MOVEMENT'

    merged['Classification'] = merged.apply(_classify, axis=1)

    # ---- Section 16: Recommended Action ----
    def _recommend(row):
        if row['Sign_Reversal'] or row['Mirror_Value']:
            return 'Review dokumen stock opname P1 & P2, lakukan physical count ulang untuk item ini.'
        if row['Duplicate_Flag']:
            return 'Periksa apakah duplikasi valid (lokasi/baris berbeda yang sah) atau kesalahan input berganda.'
        if row['Status_Exist'] == 'NEW_IN_P2':
            return 'Konfirmasi ke tim toko: item baru resmi, atau kesalahan mapping/Article Code.'
        if row['Status_Exist'] == 'MISSING_IN_P2':
            return 'Konfirmasi ke tim toko: item discontinued, pindah lokasi, atau terlewat saat stock opname.'
        if row['Extreme_Variance_Flag']:
            return 'Telusuri histori pergerakan stok item ini, pastikan bukan kesalahan input/adjustment.'
        return 'Tidak perlu tindakan lanjutan.'

    merged['Recommended_Action'] = merged.apply(_recommend, axis=1)

    merged = merged.rename(columns={'ArticleDescription': 'Article Description'})

    return merged


def build_reconciliation_summary(merged):
    '''Section 15 - Reconciliation Summary.'''
    return {
        'Total Item Periode Sebelumnya (P1)': int((merged['Status_Exist'] != 'NEW_IN_P2').sum()),
        'Total Item Periode Saat Ini (P2)': int((merged['Status_Exist'] != 'MISSING_IN_P2').sum()),
        'Item di Kedua Periode': int((merged['Status_Exist'] == 'BOTH').sum()),
        'Item Baru (New in P2)': int((merged['Status_Exist'] == 'NEW_IN_P2').sum()),
        'Item Hilang (Missing in P2)': int((merged['Status_Exist'] == 'MISSING_IN_P2').sum()),
        'Normal': int((merged['Risk_Level'] == 'NORMAL').sum()),
        'Low Risk': int((merged['Risk_Level'] == 'LOW').sum()),
        'Medium Risk': int((merged['Risk_Level'] == 'MEDIUM').sum()),
        'High Risk': int((merged['Risk_Level'] == 'HIGH').sum()),
        'Critical Risk': int((merged['Risk_Level'] == 'CRITICAL').sum()),
        'Sign Reversal': int(merged['Sign_Reversal'].sum()),
        'Mirror Value': int(merged['Mirror_Value'].sum()),
        'Duplicate': int(merged['Duplicate_Flag'].sum()),
    }

# ==================================================
# UPLOAD FILE
# ==================================================
col_upload_current, col_upload_prev = st.columns(2)

with col_upload_current:
    uploaded_file = st.file_uploader(
        'Upload file stock take (Excel atau CSV)',
        type=['xlsx', 'csv'],
        key='uploader_current_period'
    )

with col_upload_prev:
    uploaded_file_prev = st.file_uploader(
        'Upload file stock take periode sebelumnya (opsional — untuk Stock Reconciliation)',
        type=['xlsx', 'csv'],
        key='uploader_previous_period'
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

    # File periode sebelumnya (untuk tab Stock Reconciliation)
    raw_df_prev = None
    if uploaded_file_prev is not None:
        raw_df_prev = load_and_validate_recon_file(uploaded_file_prev, 'Periode Sebelumnya')

    # Baca ulang file periode saat ini khusus untuk reconciliation engine
    # (perlu versi dengan NaN asli + metadata source file/baris, berbeda
    # dari `raw_df` di atas yang NaN-nya sudah di-fillna(0) untuk dashboard)
    raw_df_current_recon = None
    if uploaded_file_prev is not None:
        uploaded_file.seek(0)
        raw_df_current_recon = load_and_validate_recon_file(uploaded_file, 'Periode Saat Ini')

    tab_dashboard, tab_report, tab_reconciliation = st.tabs([
        'Executive Dashboard',
        'Stock Variance Report',
        'Stock Reconciliation'
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
    # STOCK RECONCILIATION
    # ==================================================
    with tab_reconciliation:

        st.markdown(
            '''
            <div class="glass-panel" style="padding:18px 24px;margin-bottom:22px;">
                <p style="color:#A855F7;font-size:11px;font-weight:700;letter-spacing:0.14em;
                          text-transform:uppercase;margin:0 0 6px 0;">Multi-Period Analysis</p>
                <h2 style="margin:0;font-size:22px;font-weight:800;color:#241F47;">
                    Stock Reconciliation
                </h2>
                <p style="margin:8px 0 0 0;color:#6D6690;font-size:13.5px;">
                    Deteksi anomali antar periode: sign reversal, mirror value,
                    variance ekstrem, item baru/hilang, dan duplikasi.
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )

        if raw_df_prev is None:
            st.info(
                '📤 Upload **"file stock take periode sebelumnya"** di kotak upload '
                'kedua (bagian paling atas halaman) untuk mengaktifkan analisa '
                'Stock Reconciliation.'
            )
        else:

            with st.expander('⚙️ Konfigurasi Reconciliation'):

                qty_col_options = {
                    'Stock Take Variance Qty': 'Stock Take Variance Qty',
                    'SOH Qty': 'SOH Qty',
                    'Qty Counted': 'Qty Counted'
                }
                qty_col_label = st.selectbox(
                    'Kolom quantity yang direkonsiliasi antar periode',
                    list(qty_col_options.keys()),
                    index=0,
                    help='Default: Stock Take Variance Qty (paling relevan untuk '
                         'mendeteksi anomali stock opname). Bisa diganti sesuai kebutuhan.'
                )
                qty_col = qty_col_options[qty_col_label]

                st.markdown('**Threshold Variance (%)**')
                cfg1, cfg2, cfg3 = st.columns(3)
                with cfg1:
                    thr_low = st.number_input('Batas LOW (%)', value=10.0, min_value=0.0)
                with cfg2:
                    thr_medium = st.number_input('Batas MEDIUM (%)', value=25.0, min_value=0.0)
                with cfg3:
                    thr_high = st.number_input('Batas HIGH (%) — di atasnya = CRITICAL', value=50.0, min_value=0.0)

                cfg4, cfg5 = st.columns(2)
                with cfg4:
                    materiality = st.number_input(
                        'Materiality threshold (variance absolut minimum)',
                        value=50.0, min_value=0.0,
                        help='Item dengan %variance tinggi TAPI variance absolut di '
                             'bawah angka ini tidak akan ditandai sebagai variance ekstrem.'
                    )
                with cfg5:
                    mirror_tolerance = st.number_input(
                        'Mirror tolerance', value=0.0, min_value=0.0,
                        help='Toleransi selisih agar P2 dianggap "mendekati kebalikan" dari P1.'
                    )

                st.markdown('**Bobot Risk Scoring** (total dibatasi maksimum 100)')
                wcol1, wcol2, wcol3 = st.columns(3)
                with wcol1:
                    w_sign = st.number_input('Sign Reversal', value=40, min_value=0)
                    w_mirror = st.number_input('Mirror Value', value=30, min_value=0)
                with wcol2:
                    w_variance = st.number_input('Extreme Variance', value=20, min_value=0)
                    w_duplicate = st.number_input('Duplicate', value=20, min_value=0)
                with wcol3:
                    w_new = st.number_input('New Item', value=10, min_value=0)
                    w_missing = st.number_input('Missing Item', value=15, min_value=0)

            config = {
                'thr_low': thr_low, 'thr_medium': thr_medium, 'thr_high': thr_high,
                'materiality': materiality, 'mirror_tolerance': mirror_tolerance,
                'w_sign_reversal': w_sign, 'w_mirror': w_mirror, 'w_variance': w_variance,
                'w_duplicate': w_duplicate, 'w_new': w_new, 'w_missing': w_missing
            }

            # ---- Data Quality Report (Section 19) ----
            dq_issues = (
                recon_data_quality_report(raw_df_prev, 'Periode Sebelumnya (P1)') +
                recon_data_quality_report(raw_df_current_recon, 'Periode Saat Ini (P2)')
            )

            with st.expander(
                f'🔍 Data Quality Report ({len(dq_issues)} isu ditemukan)',
                expanded=(len(dq_issues) > 0)
            ):
                if dq_issues:
                    st.dataframe(
                        pd.DataFrame(dq_issues),
                        use_container_width=True,
                        hide_index=True
                    )
                    st.caption(
                        'Data tetap diproses meski ada isu di atas — mohon divalidasi '
                        'sebelum mengambil kesimpulan final.'
                    )
                else:
                    st.success('Tidak ada isu kualitas data terdeteksi pada kedua periode.')

            # ---- Run Engine ----
            merged = run_reconciliation(raw_df_prev, raw_df_current_recon, qty_col, config)
            summary = build_reconciliation_summary(merged)

            st.markdown('### 📊 Reconciliation Summary')

            k1, k2, k3, k4 = st.columns(4)
            k1.metric('Total Item (P1)', f"{summary['Total Item Periode Sebelumnya (P1)']:,}")
            k2.metric('Total Item (P2)', f"{summary['Total Item Periode Saat Ini (P2)']:,}")
            k3.metric('Item Baru (New)', f"{summary['Item Baru (New in P2)']:,}")
            k4.metric('Item Hilang (Missing)', f"{summary['Item Hilang (Missing in P2)']:,}")

            k5, k6, k7, k8 = st.columns(4)
            k5.metric('Sign Reversal', f"{summary['Sign Reversal']:,}")
            k6.metric('Mirror Value', f"{summary['Mirror Value']:,}")
            k7.metric('Duplicate', f"{summary['Duplicate']:,}")
            k8.metric('Critical Risk', f"{summary['Critical Risk']:,}")

            st.markdown('---')

            st.markdown('### 🥧 Distribusi Risk Level')

            risk_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NORMAL']
            risk_counts = (
                merged['Risk_Level'].value_counts()
                .reindex(risk_order)
                .fillna(0)
                .astype(int)
                .reset_index()
            )
            risk_counts.columns = ['Risk Level', 'Jumlah Item']

            fig_risk = px.bar(
                risk_counts,
                x='Risk Level',
                y='Jumlah Item',
                text='Jumlah Item',
                color='Risk Level',
                color_discrete_map={
                    'CRITICAL': '#DC2626',
                    'HIGH': '#FB7185',
                    'MEDIUM': '#F59E0B',
                    'LOW': '#A855F7',
                    'NORMAL': '#34D399'
                },
                category_orders={'Risk Level': risk_order}
            )
            fig_risk.update_traces(textposition='outside')
            fig_risk.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#4B4468', family='Manrope'),
                xaxis=dict(gridcolor='rgba(147,51,234,0.10)'),
                yaxis=dict(gridcolor='rgba(147,51,234,0.10)')
            )
            st.plotly_chart(fig_risk, use_container_width=True)

            st.markdown('---')

            st.markdown('### 📈 Top 20 Absolute Variance')

            top20_abs = merged.sort_values('Abs_Variance', ascending=False).head(20)

            if not top20_abs.empty:
                fig_top20 = px.bar(
                    top20_abs,
                    x='Abs_Variance',
                    y='Article Description',
                    orientation='h',
                    text='Abs_Variance',
                    color_discrete_sequence=['#7C3AED']
                )
                fig_top20.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
                fig_top20.update_layout(
                    height=600,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#4B4468', family='Manrope'),
                    xaxis=dict(gridcolor='rgba(147,51,234,0.10)'),
                    yaxis=dict(gridcolor='rgba(147,51,234,0.05)')
                )
                st.plotly_chart(fig_top20, use_container_width=True)

            st.markdown('---')

            sr_df = merged[merged['Sign_Reversal'] | merged['Mirror_Value']]

            st.markdown(f'### 🔴 Sign Reversal & Mirror Value ({len(sr_df)} item)')

            if not sr_df.empty:
                sr_display = sr_df[[
                    'Store', 'Article', 'Article Description',
                    'Qty_P1', 'Qty_P2', 'Change', 'Risk_Level', 'Risk_Score'
                ]].sort_values('Risk_Score', ascending=False).copy()

                sr_display.columns = [
                    'Store', 'Article', 'Article Description',
                    'P1 Qty', 'P2 Qty', 'Change', 'Risk Level', 'Score'
                ]

                st.dataframe(
                    sr_display,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        'Store': st.column_config.TextColumn(width=170),
                        'Article': st.column_config.TextColumn(width=80),
                        'Article Description': st.column_config.TextColumn(width=220),
                        'P1 Qty': st.column_config.NumberColumn(width=90),
                        'P2 Qty': st.column_config.NumberColumn(width=90),
                        'Change': st.column_config.NumberColumn(width=90),
                        'Risk Level': st.column_config.TextColumn(width=100),
                        'Score': st.column_config.NumberColumn(width=70)
                    }
                )
            else:
                st.success('Tidak ada item dengan sign reversal / mirror value pada konfigurasi saat ini.')

            st.markdown('---')

            st.markdown('### 📋 Exception Detail Report')

            risk_filter = st.multiselect(
                'Filter Risk Level',
                risk_order,
                default=['CRITICAL', 'HIGH', 'MEDIUM']
            )

            exception_df = merged[merged['Risk_Level'].isin(risk_filter)].copy()

            risk_order_map = {level: i for i, level in enumerate(risk_order)}
            exception_df['__sort__'] = exception_df['Risk_Level'].map(risk_order_map)
            exception_df = exception_df.sort_values(
                ['__sort__', 'Abs_Variance'],
                ascending=[True, False]
            )

            if not exception_df.empty:
                display_exception = exception_df[[
                    'Risk_Level', 'Risk_Score', 'Store', 'Article', 'Article Description',
                    'Qty_P1', 'Qty_P2', 'Change', 'Pct_Change', 'Classification', 'Status_Exist'
                ]].copy()

                display_exception.columns = [
                    'Risk', 'Score', 'Store', 'Article', 'Article Description',
                    'P1 Qty', 'P2 Qty', 'Change', '% Change', 'Classification', 'Status'
                ]

                display_exception['% Change'] = display_exception['% Change'].apply(
                    lambda x: f'{x:,.1f}%' if pd.notna(x) else 'N/A'
                )

                tbl_height = min(int(35.2 * (len(display_exception) + 1)) + 3, 700)

                st.dataframe(
                    display_exception,
                    use_container_width=True,
                    hide_index=True,
                    height=tbl_height
                )
                st.caption(
                    f'Menampilkan {len(display_exception):,} item, diurutkan dari risiko '
                    'tertinggi lalu variance absolut terbesar.'
                )
            else:
                st.info('Tidak ada item pada filter Risk Level yang dipilih.')

            st.markdown('---')

            st.markdown('### 🔍 Detail Investigasi per Item')

            if not exception_df.empty:
                exception_df['__label__'] = (
                    exception_df['Store'].astype(str) + ' | ' +
                    exception_df['Article'].astype(str) + ' - ' +
                    exception_df['Article Description'].astype(str)
                )

                selected_label = st.selectbox(
                    'Pilih item untuk melihat detail investigasi',
                    exception_df['__label__'].tolist()
                )

                row = exception_df[exception_df['__label__'] == selected_label].iloc[0]

                pct_display = (
                    f"{row['Pct_Change']:.1f}%" if pd.notna(row['Pct_Change'])
                    else 'N/A (Qty Periode Sebelumnya = 0)'
                )

                reasons_html = ''.join(f'<li>{r}</li>' for r in row['Reasons'])

                st.markdown(
                    f'''
                    <div class="glass-panel" style="padding:22px 26px;">
                        <p style="margin:0 0 4px 0;color:#8A82AD;font-size:11px;
                                  text-transform:uppercase;letter-spacing:0.1em;font-weight:700;">
                            Item
                        </p>
                        <h3 style="margin:0 0 14px 0;color:#241F47;">
                            {row['Article']} — {row['Article Description']}
                        </h3>
                        <p style="color:#4B4468;"><b>Store:</b> {row['Store']}</p>
                        <p style="color:#4B4468;"><b>Qty Periode Sebelumnya (P1):</b> {row['Qty_P1']:,.0f}</p>
                        <p style="color:#4B4468;"><b>Qty Periode Saat Ini (P2):</b> {row['Qty_P2']:,.0f}</p>
                        <p style="color:#4B4468;"><b>Variance:</b> {row['Change']:,.0f} ({pct_display})</p>
                        <p style="color:#4B4468;"><b>Klasifikasi:</b> {row['Classification']}</p>
                        <p style="color:#4B4468;">
                            <b>Risk Score:</b> {row['Risk_Score']}/100 —
                            <b>{row['Risk_Level']}</b>
                        </p>
                        <p style="margin-top:14px;color:#4B4468;"><b>Kemungkinan Penyebab:</b></p>
                        <ul style="color:#4B4468;">{reasons_html}</ul>
                        <p style="color:#4B4468;">
                            <b>Rekomendasi Tindakan:</b> {row['Recommended_Action']}
                        </p>
                        <p style="margin-top:14px;color:#948FB0;font-size:12px;">
                            Sumber P1: {row['SourceFile_P1']} (baris {row['SourceRow_P1']}) &nbsp;•&nbsp;
                            Sumber P2: {row['SourceFile_P2']} (baris {row['SourceRow_P2']})
                        </p>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            else:
                st.info('Tidak ada item pada filter Risk Level yang dipilih untuk diinvestigasi.')

            st.markdown('---')

            st.markdown('### 📥 Export Hasil Reconciliation')

            merged_export = merged.drop(columns=['__MatchKey__']).copy()
            merged_export['Reasons'] = merged_export['Reasons'].apply(lambda r: '; '.join(r))

            exception_export = exception_df.drop(
                columns=['__MatchKey__', '__sort__', '__label__'],
                errors='ignore'
            ).copy()
            if 'Reasons' in exception_export.columns:
                exception_export['Reasons'] = exception_export['Reasons'].apply(
                    lambda r: '; '.join(r) if isinstance(r, list) else r
                )

            recon_output = BytesIO()
            with pd.ExcelWriter(recon_output, engine='openpyxl') as writer:
                merged_export.to_excel(writer, sheet_name='Reconciliation Detail', index=False)
                exception_export.to_excel(writer, sheet_name='Exception Report', index=False)
                if dq_issues:
                    pd.DataFrame(dq_issues).to_excel(writer, sheet_name='Data Quality Report', index=False)
                pd.DataFrame(
                    list(summary.items()), columns=['Metric', 'Result']
                ).to_excel(writer, sheet_name='Management Summary', index=False)

            st.download_button(
                label='Download Reconciliation Report (Excel)',
                data=recon_output.getvalue(),
                file_name='Stock_Reconciliation_Report.xlsx',
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