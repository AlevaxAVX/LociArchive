import yt_dlp
import os
from PySide6.QtCore import QObject, Signal, QThread

class DownloadWorker(QThread):
    """Thread de téléchargement pour ne pas geler l'UI."""
    finished = Signal(dict)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, url, download_dir="data/videos"):
        super().__init__()
        self.url = url
        self.download_dir = download_dir

    def run(self):
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'{self.download_dir}/%(extractor)s/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.progress.emit("Analyse des métadonnées...")
                info = ydl.extract_info(self.url, download=True)
                
                # On récupère le chemin final
                filename = ydl.prepare_filename(info)
                info['local_path'] = filename
                
                self.finished.emit(info)
        except Exception as e:
            self.error.emit(str(e))
