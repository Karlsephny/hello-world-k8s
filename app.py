"""
Hello World web app for the DevOps internship test task.
Listens on port 32777 by default (overridable via the PORT env var).
"""
import os
import socket
from datetime import datetime

from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "1.0.0"


@app.route("/")
def hello():
    hostname = socket.gethostname()
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Hello World - DevOps Task</title>
        <style>
            body {{
                font-family: -apple-system, Arial, sans-serif;
                background: #0f172a;
                color: #f8fafc;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            h1 {{ font-size: 2.5rem; margin-bottom: 0.2rem; }}
            .card {{
                background: #1e293b;
                padding: 2rem 3rem;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            }}
            .pod {{ color: #38bdf8; font-weight: bold; }}
            .meta {{ margin-top: 1rem; font-size: 0.9rem; color: #94a3b8; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Hello, World!</h1>
            <p>Served by pod: <span class="pod">{hostname}</span></p>
            <p class="meta">v{APP_VERSION} - {datetime.utcnow().isoformat()}Z</p>
        </div>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(status="ok", hostname=socket.gethostname())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 32777))
    app.run(host="0.0.0.0", port=port)
