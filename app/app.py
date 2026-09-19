from http.server import BaseHTTPRequestHandler, HTTPServer

APP_MESSAGE = "AI-Assisted DevOps Demo Application"


def get_response(path):
    if path == "/":
        return 200, APP_MESSAGE

    if path == "/health":
        return 200, "OK"

    return 404, "Not Found"


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        status, message = get_response(self.path)

        self.send_response(status)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(message.encode())

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)

    print("Server running on port 8080")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
