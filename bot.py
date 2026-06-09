import asyncio
import os
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv
from scraper import get_todays_matches, get_odds, get_team_stats, get_injuries
from analyzer import analyze_match

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_daily_tips():
    print("מביא משחקי היום...")
    matches = get_todays_matches()

    if not matches:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="אין משחקי מונדיאל היום. נתראה מחר!",
        )
        return

    from datetime import date
    header = f"טיפים יומיים - מונדיאל 2026\n{date.today().strftime('%d/%m/%Y')}"
    await bot.send_message(chat_id=CHAT_ID, text=header)

    for match in matches:
        print(f"מנתח: {match['home']} vs {match['away']}")
        stats = get_team_stats(match['home'], match['away'])
        odds = get_odds(match['home'], match['away'])
        injuries = get_injuries(match['home'], match['away'])
        analysis = analyze_match(match, stats, odds, injuries)
        await bot.send_message(chat_id=CHAT_ID, text=analysis)
        await asyncio.sleep(2)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"סיכום: {len(matches)} משחקים נותחו\nהימורים אחראיים בלבד"
    )

if __name__ == "__main__":
    asyncio.run(send_daily_tips())