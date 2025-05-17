# WhatsApp Auto Messenger (Python + Selenium)

This project allows you to automatically send personalized WhatsApp messages to multiple contacts using Python, Selenium, and Chrome WebDriver.

---

## Setup Instructions

### 1. Install Python
- Download and install Python from: https://www.python.org/downloads/
- During installation, make sure to check **"Add Python to PATH"** option.
---

### 2. Install pip (if not already installed)
- Check if pip is already installed:
  ```bash
  pip --version
  ```
- If not installed run 
```bash 
python -m ensurepip --upgrade
```
### 3. Install Required Python Packages
```bash 
pip install -r requirements.txt
```
### 4. Download this code 
- cd into `whatsapp-multi-messanger` folder
## Prepare Your Files
### contacts.csv
Note: Use full mobile numbers with country code (without spaces, dashes, or plus sign).

    ```
    number,name
    919876543210,Ahmed Khan
    919812345678,Fatima Noor
    919800112233,Omar Ansari
    ```
### message_template.txt
```
    Assalamu Alaikum {name},
    Hope you are doing well!
    Automated message from Ahsan Bhai
```    
## Running the Script
```bash 
python send_whatsapp_messages_with_selenium.py
```
- WhatsApp Web will open automatically.
- Scan your QR code using your phone; then press enter on the running program
- Messages will start sending automatically.

## Important Notes
- Keep your phone connected to the internet throughout the process.
- Do not close the Chrome window during message sending.
- It's recommended not to send too many messages at once to avoid temporary blocks from WhatsApp.


