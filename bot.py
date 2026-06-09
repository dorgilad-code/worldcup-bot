import asyncio
import os
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv
from scraper import get_todays_matches, get_odds, get_team_stats
from analyzer import analyze_match

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_daily_tips():
    print("🔍 מביא משחקי היום...")
    matches = get_todays_matches()

    if not matches:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="⚽ אין משחקי מונדיאל היום. נתראה מחר!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    from datetime import date
    header = f"🏆 *טיפים יומיים - מונדיאל 2026*\n📅 {date.today().strftime('%d/%m/%Y')}\n{'='*30}\n"
    await bot.send_message(chat_id=CHAT_ID, text=header, parse_mode=ParseMode.MARKDOWN)

    for match in matches:
        print(f"📊 מנתח: {match['home']} vs {match['away']}")
        stats = get_team_stats(match['home'], match['away'])
        odds = get_odds(match['home'], match['away'])
        analysis = analyze_match(match, stats, odds)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=analysis,
            parse_mode=ParseMode.MARKDOWN
        )
        await asyncio.sleep(2)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"✅ *סיכום:* {len(matches)} משחקים נותחו\n⚠️ _הימורים אחראיים בלבד_",
        parse_mode=ParseMode.MARKDOWN
    )

if __name__ == "__main__":
    asyncio.run(send_daily_tips())