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
            # Highlighting di dalam card gelap (background hijau tua transparan)
            return ['background-color: rgba(0, 150, 0, 0.7)' for _ in row] 
    return ['' for _ in row]

def highlight_not_row(row):
    """Menyorot baris di Tabel Kebenaran untuk gerbang NOT."""
    if 'last_A' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        is_current_row = (row['A'] == last_A)
        if is_current_row:
            # Highlighting di dalam card gelap
            return ['background-color: rgba(0, 150, 0, 0.7)' for _ in row] 
    return ['' for _ in row]

def style_output(val: Literal[0, 1]):
    """Mengubah warna teks Output 1 (hijau) dan 0 (putih)."""
    if val == 1:
        return (f'color: #00ff7f; '
                f'font-weight: bold; '
                f'text-align: center; '
                f'padding: 5px;')
    else:
        return (f'color: white; '
                f'text-align: center; '
                f'padding: 5px;')

# --- APLIKASI UTAMA ---

st.set_page_config(layout="centered") 

# --- STYLING GLOBAL & CARD UTAMA ---
custom_css = """
<style>
/* --- 1. BACKGROUND LUAR (Gradasi Biru) --- */
.stApp {
    background: linear-gradient(to bottom, #03045e, #00b4d8); /* Gradasi Biru Tua ke Biru Muda */
    background-attachment: fixed; 
}

header {
    visibility: hidden;
}

/* --- 2. CARD UTAMA (section.main) --- */
/* Menggunakan section.main sebagai card utama yang terpusat dan berbayangan */
section.main {
    background-color: #001f3f; /* Warna Biru Tua Solid (Opaque) */
    color: white; 
    border-radius: 15px; /* Sudut membulat */
    padding: 30px; 
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5); /* Bayangan kuat */
    margin: 40px auto; /* Centered dan margin atas/bawah */
    max-width: 800px; 
    border: 2px solid #0077b6; /* Border tipis untuk definisi card */
}

/* --- JUDUL & TATA LETAK DI DALAM CARD --- */
h1 {
    color: #00b4d8; /* Judul Biru Cyan Cerah */
    font-size: 38px; 
    font-weight: 800;
    text-align: center; /* Dipusatkan seperti contoh HTML */
    margin-bottom: 5px; 
    padding-top: 0; 
}
.stMarkdown p {
    color: #f0f0f0; /* Deskripsi agak putih */
    text-align: center;
    margin-top: 0;
    margin-bottom: 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 15px;
}
h3 {
    color: #00b4d8; /* Subheader (Tabel Kebenaran) */
}


/* Styling Dropdown/Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: #2c3e50 !important; /* Warna input dropdown gelap */
    color: white;
    border-radius: 5px;
}
.stSelectbox p {
    color: white !important;
}
.stSelectbox label {
    color: #00b4d8 !important; /* Label input biru cerah */
}

/* Styling untuk tombol Hitung */
div.stButton > button {
    background-color: #00b4d8; /* DIUBAH: Biru Cyan */
    color: #001f3f; /* Teks Biru Tua Solid */
    border-radius: 8px;
    border: none;
    padding: 10px 16px;
    font-size: 15px;
    font-weight: bold;
    transition: 0.3s;
    margin-top: -3px; 
}

div.stButton > button:hover {
    background: #0077b6; /* Warna biru lebih gelap saat hover */
    transform: scale(1.03); 
    color: white; /* Teks putih saat hover */
}

/* Mengubah style tabel agar kontras di Card gelap */
.dataframe {
    background-color: rgba(0, 0, 0, 0.7); 
    color: white; 
    border-radius: 5px;
}
.dataframe th {
    background-color: rgba(0, 0, 0, 0.9) !important; 
    color: #00b4d8 !important; /* Header tabel biru cerah */
}

/* Styling Kotak Hasil (Success Box) */
.stSuccess > div {
    background-color: rgba(0, 179, 216, 0.2) !important; 
    color: white !important;
    border-left: 5px solid #00b4d8 !important;
    border-radius: 10px; /* Sudut membulat seperti result-box */
}

/* --- FOOTER --- */
.footer {
    position: fixed;
    left: 0;
    bottom: 0;      
    width: 100%;
    background-color: transparent;
    color: #90e0ef; 
    text-align: center;
    padding: 10px;
    font-size: 12px; 
    z-index: 1000; 
    font-weight: bold;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
    
# --- KONTEN (SEKARANG BERADA DI DALAM CARD UTAMA) ---

# 1. JUDUL DAN DESKRIPSI
st.title("Kalkulator Gerbang Logika")
st.markdown("Tugas Kalkulator Logika | By Aditya Rizky Nugroho")

# Garis pemisah
st.markdown("<hr style='border: 1px solid rgba(255, 255, 255, 0.1); margin: 20px 0;'>", unsafe_allow_html=True)


# 2. INPUT 
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
        # Teks bantuan di dalam card
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
        B_display = st.session_state['last_B']
        
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


# FOOTER COPYRIGHT (Fixed)
footer_html = """
<div class="footer">
    <p>© 2025 Aditya Rizky Nugroho — Kalkulator Logika</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)