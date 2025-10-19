import streamlit as st

from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# -- Me --
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("assets/profilepic.png", width=230)
with col2:
    st.title("Lanre Adetola", anchor=False)
    

    st.write(
        "**Email**: r0913836@student.thomasmore.be"
    )
    if st.button("Contact Me"):
        show_contact_form()


#--- Experience---

st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    -Dive into player performance analytics powered by the Microsoft Cloud.
    -From raw stats to real-time insights, these visuals shows how data engineering and visualization can change the way we understand the game.
    -delivering visuals that highlight trends, player performance, and tactical insights.
    -I also use this to monitor the performance of KRC Genk 😁.
    """
)


#---Skills---

st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - **Programming Languages**: Python (with libraries such as **Scikit-learn**, **Pandas**), **SQL**
    - **Data Visualization**: Proficent in **Matplotlib**, **Plotly**, **Seaborn** for creating interactive and insightful visualizations
    - **Machine Learning & Modeling**: Experience with **Logistic Regression**, **Linear Regression**, **Decision Trees** etc for predictive modeling
    """
)
