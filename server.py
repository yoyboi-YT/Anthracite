import json
import random
import string
import http.server
import socketserver

def log(txt: str):
    print(txt)
    with open('log.txt', 'a') as f:
        f.write(txt + '\n')

try:
    with open('cfg.json', 'r') as f:
        cfg = json.load(f)
except FileNotFoundError:
    default_cfg = {
        "key": "",
        "allow-pull": True,
        "allow-push": False,
        "port": 1024
    }
    with open('cfg.json', 'w') as f:
        json.dump(default_cfg, f, indent=4)
    log("Default config has been loaded")
    cfg = default_cfg

try:
    with open('ldb.json', 'r') as f:
        pass
except:
    with open('ldb.json', 'w') as f:
        json.dump({}, f, indent=4)
    log("LDB missing, created new one")

if len(cfg.get("key")) < 64:
    log("The provided key is too short")
    chs = string.ascii_letters + string.digits + string.punctuation
    chs = chs.replace('"', '').replace('\\', '')  # Avoid JSON issues
    cfg["key"] = ''.join(random.choices(chs, k=64))
    with open('cfg.json', 'w') as f:
        json.dump(cfg, f, indent=4)
    log("A new key has been placed in the config")
    quit()

log("Key accepted")

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ldb":
            if not cfg.get("allow-pull", False):
                self.send_response(403)
                self.end_headers()
                log("GET 403")
                return
            
            if self.headers.get("X_API_KEY") != cfg["key"]:
                self.send_response(401)
                self.end_headers()
                log("GET 401")
                return
            
            try:
                with open("ldb.json", "r") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode())
                log("GET 200")
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                log("GET 404")
                with open('ldb.json', 'w') as f:
                    json.dump({}, f, indent=4)
                log("LDB missing, created new one")
        else:
            self.send_response(404)
            self.end_headers()
            log("GET 404 (cl)")

    def do_POST(self):
        if self.path == "/ldb":
            if not cfg.get("allow-push", False):
                self.send_response(403)
                self.end_headers()
                log("POST 403")
                return
            
            if self.headers.get("X_API_KEY") != cfg["key"]:
                self.send_response(401)
                self.end_headers()
                log("POST 401")
                return
            
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()

            try:
                json.loads(body)
                with open("ldb.json", "w") as f:
                    f.write(body)
                self.send_response(200)
                self.end_headers()
                log("POST 200")
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                log("POST 400")
        else:
            self.send_response(404)
            self.end_headers()
            log("POST 404")

port = cfg.get("port", 1024)
log(f"Starting server on port {port}")

with socketserver.TCPServer(("0.0.0.0", port), RequestHandler) as httpd:
    log(f"Serving on port {port}")
    httpd.serve_forever()