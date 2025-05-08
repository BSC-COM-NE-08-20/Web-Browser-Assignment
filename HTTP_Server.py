from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import urllib.parse
from html import load_html
from pathlib import Path

TEMPLATES_FOLDER = Path("Templates")
PORT = 8080
DATABASE_FILE = "db.txt"

class TemplateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.respond_with_template("register.html")
        elif self.path.startswith("/search") and "query=" in self.path:
            self.handle_search()
        elif self.path == "/search":
            self.respond_with_template("search.html")
        else:
            self.handle_search_direct()

    def do_POST(self):
        if self.path == "/register":
            self.handle_registration()
        else:
            self.send_error(404)

    def respond_with_template(self, filename):
        content = load_html(filename)
        if content:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.respond_not_found()

    def handle_registration(self):
        length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(post_data)
        name = data.get("name", [""])[0]
        email = data.get("email", [""])[0]
        with open(DATABASE_FILE, "a") as f:
            f.write(f"{name},{email}\n")
        self.send_response(302)
        self.send_header("Location", "/search")
        self.end_headers()

    def handle_search(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        search_term = params.get("query", [""])[0]
        filename = f"{search_term}.html"
        if load_html(filename):
            self.respond_with_template(filename)
        else:
            self.respond_with_template("404.html")

    def handle_search_direct(self):
        term = self.path.lstrip("/")
        filename = f"{term}.html"
        if load_html(filename):
            self.respond_with_template(filename)
        else:
            self.respond_with_template("404.html")

    def respond_not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = load_html("404.html") or b"<h1>Not found</h1>"
        self.wfile.write(content)

if __name__ == "__main__":
    with TCPServer(("", PORT), TemplateHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()
