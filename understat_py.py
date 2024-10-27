# -*- coding: utf-8 -*-
"""understat.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18mJF0AvgtkXLhpYPajlK-96tRUNx3paT
"""

import understatapi
import pandas as pd
import streamlit as st

client = understatapi.UnderstatClient()

st.title("Understat Data for all leagues available for the 2024 season")
st.subheader("Filter to any team/player to see all their shots taken!")

league_op = st.selectbox("Select a league", client.player(player = "11094").leagues, index = None)

if league_op != None:
    
    league_data = client.league(league_op).get_match_data(season = "2024")
    team_op = st.selectbox("Select a team", pd.json_normalize(league_data)["a.title"].sort_values().unique(), index=None)

    if team_op != None:
        
        team_data = client.team(team_op).get_player_data(season = "2024")
        player_op = st.selectbox("Select a plyer", pd.json_normalize(team_data)["player_name"].sort_values().unique(), index=None)
