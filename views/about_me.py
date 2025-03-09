import streamlit as st

from forms.contact import contact_form

def show_contact_form():
    contact_form()

# -- Me --
col1, col2 = st.columns(2)
with col1:
    st.image("assets/profilepic.png", width=230)
with col2:
    st.title("Lanre Adetola")
    st.write(
        "Data Analyst/Data Scientist Intern, seeking to assist enterprises by supporting data-driven decision-making."
    )
    if st.button("Contact Me"):
        show_contact_form()


#--- Experience---

st.write("\n")
st.subheader("Experience & Qualifications")
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
st.subheader("Hard Skills")
st.write(
    """
    - **Programming Languages**: Python (with libraries such as **Scikit-learn**, **Pandas**), **SQL**, **C#**
    - **Data Visualization**: Expertise in **Power BI**, **MS Excel**, **Matplot**, **Plotly** for creating interactive and insightful visualizations
    - **Machine Learning & Modeling**: Experience with **Logistic Regression**, **Linear Regression**, **Decision Trees** for predictive modeling
    - **Databases**: Proficient in **MySQL**, **LiteDB**, **MongoDB** for data storage and management
    """
)
