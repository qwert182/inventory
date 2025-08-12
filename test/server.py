#!/usr/bin/env python3
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer
from time import sleep
import os, sys
import json

opts = {
  "insert-timeout-element": False,
  "print-user-agent": False,
}

for arg in sys.argv[1:]:
  if arg.startswith("--") and arg[2:] in opts:
    opts[arg[2:]] = True

class RequestHandler(SimpleHTTPRequestHandler):
  timeouts = {
    "Unknown": 30,
    "MSIE": 10,
    "Firefox": 5,
  }
  def do_GET(self):
    user_agent = self.headers.get("User-Agent")
    if opts["print-user-agent"]:
      print(f"User-Agent: {user_agent}", file=sys.stderr)

    if self.path.startswith("/timeout."):
      browser = "Unknown"
      if user_agent:
        for browser_name in RequestHandler.timeouts.keys():
          if browser_name != "Unknown" and browser_name in user_agent:
            browser = browser_name
            break
      timeout = RequestHandler.timeouts[browser]
      print(f"! sleep({timeout}) for {browser}", file=sys.stderr)
      sleep(timeout)
      self.send_response(HTTPStatus.GATEWAY_TIMEOUT)
      self.end_headers()
      return

    if opts["insert-timeout-element"] and (self.path.endswith("/src/") or
                                           self.path.endswith("/src/index.htm")):
      path = self.path + "index.htm" if self.path.endswith("/") else self.path
      try:
        with open(self.translate_path(path), "rb") as f:
          index_data = f.read()
        body_close_pos = index_data.rfind(b"</body>")
      except:
        body_close_pos = -1
      if body_close_pos < 0:
        self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.end_headers()
      else:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(index_data[:body_close_pos])
        self.wfile.write(b"<img src=\"/timeout.jpg\" width=\"100\" height=\"50\">")
        self.wfile.write(index_data[body_close_pos:])
      return

    if self.path.find("/src/test_") >= 0 and self.path.endswith(".htm"):
      try:
        with open(self.translate_path(self.path.replace("/src/test_", "/test/unit/test_")[:-4] + ".js"), "rb") as f:
          unit_test_data = f.read()
        with open(os.path.join(os.path.dirname(__file__), "unit/helper.js"), "rb") as f:
          helper_data = f.read()
        with open(os.path.join(os.path.dirname(__file__), "../src/index.htm"), "rb") as f:
          index_data = f.read()
        init_func_pos = index_data.find(b"  function init() {")
      except:
        init_func_pos = -1
      if init_func_pos < 0:
        self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.end_headers()
      else:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(index_data[:init_func_pos])
        self.wfile.write(helper_data)
        self.wfile.write(b"\n")
        self.wfile.write(unit_test_data)
        self.wfile.write(b"  function pass() {\n" +
                         b"    log('Test PASSED', 'color:green;');\n" +
                         b"    document.title = 'Test PASSED';\n" +
                         b"  }\n")
        self.wfile.write(b"  function init() {\n" +
                         b"    document.title = 'Testing...';\n" +
                         b"    if (test() !== 'async_test')\n" +
                         b"      pass();\n" +
                         b"  }\n\n")
        self.wfile.write(b"  function _init() {")
        self.wfile.write(index_data[init_func_pos+19:])
      return

    if self.path.startswith("/api.gh/"):
      for h in self.headers:
        print(f"{h}: {self.headers[h]}", file=sys.stderr)
      self.send_response(HTTPStatus.OK)
      self.send_header("Content-type", "application/json; charset=utf-8")
      self.send_header("Cache-control", "private, max-age=60, s-maxage=60")
      self.send_header("x-github-media-type", "github.v3; format=json")
      self.end_headers()
      response = {
        "id": 0,
        "name": "repo",
        "full_name": "example/repo",
        "owner": { "login": "example", "id": 0 },
        "html_url": "/gh/example/repo",
        "url": "/api.gh/repos/example/repo",
        "default_branch": "main",
      }
      self.wfile.write(json.dumps(response, indent=2).encode())
      return

    super().do_GET()

if __name__ == "__main__":
  with HTTPServer(("", 8080), RequestHandler) as server:
    host, port = server.socket.getsockname()[:2]
    url_host = f"[{host}]" if ":" in host else host
    print(f"Serving HTTP on {host} port {port} "
          f"(http://{url_host}:{port}/) ...",
          file=sys.stderr)
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      print("\nKeyboard interrupt received, exiting.",
            file=sys.stderr)
