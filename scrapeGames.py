import argparse
import sys
import requests
import json
import random

# curl -X GET "https://open.faceit.com/data/v4/players?nickname=mrmatthew2k&game=csgo" -H "accept: application/json" -H "Authorization: Bearer 68bbc795-8a18-478e-8da0-79a639fb6540"

def pullMatch(matchID, apiKey):
    
    url = f"https://open.faceit.com/data/v4/matches/{matchID}"
    r = requests.get(url, headers={"accept": "application/json", "Authorization": f"Bearer {apiKey}"})
    assert r.status_code == 200
    return r.json()

def getPlayerMatch(playerId, apiKey):
    url = f"https://open.faceit.com/data/v4/players/{playerId}/history?game=csgo&offset=0&limit=20"
    r = requests.get(url, headers={"accept": "application/json", "Authorization": f"Bearer {apiKey}"})
    assert r.status_code == 200
    items = r.json()["items"]
    index = random.randint(0, len(items)-1)
    return items[index]["match_id"]

def getNextMatch(matchJson, apiKey):
    faction = random.choice(["faction1", "faction2"])
    roster = matchJson["teams"][faction]["roster"]
    playerIndex = random.randint(0, len(roster)-1)
    playerId = matchJson["teams"][faction]["roster"][playerIndex]["player_id"]
    return getPlayerMatch(playerId, apiKey)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", dest="apiKey", required=True, help="faceit api key", type=str, default="")
    parser.add_argument("-s", "--startGame", dest="initMatch", required=True, help="game to start pull sequence", type=str, default="")
    parser.add_argument("-n", "--numMatches", dest="numMatches", required=False, help="Numbers of matches to try and pull", type=int, default=1000)
    args = parser.parse_args()

    cMatch = args.initMatch
    apiKey = args.apiKey
    count = 0
    while count < args.numMatches:
        print(f"{cMatch}", flush=True, end="\n")
        cMatch = getNextMatch(pullMatch(cMatch, apiKey), apiKey)
        count += 1
