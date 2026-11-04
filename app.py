
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
# TITRATION II
# --------------------------------

elif page == "Titration II - Chloride Estimation":

    st.title("Titration II - Estimation of Chloride")

    st.subheader("Principle")

    st.write("""
    Chloride ions react with silver ions to form
    silver chloride precipitate.

    Ag+ + Cl- → AgCl

    At the endpoint, excess silver ions react with
    chromate indicator to produce reddish-brown
    silver chromate.
    """)

    st.subheader("Observation Values")

    sample_volume = st.number_input(
        "Water sample volume (mL)",
        min_value=1.0,
        value=50.0
    )

    titre = st.number_input(
        "AgNO3 titre value (mL)",
        min_value=0.0,
        value=7.5
    )

    blank = st.number_input(
        "Blank titre value (mL)",
        min_value=0.0,
        value=0.0
    )

    normality = st.number_input(
        "Standardized AgNO3 Normality",
        min_value=0.00001,
        value=float(st.session_state.agno3_n),
        format="%.5f"
    )

    if st.button("Calculate Chloride Content"):

        corrected_titre = titre - blank

        if corrected_titre < 0:
            st.error("Titre value cannot be less than blank value.")

        else:
            chloride = (
                corrected_titre
                * normality
                * 35.45
                * 1000
            ) / sample_volume

            st.session_state.chloride_result = chloride

            st.success(
                f"Chloride Content = {chloride:.2f} mg/L"
            )

            st.write("Calculation formula:")

            st.latex(
                r"Cl^- (mg/L) = "
                r"\frac{(A-B)\times N\times 35.45\times 1000}"
                r"{V}"
            )

    st.markdown("---")

    st.subheader("Virtual Titration Simulator")

    added = st.slider(
        "Volume of AgNO3 added (mL)",
        min_value=0.0,
        max_value=15.0,
        value=0.0,
        step=0.1,
        key="chloride_sim"
    )

    if added < titre:
        st.info("Titration in progress...")

    else:
        st.success("Endpoint reached! Reddish-brown colour observed.")

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
