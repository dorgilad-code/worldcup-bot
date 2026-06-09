import requests
from bs4 import BeautifulSoup
import os
from datetime import date

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_todays_matches():
    matches = []
    try:
        url = "https://api.football-data.org/v4/competitions/WC/matches"
        headers = {**HEADERS, "X-Auth-Token": os.getenv("FOOTBALL_DATA_KEY")}
        params = {"status": "SCHEDULED"}
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        data = resp.json()
        today = date.today().isoformat()
        for match in data.get("matches", []):
            if match["utcDate"][:10] == today:
                matches.append({
                    "home": match["homeTeam"]["name"],
                    "away": match["awayTeam"]["name"],
                    "time": match["utcDate"][11:16],
                    "stage": match.get("stage", "")
                })
    except Exception as e:
        print(f"Error fetching matches: {e}")
    return matches

def get_odds(home_team, away_team):
    try:
        url = "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
        params = {
            "apiKey": os.getenv("ODDS_API_KEY"),
            "regions": "eu",
            "markets": "h2h,totals",
            "oddsFormat": "decimal"
        }
        resp = requests.get(url, params=params, timeout=10)
        games = resp.json()
        for game in games:
            if home_team.lower() in game.get("home_team", "").lower():
                bookmakers = game.get("bookmakers", [])
                if bookmakers:
                    return bookmakers[0]
    except Exception as e:
        print(f"Odds error: {e}")
    return {}

def get_team_stats(home_team, away_team):
    stats = {}
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/news"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        articles = resp.json().get("articles", [])
        relevant = [a["headline"] for a in articles
                   if home_team.lower() in a.get("headline", "").lower()
                   or away_team.lower() in a.get("headline", "").lower()]
        stats["espn_headlines"] = relevant[:3]
    except Exception as e:
        print(f"Stats error: {e}")
    return stats