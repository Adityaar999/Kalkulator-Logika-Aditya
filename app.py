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
st.title("🔢 Kalkulator Gerbang Logika")
st.markdown("Pilih gerbang logika dan masukkan nilai **A** dan **B** (0 atau 1).")

# Pilihan Gerbang di Sidebar
selected_gate = st.sidebar.radio(
    "Pilih Gerbang Logika:",
    ('AND', 'OR', 'NOT', 'XOR')
)

# Input Nilai A dan B
if selected_gate != 'NOT':
    col1, col2 = st.columns(2)
    with col1:
        A = st.radio("Input A", [0, 1])
    with col2:
        B = st.radio("Input B", [0, 1])
else:
    # Hanya Input A yang diperlukan untuk NOT
    A = st.radio("Input A", [0, 1])
    B = 0 

# Tombol Hitung
if st.button(f"Hitung Hasil {selected_gate}"):
    hasil = None
    
    # Menghitung hasil berdasarkan pilihan gerbang
    if selected_gate == 'AND':
        hasil = gate_and(A, B)
    elif selected_gate == 'OR':
        hasil = gate_or(A, B)
    elif selected_gate == 'NOT':
        hasil = gate_not(A)
    elif selected_gate == 'XOR':
        hasil = gate_xor(A, B)
    
    # Menampilkan output
    if selected_gate == 'NOT':
        st.success(f"Hasil **NOT** dari **{A}** adalah: **{hasil}**")
    else:
        st.success(f"Hasil **{selected_gate}** dari **{A}** dan **{B}** adalah: **{hasil}**")

# Tampilkan Tabel Kebenaran (Opsional, untuk referensi)
st.markdown("---")
if selected_gate != 'NOT':
    st.subheader(f"Tabel Kebenaran {selected_gate}")
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
    st.subheader(f"Tabel Kebenaran {selected_gate}")
    data = {
        'A': [0, 1],
        f'NOT A': [gate_not(0), gate_not(1)],
    }
    st.table(data)