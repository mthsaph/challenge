# -*- coding: utf-8 -*-
"""understat.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18mJF0AvgtkXLhpYPajlK-96tRUNx3paT
"""

import understatapi
import pandas as pd
import streamlit as st
from mplsoccer import VerticalPitch
import json

def plot_shots(df, ax, pitch):
    
    for x in df.to_dict(orient='records'):
        
        pitch.scatter(
            x=float(x['X']) * 120,
            y=float(x['Y']) * 74,
            ax=ax,
            s = 1000 * float(x['xG']),
            color='green' if x['result'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['result'] == 'Goal' else .5,
            zorder=2 if x['result'] == 'Goal' else 1,
        )
        
    return pitch

def build_standings(data):
  pts = 0
  wins = 0
  draws = 0
  losses = 0
  goals = 0
  conceded = 0
  L = []

  for i in data:
    for j in data[i]["history"]:
      pts += j["pts"]
      wins += j["wins"]
      draws += j["draws"]
      losses += j["loses"]
      goals += j["scored"]
      conceded += j["missed"]

    L.append({"TEAM": data[i]["title"], "PTS": pts, "G": wins + draws + losses,"W": wins, "D": draws, "L": losses, "GOALS": goals, "GA": conceded})
    pts = 0
    wins = 0
    draws = 0
    losses = 0
    goals = 0
    conceded = 0

  return L

season = "2024"
client = understatapi.UnderstatClient()

st.title("Understat Data for all leagues available for the 2014-2024 season usin the understatapi")
st.subheader("Filter to any team/player to see all their shots taken!")

seasons = [str(x) + "/" + str(x + 1) for x in range(2014, 2025)]

league_op = st.selectbox("Select a league", client.player(player = "11094").leagues, index = None)
season = st.selectbox("Select a season", seasons, index = None)

if season != None:
    season = season[0:4]

if league_op != None and season != None:

    team_data = client.league(league_op).get_team_data(season)
    standings = build_standings(team_data)
    standings = pd.DataFrame(standings).sort_values(by = ["PTS", "G", "GA"], ascending = [False, False, True])
    standings = standings.reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill="")
    standings.index += 1
    st.table(standings)

    top_league_players = pd.json_normalize(client.league(league_op).get_player_data(season))
    top_league_players = top_league_players[["player_name", "games",	"time",	"goals", "assists", "shots", "key_passes", "yellow_cards", "red_cards", "team_title"]]	
    top_league_players.index += 1
    top_league_players = top_league_players.rename(columns = {"player_name":"PLAYER", "games":"G", "time":"MIN PLAYED", "goals":"GOALS", "assists":"A", "shots":"SHOTS", 
                                                              "key_passes":"KEY PASSES", "yellow_cards":"YELLOW CARDS", "red_cards":"RED CARDS", "team_title":"TEAM"})
    st.table(top_league_players.head(10))
    
    league_data = client.league(league_op).get_match_data(season)
    norm_league_data = pd.json_normalize(league_data)
    team_op = st.selectbox("Select a team", norm_league_data["a.title"].sort_values().unique(), index=None)

    if team_op != None:
        
        team_matches = norm_league_data[((norm_league_data["h.title"] == team_op) | (norm_league_data["a.title"] == team_op)) & (norm_league_data["isResult"] == True)]
        team_matches = team_matches[["datetime", "h.title", "a.title", "goals.h", "goals.a"]].reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill="")
        team_matches = team_matches.rename(columns = {"datetime":"DATE AND TIME", "h.title":"HOME TEAM", "a.title":"AWAY TEAM", "goals.h":"HOME GOALS", "goals.a":"AWAY GOALS"})
        team_matches.index += 1
        st.table(team_matches.sort_values(by = "DATE AND TIME", ascending = False))

        team_data = pd.json_normalize(client.team(team_op).get_player_data(season))
        player_op = st.selectbox("Select a plyer", team_data["player_name"].sort_values().unique(), index=None)

        if player_op != None:

            player_id = team_data[team_data["player_name"] == player_op]["id"]
            player_id = player_id.iloc[0]
            
            player_stats = top_league_players[top_league_players["player_name"] == player_op]
            st.table(player_stats)
            
            df = pd.json_normalize(client.player(player = player_id).get_shot_data())
            df = df[df["season"] == season]
            pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#f0f0f0', line_color='black', half=True)
            fig, ax = pitch.draw(figsize=(10, 10))
            plot_shots(df, ax, pitch)
            st.pyplot(fig)
