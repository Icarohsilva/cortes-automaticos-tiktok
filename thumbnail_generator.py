# thumbnail_generator.py
import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ImageClip
from moviepy.video.fx.Resize import Resize
from moviepy.video.fx.Margin import Margin

# ========== CONFIGURAÇÕES ==========
RESOLUCAO_FINAL = (1080, 1920)
FONTE = "Arial-Bold"
TAMANHO_TEXTO = 80
COR_TEXTO = "white"
COR_CONTORNO = "black"
MARGEM_CONTORNO = 5
CAMINHO_LOGO = "assets/logo.png"
PASTA_CORTES = "cortes"
PASTA_THUMBNAILS = "thumbnails"
os.makedirs(PASTA_THUMBNAILS, exist_ok=True)

def gerar_thumbnail(caminho_video: str, titulo: str, indice: int):
    try:
        clip = VideoFileClip(caminho_video).subclip(0, 1)  # Pega 1 segundo como base
        frame = clip.get_frame(0)

        # Cria fundo com primeiro frame
        imagem_fundo = ImageClip(frame).resize(height=RESOLUCAO_FINAL[1]).with_duration(1)

        # Texto central
        texto = TextClip(
            txt=titulo,
            fontsize=TAMANHO_TEXTO,
            color=COR_TEXTO,
            font=FONTE,
            stroke_color=COR_CONTORNO,
            stroke_width=MARGEM_CONTORNO
        ).set_position("center").set_duration(1)

        elementos = [imagem_fundo, texto]

        # Adiciona logo se existir
        if os.path.exists(CAMINHO_LOGO):
            logo = ImageClip(CAMINHO_LOGO).resize(height=150).set_duration(1)
            pos = ((RESOLUCAO_FINAL[0] - logo.w) // 2, RESOLUCAO_FINAL[1] - logo.h - 50)
            logo = logo.set_position(pos)
            elementos.append(logo)

        thumbnail = CompositeVideoClip(elementos, size=RESOLUCAO_FINAL)
        caminho_thumb = os.path.join(PASTA_THUMBNAILS, f"thumb_parte_{indice}.png")
        thumbnail.save_frame(caminho_thumb, t=0.5)

        print(f"✅ Thumbnail gerada: {caminho_thumb}")

    except Exception as e:
        print(f"❌ Erro ao gerar thumbnail da parte {indice}: {e}")

# Exemplo de uso manual
# gerar_thumbnail("cortes/parte_1.mp4", "Parte 1: O Despertar do Código", 1)
