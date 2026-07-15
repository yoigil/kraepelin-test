import streamlit as st
import time

st.set_page_config(page_title="Tes Berjalan", layout="centered")
st.markdown("<style>section[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

# Safety check: if accessed directly without registering
if not st.session_state.get("user_name"):
    st.switch_page("app.py")

TOTAL_COLUMNS = 50
TIME_PER_COLUMN = 15

def next_column():
    st.session_state["current_column"] += 1
    st.session_state["row_index"] = 0
    st.session_state["start_time"] = time.time()
    if st.session_state["current_column"] >= TOTAL_COLUMNS:
        st.session_state["step"] = "finished"
        st.switch_page("pages/2_hasil.py")

def process_answer(user_input, correct_digit):
    col = st.session_state["current_column"]
    st.session_state["attempts"][col] += 1
    if user_input == correct_digit:
        st.session_state["corrects"][col] += 1
    else:
        st.session_state["errors"][col] += 1
    st.session_state["row_index"] += 1

with st.expander("PANDUAN SINGKAT CARA MENJAWAB (Klik untuk tutup/buka)", expanded=False):
    st.info(
        "**Jumlahkan dua angka aktif** (berwarna biru). Input **digit terakhir** dari hasil penjumlahan.\n\n"
        "* *Contoh:* $4 + 5 = \\mathbf{9}$ (Ketik **9**) | $8 + 7 = 1\\mathbf{5}$ (Ketik **5**)"
    )

col_idx = st.session_state["current_column"]

# CRITICAL SAFETY CHECK: Stop execution if the test is completed!
if col_idx >= TOTAL_COLUMNS or st.session_state["step"] == "finished":
    st.switch_page("pages/2_hasil.py")
    st.stop() # Force stops Python from reading any further down!

row_idx = st.session_state["row_index"]

st.divider()

# Line 55 now stays completely safe:
matrix = st.session_state["numbers_matrix"][col_idx]
row_idx = st.session_state["row_index"]

elapsed_time = time.time() - st.session_state["start_time"]
time_left = max(0, int(TIME_PER_COLUMN - elapsed_time))

if elapsed_time >= TIME_PER_COLUMN:
    next_column()
    st.rerun()
    
st.subheader(f"Peserta: {st.session_state['user_name']}")
c1, c2, c3 = st.columns(3)
c1.metric("Kolom Aktif", f"{col_idx + 1} / {TOTAL_COLUMNS}")
c2.metric("Sisa Waktu Kolom", f"{time_left} detik")
c3.metric("Total Soal Terjawab", sum(st.session_state["attempts"]))

st.divider()

matrix = st.session_state["numbers_matrix"][col_idx]
num_bottom_preview = matrix[row_idx]
num_lower_active = matrix[row_idx + 1]
num_upper_active = matrix[row_idx + 2]
num_top_preview = matrix[row_idx + 3]
correct_digit = (num_lower_active + num_upper_active) % 10

m1, m2 = st.columns([2, 3])

with m1:
    st.markdown("### Angka")
    st.markdown(f"<div style='background-color:#f0f2f6; padding:10px; border-radius:5px; text-align:center; font-size:28px; color:#555;'>{num_top_preview}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#1f497d; padding:15px; margin:5px 0; border-radius:5px; text-align:center; font-size:36px; font-weight:bold; color:white;'>{num_upper_active}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#1f497d; padding:15px; margin:5px 0; border-radius:5px; text-align:center; font-size:36px; font-weight:bold; color:white;'>{num_lower_active}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#f0f2f6; padding:10px; border-radius:5px; text-align:center; font-size:28px; color:#555;'>{num_bottom_preview}</div>", unsafe_allow_html=True)

with m2:
    st.markdown("### Jawaban")
    st.html("<style>div[data-testid='stButton'] button p { font-size: 36px !important; font-weight: bold !important; }</style>")
    
    numpad_layout = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"]]
    for row in numpad_layout:
        btn_cols = st.columns(3)
        for i, num_str in enumerate(row):
            if btn_cols[i].button(num_str, key=f"btn_{num_str}", use_container_width=True):
                process_answer(int(num_str), correct_digit)
                st.rerun()
                
    if st.button("0", key="btn_0", use_container_width=True):
        process_answer(0, correct_digit)
        st.rerun()

js_listener = f"""
<script>
const handleKeyDown = (e) => {{
    if (e.key >= '0' && e.key <= '9') {{
        const btn = window.parent.document.querySelector(`button[key="btn_${{e.key}}"]`);
        if (btn) btn.click();
    }}
}};
window.parent.document.removeEventListener('keydown', handleKeyDown);
window.parent.document.addEventListener('keydown', handleKeyDown);
</script>
"""
st.components.v1.html(js_listener, height=0, width=0)

time.sleep(0.05)
st.rerun()
