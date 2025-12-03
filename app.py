import streamlit as st
import pandas as pd
from typing import Literal

# --- FUNGSI LOGIKA GERBANG LENGKAP ---
def gate_and(A, B):
    return 1 if (A == 1 and B == 1) else 0

def gate_or(A, B):
    return 1 if (A == 1 or B == 1) else 0

def gate_not(A):
    return 1 if A == 0 else 0

def gate_xor(A, B):
    return 1 if (A != B) else 0

def gate_nand(A, B):
    return 1 if not (A == 1 and B == 1) else 0

def gate_nor(A, B):
    return 1 if not (A == 1 or B == 1) else 0

def gate_xnor(A, B):
    return 1 if (A == B) else 0

# --- DATA PILIHAN ---
OPTIONS = {
    "0 (False)": 0,
    "1 (True)": 1
}

# --- FUNGSI STYLING TABEL ---

def highlight_current_row(row):
    """Menyorot baris yang dihitung menjadi hijau muda transparan."""
    if 'last_A' in st.session_state and 'last_B' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        last_B = st.session_state['last_B']
        is_current_row = (row['A'] == last_A) and (row['B'] == last_B)
        if is_current_row:
            # Gunakan warna kontras yang cocok dengan background gelap (contoh: hijau gelap)
            return ['background-color: rgba(0, 100, 0, 0.5)' for _ in row] 
    return ['' for _ in row]

def highlight_not_row(row):
    """Menyorot baris di Tabel Kebenaran untuk gerbang NOT menjadi hijau muda transparan."""
    if 'last_A' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        is_current_row = (row['A'] == last_A)
        if is_current_row:
            return ['background-color: rgba(0, 100, 0, 0.5)' for _ in row] 
    return ['' for _ in row]

def style_output(val: Literal[0, 1]):
    """Mengubah warna teks Output 1 dan 0 menjadi PUTIH (tetap)."""
    if val == 1:
        return (f'color: #00ff7f; ' # Hijau cerah untuk 1
                f'font-weight: bold; '
                f'text-align: center; '
                f'padding: 5px;')
    else:
        return (f'color: #ffffff; '
                f'text-align: center; '
                f'padding: 5px;')

# --- APLIKASI UTAMA ---

st.set_page_config(layout="centered") 

# --- STYLING GLOBAL & BACKGROUND (SEKARANG JADI CARD UTAMA) ---
custom_css = """
<style>
/* --- 1. BACKGROUND UTAMA (DI LUAR CARD) --- */
/* Dibuat sangat gelap/hitam agar Card utama gradasi biru terlihat menonjol */
.stApp {
    background-color: #00001a; 
    background-attachment: fixed; 
}

/* --- 2. CARD UTAMA (GRADASI BIRU TUA) --- */
/* stApp container diatur ulang sebagai Card Utama */
/* Streamlit membungkus konten di dalam `section.main`, jadi kita styling section.main */
section.main {
    /* Gradasi Biru Tua */
    background: linear-gradient(to bottom, #03045e, #001f3f); 
    color: white; /* Teks default putih */
    border-radius: 15px; /* Sudut lebih membulat */
    padding: 30px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    margin: 40px auto; /* Margin atas dan bawah agar ada ruang */
    max-width: 800px; /* Batasan lebar card utama */
}
header {
    visibility: hidden;
}

/* --- JUDUL STYLING (DI DALAM CARD UTAMA) --- */
h1 {
    color: #00b4d8; /* Warna biru cerah */
    font-size: 38px; 
    font-weight: 800;
    text-align: center; 
    margin-bottom: 5px; 
    padding-bottom: 0px;
}
.stMarkdown > div:first-child > p {
    color: #e0e0e0; 
    text-align: center;
    margin-top: 0;
    margin-bottom: 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 15px;
}
h3 {
    color: #00b4d8;
}


/* --- 3. INPUT CARD (AREA INPUT) --- */
.input-card-bg {
    /* Background area input dibuat sedikit gelap */
    background-color: rgba(0, 0, 0, 0.4); 
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 25px;
}
.input-card-bg label {
    color: #00b4d8 !important; /* Label input biru cerah */
    font-weight: bold;
}

/* Styling Dropdown/Selectbox di dalam Input Card */
.stSelectbox div[data-baseweb="select"] {
    background-color: #2c3e50 !important; /* Warna input dropdown gelap */
    color: white;
    border-radius: 5px;
}
/* Memastikan semua teks di dalam selectbox berwarna putih */
.stSelectbox p {
    color: white !important;
}

/* Styling untuk tombol Hitung */
div.stButton > button {
    background-color: #0077b6;
    color: white;
    border-radius: 5px;
    border: none;
    font-weight: bold;
    transition: background-color 0.3s ease;
    margin-top: -3px; 
}

/* Mengubah style tabel */
.dataframe {
    background-color: rgba(0, 0, 0, 0.5); /* Background tabel agak transparan gelap */
    color: white; 
    border-radius: 5px;
}
.dataframe th {
    background-color: rgba(0, 0, 0, 0.7) !important; 
    color: #00b4d8 !important; /* Header tabel biru cerah */
}

/* Styling Kotak Hasil (Success Box) */
.stSuccess > div {
    background-color: rgba(0, 179, 216, 0.2) !important; /* Biru muda transparan */
    color: white !important;
    border-left: 5px solid #00b4d8 !important;
}

/* Mengatur warna teks di footer menjadi kontras */
.footer p {
    color: #90e0ef !important; /* Biru muda sangat terang */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- JUDUL UTAMA (DI DALAM CARD GRADASI BIRU TUA) ---
st.title("Kalkulator Gerbang Logika V.3")
st.markdown("Tugas Logika Digital | By Aditya Rizky Nugroho")

# --- KARTU INPUT KHUSUS (DARK GREY) ---
st.markdown("<div class='input-card-bg'>", unsafe_allow_html=True)

# TATA LETAK INPUT: 4 kolom untuk Input A, Operator, Input B, dan Tombol Hitung
col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, 0.8]) 

with col1:
    A_label = st.selectbox(
        "Input A:", 
        options=list(OPTIONS.keys()),
        index=1,
        key="select_a"
    )
    A = OPTIONS[A_label]

with col2:
    selected_gate = st.selectbox(
        "Operator:",
        options=('AND', 'OR', 'XOR', 'NOT', 'NAND', 'NOR', 'XNOR'),
        key="select_gate"
    )

with col3:
    if selected_gate != 'NOT':
        B_label = st.selectbox(
            "Input B:", 
            options=list(OPTIONS.keys()),
            index=1,
            key="select_b"
        )
        B = OPTIONS[B_label]
    else:
        B = 0 
        st.markdown("<p style='margin-top: 30px; font-size: 12px; color: #BBBBBB;'>Input B diabaikan (NOT)</p>", unsafe_allow_html=True)
        
with col4:
    # TATA LETAK TOMBOL HITUNG
    st.markdown("<div style='height: 29px;'></div>", unsafe_allow_html=True) 
    if st.button("HITUNG", width='stretch', key="btn_hitung"):
        st.session_state['calculated'] = True
        st.session_state['last_A'] = A 
        st.session_state['last_B'] = B
        
        # Logika Hitung
        gate_func = globals()[f'gate_{selected_gate.lower()}']
        hasil = gate_func(A, B) if selected_gate != 'NOT' else gate_func(A)
        
        # Simpan hasil ke session_state
        st.session_state['hasil_display'] = hasil
        st.session_state['selected_gate_display'] = selected_gate
        st.session_state['A_display'] = A
        st.session_state['B_display'] = B

# Tutup input card custom
st.markdown("</div>", unsafe_allow_html=True)

# Logika reset 
current_B_check = B if selected_gate != 'NOT' else 0

if st.session_state.get('calculated', False):
    is_gate_changed = st.session_state.get('selected_gate_display') != selected_gate
    is_A_changed = st.session_state['last_A'] != A
    is_B_changed = st.session_state['last_B'] != current_B_check and selected_gate != 'NOT'
    
    if is_gate_changed or is_A_changed or is_B_changed:
         st.session_state['calculated'] = False

# KOTAK HASIL (Muncul setelah HITUNG ditekan)
if st.session_state.get('calculated', False):
    st.markdown("---") 
    with st.container():
        hasil = st.session_state['hasil_display']
        selected_gate_display = st.session_state['selected_gate_display']
        A_display = st.session_state['A_display']
        B_display = st.session_state['last_B'] # Gunakan last_B untuk mencocokkan hasil
        
        A_label = list(OPTIONS.keys())[list(OPTIONS.values()).index(A_display)]
        B_label = list(OPTIONS.keys())[list(OPTIONS.values()).index(B_display)]
        
        if selected_gate_display == 'NOT':
            st.success(f"Output **{selected_gate_display}** dari **{A_label}** adalah: **{hasil}**")
        else:
            st.success(f"Output **{selected_gate_display}** dari **{A_label}** dan **{B_label}** adalah: **{hasil}**")


# TABEL KEBENARAN (Hanya Muncul Setelah Hitung)
if st.session_state.get('calculated', False):
    st.markdown("---") 

    current_selected_gate = selected_gate 
    st.subheader(f"📋 Tabel Kebenaran {current_selected_gate}")

    # --- Memproses Data Tabel ---
    if current_selected_gate != 'NOT':
        # Data Gerbang 2 Input 
        gate_func = globals()[f'gate_{current_selected_gate.lower()}']
        
        data = {
            'A': [0, 0, 1, 1],
            'B': [0, 1, 0, 1],
            f'Output ({current_selected_gate})': [
                gate_func(0, 0),
                gate_func(0, 1),
                gate_func(1, 0),
                gate_func(1, 1),
            ]
        }
        df = pd.DataFrame(data)
        
        # Terapkan styling
        styled_df = df.style.map(style_output, subset=[f'Output ({current_selected_gate})'])
        styled_df = styled_df.apply(highlight_current_row, axis=1) 
        
        st.dataframe(styled_df, width='stretch', hide_index=True)

    else:
        # Data Gerbang NOT
        data = {
            'A': [0, 1],
            f'Output (NOT)': [gate_not(0), gate_not(1)],
        }
        df = pd.DataFrame(data)
        
        # Terapkan styling
        styled_df = df.style.map(style_output, subset=[f'Output (NOT)'])
        styled_df = styled_df.apply(highlight_not_row, axis=1)

        st.dataframe(styled_df, width='stretch', hide_index=True)



# FOOTER COPYRIGHT
st.markdown("---") 
footer_html = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;      
    width: 100%;
    background-color: transparent;
    color: #03045e; 
    text-align: center;
    padding: 10px;
    font-size: 12px; 
    z-index: 1000; /* Z-index yang tinggi memastikan footer berada di atas elemen lain */
    font-weight: bold;
}
</style>
<div class="footer">
    <p>© 2025 Aditya Rizky Nugroho — Kalkulator Logika</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)