# ============================================================
# LAB 03 - DATA LOADING, LAYOUT, AND FRONTEND PROTOTYPE
# EduRisk Analytics - Student Risk Monitoring Dashboard
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------
import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# 2. PAGE CONFIGURATION
# must be the first Streamlit command in the script
# ------------------------------------------------------------
st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
)

# ------------------------------------------------------------
# 3. DESIGN / CUSTOM STYLE
# CSS block that gives the app its colour scheme
#
# COLOUR PALETTE
#   Navy   #0F2238  headings and sidebar
#   Teal   #1E7A5F  main accent colour
#   Slate  #5B6B7F  secondary text
#   Line   #E3E8EF  borders
#   Page   #F7F9FC  page background
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* DESIGN: soft grey-blue page background so white cards stand out */
    .stApp {
        background-color: #F7F9FC;
    }

    /* DESIGN: all headings in deep navy */
    h1, h2, h3 {
        color: #0F2238;
    }

    /* DESIGN: teal underline under every page title */
    .stApp h1 {
        border-bottom: 3px solid #1E7A5F;
        padding-bottom: 8px;
    }

    /* DESIGN: navy gradient sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F2238 0%, #17304A 100%);
    }

    /* DESIGN: light text so it stays readable on the navy sidebar */
    section[data-testid="stSidebar"] * {
        color: #E8EEF6;
    }

    /* DESIGN: white sidebar title with a teal underline */
    section[data-testid="stSidebar"] h1 {
        color: #FFFFFF;
        border-bottom: 2px solid #1E7A5F;
        padding-bottom: 6px;
    }

    /* DESIGN: metric boxes look like white cards with a teal edge */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E3E8EF;
        border-left: 4px solid #1E7A5F;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(15, 34, 56, 0.06);
    }

    /* DESIGN: softer grey label above each metric number */
    [data-testid="stMetricLabel"] {
        color: #5B6B7F;
    }

    /* DESIGN: navy metric number */
    [data-testid="stMetricValue"] {
        color: #0F2238;
    }

    /* DESIGN: teal action buttons */
    .stButton button,
    .stFormSubmitButton button {
        background-color: #1E7A5F;
        color: #FFFFFF;
        border: 1px solid #1E7A5F;
    }

    /* DESIGN: darker teal when the mouse is over the button */
    .stButton button:hover,
    .stFormSubmitButton button:hover {
        background-color: #15614A;
        color: #FFFFFF;
        border: 1px solid #15614A;
    }

    /* DESIGN: navy download button, different from the teal action buttons */
    .stDownloadButton button {
        background-color: #0F2238;
        color: #FFFFFF;
        border: 1px solid #0F2238;
    }

    .stDownloadButton button:hover {
        background-color: #17304A;
        color: #FFFFFF;
        border: 1px solid #17304A;
    }

    /* DESIGN: white card around the risk checker form */
    [data-testid="stForm"] {
        background-color: #FFFFFF;
        border: 1px solid #E3E8EF;
        border-radius: 10px;
    }

    /* DESIGN: rounded border around the data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #E3E8EF;
        border-radius: 8px;
    }

    /* DESIGN: rounded message boxes (success / info / warning / error) */
    [data-testid="stAlert"] {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# 4. LOAD DATA FROM students.csv
# data now lives outside app.py (Lab 03)
# ------------------------------------------------------------
def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()

student_df = load_student_data()

# ------------------------------------------------------------
# 5. RISK RULE
# turns score + attendance into a risk label
# ------------------------------------------------------------
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# apply the rule to every row -> new "Risk Level" column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

# ------------------------------------------------------------
# 6. DESIGN: RISK LEVEL COLOURS
# green = Low, yellow = Medium, red = High
# ------------------------------------------------------------
risk_colors = {
    "Low Risk": "background-color: #DCFCE7; color: #166534",
    "Medium Risk": "background-color: #FEF3C7; color: #92400E",
    "High Risk": "background-color: #FEE2E2; color: #991B1B"
}

# DESIGN: paint only the "Risk Level" column of a table
def color_risk(df):
    return df.style.map(
        lambda value: risk_colors.get(value, ""),
        subset=["Risk Level"]
    )

# ------------------------------------------------------------
# 7. SIDEBAR NAVIGATION
# ------------------------------------------------------------
with st.sidebar:
    st.title("EduRisk Menu")
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )

# ============================================================
# PAGE 1: HOME
# ============================================================
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")

# ============================================================
# PAGE 2: DASHBOARD
# filters -> metrics -> table -> charts
# ============================================================
elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")

    st.write(
        "This dashboard gives a quick overview of student performance "
        "using data loaded from students.csv."
    )

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

    st.subheader("Student Records")
    st.write("This table shows student data loaded from students.csv.")
    st.dataframe(color_risk(student_df))

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Score Chart")
        score_chart = student_df.set_index("Student Name")["Score"]
        st.bar_chart(score_chart)

    with chart_col2:
        st.write("Course Count")
        course_count = student_df["Course"].value_counts()
        st.bar_chart(course_count)

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )

# ============================================================
# PAGE 3: STUDENT DATA
# full dataset, no filters
# ============================================================
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(color_risk(student_df))


# ============================================================
# PAGE 4: RISK CHECKER
# form -> check one student at a time
# ============================================================
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")
    st.write(
        "Use this page to check the risk level of one student based on "
        "score and attendance."
    )

    # --- INPUT FORM (submits all inputs together) ---
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    # --- RESULT (shown OUTSIDE the form block) ---
    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        # DESIGN: green / yellow / red message to match the risk
        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")

# ============================================================
# PAGE 5: ABOUT
# project info + ethics reminder
# ============================================================
else:
    st.title("About")

    st.write("This app is part of Lab 03.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Data Loading, Layout, and Frontend Prototype")

    st.info(
        "This frontend prototype loads real data from students.csv "
        "and displays it using Streamlit and Pandas."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )