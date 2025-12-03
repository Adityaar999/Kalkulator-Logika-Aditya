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
    """Menyorot baris yang dihitung menjadi hijau muda."""
    if 'last_A' in st.session_state and 'last_B' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        last_B = st.session_state['last_B']
        is_current_row = (row['A'] == last_A) and (row['B'] == last_B)
        if is_current_row:
            # Highlight baris yang dihitung dengan warna hijau muda transparan
            return ['background-color: rgba(0, 255, 127, 0.3)' for _ in row] 
    return ['' for _ in row]

def highlight_not_row(row):
    """Menyorot baris di Tabel Kebenaran untuk gerbang NOT menjadi hijau."""
    if 'last_A' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        is_current_row = (row['A'] == last_A)
        if is_current_row:
            # Highlight baris yang dihitung dengan warna hijau muda transparan
            return ['background-color: rgba(0, 255, 127, 0.3)' for _ in row] 
    return ['' for _ in row]

def style_output(val: Literal[0, 1]):
    """Mengubah warna teks Output 1 dan 0 menjadi PUTIH."""
    # SEMUA angka di tabel akan berwarna putih,
    # tetapi angka 1 (True) akan menjadi tebal (bold).
    if val == 1:
        return (f'color: white; '
                f'font-weight: bold; '
                f'text-align: center; '
                f'padding: 5px;')
    else:
        return (f'color: white; '
                f'text-align: center; '
                f'padding: 5px;')

# --- APLIKASI UTAMA ---

st.set_page_config(layout="centered") 

# --- STYLING GLOBAL & BACKGROUND ---
custom_css = """
<style>
/* --- BACKGROUND GRADASI BIRU --- */
.stApp {
    /* Menggunakan gradasi biru tua ke biru muda */
    background: linear-gradient(to bottom, #03045e, #00b4d8); 
    background-attachment: fixed; 
}

/* Mengatur Container Streamlit agar memiliki latar belakang putih transparan (seperti kartu) */
section.main {
    background-color: rgba(255, 255, 255, 0.95); /* Putih hampir solid */
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-top: 30px;
    margin-bottom: 30px;
}
header {
    visibility: hidden;
}

h1 {
    color: #03045e; /* Biru Tua */
    font-size: 40px;
    font-weight: 800;
    text-align: left;
    margin-bottom: 20px;
    border-bottom: 3px solid #00b4d8;
    padding-bottom: 5px;
}

/* Mengubah style tabel (membuat background tabel lebih gelap/kontras dengan background putih utama) */
.dataframe {
    background-color: rgba(0, 0, 0, 0.7); /* Latar belakang gelap untuk tabel */
    color: white; 
    border-radius: 5px;
}
.dataframe th {
    background-color: rgba(0, 0, 0, 0.9) !important; /* Header tabel lebih gelap */
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
}
div.stButton > button:hover {
    background-color: #005f99; 
}

/* Mengatur warna teks di footer menjadi biru tua */
.footer p {
    color: #03045e !important; 
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
    
# --- HEADER DAN JUDUL UTAMA ---
st.title("Kalkulator Gerbang Logika V.3")

# --- KARTU UTAMA DENGAN INPUT DAN HITUNG ---
with st.container():
    
    # TATA LETAK INPUT: 3 kolom untuk Input A, Operator, dan Input B
    col1, col2, col3 = st.columns([1, 1, 1]) 

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
            st.markdown("<p style='margin-top: 30px; font-size: 12px; color: grey;'>Input B diabaikan (NOT)</p>", unsafe_allow_html=True)
            
    # TATA LETAK TOMBOL HITUNG
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True) 
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
        B_display = st.session_state['B_display']
        
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
    z-index: 1000; 
    font-weight: bold;
}
</style>
<div class="footer">
    <p>© 2025 Aditya Rizky Nugroho — Kalkulator Logika</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)