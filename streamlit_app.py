import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import requests

#----Page Setup---
about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True,
)

project_1_page = st.Page(
    page="views/shooting.py",
    title="Shooting Profiles",
    icon=":material/bar_chart:",
    
)
project_2_page = st.Page(
    page="views/genk_dna.py",
    title="Club Profile",
    icon=":material/bar_chart:",
    
)

project_3_page = st.Page(
    page="views/player_profile.py",
    title="2023/24 Genk Player Profiles",
    icon=":material/bar_chart:",
    
)

# --- Navigation -----
pg = st.navigation( 
    {
        "Info": [about_page],
         "Projects": [project_1_page, project_2_page, project_3_page],
    }
         )

st.sidebar.text("Made by Lanre.A")


# Run Navigation
pg.run()