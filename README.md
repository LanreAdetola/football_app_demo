# Football Analytics App

A Streamlit-based web application for visualizing Belgian Jupiler Pro League football data, with a focus on KRC Genk. The app transforms complex football statistics into interactive visualizations, making analysis more intuitive than traditional tables.

**Live demo**: [lanrefcanalytics.streamlit.app](https://lanrefcanalytics.streamlit.app/)

## Features

- **Season 25-26 & 24-25**: Shooting profiles and club performance breakdowns for both seasons
- **Club Profile**: Player performance analysis by position with filters for position and minimum minutes played
- **2023/24 Player Profiles**: Individual player analysis with xG tracking, shooting accuracy, and opponent breakdowns
- **Season Comparison**: Side-by-side comparison of team metrics across seasons with delta tracking
- **Interactive Charts**: All visualizations built with Plotly for hover tooltips, zoom, and pan
- **Dark Theme**: Consistent dark styling across all charts and UI

## Pages

| Page | Description |
|------|-------------|
| About Me | Profile, skills, and contact info |
| Shooting Profiles | League-wide shooting stats: goals, shots, accuracy matrix, penalties, conversion efficiency |
| Club Profile | Genk squad breakdown by position: minutes, goals, assists with position/minutes filters |
| Player Profiles | Individual player game logs with xG vs actual goals, opponent analysis |
| Season Comparison | Compare any shooting metric (goals, shots, efficiency) between 24/25 and 25/26 |

## Directory Structure

```
streamlit_app.py       # Main app entry point and navigation
utils.py               # Shared functions: data loaders, Plotly charts, theme constants
views/                 # Page scripts (thin wrappers calling utils.py)
forms/                 # Contact form component
data/                  # CSV data files (shooting stats, squad stats, player logs)
assets/                # Static assets (profile image)
.streamlit/            # Streamlit theme configuration
```

## Getting Started

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Data

Stats are sourced from [FBref](https://fbref.com/) and stored as CSV files in `data/`. FBref uses Cloudflare protection, so data is cached locally rather than scraped live. To refresh data, use the local `refresh_data.py` script which opens a real browser to bypass Cloudflare.

## Tech Stack

- **Streamlit** - Web framework
- **Plotly** - Interactive visualizations
- **Pandas / NumPy** - Data processing

## Author

Made by [Lanre Adetola](https://github.com/LanreAdetola)
