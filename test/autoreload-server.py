#!/usr/bin/env python3
import os, sys, subprocess, signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

server_script_dir = os.path.dirname(__file__)
server_script_name = "server.py"
server_script_path = os.path.join(server_script_dir, server_script_name)

change = False

class EventHandler(FileSystemEventHandler):
  def on_any_event(self, event: FileSystemEvent) -> None:
    if os.path.basename(event.src_path) == server_script_name:
      global change
      change = True

observer = Observer()
observer.schedule(EventHandler(), server_script_dir)
observer.start()
cmd = None
try:
  while observer.is_alive():
    with subprocess.Popen([server_script_path] + sys.argv[1:]) as cmd:
      try:
        while True:
          observer.join(1)
          if change:
            change = False
            print(f"Change to {server_script_name} detected", file=sys.stderr)
            cmd.send_signal(signal.SIGINT)
            cmd.wait()
            break
      except KeyboardInterrupt:
        cmd.send_signal(signal.SIGINT)
        break
finally:
  observer.stop()
  observer.join()

sys.exit(cmd.returncode if cmd is not None else 1)
