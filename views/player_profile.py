import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import apply_dark_theme

st.markdown("<h1 style='text-align: center;'> Lanre-FC Analytics (Demo) </h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'> Player Analysis Web App</h1>", unsafe_allow_html=True)

# Set the folder path
folder_path = os.path.join(os.getcwd(), 'data')

# Find and map all CSV files in the folder
file_mapping = {}
for file in os.listdir(folder_path):
    if file.startswith("cleaned_") and file.endswith('.csv'):
        player_name = file.replace("cleaned_", "").replace(".csv", "")
        file_mapping[player_name] = os.path.join(folder_path, file)

# Sidebar input
st.sidebar.header('Select Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2023, 2024))))
selected_player = st.sidebar.selectbox('Player', list(file_mapping.keys()))

if selected_player:
    file_path = file_mapping[selected_player]
    player_df = pd.read_csv(file_path)

    if "Unnamed: 0" in player_df.columns:
        player_df = player_df.drop("Unnamed: 0", axis=1)

    player_df['Date'] = pd.to_datetime(player_df['Date'])

    st.markdown(f"<h1 style='text-align: center; color: #1f77b4; font-size: 3em'> {selected_player}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Player Data for {selected_year}</h2>", unsafe_allow_html=True)

    # Metrics
    total_minutes = player_df['Min'].sum()
    average_minutes = player_df['Min'].mean()
    st.write(f'# Minutes')
    st.write(f"### Total Minutes Played: {total_minutes}")
    st.write(f"### Average Minutes per Game: {average_minutes:.2f}")

    total_goals = player_df['Gls'].sum()
    average_goals = player_df['Gls'].mean()
    st.write('# Goals')
    st.write(f"### Total Goals: {total_goals}")
    st.write(f"### Average Goals per Game: {average_goals:.2f}")

    player_df['Venue'] = pd.to_numeric(player_df['Venue'], errors='coerce')
    player_df['Gls'] = pd.to_numeric(player_df['Gls'], errors='coerce')

    home_games = player_df[player_df['Venue'] == 1]
    away_games = player_df[player_df['Venue'] == 0]
    avg_goals_home = home_games['Gls'].mean()
    avg_goals_away = away_games['Gls'].mean()
    st.write(f"### Average Goals Scored at Home: {avg_goals_home:.2f}")
    st.write(f"### Average Goals Scored Away: {avg_goals_away:.2f}")

    avg_xg = player_df['xG'].mean()
    st.write(f"### Expected Goals (xG): {avg_xg:.2f} vs Actual Goals (aG): {average_goals:.2f}")

    total_assists = player_df['Ast'].sum()
    average_assists = player_df['Ast'].mean()
    st.write('# Assists')
    st.write(f"### Total Assists: {total_assists}")
    st.write(f"### Average Assists per Game: {average_assists:.2f}")

    contribution_per_game = (player_df['Gls'] + player_df['Ast']).mean()
    st.write('# Goal/Assist Contribution')
    st.write(f"### Goal Contribution per Game: {contribution_per_game:.2f}")

    total_shots = player_df['Sh'].sum()
    total_shots_target = player_df['SoT'].sum()
    player_df['Shooting_Accuracy'] = np.where(player_df['Sh'] > 0, player_df['SoT'] / player_df['Sh'] * 100, 0)
    average_shooting_accuracy = player_df['Shooting_Accuracy'].mean()
    st.write('# Shooting Accuracy')
    st.write(f"### Total Shots: {total_shots}")
    st.write(f"### Total Shots on Target: {total_shots_target}")
    st.write(f"### Shooting Accuracy: {average_shooting_accuracy:.2f}%")

    # Expected Goals vs Actual Goals Plot
    st.write("# Expected Goals vs Actual Goals Over Time")
    fig_xg = px.line(
        player_df, x='Date', y=['xG', 'Gls'],
        labels={'value': 'Goals', 'variable': 'Metric', 'Date': 'Date'},
        title='Expected Goals vs Actual Goals',
    )
    fig_xg.update_traces(mode='lines+markers')
    apply_dark_theme(fig_xg)
    st.plotly_chart(fig_xg, use_container_width=True)

    # Goals by Opponent
    st.write("## Goals Scored Against Opponents")
    goals_by_opponent = player_df.groupby('Opponent')['Gls'].sum().reset_index()
    goals_by_opponent = goals_by_opponent.sort_values(by='Gls', ascending=False)
    fig_opp = px.bar(
        goals_by_opponent, x='Opponent', y='Gls', text='Gls',
        title='Total Goals Scored Against Each Opponent',
        labels={'Gls': 'Total Goals'},
        color_discrete_sequence=['skyblue'],
    )
    fig_opp.update_traces(textposition='outside')
    apply_dark_theme(fig_opp)
    st.plotly_chart(fig_opp, use_container_width=True)

    # Download button
    csv = player_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{selected_player}_data_{selected_year}.csv",
        mime='text/csv',
        key='download-csv'
    )
else:
    st.write("Please select a player to view their data.")
