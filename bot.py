import logging
import os

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import aiohttp
from bs4 import BeautifulSoup

from dotenv import load_dotenv


# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_API_KEY = os.getenv('BOT_API_KEY')


async def get_video_url(url: str) -> str:
    """Get video URL from ddinstagram.com page"""
    modified_url = url.replace("instagram.com", "ddinstagram.com")
    headers = {
        "User-Agent": "TelegramBot"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(modified_url, headers=headers, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            # Look for og:video meta tag
            meta_tag = soup.find("meta", property="og:video")
            return meta_tag["content"] if meta_tag else None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages"""
    message = update.message
    if not message.text:
        return

    # Find Instagram URLs in message
    # insta_urls = re.findall(r"https?://(www\.)?instagram\.com/.+\S+", message.text)
    insta_urls = [message.text]

    for url in insta_urls:
        try:
            video_url = await get_video_url(url)
            if video_url:
                await message.reply_video("https://ddinstagram.com/" + str(video_url))
            else:
                await message.reply_text("No video found in the provided link.")
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            await message.reply_text("Failed to download video. Please check the link.")


def main() -> None:
    """Start the bot"""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token(BOT_API_KEY).build()

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    application.run_polling()


if __name__ == "__main__":
    main()