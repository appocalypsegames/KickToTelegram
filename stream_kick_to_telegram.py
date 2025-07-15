import subprocess
import config
import cloudscraper
import re

def obtener_stream_hls_kick(canal):
    scraper = cloudscraper.create_scraper()
    url = f"https://kick.com/{canal}"
    try:
        pagina = scraper.get(url, timeout=10).text
        urls_m3u8 = re.findall(r'https://[^\s"\']+?\.m3u8', pagina)
        if urls_m3u8:
            print(f"URL HLS encontrada: {urls_m3u8[0]}")
            return urls_m3u8[0], scraper  # Devolvemos scraper para usar sus cabeceras
        else:
            print("No se encontró URL .m3u8 en la página.")
            return None, None
    except Exception as e:
        print(f"Error al obtener stream HLS: {e}")
        return None, None
        
def stream_kick_canal_con_streamlink(canal):
    url_kick = f"https://kick.com/{canal}"
    rtmp_url = f"{config.TELEGRAM_RTMP_URL}/{config.TELEGRAM_STREAM_KEY}"

    print(f"🎬 Iniciando stream desde: {url_kick}")
    print(f"📡 Transmitiendo hacia Telegram: {rtmp_url}")

    try:
        # Comando streamlink + ffmpeg
        streamlink_cmd = [
            "streamlink",
            url_kick,
            "best",
            "-O"  # Output por stdout
        ]

        ffmpeg_cmd = [
            "ffmpeg",
            "-re",
            "-i", "pipe:0",  # lee desde stdin (streamlink)
            "-c:v", "copy",
            "-c:a", "aac",
            "-f", "flv",
            rtmp_url
        ]

        # Lanza streamlink y pasa salida a ffmpeg
        streamlink_proc = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE)
        ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=streamlink_proc.stdout)

        # Esperar a que termine
        ffmpeg_proc.wait()
        print("🛑 Transmisión finalizada.")

    except Exception as e:
        print(f"❌ Error durante la retransmisión: {e}")
