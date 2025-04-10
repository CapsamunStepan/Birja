import requests


# send messages in tg
def send_telegram_notification(message, chat_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.get(url, params=params)
    return response.json()
