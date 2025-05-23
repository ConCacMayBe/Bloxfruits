import requests
from bs4 import BeautifulSoup
import time
import os

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
last_stock = None

def get_bloxfruits_stock():
    url = "https://vulcanvalues.com/stock"
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    stock_div = soup.find("div", class_="stock")
    if not stock_div:
        return None
    items = stock_div.find_all("div", class_="fruit-card")
    return "\n".join(item.text.strip() for item in items)

def send_webhook(message):
    res = requests.post(WEBHOOK_URL, json={"content": message})
    print("Webhook status:", res.status_code)

def main():
    global last_stock
    while True:
        try:
            stock = get_bloxfruits_stock()
            if stock and stock != last_stock:
                send_webhook(f"**[Stock Mới Blox Fruits]**\n{stock}")
                last_stock = stock
            else:
                print("Stock không đổi.")
        except Exception as e:
            print("Lỗi:", e)
        time.sleep(1800)  # 30 phút

if __name__ == "__main__":
    main()
    
