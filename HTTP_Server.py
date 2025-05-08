from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from pathlib import Path
import urllib.parse

TEMPLATES_FOLDER = Path("Templates")
DATABASE_FILE = "db.txt"
PORT = 8080

class TemplateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.render_registration_form()
        elif self.path == "/register":
            self.handle_registration()
        elif self.path == "/search":
            self.render_search_form()
        else:
            self.handle_search_or_404()

    def render_registration_form(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
            <html><body>
            <h1>Register</h1>
            <form action="/register" method="POST">
                Name: <input type="text" name="name"><br>
                Email: <input type="text" name="email"><br>
                <input type="submit" value="Register">
            </form>
            </body></html>
        """)

    def handle_registration(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        name = self.extract_form_value(post_data, "name")
        email = self.extract_form_value(post_data, "email")

        # Save registration details in db.txt
        with open(DATABASE_FILE, "a") as f:
            f.write(f"{name},{email}\n")

        # After registration, redirect to search page
        self.send_response(302)
        self.send_header("Location", "/search")
        self.end_headers()

    def extract_form_value(self, data, field):
        
        parsed_data = urllib.parse.parse_qs(data)
        return parsed_data.get(field, [None])[0]

    def render_search_form(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
            <html><body>
            <h1>Search for a Template</h1>
            <form action="/search" method="GET">
                Search: <input type="text" name="query"><br>
                <input type="submit" value="Search">
            </form>
            </body></html>
        """)

    def handle_search_or_404(self):

        # Extract search query from URL
        search_query = self.path.split("/")[-1]
        file_path = TEMPLATES_FOLDER / f"{search_query}.html"

        if file_path.exists() and file_path.is_file():
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(file_path.read_bytes())
        else:
            self.respond_not_found()

    def respond_not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            (TEMPLATES_FOLDER / "404.html").read_bytes()
            if (TEMPLATES_FOLDER / "404.html").exists()
            else b"""
            <html><body>
            <h1>404 - Document Not Found</h1>
            <p>Try <a href="https://www.google.com/">searching Google</a>.</p>
            </body></html>
            """
        )

if __name__ == "__main__":
    with TCPServer(("", PORT), TemplateHandler) as server:
        print(f"Serving at http://localhost:{PORT}")
        server.serve_forever()
