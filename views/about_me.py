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
        "Data Analyst Intern, seeeking to assist enterprises by supporting data-driven decision-making."
    )
    if st.button(" Contact Me"):
        show_contact_form()


#--- Experience---

st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - 3 Years experience extracting actionable insights from data 
    - Hands-on experience and knowledge in Python and Sql 
    - Good understanding of statistical principles and their respective applications
    - Excellent team-player and displaying a strong sense of initiative on tasks
    """
)

#---Skills---

st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programming: Python (Scikit-learn, Pandas), SQl, VBA 
    - Data Visualization: Power BI, MS Excel, Plotly
    - Modeling: Logistic regression, Linear regression, Decision trees
    - Databases: MySQL, LiteDB, MongoDB
    """
)