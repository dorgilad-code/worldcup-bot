import anthropic
import json
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_match(match, stats, odds):
    prompt = f"""
אתה מנתח ספורט מקצועי המתמחה בהימורים על מונדיאל 2026.
נתח את המשחק הבא על בסיס כל הנתונים שנאספו.

**משחק:** {match['home']} נגד {match['away']}
**שעה:** {match['time']} UTC
**שלב:** {match['stage']}

**כותרות ESPN:**
{json.dumps(stats.get('espn_headlines', []), ensure_ascii=False)}

**קווי הימורים:**
{json.dumps(odds, ensure_ascii=False)[:500]}

תפלט ניתוח בעברית בפורמט הזה בדיוק:

🏆 *{match['home']} vs {match['away']}*
🕐 שעה: {match['time']} UTC

📊 *ניתוח:*
[2-3 שורות על כוח הקבוצות והפורמה האחרונה]

💡 *טיפ מומלץ:*
[המלצה ספציפית - 1X2 / Over/Under / BTTS עם הסבר קצר]

📈 *ערך בקו:*
[האם הקו נותן ערך? מה המכפיל המומלץ?]

⚠️ *סיכון:* [נמוך/בינוני/גבוה] - [הסבר חד שורה]
"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
    import anthropic
import json
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_match(match, stats, odds):
    prompt = f"""
אתה מנתח ספורט מקצועי המתמחה בהימורים על מונדיאל 2026.
נתח את המשחק הבא על בסיס כל הנתונים שנאספו.

**משחק:** {match['home']} נגד {match['away']}
**שעה:** {match['time']} UTC
**שלב:** {match['stage']}

**כותרות ESPN:**
{json.dumps(stats.get('espn_headlines', []), ensure_ascii=False)}

**קווי הימורים:**
{json.dumps(odds, ensure_ascii=False)[:500]}

תפלט ניתוח בעברית בפורמט הזה בדיוק:

🏆 *{match['home']} vs {match['away']}*
🕐 שעה: {match['time']} UTC

📊 *ניתוח:*
[2-3 שורות על כוח הקבוצות והפורמה האחרונה]

🎯 *תחזית תוצאה מדויקת:*
[למשל: ארגנטינה 2-1 צרפת]
[הסבר קצר למה]

💡 *טיפ מומלץ:*
[המלצה ספציפית - 1X2 / Over/Under / BTTS עם הסבר קצר]

⚽ *קומבו מומלץ:*
[שילוב של שני טיפים עם מכפיל משוער]

📈 *ערך בקו:*
[האם הקו נותן ערך? מה המכפיל המומלץ?]

⚠️ *סיכון:* [נמוך/בינוני/גבוה] - [הסבר חד שורה]
"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "use