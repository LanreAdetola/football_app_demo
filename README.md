# Football App Demo

This is a Streamlit-based web application for visualizing football data, specifically focused on Genk player and club profiles for the 2024/25 and 2025/26 seasons. The app provides a visual representation of the Jupiler Pro League, making complex football statistics easier to interpret than traditional tables with figures. It uses web scraping to gather data from FBref, ensuring up-to-date and comprehensive league and player information.

## Features
- **About Me**: Information about the creator.
- **Season 24-25**:
  - Shooting Profiles
  - Club Profile
  - 2023/24 Genk Player Profiles
- **Season 25-26**:
  - Shooting Profiles
  - Club Profile
 - **Jupiler Pro League Visualization**: Get interactive and graphical insights into league and player performance, making analysis more intuitive.
 - **Web Scraping from FBref**: Automatically fetches the latest football data for accurate and current visualizations.

## Directory Structure
```
assets/                # Static assets (images, etc.)
data/                  # Cleaned CSV data for players
forms/                 # Form components (e.g., contact form)
Miss/                  # Passing analysis
views/                 # Streamlit view scripts for each page
streamlit_app.py       # Main Streamlit app entry point
requirements.txt       # Python dependencies
```

## Getting Started
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Requirements
- Python 3.8+
- See `requirements.txt` for required packages

## Usage
- The app provides navigation between different views for club and player profiles, shooting stats, and more.
- Data is loaded from the `data/` directory and visualized using Matplotlib and Seaborn.

## Author
Made by Lanre.A
