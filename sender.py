import requests
import time

running = True

def stop_sending():
    global running
    running = False

def send_message(token, thread_id, message):
    url = "https://graph.facebook.com/v20.0/me/messages"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "messaging_type": "MESSAGE_TAG",
        "tag": "ACCOUNT_UPDATE",
        "recipient": {"thread_key": thread_id},
        "message": {"text": message}
    }
    try:
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            print(f"[✔] Sent: {message}")
        else:
            print(f"[✘] {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[Error] {e}")

def start_sending(token_file, message_file, thread_id, delay):
    global running
    running = True

    with open(token_file) as f:
        tokens = [line.strip() for line in f if line.strip()]

    with open(message_file) as f:
        messages = [line.strip() for line in f if line.strip()]

    i = 0
    while running:
        token = tokens[i % len(tokens)]
        for msg in messages:
            if not running:
                break
            send_message(token, thread_id, msg)
            time.sleep(delay)
        i += 1
