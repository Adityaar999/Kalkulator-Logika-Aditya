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

# --- FUNGSI STYLING ---
def highlight_current_row(row):
    """Menyorot baris di Tabel Kebenaran untuk gerbang 2 input."""
    if 'last_A' in st.session_state and 'last_B' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        last_B = st.session_state['last_B']
        is_current_row = (row['A'] == last_A) and (row['B'] == last_B)
        if is_current_row:
            # Mengubah highlight menjadi putih transparan 
            return ['background-color: rgba(255, 255, 255, 0.4)' for _ in row] 
    return ['' for _ in row]

def highlight_not_row(row):
    """Menyorot baris di Tabel Kebenaran untuk gerbang NOT."""
    if 'last_A' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        is_current_row = (row['A'] == last_A)
        if is_current_row:
            # Mengubah highlight menjadi putih transparan
            return ['background-color: rgba(255, 255, 255, 0.4)' for _ in row] 
    return ['' for _ in row]

def style_output(val: Literal[0, 1]):
    """Mengembalikan style CSS/HTML untuk menyorot Output = 1 (True)"""
    if val == 1:
        color = "#00FF7F" 
        background = "rgba(0, 255, 127, 0.1)" 
        return (f'color: {color}; '
                f'background-color: {background}; '
                f'font-weight: bold; '
                f'border-radius: 4px; '
                f'text-align: center; '
                f'padding: 5px;')
    else:
        return (f'color: #AAAAAA; '
                f'text-align: center; '
                f'padding: 5px;')

# --- APLIKASI UTAMA ---

# KONFIGURASI HALAMAN
st.set_page_config(layout="centered") 

# --- STYLING GLOBAL & BACKGROUND ---
# Ini akan membuat background elemen Streamlit transparan
# dan menjaga background wallpaper Anda tetap terlihat
custom_css = """
<style>
/* Membuat tampilan Streamlit lebih simpel dan transparan */
.stApp {
    background-color: transparent; 
}
section.main {
    background-color: rgba(255, 255, 255, 0.85); /* Container utama (putih transparan) */
    padding-top: 50px;
    padding-bottom: 50px;
    border-radius: 10px;
}
/* Menghapus padding/margin default jika perlu */
header {
    visibility: hidden;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
    
# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>Kalkulator Gerbang Logika V.3</h1>", unsafe_allow_html=True)

# Menggunakan container utama untuk semua input dan tombol hitung
with st.container(border=True):
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 0.7]) 

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
            

    with col4:
        # Menyejajarkan tombol dengan CSS
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True) 
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

# 6. KOTAK HASIL (Muncul setelah HITUNG ditekan)
if st.session_state.get('calculated', False):
    st.markdown("---")
    with st.container(border=True):
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


# --- 7. TABEL KEBENARAN (Hanya Muncul Setelah Hitung) ---
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
        
        styled_df = df.style.map(style_output, subset=[f'Output (NOT)'])
        styled_df = styled_df.apply(highlight_not_row, axis=1)

        st.dataframe(styled_df, width='stretch', hide_index=True)


# --- FOOTER COPYRIGHT ---
# Tambahkan di bagian paling bawah file app.py Anda
st.markdown("---")
footer_html = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: grey;
    text-align: center;
    padding: 10px;
    font-size: 12px; 
    z-index: 1000; /* Pastikan footer selalu di atas */
}
</style>
<div class="footer">
    <p>© 2025 Aditya Rizky Nugroho — Kalkulator Logika</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)