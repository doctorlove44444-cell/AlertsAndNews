import os
import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# משתני סביבה
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
SESSION = os.environ["TELEGRAM_SESSION"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
TARGET_CHANNEL = os.environ["TARGET_CHANNEL"]  # @espwn8

SOURCE_CHANNEL = "@pakarlive"

# ניקוי שורת הקישור בסוף ההודעה
def clean_message(text: str) -> str:
    if not text:
        return text
    lines = text.strip().split("\n")
    # מסיר שורות שמכילות "הגל השקט" או קישורים
    cleaned = [
        line for line in lines
        if "הגל השקט" not in line and "t.me/" not in line and "misterfix" not in line
    ]
    return "\n".join(cleaned).strip()


async def main():
    # לקוח Telethon להאזנה לערוץ המקור
    listener = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

    # לקוח בוט לשליחה לערוץ היעד
    bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    await listener.start()
    await bot.start(bot_token=BOT_TOKEN)

    print(f"✅ מאזין ל-{SOURCE_CHANNEL}, שולח ל-{TARGET_CHANNEL}")

    @listener.on(events.NewMessage(chats=SOURCE_CHANNEL))
    async def handler(event):
        text = event.message.text or ""
        cleaned = clean_message(text)

        if not cleaned:
            return

        try:
            await bot.send_message(TARGET_CHANNEL, cleaned)
            print(f"✅ נשלח: {cleaned[:60]}...")
        except Exception as e:
            print(f"❌ שגיאה בשליחה: {e}")

    await listener.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
