import requests
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
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/news"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        articles = resp.json().get("articles", [])
        relevant = [a["headline"] for a in articles
                   if home_team.lower() in a.get("headline", "").lower()
                   or away_team.lower() in a.get("headline", "").lower()]
        stats["espn_headlines"] = relevant[:3]
    except Exception as e:
        print(f"Stats error: {e}")
    return stats

def get_injuries(home_team, away_team):
    injuries = {"home": [], "away": []}
    try:
        # ESPN injuries API
        for team, key in [(home_team, "home"), (away_team, "away")]:
            url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/news"
            params = {"limit": 50}
            resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
            articles = resp.json().get("articles", [])
            for a in articles:
                headline = a.get("headline", "").lower()
                if team.lower() in headline and any(word in headline for word in ["injur", "doubt", "miss", "out", "נפצע", "ספק", "פציעה"]):
                    injuries[key].append(a["headline"])
    except Exception as e:
        print(f"Injuries error: {e}")

    try:
        # SofaScore injuries
        search_url = f"https://www.sofascore.com/api/v1/team/search?q={home_team.replace(' ', '%20')}"
        resp = requests.get(search_url, headers=HEADERS, timeout=10)
        if resp.ok:
            teams = resp.json().get("teams", [])
            if teams:
                team_id = teams[0]["id"]
                inj_url = f"https://www.sofascore.com/api/v1/team/{team_id}/players/injured"
                inj_resp = requests.get(inj_url, headers=HEADERS, timeout=10)
                if inj_resp.ok:
                    for player in inj_resp.json().get("players", []):
                        name = player.get("player", {}).get("name", "")
                        status = player.get("injuryType", "פציעה")
                        injuries["home"].append(f"{name} - {status}")
    except Exception as e:
        print(f"SofaScore injury error: {e}")

    return injuries