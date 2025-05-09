import requests
import certifi


# send messages in tg
def send_telegram_notification(message, chat_id, bot_token, parse_mode):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': parse_mode,  # позволяет распознавать HTML & Markdown
        # 'disable_web_page_preview': True  # без этого ссылка прогружается и появляется небольшая панель
    }
    response = requests.post(url, data=data, verify=False)
    return response.json()
