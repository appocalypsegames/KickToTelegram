import subprocess
import sys
import requests
import config

def obtener_url_stream_kick(canal):
    url_api = f"https://kick.com/api/v1/channels/{canal}/stream"
    try:
        response = requests.get(url_api, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Dependiendo de la estructura, ajustar la extracción del URL HLS o RTMP
        # Aquí asumo que hay un campo "streamUrl" (ajusta según respuesta real)
        stream_url = data.get("streamUrl")
        if not stream_url:
            # Intenta otras posibles claves, ejemplo:
            stream_url = data.get("stream", {}).get("source", {}).get("url")
        if stream_url:
            print(f"URL del stream de Kick: {stream_url}")
            return stream_url
        else:
            print("No se encontró URL del stream en la respuesta.")
            return None
    except Exception as e:
        print(f"Error al obtener URL del stream: {e}")
        return None

def stream_to_telegram(input_url, rtmp_url, stream_key):
    full_rtmp = f"{rtmp_url}/{stream_key}"
    print(f"Iniciando transmisión a Telegram: {full_rtmp}")
    
    # Comando ffmpeg para reenviar stream
    # Asumiendo input_url es HLS o similar
    command = [
        "ffmpeg",
        "-i", input_url,
        "-c", "copy",
        "-f", "flv",
        full_rtmp
    ]
    
    # Ejecuta ffmpeg y redirige salida a consola
    process = subprocess.Popen(command)
    process.communicate()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python stream_kick_to_telegram.py <canal_kick>")
        sys.exit(1)

    canal = sys.argv[1]
    stream_url = obtener_url_stream_kick(canal)
    if stream_url:
        stream_to_telegram(stream_url, config.TELEGRAM_RTMP_URL, config.TELEGRAM_STREAM_KEY)
    else:
        print("No se pudo obtener el stream para iniciar la transmisión.")
