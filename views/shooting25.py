import streamlit as st 
import requests 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from adjustText import adjust_text

st.title('Jupiler Pro League 25/26 - Shooting Stats')


url = "https://fbref.com/en/comps/37/shooting/Belgian-Pro-League-Stats#all_stats_shooting"


#Loading Data from the url
pd.set_option('display.max_columns', None)
html = pd.read_html(url, header=1)
df = html[0]

#raw dataframe
#st.dataframe(df)

#Rename Columns for Readability 
df.rename(columns = {
    "# Pl": "no_players",
    "90s": "no_matches",
    }, inplace=True)

# Display Dataframe in an interactive table....Clean dataframe
st.dataframe(df)
st.markdown("---")

def plot_team_goals(df):
    st.header('League Goals Scored By Teams')

    # Group by 'Squad' and 'passes_Cmp' and 'passes_Att'

    league_goals = df[['Squad','Gls']].sort_values( by='Gls', ascending=False)
                                        
    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_goals.plot(kind="bar", x='Squad', y=['Gls'], ax =ax , color=['#1f77b4'])

    ax.set_title('League Goals Scored By Teams')
    ax.set_ylabel('Number of Goals')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_goals['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 6), 
                    textcoords='offset points', fontsize=8)

    st.pyplot(fig)

# def plot_team_goals_scatter(df):
#     # Check if the required columns are present
#     if not {'xG', 'Gls', 'Squad'}.issubset(df.columns):
#         st.error("Dataframe missing one of the required columns: 'xG', 'Gls', or 'Squad'")
#         return
#     
#     # Create the scatter plot
#     fig, ax = plt.subplots(figsize=(12, 8))
#     scatter = ax.scatter(df['xG'], df['Gls'], alpha=0.6, s=100)
# 
#     # Add labels and title
#     ax.set_xlabel('Expected Goals (xG)', fontsize=12)
#     ax.set_ylabel('Actual Goals (Gls)', fontsize=12)
#     ax.set_title('Actual Goals vs Expected Goals', fontsize=14)
# 
#     # Add a diagonal line for reference (xG = Gls)
#     lims = [
#         np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
#         np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
#     ]
#     ax.plot(lims, lims, 'r--', alpha=0.75, zorder=0)
# 
#     # Add team labels to points
#     texts = [
#         ax.text(df['xG'].iloc[i], df['Gls'].iloc[i], txt, fontsize=18, alpha=0.7)
#         for i, txt in enumerate(df['Squad'])
#     ]
# 
#     # Adjust text to minimize overlap
#     adjust_text(texts, arrowprops=dict(arrowstyle="-", color='gray', lw=0.5))
# 
#     # Adjust layout to prevent clipping of tick-labels and display in Streamlit
#     fig.tight_layout()
#     st.pyplot(fig)

def plot_team_shots(df):
    st.header('League Shots By Teams')

    # Group by 'Squad' and 'Shots'

    league_shots = df[['Squad','Sh']].sort_values( by='Sh', ascending=False)

    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_shots.plot(kind="bar", x='Squad', y='Sh', ax =ax , color=['#1f77b4'])    

    ax.set_title('League Shots By Teams')
    ax.set_ylabel('Number of Shots')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_shots['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 6), 
                    textcoords='offset points', fontsize=8)

    st.pyplot(fig)


def plot_team_shotsTarget(df):
    st.header('League Shots On Target By Teams')

    # Group by 'Squad' and 'Shots On Target'

    league_shots = df[['Squad','SoT']].sort_values( by='SoT', ascending=False)

    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_shots.plot(kind="bar", x='Squad', y='SoT', ax =ax , color=['#1f77b4'])    

    ax.set_title('League Shots By Teams')
    ax.set_ylabel('Number of Shots On Target')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_shots['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 6), 
                    textcoords='offset points', fontsize=8)

    st.pyplot(fig)



def plot_compare_shots(df):
    st.header('Shots Vs Shots On Target By Teams')

    # Group by 'Squad' and 'Shots' and 'Shots On Target'

    league_shots = df[['Squad','Sh', 'SoT']].sort_values( by='Sh', ascending=False)
                                        
    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_shots.plot(kind="bar", x='Squad', y=['Sh', 'SoT'], ax =ax , color=['#1f77b4', '#ff7f0e'])

    ax.set_title('League Goals Scored By Teams')
    ax.set_ylabel('Number of Goals')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_shots['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    st.pyplot(fig)


def shooting_matrix(df):
    """Generate a scatter plot showing shot volume vs accuracy."""
    
    # Calculate median values dynamically
    median_shots_per_90 = df['Sh/90'].median()
    median_sot_per_90 = df['SoT/90'].median()

    # Define inefficient high-volume shooters
    inefficient_mask = (df['Sh/90'] > median_shots_per_90) & (df['SoT/90'] < median_sot_per_90)

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df['Sh/90'], df['SoT/90'], color='blue', label='Efficient Shooters')
    ax.scatter(df[inefficient_mask]['Sh/90'], df[inefficient_mask]['SoT/90'], color='red', label='Inefficient Shooters')

    # Add squad labels and store them in a list for adjustText
    texts = []
    for i, squad in enumerate(df['Squad']):
        color = 'red' if inefficient_mask.iloc[i] else 'black'
        texts.append(ax.text(df['Sh/90'].iloc[i], df['SoT/90'].iloc[i], squad, fontsize=9, ha='right', color=color))

    # Adjust text labels to avoid overlap
    adjust_text(texts, force_points=0.3, force_text=0.5, expand_text=(1.2, 1.2),
                arrowprops=dict(arrowstyle="->", color='black'), ax=ax)

    # Draw median reference lines
    ax.axvline(median_shots_per_90, linestyle='dashed', color='gray', alpha=0.7, label='Median Sh/90')
    ax.axhline(median_sot_per_90, linestyle='dashed', color='gray', alpha=0.7, label='Median SoT/90')

    # Labels and title
    ax.set_xlabel('Shots per 90 (Sh/90)')
    ax.set_ylabel('Shots on Target per 90 (SoT/90)')
    ax.set_title('Shot Volume vs Accuracy')

    # Grid and legend
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    # Display in Streamlit
    st.pyplot(fig)



def missed_shots(df):
    st.header('Missed Shots By Teams')

        # Calculate shooting inefficiency (Missed Shots %)
    df['Missed Shots'] = df['Sh'] - df['SoT']
    df['Shooting Inefficiency (%)'] = (df['Missed Shots'] / df['Sh']) * 100

    # Sort teams by shooting inefficiency
    df_sorted = df.sort_values(by='Shooting Inefficiency (%)', ascending=False)

    # Data for plotting
    squads = df_sorted['Squad']
    inefficiency = df_sorted['Shooting Inefficiency (%)']

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(squads, inefficiency, color='red')

    # Add annotations
    for bar in bars:
        width = bar.get_width()  # Get inefficiency percentage
        ax.text(width + 1,  # Position to the right of the bar
                bar.get_y() + bar.get_height()/2,  # Centered in height
                f'{width:.1f}%',  # Format to 1 decimal place
                ha='left', va='center', fontsize=9, color='black')

    # Labels and title
    ax.set_title('Shooting Inefficiency by Squad (Higher = Worse)')
    ax.set_xlabel('Shooting Inefficiency (%)')
    ax.set_ylabel('Squad')

    # Invert y-axis to show worst teams at the top
    ax.invert_yaxis()

    st.pyplot(fig)


def penalty_efficiency(df):
    """Generate a bar chart for penalty efficiency by squad."""
    
    # Sort by Penalty Goals (PK)
    df_sorted = df.sort_values(by='PK', ascending=False)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Penalty Attempts (Grey) and Penalty Goals (Green)
    ax.bar(df_sorted['Squad'], df_sorted['PKatt'], label='Penalty Attempts', color='grey')
    ax.bar(df_sorted['Squad'], df_sorted['PK'], label='Penalty Goals', color='green')

    # Labels and title
    ax.set_title('Penalty Efficiency by Squad')
    ax.set_xlabel('Squad')
    ax.set_ylabel('Count')
    ax.set_xticklabels(df_sorted['Squad'], rotation=90)
    ax.legend()

    # Display in Streamlit
    st.pyplot(fig)



def goal_conversion_efficiency(df):
    """Generate a bar chart for goal conversion efficiency (Goals per Shot and Goals per Shot on Target)."""
    
    # Sort by Goals per Shot (G/Sh)
    df_sorted = df.sort_values(by='G/Sh', ascending=False)

    x = np.arange(len(df_sorted['Squad']))  # Squad positions
    width = 0.35  # Bar width

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bars for Goals per Shot (G/Sh) and Goals per Shot on Target (G/SoT)
    ax.bar(x - width/2, df_sorted['G/Sh'], width, label='Goals per Shot (G/Sh)', color='#1f77b4')
    ax.bar(x + width/2, df_sorted['G/SoT'], width, label='Goals per Shot on Target (G/SoT)', color='#ff7f0e')

    # Labels and title
    ax.set_xticks(x)
    ax.set_xticklabels(df_sorted['Squad'], rotation=90)
    ax.set_title('Goal Conversion Efficiency: Shot vs. Shot on Target')
    ax.set_xlabel('Squad')
    ax.set_ylabel('Efficiency Ratio')
    ax.legend()

    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.5)

    # Display the plot in Streamlit
    st.pyplot(fig)









# Calling functions to generate each plot

if df is not None:
    plot_team_goals(df)     
    st.markdown("---")
    plot_team_shots(df)
    st.markdown("---")
    plot_team_shotsTarget(df)
    st.markdown("---")
    plot_compare_shots(df)
    st.markdown("---")
    shooting_matrix(df)
    st.markdown("---")
    missed_shots(df)
    st.markdown("---")
    penalty_efficiency(df)
    st.markdown("---")
    goal_conversion_efficiency(df)
    st.markdown("---")





#Unused code
#plot_team_goals_scatter(df)
#st.markdown("---")