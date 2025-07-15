import cloudscraper
import re
import subprocess
import config

def obtener_stream_hls_kick(canal):
    scraper = cloudscraper.create_scraper()
    url = f"https://kick.com/{canal}"
    try:
        pagina = scraper.get(url, timeout=10).text
        # Regex corregido para limitar URL hasta .m3u8 sin coger html adicional
        urls_m3u8 = re.findall(r'https://[^\s"\']+?\.m3u8', pagina)
        if urls_m3u8:
            print(f"URL HLS encontrada: {urls_m3u8[0]}")
            return urls_m3u8[0]
        else:
            print("No se encontró URL .m3u8 en la página.")
            return None
    except Exception as e:
        print(f"Error al obtener stream HLS: {e}")
        return None

def stream_kick_canal(canal):
    print(f"Obteniendo stream para canal Kick: {canal}")
    url_hls = obtener_stream_hls_kick(canal)
    if not url_hls:
        print("No se pudo obtener el stream HLS. Abortando.")
        return None
    
    full_rtmp = f"{config.TELEGRAM_RTMP_URL}/{config.TELEGRAM_STREAM_KEY}"
    print(f"Iniciando transmisión a Telegram: {full_rtmp}")

    command_str = f'ffmpeg -i "{url_hls}" -c copy -f flv "{full_rtmp}"'
    
    try:
        process = subprocess.Popen(command_str, shell=True)
        return process
    except Exception as e:
        print(f"Error al iniciar ffmpeg: {e}")
        return None
