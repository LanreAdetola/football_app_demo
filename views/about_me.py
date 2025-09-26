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
    - Experienced in deriving actionable insights from complex data sets
    - Proficient in **Python** and **SQL** for data analysis, automation, and reporting
    - Strong understanding of **statistical principles** and their real-world applications
    - Demonstrated ability to collaborate as a **team player** and take the **initiative** in driving projects to completion
    - Familiar with key data visualization tools and techniques to communicate findings effectively
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
