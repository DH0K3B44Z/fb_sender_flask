import requests
import time

running = True

def stop_sending():
    global running
    running = False

def get_profile_info(token):
    try:
        res = requests.get(f"https://graph.facebook.com/me?access_token={token}")
        data = res.json()
        if 'id' in data:
            uid = data["id"]
            name = data["name"]
            link = f"https://facebook.com/{uid}"
            return {"token": token, "name": name, "uid": uid, "link": link}
        else:
            return None
    except:
        return None

def scan_tokens(token_file):
    with open(token_file) as f:
        raw_tokens = [line.strip() for line in f if line.strip()]

    print(f"🔎 Scanning {len(raw_tokens)} tokens...")
    valid = []

    for tok in raw_tokens:
        info = get_profile_info(tok)
        if info:
            print(f"✅ {info['name']} → {info['link']}")
            valid.append(info)
        else:
            print(f"❌ Dead token: {tok[:15]}...")

    return valid

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
            print(f"[✘] Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[Error] {e}")

def start_sending(valid_tokens, message_file, thread_id, delay):
    global running
    running = True

    with open(message_file) as f:
        messages = [line.strip() for line in f if line.strip()]

    i = 0
    while running:
        token_info = valid_tokens[i % len(valid_tokens)]
        token = token_info["token"]
        for msg in messages:
            if not running:
                break
            send_message(token, thread_id, msg)
            time.sleep(delay)
        i += 1
