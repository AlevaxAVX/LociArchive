from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QLabel, QMessageBox, QProgressBar)
from PySide6.QtCore import Qt
from core.downloader import DownloadWorker
from core.library import LibraryManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LociArchive - Archivage Vidéo Local")
        self.resize(900, 600)
        self.db = LibraryManager()
        
        self.setup_ui()
        self.refresh_library()

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Zone d'ajout
        add_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Coller l'URL de la vidéo ici (YouTube, TikTok, X...)")
        self.add_btn = QPushButton("Archiver")
        self.add_btn.clicked.connect(self.start_archive)
        
        add_layout.addWidget(self.url_input)
        add_layout.addWidget(self.add_btn)
        layout.addLayout(add_layout)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Bibliothèque
        layout.addWidget(QLabel("Ma Bibliothèque Hors-ligne :"))
        self.video_list = QListWidget()
        layout.addWidget(self.video_list)

        self.setCentralWidget(central_widget)

    def start_archive(self):
        url = self.url_input.text().strip()
        if not url: return

        self.add_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0) # Mode indéterminé

        self.worker = DownloadWorker(url)
        self.worker.finished.connect(self.on_download_success)
        self.worker.error.connect(self.on_download_error)
        self.worker.start()

    def on_download_success(self, info):
        self.db.add_video(info)
        self.refresh_library()
        self.reset_ui()
        QMessageBox.information(self, "Succès", f"Vidéo archivée : {info['title']}")

    def on_download_error(self, err):
        self.reset_ui()
        QMessageBox.critical(self, "Erreur", f"Échec de l'archivage : {err}")

    def reset_ui(self):
        self.add_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.url_input.clear()

    def refresh_library(self):
        self.video_list.clear()
        videos = self.db.get_all_videos()
        for v in videos:
            item = QListWidgetItem(f"[{v['platform'].upper()}] {v['title']} - {v['author']}")
            self.video_list.addItem(item)
