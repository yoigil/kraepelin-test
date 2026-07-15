import streamlit as st
import random

st.set_page_config(page_title="Regstrasi - Tes Kraepelin", layout="centered")

TOTAL_COLUMNS = 50

# --- Initialize Global Session Variables ---
if "step" not in st.session_state:
    st.session_state["step"] = "login"
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "user_nik" not in st.session_state:
    st.session_state["user_nik"] = ""
if "current_column" not in st.session_state:
    st.session_state["current_column"] = 0
if "row_index" not in st.session_state:
    st.session_state["row_index"] = 0
if "start_time" not in st.session_state:
    st.session_state["start_time"] = 0.0
if "attempts" not in st.session_state:
    st.session_state["attempts"] = [0] * TOTAL_COLUMNS
if "corrects" not in st.session_state:
    st.session_state["corrects"] = [0] * TOTAL_COLUMNS
if "errors" not in st.session_state:
    st.session_state["errors"] = [0] * TOTAL_COLUMNS
if "numbers_matrix" not in st.session_state:
    st.session_state["numbers_matrix"] = [[random.randint(1, 9) for _ in range(120)] for _ in range(TOTAL_COLUMNS)]

# Hide the sidebar navigation automatically to keep the exam clean
st.markdown("<style>section[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

st.title("Psikotest Kraepelin")
st.divider()

st.warning(
    "**PERINGATAN PENTING:** Tes ini menggunakan penghitung waktu otomatis. "
    "Setiap kolom berjalan selama tepat **15 detik**. Ketika waktu habis, sistem akan "
    "memindahkan Anda ke kolom berikutnya secara paksa. **Jangan refresh halaman selama tes berlangsung!**",
    icon="⚠️"
)

st.warning(
    "**NOTE:** Apabila mengerjakan tes ini melalui smartphone, "
    "**Tolong gunakan Google Chrome dan pastikan website sudah dalam Mode Website**.  "
    "Tekan titik tiga pada pojok kanan atas, dan cek mode website.",
    icon="⚠️"
)
st.divider()

st.markdown("### Panduan Pelaksanaan Tes:")
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.markdown(
        "**Cara Menjawab:**\n"
        "1. Anda akan melihat **dua angka aktif** berwarna biru di tengah layar.\n"
        "2. **Jumlahkan kedua angka** tersebut (Angka Atas + Angka Bawah).\n"
        "3. Ambil **angka digit terakhir** saja dari hasil penjumlahan.\n"
        "   * *Contoh:* $4 + 5 = \\mathbf{9}$ (Ketik **9**)\n"
        "   * *Contoh:* $8 + 7 = 1\\mathbf{5}$ (Ketik **5**)"
    )
with col_g2:
    st.markdown(
        "**Metode Input & Kontrol:**\n"
        "* **Layar Sentuh/Mouse:** Anda bisa mengklik tombol angka yang tertera pada numpad digital di layar.\n"
        "* Tes terdiri dari **50 Kolom berturut-turut**."
    )
    
st.divider()

st.markdown("### Identitas Peserta")

name_input = st.text_input("Masukkan Nama Lengkap Anda sesuai KTP dengan huruf kapital:", placeholder="Contoh: BUDI SANTOSO")
nik_input = st.text_input("Masukkan NIK KTP anda:", placeholder="Contoh: 3171xxxxxxxxxxxx")

if st.button("Mulai Tes!", type="primary"):
    if not name_input.strip() or not nik_input.strip():
        st.error("Nama dan NIK tidak boleh kosong!")
    else:
        st.session_state["user_name"] = name_input.strip()
        st.session_state["user_nik"] = nik_input.strip()
        st.session_state["step"] = "active_test"
        import time
        st.session_state["start_time"] = time.time()
        
        # Native page navigation clears the DOM entirely!
        st.switch_page("pages/1_mulai_tes.py")
