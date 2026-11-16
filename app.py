import os
import requests
import urllib3
from flask import Flask, render_template_string, request 

# Suppress SSL warnings for the lab
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = ""
    target = ""
    
    if request.method == 'POST':
        target = request.form.get('url')
        if target:
            try:
                # Create a fake browser session
                session = requests.Session()
                
                # Send the request to the target
                response = session.get(target, verify=False, timeout=10)
                
                # Check if the server gave us any cookies
                cookies = session.cookies.get_dict()
                
                if cookies:
                    results = f"<div class='vulnerable'><h3>🚨 VULNERABLE!</h3><p>The server issued cookies to an unauthenticated user:</p><pre>{cookies}</pre></div>"
                else:
                    results = f"<div class='secure'><h3>✅ SECURE!</h3><p>The server did not issue any cookies without authentication.</p></div>"
                    
            except Exception as e:
                results = f"<div class='error'><h3>Error:</h3><p>{e}</p></div>"

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Session Hijack Tester</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial; padding: 20px; background: #1e1e1e; color: white; }
            input { padding: 10px; width: 60%; margin-right: 10px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .vulnerable { background: #ffcccc; color: #900; padding: 15px; margin-top: 20px; border-radius: 5px; }
            .secure { background: #ccffcc; color: #090; padding: 15px; margin-top: 20px; border-radius: 5px; }
            .error { background: #ffdddd; color: #a00; padding: 15px; margin-top: 20px; border-radius: 5px; }
            pre { white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h2>🔐 Session Hijack Tester</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter target URL (e.g., https://app.bilalsadasub.com)" value="{{ target }}" required>
            <button type="submit">Test for Vulnerability</button>
        </form>
        {{ results }}
    </body>
    </html>
    """
    return render_template_string(html, results=results, target=target)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
