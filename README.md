# 🎬 Cortes Automáticos para TikTok

Este projeto em Python permite baixar vídeos do YouTube, cortá-los automaticamente em partes ideais para TikTok (formato 9:16), adicionar marca d’água (logo) e exportar os cortes prontos para publicação.

## 🚀 Funcionalidades

- 📥 Download automático de vídeos via YouTube.
- ✂️ Corte em múltiplas partes (com sobreposição de 5s entre cortes para manter o contexto).
- 🖼️ Adição de marca d'água personalizada.
- 📱 Redimensionamento inteligente para o formato vertical (1080x1920).
- 💾 Exportação em alta qualidade com áudio sincronizado.

## 🧰 Tecnologias

- Python 3.10+
- [yt_dlp](https://github.com/yt-dlp/yt-dlp)
- [moviepy](https://github.com/Zulko/moviepy)

## 📁 Estrutura

```bash
.
├── cortar_video.py
├── original/
├── cortes/
└── assets/
````

## ⚙️ Como usar

1. Clone o repositório:

```bash
git clone https://github.com/seu_usuario/cortes-automaticos-tiktok.git
cd cortes-automaticos-tiktok
```

2. Instale as dependências:

```bash
pip install yt-dlp moviepy
```

3. Execute o script:

```bash
python cortar_video.py
```

## 🖼️ Personalização

* Substitua a logo em `assets/logo.png`.
* Altere a `URL` do vídeo no topo do script `cortar_video.py`.
* Modifique `DURACAO_POR_PARTE` para definir a duração máxima de cada parte.

## ✍️ Autor

Desenvolvido por [Icaro Silva](https://github.com/Icarohsilva).
Ideia original para facilitar a criação de conteúdo para redes sociais.

---

📌 *Futuramente: integração com legendas automáticas, upload direto para TikTok e painel com Streamlit.*

```

---

Se quiser, posso gerar também o `requirements.txt` ou um `README` com imagem e badges. Deseja algo a mais?
```
