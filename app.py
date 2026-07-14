# --- Safe View Router ---
current_step = st.session_state.get("step", "login")

def render_login_view():
    st.title("Psikotest Kraepelin")
    st.divider()

    st.warning(
        "**PERINGATAN PENTING:** Tes ini menggunakan penghitung waktu otomatis. "
        "Setiap kolom berjalan selama tepat **15 detik**. Ketika waktu habis, sistem akan "
        "memindahkan Anda ke kolom berikutnya secara paksa. Jangan refresh halaman selama tes berlangsung!",
        icon="⚠️"
    )

    st.warning(
        "**NOTE:** Apabila mengerjakan tes ini melalui smartphone, "
        "Pastikan website sudah dalam **Mode Website**.  "
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
    
    # We use temporary local variables instead of direct state mapping inside text inputs
    name_val = st.text_input("Masukkan Nama Lengkap Anda sesuai KTP dengan huruf kapital:", placeholder="Contoh: BUDI SANTOSO")
    nik_val = st.text_input("Masukkan NIK KTP anda:", placeholder="Contoh: 3171xxxxxxxxxxxx")
    
    if st.button("Mulai Tes!", type="primary"):
        if not name_val.strip() or not nik_val.strip():
            st.error("Nama dan NIK tidak boleh kosong!")
        else:
            st.session_state["user_name"] = name_val.strip()
            st.session_state["user_nik"] = nik_val.strip()
            st.session_state["step"] = "active_test"
            st.session_state["start_time"] = time.time()
            st.rerun()

def render_active_test_view():
    with st.expander("PANDUAN SINGKAT CARA MENJAWAB (Klik untuk tutup/buka)", expanded=True):
        st.info(
            "**Jumlahkan dua angka aktif** (berwarna biru). Input **digit terakhir** dari hasil penjumlahan.\n\n"
            "* *Contoh:* $4 + 5 = \\mathbf{9}$ (Ketik **9**) | $8 + 7 = 1\\mathbf{5}$ (Ketik **5**)\n"
            "* Gunakan **Keyboard/Numpad** fisik Anda atau klik tombol di bawah untuk menjawab."
        )
    
    col_idx = st.session_state.get("current_column", 0)
    row_idx = st.session_state.get("row_index", 0)
    
    elapsed_time = time.time() - st.session_state.get("start_time", time.time())
    time_left = max(0, int(TIME_PER_COLUMN - elapsed_time))
    
    if elapsed_time >= TIME_PER_COLUMN:
        next_column()
        st.rerun()
        
    st.subheader(f"Peserta: {st.session_state.get('user_name', '')}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Kolom Aktif", f"{col_idx + 1} / {TOTAL_COLUMNS}")
    c2.metric("Sisa Waktu Kolom", f"{time_left} detik")
    c3.metric("Total Soal Terjawab", sum(st.session_state.get("attempts", [0])))
    
    st.divider()
    
    matrix = st.session_state.get("numbers_matrix")[col_idx]
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
        st.html("""
            <style>
                div[data-testid="stButton"] button p {
                    font-size: 36px !important;
                    font-weight: bold !important;
                }
            </style>
        """)
        
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

    js_listener = """
    <script>
    const handleKeyDown = (e) => {
        if (e.key >= '0' && e.key <= '9') {
            const btn = window.parent.document.querySelector(`button[key="btn_${e.key}"]`);
            if (btn) btn.click();
        }
    };
    window.parent.document.removeEventListener('keydown', handleKeyDown);
    window.parent.document.addEventListener('keydown', handleKeyDown);
    </script>
    """
    st.components.v1.html(js_listener, height=0, width=0)
            
    time.sleep(0.1)
    st.rerun()

def render_finished_view():
    st.balloons()
    st.title("Tes Selesai!")
    st.success(f"Selamat {st.session_state.get('user_name', '')}, Anda telah menyelesaikan seluruh rangkaian ujian Kraepelin!")
    
    excel_data = generate_xlsx()
    
    st.download_button(
        label="Download Excel Hasil Evaluasi",
        data=excel_data,
        file_name=f"Laporan_Kraepelin_{st.session_state.get('user_name', 'peserta').replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
    
    if st.button("Ulangi Tes Baru"):
        st.session_state.clear()
        st.rerun()

# --- Execution Gatekeeper ---
if current_step == "login":
    render_login_view()
elif current_step == "active_test":
    render_active_test_view()
elif current_step == "finished":
    render_finished_view()
