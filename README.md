# SmrtiLog - Keystroke logger simulation by SudoHopeX

A smart Keystroke logger that determines user's os name, username, admin access & sends them to a server ( [Keystroke Logger Server by SudoHopeX](https://sudohopex-smrti-log.vercel.app/) )



## SmrtiLog Keystroke logger features:
  - logs keystrokes
  - determines user's **os name**, **username**, **admin privilege** & send them only once
  - **fetches new encryption key from server each time** it sends logs to encrypt data
  - encrypt data using fetched key and **send encrypted data** to server every minute
  - stop program on **ESC** key press
  - simulates keystroke logger


## SmrtiLog Server features:
- A Flask server to handle encrypted logs from a keylogger.
- Provides endpoints to get encryption keys and receive encrypted logs.
- Also includes a web interface to view and clear received logs.
- hosted on vercel
- all logs received by server are stored temporarily & removed automatically by vercel 


## Tech Stack

```text
  Technology             Uses
-------------------------------------------------------
  Python                 Core Programming Language          
  pynput (Lib)           Capture keystrokes               
  flask (Lib)            Server management                 
  cryptography (Lib)     Encrypting logs in transmit       
  json (Lib)             Storing & sending logs            
  threading (Lib)        Log sending timer                 
  requests (Lib)         Data fetch & upload on server     
  ctypes (Lib)           Hide console & check admin access 
  base64 (Lib)           Data encoding & decoding          
  Vercel (web app)       Server deployment  
```

## SmrtiLog Installation
- Clone the GitHub repository ( for linux ) or [download zip for windows & linux](https://github.com/SudoHopeX/SmrtiLog/archive/refs/heads/main.zip)  
  ```bash
  git clone https://github.com/SudoHopeX/SmrtiLog.git
  ```

- Navigate to SmrtiLog directory
    ```bash
    cd SmrtiLog
    ```
- Execute the run.sh script ( for linux or wsl only )
  ```bash
  sudo bash run.sh --setupRun
  ```
  for more usages of run.sh execute 
  ```bash
  sudo bash run.sh --help
  ```
- Make sure python is installed in windows, if not install it - [Install Python 3.13.7 - Windows installer](https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe)
- Then open the terminal & move to the SmrtiLog dir & execute 
  ```
  python main.py
  ```
- Press some keys or perform some action
- Then, visit [SudoHopeX Keystroke Simulator Server](https://sudohopex-smrti-log.vercel.app/) to see logs

## Security Notice
**Warning**: This project is for educational purposes & ethical use only. 
Do not use it for unauthorized monitoring.
Unauthorized use of keyloggers is illegal and unethical. 
Always obtain explicit permission before deploying such software.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details

## Contact
For any queries or support, contact SudoHopeX on:
- [Website DM](https://sudohopex.github.io/message-popup.html)
- [Linkedin](https://www.linkedin.com/in/dkrishna0124)
- [GitHub](https://github.com/SudoHopeX)

## Acknowledgements
- Thanku SudoHopeX 😎 for developing this project 
- Thanku 🫵 for loving 🫶 it...

(❁´◡`❁)
