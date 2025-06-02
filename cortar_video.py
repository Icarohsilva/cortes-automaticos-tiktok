# cortar_video.py
import os
import math
import logging
from typing import Tuple
import yt_dlp
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, ColorClip
# ========== CONFIGURAÇÕES ==========
URL = "https://youtu.be/ErMSHiQRnc8?feature=shared"  # URL do vídeo do YouTube
DURACAO_POR_PARTE = 100  # segundos
PASTA_ORIGINAL = "original"
PASTA_CORTES = "cortes"
PASTA_ASSETS = "assets"
LOGO_PATH = os.path.join(PASTA_ASSETS, "logo.png")
NOME_VIDEO = "video_original.mp4"
RESOLUCAO_FINAL = (1080, 1920)
FPS = 30
# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# ========== FUNÇÕES ========== 
def criar_pastas() -> None:
    os.makedirs(PASTA_ORIGINAL, exist_ok=True)
    os.makedirs(PASTA_CORTES, exist_ok=True)
    os.makedirs(PASTA_ASSETS, exist_ok=True)
    logger.info("📁 Pastas preparadas.")
def baixar_video(url: str, caminho_saida: str) -> bool:
    logger.info("🔽 Baixando vídeo do YouTube...")
    try:
        yt_opts = {
            'outtmpl': caminho_saida,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([url])
        logger.info("✅ Download finalizado!")
        return True
    except Exception as e:
        logger.error(f"❌ Falha no download: {e}")
        return False
def formatar_para_tiktok(clip: VideoFileClip) -> CompositeVideoClip:
    # Redimensiona o vídeo para caber dentro da resolução final, mantendo a proporção
    clip_redimensionado = clip.resized(height=RESOLUCAO_FINAL[1]) if clip.w / clip.h < RESOLUCAO_FINAL[0] / RESOLUCAO_FINAL[1] else clip.resized(width=RESOLUCAO_FINAL[0])
    # Cria fundo preto (tarja) com a resolução final
    fundo = ColorClip(size=RESOLUCAO_FINAL, color=(0, 0, 0), duration=clip.duration)
    # Centraliza o vídeo redimensionado no fundo
    video_final = CompositeVideoClip([fundo, clip_redimensionado.with_position("center")])
    return video_final.with_duration(clip.duration).with_audio(clip.audio)
def aplicar_marca_dagua(clip: VideoFileClip, caminho_logo: str = LOGO_PATH) -> VideoFileClip:
    if not os.path.exists(caminho_logo):
        logger.warning("⚠️ Logo não encontrada. Continuando sem marca d'água.")
        return clip
    try:
        # Aumentar o tamanho da logo proporcionalmente (por exemplo: 300px de altura)
        logo = ImageClip(caminho_logo).resirezed(height=300)
        # Centraliza na parte inferior (bottom center)
        largura_video = RESOLUCAO_FINAL[0]
        largura_logo = logo.w
        posicao_centralizada = ((largura_video - largura_logo) // 2, RESOLUCAO_FINAL[1] - logo.h - 50)  # 50px do fundo
        # Define duração e opacidade
        logo = logo.with_duration(clip.duration).with_opacity(0.9).with_position(posicao_centralizada)
        return CompositeVideoClip([clip, logo], size=RESOLUCAO_FINAL)
    except Exception as e:
        logger.warning(f"⚠️ Falha ao aplicar marca d'água: {e}")
        return clip
def exportar_video(clip: VideoFileClip, caminho_saida: str) -> bool:
    try:
        clip.write_videofile(
            caminho_saida,
            codec="libx264",
            audio_codec="aac",
            fps=FPS,
            threads=4,
            preset='medium',
            bitrate="5000k"
        )
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao exportar vídeo: {e}")
        return False
def processar_video(caminho_video: str) -> Tuple[int, int]:
    try:
        clip = VideoFileClip(caminho_video)
        duracao_total = int(clip.duration)
        num_partes = math.ceil(duracao_total / DURACAO_POR_PARTE)
        logger.info(f"✂️ Iniciando corte em {num_partes} parte(s)...")
        sucesso = 0
        for i in range(num_partes):
            try:
                if i == 0:
                    inicio = 0
                else:
                    inicio = max(i * DURACAO_POR_PARTE - 5, 0)  # Começa 5s antes do fim da parte anterior
                fim = min((i + 1) * DURACAO_POR_PARTE, duracao_total)
                parte = clip.subclipped(inicio, fim)
                parte_formatada = formatar_para_tiktok(parte)
                parte_com_logo = aplicar_marca_dagua(parte_formatada)
                parte_com_logo = parte_com_logo.with_audio(parte.audio)
                caminho_saida = os.path.join(PASTA_CORTES, f"parte_{i + 1}.mp4")
                if exportar_video(parte_com_logo, caminho_saida):
                    logger.info(f"✅ Parte {i + 1} exportada: {caminho_saida}")
                    sucesso += 1
                parte.close()
                parte_formatada.close()
                parte_com_logo.close()
            except Exception as e:
                logger.error(f"❌ Erro na parte {i + 1}: {e}")
        clip.close()
        return num_partes, sucesso
    except Exception as e:
        logger.error(f"❌ Erro ao processar vídeo completo: {e}")
        return 0, 0
# ========== EXECUÇÃO ==========
def main():
    criar_pastas()
    caminho = os.path.join(PASTA_ORIGINAL, NOME_VIDEO)
    if not baixar_video(URL, caminho):
        return
    total, ok = processar_video(caminho)
    logger.info("=" * 50)
    logger.info(f"✅ FINALIZADO: {ok}/{total} partes exportadas.")
    logger.info(f"📁 Cortes salvos em: {os.path.abspath(PASTA_CORTES)}")
    logger.info("=" * 50)
if __name__ == "__main__":
    main()