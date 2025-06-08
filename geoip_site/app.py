from flask import Flask, request, render_template
import requests
import datetime

app = Flask(__name__)

# 🛡️ Вставь свой Telegram токен и ID (если хочешь уведомления)
TELEGRAM_BOT_TOKEN = '7831915998:AAG6xUzltGXQC0Q51ARfZtNV_ZqRkFZs_Qg'  # например: '123456789:ABC...'
TELEGRAM_CHAT_ID = '6247209280'    # например: '123456789'

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon,timezone,query").json()
        return response if response['status'] == 'success' else None
    except:
        return None

def log_visitor(data):
    with open("visitors.log", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {data}\n")

def send_telegram(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    data = get_ip_info(ip)

    if data:
        log_text = f"IP: {data['query']}, Country: {data['country']}, City: {data['city']}, ISP: {data['isp']}"
        log_visitor(log_text)
        send_telegram(log_text)
        return render_template("index.html", geo=data)
    else:
        return "Ошибка при получении IP-данных"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
