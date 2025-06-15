import pyperclip
import time
import json
import os
from openai import OpenAI
from overlay import OverlayWindow
from tray import start_tray_thread


# BASE_URL = "https://api.deepseek.com"
BASE_URL = "https://openrouter.ai/api/v1"


def load_api_key():
    # Try secrets.json first
    try:
        with open("secrets.json", "r") as f:
            return json.load(f).get("openrouter_api_key")
    except Exception:
        # Fall back to env variable
        return os.environ.get("OPENROUTER_API_KEY")
    

def translate_text_with_deepseek(client: OpenAI, text: str):
    prompt = f"Translate the following Japanese text into natural English:\n\nJapanese: {text}\n\nEnglish:"
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {"role": "system", "content": "You are a skilled Japanese-to-English translator for visual novels. Avoid literal translations; preserve tone and emotion. Respond with the translation result ONLY."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    overlay = OverlayWindow()
    overlay.start()
    client = OpenAI(api_key=load_api_key(), base_url=BASE_URL)
    start_tray_thread()
    last_text = pyperclip.paste()

    while True:
        try:
            current = pyperclip.paste()
            if current != last_text and current.strip():
                last_text = current
                overlay.update_text("⏳ Translating...")
                translated = translate_text_with_deepseek(client, current)
                overlay.update_text(translated)
        except Exception as e:
            print("Translation error:", e)
        time.sleep(0.5)
