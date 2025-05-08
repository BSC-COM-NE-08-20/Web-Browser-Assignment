import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local PyQt Browser")
        self.setGeometry(100, 100, 1000, 600)

        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://localhost:8080"))
        self.setCentralWidget(self.browser)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())