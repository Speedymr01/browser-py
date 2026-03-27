import tkinter as tk
from tkinter import ttk
import webview
import argparse
import threading
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserClient:
    def __init__(self, start_url, proxy_url):
        self.proxy_url = proxy_url
        self.adblock_script = None
        self.root = tk.Tk()
        self.root.title("browser-py Client")
        self.root.geometry("1100x750")
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        self.status_var = tk.StringVar(value="Loading...")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side="left")
        
        # Top bar
        top = ttk.Frame(self.root)
        top.pack(side="top", fill="x")
        
        self.url_var = tk.StringVar(value=start_url)
        ttk.Button(top, text="◀", width=3, command=self.go_back).pack(side="left", padx=3)
        ttk.Button(top, text="▶", width=3, command=self.go_forward).pack(side="left", padx=3)
        ttk.Button(top, text="⟳", width=3, command=self.reload_page).pack(side="left", padx=3)
        
        url_entry = ttk.Entry(top, textvariable=self.url_var)
        url_entry.pack(side="left", fill="x", expand=True, padx=5)
        url_entry.bind("<Return>", self.load_page)
        ttk.Button(top, text="Go", command=self.load_page).pack(side="left", padx=5)
        
        self.browser = webview.create_window("Browser Client", start_url)
        webview.start(self._init_browser, self.browser)
    
    def _init_browser(self, window):
        self.fetch_adblock_script()
        thread = threading.Thread(target=self._adblock_loop, daemon=True)
        thread.start()
    
    def fetch_adblock_script(self):
        try:
            response = requests.get(f"{self.proxy_url}/api/adblock", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.adblock_script = data.get('script')
                self.status_var.set("✓ Connected to proxy")
                logger.info("Fetched adblock script from server")
            else:
                self.status_var.set("✗ Server error")
        except requests.exceptions.RequestException as e:
            self.status_var.set(f"✗ Cannot connect: {str(e)[:30]}")
            logger.error(f"Failed to fetch script: {e}")
    
    def _adblock_loop(self):
        while True:
            try:
                if self.adblock_script:
                    self.browser.evaluate_js(self.adblock_script)
                else:
                    self.fetch_adblock_script()
            except Exception as e:
                pass
            time.sleep(2)
    
    def load_page(self, event=None):
        url = self.url_var.get().strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            self.url_var.set(url)
        self.browser.load_url(url)
    
    def go_back(self):
        try:
            self.browser.go_back()
        except:
            pass
    
    def go_forward(self):
        try:
            self.browser.go_forward()
        except:
            pass
    
    def reload_page(self):
        try:
            self.browser.reload()
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description="browser-py Client")
    parser.add_argument("--url", type=str, default="https://www.python.org", help="Starting URL")
    parser.add_argument("--proxy", type=str, default="http://localhost:8080", help="Proxy server URL")
    args = parser.parse_args()
    
    client = BrowserClient(args.url, args.proxy)

if __name__ == "__main__":
    main()