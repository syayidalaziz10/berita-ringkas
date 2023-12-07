# main.py
import streamlit as st
import time
from summarizer import generate_summary
from keywords import generate_keywords


def main():

    st.set_page_config(
        page_title="Berita Ringkas: Temukan Esensi Berita dengan Mudah", page_icon="📖")

    # img, title = st.columns(2)

    # with img:

    # with title:
    st.image("assets/banner(3).png", use_column_width=True)
    st.subheader("Berita Ringkas: Temukan Esensi Berita dengan Mudah")
    st.caption("Berita ringkas membawa Anda pengalaman membaca berita yang efisien dan informatif. Dapatkan ringkasan berita terkini dalam hitungan detik, membantu Anda tetap terinformasi tanpa harus membaca artikel panjang. Hemat waktu dan tetap up-to-date dengan berita terkini dari berbagai sumber, disajikan secara singkat dan jelas. SimpliNews, teman setia Anda dalam menjelajahi dunia berita")
    col1, col2 = st.columns(2)

    with col1:
        num_sentences = st.selectbox("Jumlah Kalimat",
                                     options=list(range(1, 6)),
                                     index=2,
                                     key="sentences")

    with col2:
        num_keyword = st.selectbox("Jumlah Kata Kunci",
                                   options=list(range(1, 6)),
                                   index=2,
                                   key="keyword")

    news_text = st.text_area(
        "Masukkan Berita Yang Akan Diringkas", key="input_text", height=250)

    if st.button("Buat Ringkasan"):
        if news_text:
            summary = generate_summary(news_text, num_sentences)
            keywords = generate_keywords(news_text, num_keyword)

            with st.expander("Hasil Ringkasan"):
                # st.markdown("Hasil Ringkasan")
                # st.code(summary, language="plaintext")
                st.write(summary)

            with st.expander("Kata Kunci"):
                # st.markdown("Hasil Ringkasan")
                # st.code(summary, language="plaintext")
                st.info(keywords, icon="🗝️")

        else:
            time.sleep(.5)
            st.toast('Masukkan teks terlebih dahulu', icon='🤧')


if __name__ == "__main__":
    main()
