from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from cowpy import cow
import json
import sys


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        # import pdb; pdb.set_trace()

        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()

            self.wfile.write(return_html_string())
            return

        elif parsed_path.path == '/cowsay':
            self.send_response(200)
            self.end_headers()

            self.wfile.write(b'Helpful instructions about this application')
            return

        
        elif parsed_path.path == '/cow':
            try:
                # import pdb; pdb.set_trace()
                msg = parsed_qs['msg'][0]
                print(msg)
            except (KeyError, json.decoder.JSONDecodeError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'You did a bad thing')
                return

            cheese = cow.Moose(thoughts=True)
            message = cheese.milk(msg)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(message.encode('utf8'))
            return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)
        
        if parsed_path.path == '/cow':
            try:
                msg = parsed_qs['msg'][0]
                cheese = cow.Moose(thoughts=True)
                message = cheese.milk(msg)
                post_dict = {}
                post_dict['content'] = message
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(post_dict).encode('utf8'))
                return
            except (KeyError, json.decoder.JSONDecodeError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'You did a bad thing')
                return


def create_server():
    return HTTPServer(('127.0.0.1', 3000), SimpleHTTPRequestHandler)


def run_forever():
    server = create_server()

    try:
        print('Starting server on port 3000')
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
        # sys.exit()

def return_html_string():
    return b'''<!DOCTYPE html>
<html>
<head>
    <title> cowsay </title>
</head>
<body>
    <header>
        <nav>
        <ul>
            <li><a href="/cowsay">cowsay</a></li>
        </ul>
        </nav>
    <header>
    <main>
        <!-- project description -->
    </main>
</body>
</html>'''


if __name__ == '__main__':
    run_forever()
