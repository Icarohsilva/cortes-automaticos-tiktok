import os
import streamlit as st
from cortar_video import baixar_video, processar_video, criar_pastas

# ========== CONFIGURAÇÕES ==========
PASTA_ORIGINAL = "original"
PASTA_CORTES = "cortes"
NOME_VIDEO = "video_original.mp4"

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="Cortador de Vídeos YouTube para TikTok", layout="centered")
st.title("✂️ Cortador Automático de Vídeos YouTube → TikTok")

st.markdown("""
Este app baixa vídeos do YouTube, corta em partes menores, centraliza e adiciona sua marca d'água.
Ideal para conteúdos verticais no TikTok ou Reels.
""")

url = st.text_input("📥 Cole a URL do vídeo do YouTube:", placeholder="https://youtube.com/...")
duracao = st.slider("⏱️ Duração de cada parte (segundos):", 30, 300, 90)

logo_file = st.file_uploader("📷 Faça upload da logo (PNG com fundo transparente):", type=["png"])

gerar = st.button("🎬 Gerar cortes")

if gerar and url:
    criar_pastas()
    caminho = os.path.join(PASTA_ORIGINAL, NOME_VIDEO)

    # Salva logo (se houver)
    if logo_file:
        with open(os.path.join("assets", "logo.png"), "wb") as f:
            f.write(logo_file.read())
        st.success("✅ Logo carregada com sucesso!")

    # Download do vídeo
    with st.spinner("🔽 Baixando vídeo do YouTube..."):
        if not baixar_video(url, caminho):
            st.error("❌ Falha ao baixar vídeo.")
            st.stop()

    # Processamento
    with st.spinner("✂️ Processando cortes..."):
        from cortar_video import DURACAO_POR_PARTE
        DURACAO_POR_PARTE = duracao  # Atualiza config
        total, ok = processar_video(caminho)

    st.success(f"✅ {ok}/{total} partes geradas com sucesso!")

    for i in range(1, total + 1):
        parte_path = os.path.join(PASTA_CORTES, f"parte_{i}.mp4")
        if os.path.exists(parte_path):
            with open(parte_path, "rb") as f:
                st.download_button(
                    label=f"📥 Baixar Parte {i}",
                    data=f,
                    file_name=f"parte_{i}.mp4",
                    mime="video/mp4"
                )
