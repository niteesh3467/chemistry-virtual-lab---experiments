
import streamlit as st
from datetime import datetime

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Chemistry Virtual Lab",
    page_icon="🧪",
    layout="wide"
)

# --------------------------------
# SESSION DATA
# --------------------------------

if "agno3_n" not in st.session_state:
    st.session_state.agno3_n = 0.0141

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

# --------------------------------
# CUSTOM DESIGN
# --------------------------------

st.markdown("""
<style>
.main {
    background-color: #f4f7fb;
}
h1, h2, h3 {
    color: #174b78;
}
.stButton>button {
    background-color: #1769aa;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("🧪 Chemistry Virtual Lab")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Apparatus Setup",
        "Titration I - Standardization",
        "Titration II - Chloride Estimation",
        "Chemistry Quiz",
        "Experiment Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Virtual Chemistry Laboratory")

# --------------------------------
# HOME PAGE
# --------------------------------

if page == "Home":

    st.title("🧪 Chemistry Virtual Laboratory")

    st.subheader("Estimation of Chloride in Water")

    st.markdown("""
    Welcome to the interactive chemistry virtual laboratory.

    **Experiment:** Estimation of Chloride Content in Water
    using Mohr's Method.

    ### Objectives

    - Understand argentometric titration.
    - Learn the standardization of silver nitrate.
    - Estimate chloride concentration in water.
    - Understand chemical reactions and calculations.

    ### Experiment Overview

    1. Study the principle.
    2. Identify the apparatus.
    3. Standardize AgNO3 solution.
    4. Estimate chloride content.
    5. Calculate the final result.
    """)

    st.success("Welcome! Select an experiment from the sidebar.")

    st.image(
        "https://images.unsplash.com/photo-1532094349884-543bc11b234d",
        caption="Chemistry Laboratory",
        use_container_width=True
    )

# --------------------------------
# APPARATUS SETUP
# --------------------------------

elif page == "Apparatus Setup":

    st.title("Apparatus Setup")

    st.write("Select the apparatus used in this experiment.")

    apparatus = [
        "Burette",
        "Pipette",
        "Conical Flask",
        "Beaker",
        "Funnel",
        "Wash Bottle",
        "Measuring Cylinder"
    ]

    selected = []

    for item in apparatus:
        if st.checkbox(item):
            selected.append(item)

    st.markdown("---")

    if st.button("Check Apparatus"):

        required = [
            "Burette",
            "Pipette",
            "Conical Flask",
            "Beaker"
        ]

        missing = [
            item for item in required
            if item not in selected
        ]

        if not missing:
            st.success("Correct! All essential apparatus selected.")
        else:
            st.warning(
                "Missing apparatus: " + ", ".join(missing)
            )

# --------------------------------
# TITRATION I
# --------------------------------

elif page == "Titration I - Standardization":

    st.title("Titration I - Standardization of AgNO3")

    st.subheader("Principle")

    st.write("""
    Silver nitrate reacts with sodium chloride to form
    a white precipitate of silver chloride.

    AgNO3 + NaCl → AgCl + NaNO3

    Potassium chromate acts as the indicator.
    """)

    st.subheader("Enter Observation Values")

    nacl_n = st.number_input(
        "Normality of standard NaCl",
        min_value=0.0001,
        value=0.0141,
        format="%.5f"
    )

    nacl_volume = st.number_input(
        "Volume of NaCl (mL)",
        min_value=0.1,
        value=10.0
    )

    agno3_volume = st.number_input(
        "Titre value of AgNO3 (mL)",
        min_value=0.1,
        value=10.0,
        key="standard_titre"
    )

    if st.button("Calculate AgNO3 Normality"):

        normality = (
            nacl_n * nacl_volume
        ) / agno3_volume

        st.session_state.agno3_n = normality

        st.success(
            f"Standardized AgNO3 Normality: {normality:.5f} N"
        )

        st.info(
            "Formula: N1V1 = N2V2"
        )

    st.markdown("---")

    st.subheader("Virtual Endpoint Simulator")

    volume = st.slider(
        "Add AgNO3 (mL)",
        min_value=0.0,
        max_value=15.0,
        value=0.0,
        step=0.1,
        key="standard_sim"
    )

    if volume < agno3_volume:
        st.info("Continue adding AgNO3. Endpoint not reached.")
    else:
        st.success(
            "Endpoint reached! A permanent reddish-brown colour appears."
        )

 
# --------------------------------
# TITRATION II - ANIMATED SIMULATOR
# --------------------------------

elif page == "Titration II - Chloride Estimation":

    import time

    st.title("🧪 Advanced Chloride Titration Simulator")

    st.write(
        "Estimate chloride content using Mohr's method."
    )

    st.subheader("Experiment Setup")

    sample_volume = st.number_input(
        "Water sample volume (mL)",
        min_value=1.0,
        value=50.0
    )

    normality = st.number_input(
        "AgNO3 Normality",
        min_value=0.00001,
        value=float(st.session_state.agno3_n),
        format="%.5f"
    )

    endpoint_volume = st.number_input(
        "Expected endpoint volume (mL)",
        min_value=0.1,
        value=7.5
    )

    st.markdown("---")

    # SIMULATOR STATE

    if "added_volume" not in st.session_state:
        st.session_state.added_volume = 0.0

    if "titration_started" not in st.session_state:
        st.session_state.titration_started = False

    volume = st.session_state.added_volume

    progress = min(volume / endpoint_volume, 1.0)

    st.subheader("🔬 Virtual Laboratory")

    # BURETTE VISUAL

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Burette")

        st.markdown(
            f"""
            <div style="
            margin:auto;
            width:55px;
            height:240px;
            border:3px solid #555;
            border-radius:12px;
            position:relative;
            background:#f0f8ff;
            overflow:hidden;">

            <div style="
            position:absolute;
            bottom:0;
            width:100%;
            height:{max(0,100-progress*100)}%;
            background:linear-gradient(#64b5f6,#1565c0);">
            </div>

            </div>
            <p style="text-align:center;">
            AgNO3 Solution
            </p>
            """,
            unsafe_allow_html=True
        )

        st.metric("Volume Added", f"{volume:.2f} mL")

    with col2:

        st.markdown("### Conical Flask")

        if progress < 1:
            flask_color = "#eeeeee"
        else:
            flask_color = "#b85c42"

        st.markdown(
            f"""
            <div style="
            width:150px;
            height:170px;
            margin:auto;
            clip-path:polygon(25% 0%,75% 0%,100% 90%,90% 100%,10% 100%,0% 90%);
            background:{flask_color};
            border:3px solid #555;
            opacity:0.95;">
            </div>
            <p style="text-align:center;">
            Water Sample + Indicator
            </p>
            """,
            unsafe_allow_html=True
        )

    st.progress(progress)

    st.markdown("---")

    st.subheader("Control Panel")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("💧 Add 0.1 mL AgNO3", use_container_width=True):

            if volume < endpoint_volume:

                st.session_state.added_volume = round(
                    volume + 0.1, 2
                )

                st.session_state.titration_started = True

                st.rerun()

            else:
                st.warning("Endpoint already reached.")

    with col2:

        if st.button("🔄 Reset Experiment", use_container_width=True):

            st.session_state.added_volume = 0.0
            st.session_state.titration_started = False

            st.rerun()

    # ENDPOINT DETECTION

    if volume >= endpoint_volume:

        st.success(
            "🎉 Endpoint reached! "
            "Permanent reddish-brown colour observed."
        )

        chloride = (
            volume * normality * 35.45 * 1000
        ) / sample_volume

        st.metric(
            "Calculated Chloride Content",
            f"{chloride:.2f} mg/L"
        )

        st.session_state.chloride_result = chloride

    else:

        st.info(
            "Titration in progress. Continue adding AgNO3."
        )

    st.caption(
        "Educational simulation: endpoint volume is predefined. "
        "Use experimentally observed readings for actual calculations."
    )

# --------------------------------
# CHEMISTRY QUIZ
# --------------------------------

elif page == "Chemistry Quiz":

    st.title("Chemistry Knowledge Quiz")

    questions = [
        (
            "Which indicator is used in Mohr's method?",
            [
                "Phenolphthalein",
                "Potassium chromate",
                "Methyl orange",
                "Litmus"
            ],
            "Potassium chromate"
        ),
        (
            "What is the formula of silver nitrate?",
            [
                "AgCl",
                "NaCl",
                "AgNO3",
                "K2CrO4"
            ],
            "AgNO3"
        ),
        (
            "What is the colour of silver chloride precipitate?",
            [
                "White",
                "Blue",
                "Green",
                "Black"
            ],
            "White"
        ),
        (
            "Which method is used to estimate chloride?",
            [
                "Gravimetric",
                "Mohr's method",
                "Distillation",
                "Filtration"
            ],
            "Mohr's method"
        ),
        (
            "What is the endpoint colour in Mohr's method?",
            [
                "Blue",
                "Green",
                "Reddish-brown",
                "Colourless"
            ],
            "Reddish-brown"
        )
    ]

    answers = []

    for i, (question, options, correct) in enumerate(questions):

        st.subheader(f"Question {i+1}")

        answer = st.radio(
            question,
            options,
            key=f"quiz_{i}"
        )

        answers.append(answer)

    if st.button("Submit Quiz"):

        score = 0

        for i, (_, _, correct) in enumerate(questions):
            if answers[i] == correct:
                score += 1

        st.session_state.quiz_score = score

        st.success(
            f"Your Score: {score}/{len(questions)}"
        )

        if score == 5:
            st.balloons()
            st.success("Excellent work!")

        else:
            st.info("Review the experiment and try again.")

# --------------------------------
# EXPERIMENT REPORT
# --------------------------------

elif page == "Experiment Report":

    st.title("Experiment Report Generator")

    name = st.text_input("Student Name")

    registration = st.text_input(
        "Registration Number"
    )

    section = st.text_input("Section")

    st.markdown("---")

    st.subheader("Experiment Results")

    chloride = st.session_state.get(
        "chloride_result",
        None
    )

    if chloride is not None:
        st.write(
            f"Chloride Content: {chloride:.2f} mg/L"
        )
    else:
        st.warning(
            "Complete Titration II to calculate the result."
        )

    st.write(
        f"AgNO3 Normality: {st.session_state.agno3_n:.5f} N"
    )

    if st.button("Generate Report"):

        if not name or not registration:
            st.error("Enter your name and registration number.")

        elif chloride is None:
            st.error("Calculate chloride content first.")

        else:

            report = f"""
CHEMISTRY VIRTUAL LABORATORY
EXPERIMENT REPORT

Student Name: {name}
Registration Number: {registration}
Section: {section}

Experiment:
Estimation of Chloride Content in Water
using Mohr's Method.

AgNO3 Normality:
{st.session_state.agno3_n:.5f} N

Chloride Content:
{chloride:.2f} mg/L

Date:
{datetime.now().strftime("%d-%m-%Y")}

Result:
The chloride content of the given water
sample was calculated using Mohr's method.

End of Report.
"""

            st.download_button(
                "Download Experiment Report",
                data=report,
                file_name="Chemistry_Lab_Report.txt",
                mime="text/plain"
            )

            st.success("Your report is ready!")
