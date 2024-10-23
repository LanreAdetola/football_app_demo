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
    page="views/genk.py",
    title="Genk Player Profiles",
    icon=":material/bar_chart:",
    
)

# --- Navigation -----
pg = st.navigation(
    {
        "Info": [about_page],
         "Projects": [project_1_page],
    }
         )

st.sidebar.text("Made by Lanre.A")


# Run Navigation
pg.run()