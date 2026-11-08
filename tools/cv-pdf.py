#!/usr/bin/env python3
"""Make a PDF of your CV with the Live CV theme.

The theme publishes a printable CV at cv/ (built from the same data as the home page).
This tool builds the site into a temporary folder, serves it locally, and has a
headless Chrome, Edge or Chromium print cv/ to static/cv.pdf. The "Download PDF"
link on the home page then points to it (unless you set params.pdf yourself).

Run it from the root of your Hugo site:

    python themes/hugo-theme-live-cv/tools/cv-pdf.py

Options:
    --out PATH       where to write the PDF (default: static/cv.pdf)
    --hugo PATH      the hugo command (default: hugo, or $HUGO)
    --browser PATH   Chrome, Edge or Chromium (default: found automatically, or $CHROME)
    --               everything after this is passed to hugo, e.g. -- --themesDir ../..

Requires Python 3.8+, Hugo and a Chromium-based browser. No other packages.
"""

import argparse
import functools
import http.server
import os
import platform
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request


def find_browser(explicit=None):
    """Return the path to a Chromium-based browser, or None."""
    candidates = [explicit, os.environ.get("CHROME")]
    system = platform.system()
    if system == "Windows":
        roots = [os.environ.get(k) for k in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
        for root in filter(None, roots):
            candidates += [
                os.path.join(root, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(root, "Microsoft", "Edge", "Application", "msedge.exe"),
                os.path.join(root, "Chromium", "Application", "chrome.exe"),
            ]
    elif system == "Darwin":
        candidates += [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "microsoft-edge", "msedge", "chrome"):
        candidates.append(shutil.which(name))
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(directory):
    """Serve a directory on a free local port in a background thread. Returns (server, port)."""
    handler = functools.partial(QuietHandler, directory=directory)
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


def main():
    parser = argparse.ArgumentParser(
        description="Print the Live CV printable CV (cv/) to a PDF.",
        epilog="Arguments after -- are passed to hugo, e.g. -- --themesDir ../..")
    parser.add_argument("--out", default=os.path.join("static", "cv.pdf"))
    parser.add_argument("--hugo", default=os.environ.get("HUGO", "hugo"))
    parser.add_argument("--browser", default=None)
    args, hugo_args = parser.parse_known_args()
    hugo_args = [a for a in hugo_args if a != "--"]

    hugo = shutil.which(args.hugo) or args.hugo
    browser = find_browser(args.browser)
    if not browser:
        sys.exit("cv-pdf: no Chrome, Edge or Chromium found; pass --browser PATH or set $CHROME.")

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="live-cv-pdf-") as tmp:
        site_dir = os.path.join(tmp, "public")
        profile_dir = os.path.join(tmp, "browser")
        server, port = serve(site_dir)
        base = f"http://127.0.0.1:{port}/"
        try:
            # 1. Build the site for the local server.
            print(f"cv-pdf: building the site with {os.path.basename(hugo)} ...")
            cmd = [hugo, "--destination", site_dir, "--baseURL", base, "--quiet"] + hugo_args
            if subprocess.run(cmd).returncode != 0:
                sys.exit("cv-pdf: hugo failed.")
            if not os.path.isfile(os.path.join(site_dir, "cv", "index.html")):
                sys.exit("cv-pdf: the site has no cv/ page. Is the Live CV theme in use, "
                         "and is params.cv.enable not set to false?")

            # 2. Make sure the page is reachable before printing it.
            for _ in range(50):
                try:
                    urllib.request.urlopen(base + "cv/", timeout=2).read()
                    break
                except OSError:
                    time.sleep(0.1)

            # 3. Print it.
            print(f"cv-pdf: printing {base}cv/ with {os.path.basename(browser)} ...")
            cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run",
                   f"--user-data-dir={profile_dir}", "--no-pdf-header-footer",
                   "--run-all-compositor-stages-before-draw", "--virtual-time-budget=10000",
                   f"--print-to-pdf={out}", base + "cv/"]
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                cmd.insert(1, "--no-sandbox")  # Chrome refuses to run sandboxed as root (e.g. in Docker)
            if os.path.exists(out):
                os.remove(out)
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        finally:
            server.shutdown()
            server.server_close()

    if not os.path.isfile(out) or os.path.getsize(out) == 0:
        sys.exit("cv-pdf: the browser did not write a PDF.")
    print(f"cv-pdf: wrote {os.path.relpath(out)} ({os.path.getsize(out) // 1024} KB)")
    if os.path.normpath(args.out) == os.path.join("static", "cv.pdf"):
        print("cv-pdf: rebuild the site to publish it; the home page links to it as \"Download PDF\".")


if __name__ == "__main__":
    main()
