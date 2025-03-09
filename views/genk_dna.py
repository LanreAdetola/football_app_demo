import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Jupiler Pro League - Player Performance Breakdown")

url = "https://fbref.com/en/squads/1e972a99/Genk-Stats"  # Example URL

# Load and preprocess data
pd.set_option('display.max_columns', None)
html = pd.read_html(url, header=1)
df = html[0]
df = df[:-2]  # Drop the last two rows for cleaner data

# Ensure we are working with a copy of the DataFrame slice
df = df.copy()

# Update 'Primary Pos' and 'Secondary Pos' using .loc
df.loc[:, 'Primary Pos'] = df['Pos'].apply(lambda x: x.split(',')[0].strip())
df.loc[:, 'Secondary Pos'] = df['Pos'].apply(lambda x: ', '.join(x.split(',')[1:]).strip() if ',' in x else None)

# Display cleaned data
st.dataframe(df)
st.markdown("---")

# Sidebar for feature selection
available_features = {
    'Minutes': 'Min',
    'Goals': 'Goals',
    'Assists': 'Assists'
}
selected_feature_label = st.sidebar.selectbox("Choose a feature", list(available_features.keys()))
selected_feature = available_features[selected_feature_label]



def plot_gk_minutes(df):
    """
    Plots the total minutes played by goalkeepers (GK), sorted by ascending minutes played.
    """
    gk_df = df[df['Primary Pos'] == 'GK']
    gk_minutes = gk_df.groupby(['Player', 'Primary Pos'])['Min'].sum().reset_index()
    gk_minutes = gk_minutes.sort_values(by='Min', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.barh(gk_minutes['Player'], gk_minutes['Min'], color='lightblue')
    ax.set_title('Goalkeepers (GK) - Total Minutes Played', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Minutes Played', fontsize=12)
    ax.set_ylabel('Player', fontsize=12)

    # Add the minute labels on the bars
    for i, (player, minutes) in enumerate(zip(gk_minutes['Player'], gk_minutes['Min'])):
        ax.text(minutes + 20, i, f'{minutes}', va='center', fontsize=10)

    plt.tight_layout()
    st.pyplot(fig)


def plot_df_minutes(df):
    """
    Plots the total minutes played by defenders (DF), sorted by ascending minutes played.
    """
    df_df = df[df['Primary Pos'] == 'DF']
    df_minutes = df_df.groupby(['Player', 'Primary Pos'])['Min'].sum().reset_index()
    df_minutes = df_minutes.sort_values(by='Min', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.barh(df_minutes['Player'], df_minutes['Min'], color='lightgreen')
    ax.set_title('Defenders (DF) - Total Minutes Played', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Minutes Played', fontsize=12)
    ax.set_ylabel('Player', fontsize=12)

    # Add the minute labels on the bars
    for i, (player, minutes) in enumerate(zip(df_minutes['Player'], df_minutes['Min'])):
        ax.text(minutes + 20, i, f'{minutes}', va='center', fontsize=10)

    plt.tight_layout()
    st.pyplot(fig)


def plot_mf_minutes(df):
    """
    Plots the total minutes played by midfielders (MF), sorted by ascending minutes played.
    """
    mf_df = df[df['Primary Pos'] == 'MF']
    mf_minutes = mf_df.groupby(['Player', 'Primary Pos'])['Min'].sum().reset_index()
    mf_minutes = mf_minutes.sort_values(by='Min', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.barh(mf_minutes['Player'], mf_minutes['Min'], color='salmon')
    ax.set_title('Midfielders (MF) - Total Minutes Played', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Minutes Played', fontsize=12)
    ax.set_ylabel('Player', fontsize=12)

    # Add the minute labels on the bars
    for i, (player, minutes) in enumerate(zip(mf_minutes['Player'], mf_minutes['Min'])):
        ax.text(minutes + 20, i, f'{minutes}', va='center', fontsize=10)

    plt.tight_layout()
    st.pyplot(fig)


def plot_fw_minutes(df):
    """
    Plots the total minutes played by forwards (FW), sorted by ascending minutes played.
    """
    fw_df = df[df['Primary Pos'] == 'FW']
    fw_minutes = fw_df.groupby(['Player', 'Primary Pos'])['Min'].sum().reset_index()
    fw_minutes = fw_minutes[fw_minutes ['Min'] >= 5]
    fw_minutes = fw_minutes.sort_values(by='Min', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.barh(fw_minutes['Player'], fw_minutes['Min'], color='yellowgreen')
    ax.set_title('Forwards (FW) - Total Minutes Played', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Minutes Played', fontsize=12)
    ax.set_ylabel('Player', fontsize=12)

    # Add the minute labels on the bars
    for i, (player, minutes) in enumerate(zip(fw_minutes['Player'], fw_minutes['Min'])):
        ax.text(minutes + 20, i, f'{minutes}', va='center', fontsize=10)

    
    st.pyplot(fig)


def plot_minutes_pie_chart(df):
    """
    Plots a pie chart of total minutes played by primary position in Streamlit.
    """
    # Aggregate total minutes by Primary Position
    min_by_position = df.groupby('Primary Pos')['Min'].sum().sort_values()

    # Create the pie chart
    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    ax.pie(min_by_position, 
           labels=min_by_position.index, 
           autopct='%1.1f%%', 
           startangle=90, 
           colors=['lightblue', 'lightgreen', 'salmon', 'yellowgreen'])
    
    ax.set_title('Percentage of Minutes Played by Position', fontsize=14, fontweight='bold')
    
    # Display the plot in Streamlit
    st.pyplot(fig)


def plot_minutes_bar_chart(df):
    """
    Plots a bar chart of total minutes played by primary position in Streamlit.
    """
    # Aggregate total minutes by Primary Position
    min_by_position = df.groupby('Primary Pos')['Min'].sum().sort_values()

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    ax.bar(min_by_position.index, 
           min_by_position.values, 
           color=['lightblue', 'lightgreen', 'salmon', 'yellowgreen'])
    
    ax.set_title('Total Minutes Played by Position', fontsize=14, fontweight='bold')
    ax.set_xlabel('Primary Position', fontsize=12)
    ax.set_ylabel('Total Minutes', fontsize=12)
    
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig)

#Goals
#Goals
#Goals

# Function to plot the total Goals played by Primary Position
def plot_goals_bar_chart(df):
    goals_by_position = df.groupby('Primary Pos')['Gls'].sum().sort_values()

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    ax.bar(goals_by_position.index, goals_by_position.values, color=['lightblue', 'lightgreen', 'salmon', 'yellowgreen'])
    ax.set_title('Total Goals by Position', fontsize=14, fontweight='bold')
    ax.set_xlabel('Primary Position', fontsize=12)
    ax.set_ylabel('Total Goals', fontsize=12)

    plt.tight_layout()
    st.pyplot(fig)



def plot_goals_players(df):
    goals_by_players = df[df['Gls'] >0 ] [['Player', 'Gls']].sort_values(by='Gls', ascending= True) 

    if goals_by_players.empty:
        st.write("No players have scored goals.")
        return

    fig, ax = plt.subplots(figsize=(8,6), dpi=100 )
    
    ax.barh(goals_by_players['Player'], goals_by_players['Gls'], color='skyblue')

    # Add dynamic data labels
    max_goals = goals_by_players['Gls'].max()
    label_offset = max_goals * 0.005  # % of max value as offset for clarity

    # Add data labels on bars
    for i, (goals, player) in enumerate(zip(goals_by_players['Gls'], goals_by_players['Player'])):
        ax.text(goals + label_offset, i, f'{goals}', va='center', fontsize=10)

    ax.set_title('Goals by Players', fontsize=14,fontweight='bold')
    ax.set_xlabel('Goals', fontsize=12)
    ax.set_ylabel('Player',fontsize=12)
    
    plt.tight_layout()

    st.pyplot(fig) 


def plot_avg_goals_per_90(df):
    # Calculate Goals per 90 for each player
    df['Gls per 90'] = (df['Gls'] / df['Min']) * 90
    
    # Filter out players who haven't played at least 90 minutes
    df_filtered = df[(df['Gls'] > 0) & (df['Min'] > 90)]
    
    # Sort by Goals per 90
    df_filtered = df_filtered.sort_values(by='Gls per 90', ascending=False)
    
    if df_filtered.empty:
        st.write("No players have played enough minutes to calculate goals per 90.")
        return
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.barh(df_filtered['Player'], df_filtered['Gls per 90'], color='skyblue')
    
    # Add data labels on bars
    for i, (goals_per_90, player) in enumerate(zip(df_filtered['Gls per 90'], df_filtered['Player'])):
        ax.text(goals_per_90 + 0.05, i, f'{goals_per_90:.2f}', va='center', fontsize=10)
    
    ax.set_title('Average Goals per 90 Minutes by Player', fontsize=14, fontweight='bold')
    ax.set_xlabel('Goals per 90', fontsize=12)
    ax.set_ylabel('Player', fontsize=12)
    
    plt.tight_layout()
    st.pyplot(fig)








#Assists
#Assists
#Assists


# Function to plot the total Assists played by Primary Position
def plot_assists_bar_chart(df):
    assists_by_position = df.groupby('Primary Pos')['Ast'].sum().sort_values()

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    ax.bar(assists_by_position.index, assists_by_position.values, color=['lightblue', 'lightgreen', 'salmon', 'yellowgreen'])
    ax.set_title('Total Assists by Position', fontsize=14, fontweight='bold')
    ax.set_xlabel('Primary Position', fontsize=12)
    ax.set_ylabel('Total Assists', fontsize=12)

    plt.tight_layout()
    st.pyplot(fig)











# Conditional Plot Display
if selected_feature_label == 'Minutes':
    st.subheader("Bar Chart: Goalkeeper Minutes Played")
    plot_gk_minutes(df)
    st.markdown("---")
    st.subheader("Bar Chart: Defender Minutes Played")
    plot_df_minutes(df)
    st.markdown("---")
    st.subheader("Bar Chart: Midfielder Minutes Played")
    plot_mf_minutes(df)
    st.markdown("---")
    st.subheader("Bar Chart: Forward Minutes Played")
    plot_fw_minutes(df)
    st.markdown("---")
    st.subheader("Pie Chart: Minutes Distribution by Position")
    plot_minutes_pie_chart(df)
    st.markdown("---")
    st.subheader("Bar Chart: Total Minutes by Position")
    plot_minutes_bar_chart(df)
    st.markdown("---")

elif selected_feature_label == 'Goals':
    st.subheader("Bar Chart: Total Goals by Position")
    plot_goals_bar_chart(df)
    st.markdown("---")
    st.subheader("Bar Chart: Total Goals by Position")
    plot_goals_players(df)
    st.markdown("---")
    st.subheader("Scatter Plot: Goals vs Minutes Played")
    plot_avg_goals_per_90(df)


elif selected_feature_label == 'Assists':
    st.subheader("Bar Chart: Total Assists by Position")
    plot_assists_bar_chart(df)


else:
    st.write(f"Currently, no specific plot is defined for {selected_feature_label}.")

