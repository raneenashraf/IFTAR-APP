import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import base64

FILE_NAME = "iftar_data.xlsx"

# 🌙 Page Config
st.set_page_config(
    page_title="FCDS IFTAR Registration ",
    page_icon="🌙",
    layout="wide"
)

# -----------------------
# SOFT FULL BACKGROUND
# -----------------------
def set_bg(image_file):
    import base64

    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
            position: relative;
            z-index: 1;
        }}

        header {{
            visibility: hidden;
        }}

        /* ===== BACKGROUND ===== */

        .background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: url("data:image/png;base64,{encoded}") no-repeat center center;
            background-size: cover;
            filter: blur(1.75px);
            transform: scale(1.05);
            z-index: -2;
        }}

        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(10, 20, 40, 0.35);
            z-index: -1;
        }}

        /* ===== TEXT ===== */

        * {{
            color: white !important;
        }}

        [data-testid="stMetricValue"] {{
            font-size: 20px !important;
        }}

        [data-testid="stMetricLabel"] {{
            font-size: 14px !important;
        }}

        /* ===== BUTTONS ===== */

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] > button {{
            background-color: #0f3460 !important;
            color: white !important;
            border: 1px solid white !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 6px 16px !important;
        }}

        .stButton > button:hover {{
            background-color: #16213e !important;
        }}

        /* ===== INPUTS ===== */

        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid white !important;
            color: white !important;
        }}

        /* ===== SELECTBOX MAIN BOX ===== */

        div[data-baseweb="select"] > div {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid white !important;
            color: white !important;
        }}

        /* ===== DROPDOWN LIST ===== */

        ul[role="listbox"] {{
            background-color: #0f3460 !important;
        }}

        li[role="option"] {{
            background-color: #0f3460 !important;
            color: white !important;
        }}

        li[role="option"]:hover {{
            background-color: #16213e !important;
        }}

        /* ===== RADIO BUTTON ===== */

        div[role="radiogroup"] label {{
            color: white !important;
            font-weight: bold;
        }}

        /* ===== CHECKBOX ===== */

        input[type="checkbox"] {{
            accent-color: white !important;
        }}

        div[data-testid="stCheckbox"] label {{
            color: white !important;
            font-weight: bold;
        }}

        /* إزالة أي outline أبيض مزعج */
        *:focus {{
            box-shadow: none !important;
            outline: none !important;
        }}

        </style>

        <div class="background"></div>
        <div class="overlay"></div>
        """,
        unsafe_allow_html=True
    )
set_bg("background.jpg")

st.title("🌙 Iftar Registration System")

# -----------------------
# LOAD DATA
# -----------------------
# -----------------------
# LOAD DATA (SAFE VERSION)
# -----------------------
if os.path.exists(FILE_NAME):
    try:
        df_existing = pd.read_excel(FILE_NAME, engine="openpyxl")
        
        # إجبار الأعمدة النصية تكون String
        df_existing["Level"] = df_existing["Level"].astype(str)
        df_existing["Department"] = df_existing["Department"].astype(str)
        df_existing["Meal"] = df_existing["Meal"].astype(str)
        df_existing["Juice"] = df_existing["Juice"].astype(str)

        last_ticket = df_existing["Ticket Number"].max()
    except:
        os.remove(FILE_NAME)
        df_existing = pd.DataFrame()
        last_ticket = 0
else:
    df_existing = pd.DataFrame()
    last_ticket = 0
# -----------------------
# FORM
# -----------------------
with st.form("registration_form"):

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Student Name")
        student_id = st.text_input("Student ID")
        department = st.selectbox(
            "Department",
            ["Data Science", "AI", "Cyber", "Healthcare",
             "Business", "Media", "Graduate", "Else"]
        )

    with col2:
        level = st.selectbox(
            "Level",
            ["One", "Two", "Three", "Four",
             "Graduate", "Doctor", "TA", "Volunteer or Ithad"]
        )
        meal = st.selectbox(
            "Meal",
            ["Meal 1", "Meal 2", "Meal 3", "Without Meal"]
        )
        juice = st.selectbox(
            "Juice",
            ["Sobya", "Kharoub", "3enab", "Tamr Hendi", "Without"]
        )

    submitted = st.form_submit_button("Submit")

# -----------------------
# AFTER SUBMIT
# -----------------------
if submitted:

    if name == "" or student_id == "":
        st.error("Please fill all required fields")
    else:
        new_ticket = last_ticket + 1
        total_price = 110 if meal == "Without Meal" else 300

        new_data = pd.DataFrame({
            "Ticket Number": [new_ticket],
            "Name": [name],
            "Student ID": [student_id],
            "Department": [department],
            "Level": [level],
            "Meal": [meal],
            "Juice": [juice],
            "Total Price": [total_price],
            "Timestamp": [datetime.now()]
        })

        updated = pd.concat([df_existing, new_data], ignore_index=True)
        updated.to_excel(FILE_NAME, index=False)

        st.success("✅ Registration Successful!")
        st.markdown(f"## 🎟 Ticket Number: {new_ticket}")
        st.markdown(f"### 💰 Total Amount: {total_price} EGP")

# -----------------------
# DASHBOARD
# -----------------------
if os.path.exists(FILE_NAME):

    df = pd.read_excel(FILE_NAME, engine="openpyxl")

    df["Level"] = df["Level"].astype(str)
    df["Department"] = df["Department"].astype(str)
    df["Meal"] = df["Meal"].astype(str)
    df["Juice"] = df["Juice"].astype(str)

    st.divider()

    with st.expander("📊 Show Dashboard Analysis", expanded=False):

        # ===== Metrics =====
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Registrations", len(df))
        col2.metric("Total Revenue", f"{df['Total Price'].sum()} EGP")
        col3.metric("Without Meal Count", (df["Meal"] == "Without Meal").sum())

        st.divider()

        # ===== Charts Row =====
        chart1, chart2, chart3 = st.columns(3)

        # 🍽 Meal Pie
        with chart1:
            st.markdown("### 🍽 Meals")
            meal_counts = df["Meal"].value_counts()

            fig_meal, ax_meal = plt.subplots(figsize=(3,3))
            wedges, texts, autotexts = ax_meal.pie(
                meal_counts.values,
                labels=meal_counts.index,
                autopct='%1.1f%%',
                textprops={'fontsize':8}
            )

            for t in texts:
                t.set_color("white")
            for t in autotexts:
                t.set_color("white")

            fig_meal.patch.set_alpha(0)
            ax_meal.set_facecolor("none")
            st.pyplot(fig_meal)

        # 🥤 Juice Bar
        with chart2:
            st.markdown("### 🥤 Juices")
            juice_counts = df["Juice"].value_counts()

            fig_juice, ax_juice = plt.subplots(figsize=(3,2.5))
            ax_juice.bar(juice_counts.index, juice_counts.values)

            ax_juice.tick_params(axis='x', rotation=45, labelsize=8, colors='white')
            ax_juice.tick_params(axis='y', labelsize=8, colors='white')

            for spine in ax_juice.spines.values():
                spine.set_color('white')

            fig_juice.patch.set_alpha(0)
            ax_juice.set_facecolor("none")

            st.pyplot(fig_juice)

        # 💰 Revenue Bar
        with chart3:
            st.markdown("### 💰 Revenue")
            revenue_dept = df.groupby("Department")["Total Price"].sum()

            fig_rev, ax_rev = plt.subplots(figsize=(3,2.5))
            ax_rev.bar(revenue_dept.index, revenue_dept.values)

            ax_rev.tick_params(axis='x', rotation=45, labelsize=8, colors='white')
            ax_rev.tick_params(axis='y', labelsize=8, colors='white')

            for spine in ax_rev.spines.values():
                spine.set_color('white')

            fig_rev.patch.set_alpha(0)
            ax_rev.set_facecolor("none")

            st.pyplot(fig_rev)

        # ===== Detailed Counts =====
        detail_col1, detail_col2 = st.columns(2)

        # 🍽 Detailed Meal Count
        with detail_col1:
            st.markdown("### 🍽 Detailed Meal Count")
            meal_counts = df["Meal"].value_counts()
            st.dataframe(
                meal_counts.rename("Count"),
                width="stretch"
            )

        # 🥤 Detailed Juice Count
        with detail_col2:
            st.markdown("### 🥤 Detailed Juice Count")
            juice_counts = df["Juice"].value_counts()
            st.dataframe(
                juice_counts.rename("Count"),
                width="stretch"
            )

        st.divider()

        # Table
        st.dataframe(df)

    # ===== Buttons Row =====
    btn1, btn2, btn3 = st.columns(3)

    with btn1:
        if st.button("🗑 Clear Last Record"):
            df = df.iloc[:-1]
            df.to_excel(FILE_NAME, index=False)
            st.rerun()

    with btn2:
        if st.button("❌ Clear All Data"):
            os.remove(FILE_NAME)
            st.rerun()

    with btn3:
        with open(FILE_NAME, "rb") as file:
            st.download_button(
                label="⬇ Download Excel",
                data=file,
                file_name="iftar_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )