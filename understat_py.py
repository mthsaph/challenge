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

season = "2024"
client = understatapi.UnderstatClient()

st.title("Understat Data for all leagues available for the 2014-2024 season")
st.subheader("Filter to any team/player to see all their shots taken!")

seasons = [str(x) for x in range(2014, 2025)]

league_op = st.selectbox("Select a league", client.player(player = "11094").leagues, index = None)

season = st.selectbox("Select a season", seasons, index = None)

if league_op != None and season != None:
    
    league_data = client.league(league_op).get_match_data(season)
    team_op = st.selectbox("Select a team", pd.json_normalize(league_data)["a.title"].sort_values().unique(), index=None)

    if team_op != None:

        data = client.league(league = "EPL").get_team_data(season = "2024")
        team_id = "71"
        st.table(pd.json_normalize(data[team_id]["history"]))
        
        team_data = pd.json_normalize(client.team(team_op).get_player_data(season))
        player_op = st.selectbox("Select a plyer", team_data["player_name"].sort_values().unique(), index=None)

        if player_op != None:
            
            player_id = team_data[team_data["player_name"] == player_op]["id"]
            player_id = player_id.iloc[0]
            df = pd.json_normalize(client.player(player = player_id).get_shot_data())
            df = df[df["season"] == season]
            pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#f0f0f0', line_color='black', half=True)
            fig, ax = pitch.draw(figsize=(10, 10))
            plot_shots(df, ax, pitch)
            st.pyplot(fig)
