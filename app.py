import streamlit as st
import pandas as pd
# Tambahkan ini di bagian atas file, di bawah import pd:
from typing import Literal # Digunakan untuk tipe data yang lebih spesifik


# ... (Fungsi gate_and, gate_or, gate_not, gate_xor, style_output tetap sama) ...

# 4. TABEL KEBENARAN BARU
st.markdown("---")
st.subheader("📋 Tabel Kebenaran")

# --- Fungsi Styling untuk HTML ---
# Fungsi ini tetap sama, hanya untuk styling sel Output 1
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

# --- Fungsi Styling BARIS BARU ---
def highlight_current_row(row):
    """Menyorot baris di Tabel Kebenaran yang sesuai dengan Input A dan B terakhir yang dihitung."""
    # Ambil input terakhir yang dihitung dari session_state
    if 'last_A' in st.session_state and 'last_B' in st.session_state:
        last_A = st.session_state['last_A']
        last_B = st.session_state['last_B']
        
        # Periksa apakah baris data A dan B sama dengan input terakhir
        is_current_row = (row['A'] == last_A) and (row['B'] == last_B)
        
        if is_current_row:
            # Mengatur styling untuk seluruh baris
            # Kita bisa menggunakan warna background yang lembut untuk row yang aktif
            return ['background-color: rgba(255, 255, 255, 0.1)' for _ in row] 
    
    # Mengembalikan style kosong untuk baris lainnya
    return ['' for _ in row]

# --- Tambahkan Session State di PROSES HITUNG (Langkah 2) ---

# Ubah bagian 2. PROSES HITUNG menjadi:
# ...
    if st.button(f"Hitung Hasil **{selected_gate}**", use_container_width=True):
        
        # --- PERBARUAN PENTING: Simpan input saat ini di session state ---
        st.session_state['last_A'] = A 
        st.session_state['last_B'] = B
        # ----------------------------------------------------------------
        
        hasil = None
# ... (lanjutkan kode hitung sampai ke 3. KOTAK HASIL) ...

# --- MODIFIKASI 4. TABEL KEBENARAN ---

# 4. TABEL KEBENARAN BARU
st.markdown("---")
st.subheader("📋 Tabel Kebenaran")

# --- Memproses Data Tabel ---
if selected_gate != 'NOT':
    # Data Gerbang 2 Input (AND, OR, XOR)
    data = {
        'A': [0, 0, 1, 1],
        'B': [0, 1, 0, 1],
        f'Output {selected_gate}': [
            globals()[f'gate_{selected_gate.lower()}'](0, 0),
            globals()[f'gate_{selected_gate.lower()}'](0, 1),
            globals()[f'gate_{selected_gate.lower()}'](1, 0),
            globals()[f'gate_{selected_gate.lower()}'](1, 1),
        ]
    }
    df = pd.DataFrame(data)
    
    # 1. Terapkan styling sel Output (hijau jika 1)
    styled_df = df.style.applymap(style_output, subset=[f'Output {selected_gate}'])
    
    # 2. Terapkan styling baris (sorot baris yang baru dihitung)
    styled_df = styled_df.apply(highlight_current_row, axis=1) # axis=1 berarti apply per baris
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)


else:
    # Data Gerbang NOT
    data = {
        'A': [0, 1],
        f'Output NOT': [gate_not(0), gate_not(1)],
    }
    df = pd.DataFrame(data)
    
    # Terapkan styling sel Output
    styled_df = df.style.applymap(style_output, subset=['Output NOT'])
    
    # Karena NOT hanya punya satu input, kita hanya perlu mencocokkan A
    if 'last_A' in st.session_state:
        last_A = st.session_state['last_A']
        
        def highlight_not_row(row):
            is_current_row = (row['A'] == last_A)
            if is_current_row:
                return ['background-color: rgba(255, 255, 255, 0.1)' for _ in row] 
            return ['' for _ in row]
            
        styled_df = styled_df.apply(highlight_not_row, axis=1)

    st.dataframe(styled_df, use_container_width=True, hide_index=True)