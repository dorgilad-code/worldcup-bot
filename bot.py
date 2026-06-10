import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv
from scraper import get_todays_matches, get_odds, get_team_stats, get_injuries
from analyzer import analyze_match
import anthropic

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def send_top_scorer_analysis():
    print("מנתח מלך שערים...")
    
    prompt = """
אתה מנתח ספורט מקצועי למונדיאל 2026.
נתח מי הסיכוי הטוב ביותר לזכות בפרס מלך השערים.

בדוק את הפרמטרים האלה לכל שחקן מועדף:
1. קווי הימורים נוכחיים למלך שערים
2. קלות לוח המשחקים בשלב הבתים
3. פורמה אחרונה בקבוצת המועדון
4. היסטוריית גולים במונדיאלים קודמים
5. מצב בריאותי ידוע

רשום את 5 המועדפים הגדולים ביותר בפורמט הזה:

🏆 ניתוח מלך השערים - מונדיאל 2026

1. [שם שחקן] - [קבוצה]
⚽ קו הימורים: @X.XX
📋 קבוצות בשלב הבתים: [רשום מול מי משחק]
💪 פורמה: [תאר בקצרה]
✅ יתרון: [למה הוא מועדף]
⚠️ סיכון: [מה יכול לעצור אותו]

[חזור על זה ל-5 שחקנים]

💡 המלצת הימור:
[מי הכי שווה להמר עליו ולמה]

⚽ קומבו מומלץ:
[שילוב של 2-3 שחקנים בהימור]
"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    await bot.send_message(chat_id=CHAT_ID, text=message.content[0].text)
    print("ניתוח מלך שערים נשלח!")

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

async def main():
    await send_top_scorer_analysis()
    await send_daily_tips()

if __name__ == "__main__":
    asyncio.run(main())