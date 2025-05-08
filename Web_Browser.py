from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import requests

LOCAL_SERVER = "http://localhost:8000"

class Browser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Browser")

        self.web_view = QWebEngineView()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search or enter page name")
        self.search_bar.returnPressed.connect(self.load_page)

        self.go_button = QPushButton("Search")
        self.go_button.clicked.connect(self.load_page)

        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.go_button)
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def load_page(self):
        query = self.search_bar.text().strip().lower()
        if not query:
            return

        url = f"{LOCAL_SERVER}/{query}.html"
        try:
            r = requests.head(url)
            if r.status_code == 200:
                self.web_view.load(url)
            else:
                self.web_view.load(f"{LOCAL_SERVER}/not_found.html")
        except:
            self.web_view.setHtml(f"<h1>Server not reachable</h1>")

app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())
