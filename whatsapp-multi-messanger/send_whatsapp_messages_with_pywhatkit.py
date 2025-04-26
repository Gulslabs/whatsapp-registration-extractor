import pywhatkit as kit
import pyautogui
pyautogui.FAILSAFE = False
import time
import csv

# Function to send WhatsApp messages
def send_whatsapp_messages():
    # File path
    csv_file = "contacts.csv"  # Example file name

    # Read contacts from CSV
    contacts = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contacts.append({
                'number': row['number'],
                'name': row['name']
            })

    # Message template
    message_template = "Assalamu Alaikum {name}, Umeed hai aap Kariyat se hoonge. \\n Automated - Ahsan Bhai!"
    print("Message template:", message_template)
    print("Total contacts:", len(contacts))
    # Counters
    sent_count = 0

    for idx, contact in enumerate(contacts):
        # Fill the template
        message = message_template.format(name=contact['name'])
        
        # Get current time
        current_time = time.localtime()
        hour = current_time.tm_hour
        #minute = current_time.tm_min + 2  # +2 minutes buffer
        minute = current_time.tm_min + 2  # +1 minute buffer
        print("Message will sent at:", hour, minute)
        # Send message
        kit.sendwhatmsg(f"+{contact['number']}", message, hour, minute)
    # Send message instantly
        kit.sendwhatmsg_instantly(
            phone_no=f"+{contact['number']}",
            message=message,
            wait_time=20,     # seconds to wait before sending
            tab_close=True,   # close tab after sending
            close_time=5      # seconds to wait before closing
        )
        time.sleep(12)  
        # Move mouse to the chat box and click
        pyautogui.click(x=-1104, y=1090)  # <-- You MUST set correct X,Y coordinates for YOUR screen

        # NEW: Press "Enter" key after sending
        time.sleep(2)   # Small wait after WhatsApp Web loads the message
        pyautogui.press("enter")
        print("✅ Clicked textbox and pressed ENTER to send the message.")
        sent_count += 1
        print(f"[{sent_count}] Message sent to {contact['name']} ({contact['number']})")




        time.sleep(10)  # Small gap between each message

        # After every 20 messages, wait 15 minutes
        
        # if sent_count % 20 == 0:
        #     print("✅ 20 messages sent. Waiting 15 minutes to avoid blocking...")
        #     time.sleep(900)  # 15 minutes = 900 seconds

# Main function
def main():
    send_whatsapp_messages()

# Run the script
if __name__ == "__main__":
    main()