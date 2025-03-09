import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import requests
import os

# Page functions
def about_page():
    st.title("About Me")
    st.write("This is the About Me page.")

def passing_profiles():
    st.title("Passing Profiles")
    st.write("This is the Passing Profiles page.")

def shooting_profiles():
    st.title("Shooting Profiles")
    st.write("This is the Shooting Profiles page.")

def club_profile():
    st.title("Club Profile")
    st.write("This is the Club Profile page.")

def genk_profiles():
    st.title("2023/24 Genk Player Profiles")
    st.write("This is the Genk Player Profiles page.")

# Navigation
pages = {
    "About Me": about_page,
    "Passing Profiles": passing_profiles,
    "Shooting Profiles": shooting_profiles,
    "Club Profile": club_profile,
    "2023/24 Genk Player Profiles": genk_profiles
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display selected page
pages[selection]()

st.sidebar.text("Made by Lanre.A")
