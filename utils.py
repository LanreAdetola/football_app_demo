import os
import datetime

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Theme constants (match .streamlit/config.toml)
# ---------------------------------------------------------------------------
DARK_BG = "#002b36"
TEXT_COLOR = "#ffffff"
ACCENT_BLUE = "#1f77b4"
ACCENT_ORANGE = "#ff7f0e"
POS_COLORS = {
    "GK": "lightblue",
    "DF": "lightgreen",
    "MF": "salmon",
    "FW": "yellowgreen",
}
POS_ORDER = ["GK", "DF", "MF", "FW"]


def apply_dark_theme(fig):
    fig.update_layout(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        font=dict(color=TEXT_COLOR),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#586e75"),
        yaxis=dict(gridcolor="#586e75"),
        margin=dict(l=40, r=20, t=50, b=40),
    )


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
def show_last_updated(csv_path: str):
    mtime = os.path.getmtime(csv_path)
    dt = datetime.datetime.fromtimestamp(mtime)
    st.caption(f"Data last updated: {dt.strftime('%d %B %Y')}")


def show_insight(text: str):
    st.caption(f"💡 {text}")


# ---------------------------------------------------------------------------
# Cached data loaders
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@st.cache_data
def load_shooting_data(season: str) -> pd.DataFrame:
    csv_path = os.path.join(DATA_DIR, f"shooting{season}.csv")
    df = pd.read_csv(csv_path)
    df.rename(columns={"# Pl": "no_players", "90s": "no_matches"}, inplace=True)
    # Ensure numeric types
    for col in ["Gls", "Sh", "SoT", "PK", "PKatt"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["SoT%", "Sh/90", "SoT/90", "G/Sh", "G/SoT"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@st.cache_data
def load_genk_dna_data(season: str) -> pd.DataFrame:
    csv_path = os.path.join(DATA_DIR, f"genk_dna{season}.csv")
    df = pd.read_csv(csv_path)
    df["Min"] = pd.to_numeric(df["Min"].astype(str).str.replace(",", ""), errors="coerce")
    df["Gls"] = pd.to_numeric(df["Gls"], errors="coerce")
    df["Ast"] = pd.to_numeric(df["Ast"], errors="coerce")
    df = df.copy()
    df["Primary Pos"] = df["Pos"].apply(lambda x: x.split(",")[0].strip())
    df["Secondary Pos"] = df["Pos"].apply(
        lambda x: ", ".join(x.split(",")[1:]).strip() if "," in x else None
    )
    return df


def _shooting_csv_path(season: str) -> str:
    return os.path.join(DATA_DIR, f"shooting{season}.csv")


def _genk_csv_path(season: str) -> str:
    return os.path.join(DATA_DIR, f"genk_dna{season}.csv")


# ---------------------------------------------------------------------------
# Shooting chart functions (Plotly)
# ---------------------------------------------------------------------------
def plot_team_goals(df):
    st.header("League Goals Scored By Teams")
    show_insight("Total goals scored across the league — shows attacking output at a glance.")
    data = df[["Squad", "Gls"]].sort_values(by="Gls", ascending=False)
    fig = px.bar(data, x="Squad", y="Gls", text="Gls",
                 labels={"Gls": "Number of Goals"}, color_discrete_sequence=[ACCENT_BLUE])
    fig.update_traces(textposition="outside")
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_team_shots(df):
    st.header("League Shots By Teams")
    show_insight("Total shots attempted — high volume doesn't always mean high efficiency.")
    data = df[["Squad", "Sh"]].sort_values(by="Sh", ascending=False)
    fig = px.bar(data, x="Squad", y="Sh", text="Sh",
                 labels={"Sh": "Number of Shots"}, color_discrete_sequence=[ACCENT_BLUE])
    fig.update_traces(textposition="outside")
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_team_shots_on_target(df):
    st.header("League Shots On Target By Teams")
    show_insight("Shots on target is a better indicator of finishing quality than total shots.")
    data = df[["Squad", "SoT"]].sort_values(by="SoT", ascending=False)
    fig = px.bar(data, x="Squad", y="SoT", text="SoT",
                 labels={"SoT": "Shots On Target"}, color_discrete_sequence=[ACCENT_BLUE])
    fig.update_traces(textposition="outside")
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_compare_shots(df):
    st.header("Shots vs Shots On Target By Teams")
    show_insight("The gap between total shots and shots on target reveals shooting discipline.")
    data = df[["Squad", "Sh", "SoT"]].sort_values(by="Sh", ascending=False)
    melted = data.melt(id_vars="Squad", value_vars=["Sh", "SoT"],
                       var_name="Metric", value_name="Count")
    fig = px.bar(melted, x="Squad", y="Count", color="Metric", barmode="group",
                 color_discrete_map={"Sh": ACCENT_BLUE, "SoT": ACCENT_ORANGE})
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_shooting_matrix(df):
    st.header("Shot Volume vs Accuracy")
    show_insight(
        "Top-right = high volume + accurate. Bottom-right = shoot often but miss frequently."
    )
    median_sh = df["Sh/90"].median()
    median_sot = df["SoT/90"].median()

    df = df.copy()
    df["Efficiency"] = df.apply(
        lambda r: "Inefficient" if r["Sh/90"] > median_sh and r["SoT/90"] < median_sot else "Efficient",
        axis=1,
    )

    fig = px.scatter(
        df, x="Sh/90", y="SoT/90", color="Efficiency", text="Squad",
        color_discrete_map={"Efficient": ACCENT_BLUE, "Inefficient": "red"},
        labels={"Sh/90": "Shots per 90", "SoT/90": "Shots on Target per 90"},
    )
    fig.update_traces(textposition="top center", textfont_size=10)
    fig.add_hline(y=median_sot, line_dash="dash", line_color="gray", opacity=0.7)
    fig.add_vline(x=median_sh, line_dash="dash", line_color="gray", opacity=0.7)
    apply_dark_theme(fig)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def plot_missed_shots(df):
    st.header("Shooting Inefficiency By Teams")
    show_insight("Higher percentage means more shots are missing the target.")
    df = df.copy()
    df["Missed Shots"] = df["Sh"] - df["SoT"]
    df["Inefficiency"] = (df["Missed Shots"] / df["Sh"]) * 100
    data = df[["Squad", "Inefficiency"]].sort_values(by="Inefficiency", ascending=True)
    fig = px.bar(
        data, x="Inefficiency", y="Squad", orientation="h",
        text=data["Inefficiency"].apply(lambda v: f"{v:.1f}%"),
        labels={"Inefficiency": "Shooting Inefficiency (%)"},
        color_discrete_sequence=["red"],
    )
    fig.update_traces(textposition="outside")
    apply_dark_theme(fig)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def plot_penalty_efficiency(df):
    st.header("Penalty Efficiency By Squad")
    show_insight("Gap between attempts and conversions highlights missed penalty opportunities.")
    data = df[["Squad", "PK", "PKatt"]].sort_values(by="PK", ascending=False)
    melted = data.melt(id_vars="Squad", value_vars=["PKatt", "PK"],
                       var_name="Metric", value_name="Count")
    melted["Metric"] = melted["Metric"].map({"PKatt": "Penalty Attempts", "PK": "Penalty Goals"})
    fig = px.bar(melted, x="Squad", y="Count", color="Metric", barmode="group",
                 color_discrete_map={"Penalty Attempts": "grey", "Penalty Goals": "green"})
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_goal_conversion_efficiency(df):
    st.header("Goal Conversion Efficiency")
    show_insight("Higher ratios mean the team converts a larger share of their shots into goals.")
    data = df[["Squad", "G/Sh", "G/SoT"]].sort_values(by="G/Sh", ascending=False)
    melted = data.melt(id_vars="Squad", value_vars=["G/Sh", "G/SoT"],
                       var_name="Metric", value_name="Ratio")
    melted["Metric"] = melted["Metric"].map({
        "G/Sh": "Goals per Shot", "G/SoT": "Goals per Shot on Target"
    })
    fig = px.bar(melted, x="Squad", y="Ratio", color="Metric", barmode="group",
                 color_discrete_map={"Goals per Shot": ACCENT_BLUE, "Goals per Shot on Target": ACCENT_ORANGE})
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Genk DNA chart functions (Plotly)
# ---------------------------------------------------------------------------
def plot_position_minutes(df, position: str, color: str):
    pos_df = df[df["Primary Pos"] == position]
    pos_minutes = pos_df.groupby("Player")["Min"].sum().reset_index()
    pos_minutes = pos_minutes.sort_values(by="Min", ascending=True)

    pos_names = {"GK": "Goalkeepers", "DF": "Defenders", "MF": "Midfielders", "FW": "Forwards"}
    title = f"{pos_names.get(position, position)} ({position}) - Total Minutes Played"

    fig = px.bar(pos_minutes, x="Min", y="Player", orientation="h", text="Min",
                 labels={"Min": "Total Minutes Played"}, color_discrete_sequence=[color])
    fig.update_traces(textposition="outside")
    fig.update_layout(title=title)
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_minutes_pie_chart(df):
    min_by_pos = df.groupby("Primary Pos")["Min"].sum().reset_index()
    fig = px.pie(
        min_by_pos, values="Min", names="Primary Pos",
        color="Primary Pos", color_discrete_map=POS_COLORS,
        title="Percentage of Minutes Played by Position",
    )
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_minutes_bar_chart(df):
    min_by_pos = df.groupby("Primary Pos")["Min"].sum().reset_index().sort_values(by="Min")
    fig = px.bar(
        min_by_pos, x="Primary Pos", y="Min", text="Min",
        color="Primary Pos", color_discrete_map=POS_COLORS,
        title="Total Minutes Played by Position",
        labels={"Min": "Total Minutes", "Primary Pos": "Position"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_goals_bar_chart(df):
    goals_by_pos = df.groupby("Primary Pos")["Gls"].sum().reset_index().sort_values(by="Gls")
    fig = px.bar(
        goals_by_pos, x="Primary Pos", y="Gls", text="Gls",
        color="Primary Pos", color_discrete_map=POS_COLORS,
        title="Total Goals by Position",
        labels={"Gls": "Total Goals", "Primary Pos": "Position"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_goals_players(df):
    goals_data = df[df["Gls"] > 0][["Player", "Gls"]].sort_values(by="Gls", ascending=True)
    if goals_data.empty:
        st.write("No players have scored goals.")
        return
    fig = px.bar(
        goals_data, x="Gls", y="Player", orientation="h", text="Gls",
        title="Goals by Players", labels={"Gls": "Goals"},
        color_discrete_sequence=["skyblue"],
    )
    fig.update_traces(textposition="outside")
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_avg_goals_per_90(df):
    df = df.copy()
    df["Gls per 90"] = (df["Gls"] / df["Min"]) * 90
    df_filtered = df[(df["Gls"] > 0) & (df["Min"] > 90)]
    df_filtered = df_filtered.sort_values(by="Gls per 90", ascending=True)

    if df_filtered.empty:
        st.write("No players have played enough minutes to calculate goals per 90.")
        return

    fig = px.bar(
        df_filtered, x="Gls per 90", y="Player", orientation="h",
        text=df_filtered["Gls per 90"].apply(lambda v: f"{v:.2f}"),
        title="Average Goals per 90 Minutes by Player",
        labels={"Gls per 90": "Goals per 90"},
        color_discrete_sequence=["skyblue"],
    )
    fig.update_traces(textposition="outside")
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def plot_assists_bar_chart(df):
    assists_by_pos = df.groupby("Primary Pos")["Ast"].sum().reset_index().sort_values(by="Ast")
    fig = px.bar(
        assists_by_pos, x="Primary Pos", y="Ast", text="Ast",
        color="Primary Pos", color_discrete_map=POS_COLORS,
        title="Total Assists by Position",
        labels={"Ast": "Total Assists", "Primary Pos": "Position"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Page orchestrators
# ---------------------------------------------------------------------------
def render_shooting_page(season: str, title: str):
    st.title(title)
    df = load_shooting_data(season)
    show_last_updated(_shooting_csv_path(season))

    st.dataframe(df)
    st.markdown("---")

    plot_team_goals(df)
    st.markdown("---")
    plot_team_shots(df)
    st.markdown("---")
    plot_team_shots_on_target(df)
    st.markdown("---")
    plot_compare_shots(df)
    st.markdown("---")
    plot_shooting_matrix(df)
    st.markdown("---")
    plot_missed_shots(df)
    st.markdown("---")
    plot_penalty_efficiency(df)
    st.markdown("---")
    plot_goal_conversion_efficiency(df)


def render_genk_dna_page(season: str):
    st.title("Jupiler Pro League - Player Performance Breakdown")
    df = load_genk_dna_data(season)
    show_last_updated(_genk_csv_path(season))

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        pos_filter = st.multiselect(
            "Filter by position",
            options=sorted(df["Primary Pos"].unique()),
            default=sorted(df["Primary Pos"].unique()),
        )
    with col2:
        max_min = int(df["Min"].max()) if not df["Min"].isna().all() else 0
        min_minutes = st.slider("Minimum minutes played", 0, max_min, 0)

    df_filtered = df[(df["Primary Pos"].isin(pos_filter)) & (df["Min"] >= min_minutes)]

    st.dataframe(df_filtered)
    st.markdown("---")

    # Sidebar feature selector
    selected_feature = st.sidebar.selectbox("Choose a feature", ["Minutes", "Goals", "Assists"])

    if selected_feature == "Minutes":
        for pos in POS_ORDER:
            if pos in pos_filter:
                st.subheader(f"Bar Chart: {pos} Minutes Played")
                plot_position_minutes(df_filtered, pos, POS_COLORS[pos])
                st.markdown("---")
        st.subheader("Pie Chart: Minutes Distribution by Position")
        plot_minutes_pie_chart(df_filtered)
        st.markdown("---")
        st.subheader("Bar Chart: Total Minutes by Position")
        plot_minutes_bar_chart(df_filtered)

    elif selected_feature == "Goals":
        st.subheader("Bar Chart: Total Goals by Position")
        plot_goals_bar_chart(df_filtered)
        st.markdown("---")
        st.subheader("Bar Chart: Goals by Players")
        plot_goals_players(df_filtered)
        st.markdown("---")
        st.subheader("Bar Chart: Goals per 90 Minutes")
        plot_avg_goals_per_90(df_filtered)

    elif selected_feature == "Assists":
        st.subheader("Bar Chart: Total Assists by Position")
        plot_assists_bar_chart(df_filtered)
