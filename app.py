import streamlit as st

# --- Fungsi Logika Gerbang ---
def gate_and(A, B):
    # AND: Output 1 hanya jika A=1 DAN B=1
    return 1 if (A == 1 and B == 1) else 0

def gate_or(A, B):
    # OR: Output 1 jika A=1 ATAU B=1
    return 1 if (A == 1 or B == 1) else 0

def gate_not(A):
    # NOT: Membalikkan input
    return 1 if A == 0 else 0

def gate_xor(A, B):
    # XOR: Output 1 jika input BERBEDA
    return 1 if (A != B) else 0

# --- Antarmuka Streamlit ---
# --- Antarmuka Streamlit Baru ---
st.set_page_config(layout="centered") # Membuat konten berada di tengah
st.title("💡 Kalkulator Logika Kustom")
st.markdown("---")


# 1. KOTAK PENGATURAN INPUT
with st.container(border=True):
    st.header("⚙️ Pengaturan Gerbang")

    # Membuat 3 kolom untuk Input A, Operator, dan Input B
    col_A, col_OP, col_B = st.columns([1, 1.5, 1]) 

    with col_A:
        # Mengubah label input menjadi Teks True/False
        A_label = st.radio("**Input A**", ["0 (False)", "1 (True)"], horizontal=True)
        A = int(A_label[0]) # Mengambil nilai biner (0 atau 1)

    with col_B:
        # Input B akan didefinisikan nanti, karena bisa disembunyikan
        B_label = st.radio("**Input B**", ["0 (False)", "1 (True)"], horizontal=True)
        B = int(B_label[0])

    with col_OP:
        selected_gate = st.radio(
            "**Pilih Operator**",
            ('AND', 'OR', 'XOR', 'NOT'),
            horizontal=True # Tombol operator disusun horizontal
        )
        # Menghilangkan Input B jika operatornya adalah NOT
        if selected_gate == 'NOT':
            # Ini akan menyembunyikan input B dari tampilan
            B = 0 
            col_B.empty() # Membersihkan kolom B jika NOT
        
    # Tombol Hitung diletakkan di bawah kolom
    st.markdown("---")
    
    # 2. PROSES HITUNG
    if st.button(f"Hitung Hasil **{selected_gate}**", use_container_width=True):
        hasil = None
        
        if selected_gate == 'AND':
            hasil = gate_and(A, B)
        elif selected_gate == 'OR':
            hasil = gate_or(A, B)
        elif selected_gate == 'NOT':
            hasil = gate_not(A)
        elif selected_gate == 'XOR':
            hasil = gate_xor(A, B)
        
        # 3. KOTAK HASIL
        st.subheader("✅ Hasil")
        if selected_gate == 'NOT':
             st.success(f"Output **NOT** dari **{A} ({A_label.split(' ')[1]})** adalah: **{hasil}**")
        else:
            st.success(f"Output **{selected_gate}** dari **{A}** dan **{B}** adalah: **{hasil}**")


# 4. TABEL KEBENARAN
st.markdown("---")
st.subheader("📋 Tabel Kebenaran")

if selected_gate != 'NOT':
    data = {
        'A': [0, 0, 1, 1],
        'B': [0, 1, 0, 1],
        f'A {selected_gate} B': [
            globals()[f'gate_{selected_gate.lower()}'](0, 0),
            globals()[f'gate_{selected_gate.lower()}'](0, 1),
            globals()[f'gate_{selected_gate.lower()}'](1, 0),
            globals()[f'gate_{selected_gate.lower()}'](1, 1),
        ]
    }
    st.table(data)
else:
    data = {
        'A': [0, 1],
        f'NOT A': [gate_not(0), gate_not(1)],
    }
    st.table(data)