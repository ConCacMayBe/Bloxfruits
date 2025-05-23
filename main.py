import requests
from bs4 import BeautifulSoup
import time
import os

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Lấy từ biến môi trường
last_stock = None

def get_bloxfruits_stock():
    url = "https://vulcanvalues.com/stock"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Lỗi lấy stock: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Dựa vào cấu trúc hiện tại của web (có thể cần cập nhật nếu web thay đổi)
    stock_div = soup.find("div", class_="stock")
    if not stock_div:
        return None

    stock_items = stock_div.find_all("div", class_="fruit-card")
    stock_text = "\n".join(item.text.strip() for item in stock_items)

    return stock_text.strip()

def send_webhook(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code in [200, 204]:
        print("Đã gửi webhook.")
    else:
        print("Lỗi gửi webhook:", response.status_code, response.text)

def main():
    global last_stock
    while True:
        try:
            print("Đang kiểm tra stock...")
            current_stock = get_bloxfruits_stock()
            if not current_stock:
                print("Không lấy được stock.")
            elif current_stock != last_stock:
                send_webhook(f"**[Stock Mới Blox Fruits]**\n{current_stock}")
                last_stock = current_stock
            else:
                print("Stock chưa thay đổi.")
        except Exception as e:
            print("Lỗi:", e)

        print("Chờ 30 phút...\n")
        time.sleep(1800)  # 30 phút

if __name__ == "__main__":
    main()
  
