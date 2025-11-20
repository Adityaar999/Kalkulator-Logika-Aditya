import streamlit as st
import pandas as pd
from typing import Literal

# --- Fungsi Logika Gerbang ---
def gate_and(A, B):
    return 1 if (A == 1 and B == 1) else 0

def gate_or(A, B):
    return 1 if (A == 1 or B == 1) else 0

def gate_not(A):
    return 1 if A == 0 else 0

def gate_xor(A, B):
    return 1 if (A != B) else 0

# --- DATA PILIHAN ---
OPTIONS = {
    "0 (False)": 0,
    "1 (True)": 1
}

# --- FUNGSI STYLING (HIGHLIGHT BARIS AKTIF) ---
# Fungsi ini menyorot baris input aktif
def highlight_current_row(row):
    """Menyorot baris di Tabel Kebenaran yang sesuai dengan Input A dan B terakhir yang dihitung."""
    # Pastikan perhitungan sudah dilakukan
    if 'last_A' in st.session_state and 'last_B' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        last_B = st.session_state['last_B']
        
        # Logika pencocokan baris untuk gerbang 2 input
        is_current_row = (row['A'] == last_A) and (row['B'] == last_B)
        
        if is_current_row:
            # Warna background yang lembut untuk baris aktif
            return ['background-color: rgba(255, 255, 255, 0.1)' for _ in row] 
    return ['' for _ in row]

def highlight_not_row(row):
    # Pastikan perhitungan sudah dilakukan
    if 'last_A' in st.session_state and st.session_state.get('calculated', False):
        last_A = st.session_state['last_A']
        is_current_row = (row['A'] == last_A)
        
        if is_current_row:
            return ['background-color: rgba(255, 255, 255, 0.1)' for _ in row] 
    return ['' for _ in row]

# Fungsi styling sel Output 1 (dihidupkan kembali untuk visualisasi)
def style_output(val: Literal[0, 1]):
    """Mengembalikan style CSS/HTML untuk menyorot Output = 1 (True)"""
    if val == 1:
        color = "#00FF7F" # Hijau Cerah
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

# --- Memuat CSS kustom ---
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# --- TAMPILAN STREAMLIT (Mockup Horizontal Flow) ---
st.set_page_config(layout="centered") 

st.markdown("<h1 style='text-align: center;'>Kalkulator Gerbang Logika</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>sekut646yf4t</h3>", unsafe_allow_html=True)
st.markdown("---")

# Menggunakan container utama untuk semua input dan tombol hitung
with st.container(border=True):
    
    # 1. SETUP TATA LETAK 4 KOLOM
    col1, col2, col3, col4 = st.columns([1, 1, 1, 0.7]) 

    # 2. INPUT A
    with col1:
        A_label = st.selectbox(
            "Input A:", 
            options=list(OPTIONS.keys()),
            index=1, # Default ke 1 (True)
            key="select_a"
        )
        A = OPTIONS[A_label]

    # 3. OPERATOR
    with col2:
        selected_gate = st.selectbox(
            "Operator:",
            options=('AND', 'OR', 'XOR', 'NOT'),
            key="select_gate"
        )

    # 4. INPUT B
    with col3:
        if selected_gate != 'NOT':
            B_label = st.selectbox(
                "Input B:", 
                options=list(OPTIONS.keys()),
                index=1, # Default ke 1 (True)
                key="select_b"
            )
            B = OPTIONS[B_label]
        else:
            B = 0 
            # Memberikan placeholder agar kolom tidak kosong saat NOT dipilih
            st.markdown("<p style='margin-top: 30px; font-size: 12px; color: grey;'>Input B diabaikan (NOT)</p>", unsafe_allow_html=True)
            

    # 5. TOMBOL HITUNG
    with col4:
        # Menambahkan spasi vertikal agar tombol sejajar dengan input
        st.markdown("<br>", unsafe_allow_html=True) 
        if st.button("HITUNG", use_container_width=True, key="btn_hitung"):
            st.session_state['calculated'] = True
            st.session_state['last_A'] = A 
            st.session_state['last_B'] = B 
            
            # Logika Hitung
            hasil = None
            if selected_gate == 'AND':
                hasil = gate_and(A, B)
            elif selected_gate == 'OR':
                hasil = gate_or(A, B)
            elif selected_gate == 'NOT':
                hasil = gate_not(A)
            elif selected_gate == 'XOR':
                hasil = gate_xor(A, B)
            
            # Tampilkan Hasil di luar container input
            st.session_state['hasil_display'] = hasil
            st.session_state['selected_gate_display'] = selected_gate
            st.session_state['A_display'] = A
            st.session_state['B_display'] = B
            st.session_state['A_label_display'] = A_label
        
        # Reset status calculated saat input berubah
        if st.session_state.get('calculated', False) and (st.session_state['last_A'] != A or st.session_state['last_B'] != B or st.session_state['selected_gate_display'] != selected_gate):
            st.session_state['calculated'] = False

# 6. KOTAK HASIL (Muncul setelah HITUNG ditekan)
if st.session_state.get('calculated', False):
    st.markdown("---")
    with st.container(border=True):
        hasil = st.session_state['hasil_display']
        selected_gate = st.session_state['selected_gate_display']
        A_display = st.session_state['A_display']
        B_display = st.session_state['B_display']
        A_label_display = st.session_state['A_label_display']
        
        if selected_gate == 'NOT':
            st.success(f"Output **NOT** dari **{A_display} ({A_label_display.split(' ')[1]})** adalah: **{hasil}**")
        else:
            st.success(f"Output **{selected_gate}** dari **{A_display}** dan **{B_display}** adalah: **{hasil}**")


# # --- 7. TABEL KEBENARAN ---
st.markdown("---")

# Ambil nilai gerbang yang dipilih dari selectbox (untuk eksekusi awal/perubahan)
# Kita pastikan selected_gate selalu memiliki nilai di sini.
current_selected_gate = selected_gate 

# Tampilkan Judul Tabel
st.subheader(f"📋 Tabel Kebenaran {current_selected_gate}")

# --- Memproses Data Tabel ---
if current_selected_gate not in ('NOT'):
    # Data Gerbang 2 Input (AND, OR, XOR, NAND, NOR, XNOR)
    
    # Ambil fungsi gerbang dari globals()
    # PENTING: Kita menggunakan current_selected_gate, BUKAN variabel yang belum tentu didefinisikan.
    gate_func = globals()[f'gate_{current_selected_gate.lower()}']
    
    data = {
        'A': [0, 0, 1, 1],
        'B': [0, 1, 0, 1],
        f'Output ({current_selected_gate})': [ # Ganti 'Output' dengan 'Output (Gerbang)'
            gate_func(0, 0),
            gate_func(0, 1),
            gate_func(1, 0),
            gate_func(1, 1),
        ]
    }
    df = pd.DataFrame(data)
    
    # 1. Terapkan styling sel Output (hijau jika 1)
    # Gunakan nama kolom yang sudah diperbarui
    styled_df = df.style.applymap(style_output, subset=[f'Output ({current_selected_gate})'])
    
    # 2. Terapkan styling baris (sorot baris yang baru dihitung)
    if st.session_state.get('calculated', False):
        styled_df = styled_df.apply(highlight_current_row, axis=1) 
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)


else:
    # Data Gerbang NOT
    data = {
        'A': [0, 1],
        f'Output (NOT)': [gate_not(0), gate_not(1)],
    }
    df = pd.DataFrame(data)
    
    # 1. Terapkan styling sel Output (hijau jika 1)
    styled_df = df.style.applymap(style_output, subset=[f'Output (NOT)'])
    
    # 2. Terapkan styling baris khusus NOT
    if st.session_state.get('calculated', False):
        styled_df = styled_df.apply(highlight_not_row, axis=1)

    st.dataframe(styled_df, use_container_width=True, hide_index=True)