# ============================================================
# LAB 02 - STREAMLIT I: CORE BUILDING BLOCKS
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
    page_title="EduRisk Analytics - Lab 02",
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
# 4. PREPARE DATA
# 8 students used by every page
# ------------------------------------------------------------
student_df = pd.DataFrame({
    "Student Name": ["Dara", "Sophea", "Vuthy", "Malis", "Rithy", "Sreyneang", "Chan", "Bopha"],
    "Course": ["Python", "Statistics", "Python", "Database", "Web App", "Database", "Python", "Statistics"],
    "Score": [85, 68, 45, 92, 58, 91, 72, 62],
    "Attendance": [90, 75, 50, 95, 60, 94, 80, 88],
    "Study Hours": [12, 8, 3, 15, 5, 14, 9, 7]
})

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
    st.subheader("Interactive Student Risk Monitoring Dashboard")
    st.write("Welcome to Lab 02.")
    st.write("In this lab, you will use Streamlit widgets to explore student performance data.")
    st.success("Lab 02 app is running successfully!")

# ============================================================
# PAGE 2: DASHBOARD
# filters -> metrics -> table -> charts
# ============================================================
elif selected_page == "Dashboard":
    st.title("Interactive Dashboard")

    st.write("Use the filters below to explore student performance.")

    # --- FILTER 1: COURSE (selectbox) ---
    selected_course = st.selectbox(
        "Select Course",
        ["All"] + list(student_df["Course"].unique())
    )

    # --- FILTER 2: RISK LEVEL (selectbox) ---
    selected_risk = st.selectbox(
        "Select Risk Level",
        ["All", "Low Risk", "Medium Risk", "High Risk"]
    )

    # --- FILTER 3: MINIMUM ATTENDANCE (slider) ---
    min_attendance = st.slider(
        "Minimum Attendance",
        0,
        100,
        0
    )

    # --- FILTER 4: MINIMUM SCORE (slider) ---
    min_score = st.slider(
        "Minimum Score",
        0,
        100,
        0
    )

    # --- APPLY ALL FOUR FILTERS ---
    # start from a copy so the original data is never changed
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    # --- CALCULATE METRIC VALUES ---
    total_students = len(filtered_df)

    # guard against division by zero when no student matches
    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    # --- METRICS IN 4 COLUMNS ---
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

    # --- FILTERED TABLE + CSV DOWNLOAD ---
    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Filtered Student Dataset")
        # DESIGN: color_risk() colours the Risk Level column
        st.dataframe(color_risk(filtered_df))

        # download exactly what is shown on screen
        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Filtered dataset is hidden.")

    # --- CHARTS (two side by side) ---
    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    # CHART 1: SCORE BAR CHART - one bar per student
    with chart_col1:
        st.write("Student Scores")

        if len(filtered_df) > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.warning("No data available for score chart.")

    # CHART 2: RISK BAR CHART - how many students per risk level
    with chart_col2:
        st.write("Risk Level Count")

        if len(filtered_df) > 0:
            risk_count = filtered_df["Risk Level"].value_counts()
            st.bar_chart(risk_count)
        else:
            st.warning("No data available for risk chart.")

# ============================================================
# PAGE 3: STUDENT DATA
# full dataset, no filters
# ============================================================
elif selected_page == "Student Data":
    st.title("Student Data")

    # --- CLASS SUMMARY VALUES ---
    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    # --- METRICS IN 4 COLUMNS ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk Students", high_risk_students)

    # --- FULL TABLE ---
    st.subheader("Full Student Dataset")
    # DESIGN: same risk colours as the dashboard table
    st.dataframe(color_risk(student_df))

# ============================================================
# PAGE 4: RISK CHECKER
# form -> check one student at a time
# ============================================================
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

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
    st.write("This app is part of Lab 02.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Streamlit Interactive Dashboard")
    st.info("Ethics Reminder: Risk prediction should support students, not punish them.")
