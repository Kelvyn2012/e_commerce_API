#!/usr/bin/env python3
"""
Simple HTTP server for the frontend
Run this from the frontend directory: python server.py
"""
import http.server
import socketserver
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

Handler = MyHTTPRequestHandler

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n{'='*60}")
        print(f"  ShopHub Frontend Server")
        print(f"{'='*60}")
        print(f"  Server running at: http://localhost:{PORT}")
        print(f"  Press Ctrl+C to stop")
        print(f"{'='*60}\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
