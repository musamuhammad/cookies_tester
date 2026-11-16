import os
import requests
import urllib3
from flask import Flask, render_template_string, request

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
                session = requests.Session()
                
                # Make the request to the target
                response = session.get(target, verify=False, timeout=10)
                
                # Check the raw 'Set-Cookie' header
                set_cookie_header = response.headers.get('Set-Cookie', '')
                
                if set_cookie_header:
                    is_httponly = "HttpOnly" in set_cookie_header
                    is_secure = "Secure" in set_cookie_header
                    
                    report = "<ul>"
                    if is_httponly:
                        report += "<li style='color: #4CAF50;'>✅ <b>HttpOnly</b> is set.</li>"
                    else:
                        report += "<li style='color: #f44336;'>❌ <b>HttpOnly</b> is MISSING. A hacker can steal this cookie via XSS.</li>"
                        
                    if is_secure:
                        report += "<li style='color: #4CAF50;'>✅ <b>Secure</b> is set.</li>"
                    else:
                        report += "<li style='color: #f44336;'>❌ <b>Secure</b> is MISSING. Cookie can be sniffed over HTTP.</li>"
                    report += "</ul>"
                    
                    if is_httponly and is_secure:
                        results = f"<div class='secure'><h3>✅ SECURE COOKIES</h3>{report}<p><b>Raw Header:</b><br>{set_cookie_header}</p></div>"
                    else:
                        results = f"<div class='vulnerable'><h3>🚨 VULNERABLE COOKIES</h3>{report}<p><b>Raw Header:</b><br>{set_cookie_header}</p></div>"
                else:
                    results = "<div class='info'><h3>ℹ️ No Cookies Found</h3><p>This page does not issue cookies. It is secure.</p></div>"
                    
            except Exception as e:
                results = f"<div class='error'><h3>Error:</h3><p>{e}</p></div>"

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cookie Security Auditor</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial; padding: 20px; background: #1e1e1e; color: white; }
            input { padding: 10px; width: 60%; font-size: 16px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; font-size: 16px; }
            .vulnerable { background: #ffcccc; color: #900; padding: 15px; margin-top: 20px; border-radius: 5px; }
            .secure { background: #ccffcc; color: #090; padding: 15px; margin-top: 20px; border-radius: 5px; }
            .info { background: #e3f2fd; color: #0d47a1; padding: 15px; margin-top: 20px; border-radius: 5px; }
            pre { white-space: pre-wrap; font-size: 12px; }
        </style>
    </head>
    <body>
        <h2>🔐 Cookie Security Auditor</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter URL" value="{{ target }}" required>
            <button type="submit">Test Cookies</button>
        </form>
        {{ results|safe }}
    </body>
    </html>
    """
    return render_template_string(html, results=results, target=target)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
