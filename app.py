
#Muhammad Fadhilah Ramadhan dan Muhammad Naffa XI-2


import streamlit as st

st.set_page_config(page_title="Bioskop Skuza", page_icon="🎬")



users = {
    "Fadhil": {"password": "fadhil123", "member": True,},
    "Naffa": {"password": "naffa123", "member" : True,},
}

films = {
    "Interstellar": {"Harga": 45000},
    "Avengers": {"Harga": 50000},
    "Upin-Ipin": {"Harga": 35000}
}

def init_session ():
    if"logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.login_attempts = 0

def login (username, password):
    return username in users and users[username]["password"] == password

def halaman_login ():
    st.title("Bioskop Skuza")
    st.subheader("silahkan login")


    if st.session_state.login_attempts >= 3:
        st.error("akunmu dikunci silahkan hubungi admin")
        st.stop()
        

    username = st.text_input("Username")
    password = st.text_input("Password",  type="password")


    sisa = 3 - st.session_state.login_attempts
    st.caption(f"sisa percobaan login: {sisa}x")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_attempts = 0
            st.rerun()
        else:
            st.session_state.login_attempts += 1
            st.error("Username atau password salah!")
            st.rerun()

def pilih_film():
    st.divider()
    st.subheader("🎥 Pilih Film")

    pilihan_film = st.selectbox("Film yang ingin ditonton:", list(films.keys()))
    film = films[pilihan_film]

    st.metric("Harga", f"Rp {film['Harga']:,}")


    return pilihan_film, film


def pilih_jadwal (film):
    st.divider()
    st.subheader("silahkan pilih jadwal🕰️")

    jadwal = st.selectbox("pilih jadwal:", [
        "12:00 - 14:00",
        "14:00 - 16:00",
        "16:00 - 18:00",
        "18:00-20:00",
    ])
    jumlah = st.number_input("Jumlah tiket:", min_value=1, max_value=10, value=1)

    is_member = users[st.session_state.username]["member"]
    harga_asli = film["Harga"] * jumlah

    if is_member:
        diskon = harga_asli * 0.10
        total = harga_asli - diskon
        st.success(f"✅ Kamu member! Diskon 10% = -Rp {diskon:,.0f}")
    else:
        diskon = 0
        total = harga_asli
        st.info("💡 Bukan member, tidak ada diskon.")

    st.info(f"Total harga: Rp {total:,.0f}")

    return jadwal, jumlah, total, diskon

def buat_struk(username, pilihan_film, film, jadwal, jumlah, total, diskon):
    is_member = users[username]["member"]
    struk = f"""
====================================
        STRUK PEMESANAN TIKET
         Bioskop Skuza
====================================
Nama User   : {username}
Status      : {"Member " if is_member else "Non-Member"}
Film        : {pilihan_film}
Jadwal      : {jadwal}
Jumlah      : {jumlah} tiket
Harga/tiket : Rp {film['Harga']:,}
Diskon      : Rp {diskon:,.0f}
------------------------------------
Total       : Rp {total:,.0f}
====================================
Terima kasih telah memesan!
Selamat menikmati film 
====================================
"""
    return struk

def konfirmasi_pesanan(username, pilihan_film, film, jadwal, jumlah, total, diskon):
    st.divider()
    st.subheader("📋 Konfirmasi Pesanan")

    st.table({
        "Detail": ["Film", "Jadwal", "Jumlah Tiket", "Diskon", "Total Harga"],
        "Info": [
            pilihan_film,
            jadwal,
            f"{jumlah} tiket",
            f"Rp {diskon:,.0f}",
            f"Rp {total:,.0f}"
        ]
    })

    if st.button("✅ Pesan Sekarang!"):
        st.success(f"🎉 Pesanan berhasil! Selamat menikmati {pilihan_film}!")
        st.balloons()

        struk = buat_struk(username, pilihan_film, film, jadwal, jumlah, total, diskon)

        st.download_button(
            label="📄 Download Struk",
            data=struk,
            file_name="struk_tiket.txt",
            mime="text/plain"
        )

def halaman_utama():
    st.title("Bioskop Skuza")
    st.write(f"Halo, **{st.session_state.username}**! 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    pilihan_film, film = pilih_film()
    jadwal, jumlah, total, diskon = pilih_jadwal(film)
    konfirmasi_pesanan(st.session_state.username, pilihan_film, film, jadwal, jumlah, total, diskon)



# Main
init_session()

if not st.session_state.logged_in:
    halaman_login()
else:
    halaman_utama()







