import yt_dlp

class ArchiveEngine:
    def __init__(self, download_path="./data/videos"):
        self.download_path = download_path

    def process_video(self, url: str):
        # Configuration respectueuse : pas de contournement de DRM
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{self.download_path}/%(uploader)s/%(title)s.%(ext)s',
            'restrictfilenames': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Extraction des infos
            info = ydl.extract_info(url, download=False)
            
            # 2. Logique de validation (Droits, durée, etc.)
            print(f"Archivage de : {info.get('title')}")
            
            # 3. Téléchargement effectif
            ydl.download([url])
            
            return info
