
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

    st.title("🧪 Titration I - AgNO3 Standardization")

    st.subheader("Principle")

    st.write("""
    Silver nitrate reacts with sodium chloride to form
    a white precipitate of silver chloride.

    AgNO3 + NaCl → AgCl + NaNO3

    Potassium chromate acts as the indicator.
    At the endpoint, a permanent reddish-brown colour appears.
    """)

    st.markdown("---")
    st.subheader("Experiment Setup")

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

    endpoint_volume = st.number_input(
        "Simulated endpoint volume (mL)",
        min_value=0.1,
        value=10.0
    )

    if "standard_added_volume" not in st.session_state:
        st.session_state.standard_added_volume = 0.0

    volume = st.session_state.standard_added_volume
    progress = min(volume / endpoint_volume, 1.0)

    st.markdown("---")
    st.subheader("🔬 Virtual Laboratory")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Burette")

        liquid_height = max(0, 100 - progress * 100)

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
                    height:{liquid_height}%;
                    background:linear-gradient(#64b5f6,#1565c0);">
                </div>
            </div>
            <p style="text-align:center;">AgNO3 Solution</p>
            """,
            unsafe_allow_html=True
        )

        st.metric("AgNO3 Added", f"{volume:.2f} mL")

    with col2:
        st.markdown("### Conical Flask")

        if progress >= 1:
            flask_color = "#b85c42"
        else:
            flask_color = "#eeeeee"

        st.markdown(
            f"""
            <div style="
                width:150px;
                height:170px;
                margin:auto;
                clip-path:polygon(
                    25% 0%,75% 0%,100% 90%,
                    90% 100%,10% 100%,0% 90%
                );
                background:{flask_color};
                border:3px solid #555;">
            </div>
            <p style="text-align:center;">
                NaCl + Potassium Chromate
            </p>
            """,
            unsafe_allow_html=True
        )

    st.progress(progress)

    st.markdown("---")
    st.subheader("Control Panel")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💧 Add 0.1 mL AgNO3",
                     use_container_width=True):

            if volume < endpoint_volume:
                st.session_state.standard_added_volume = round(
                    min(volume + 0.1, endpoint_volume), 2
                )
                st.rerun()
            else:
                st.warning("Endpoint already reached.")

    with col2:
        if st.button("🔄 Reset Experiment",
                     use_container_width=True):

            st.session_state.standard_added_volume = 0.0
            st.rerun()

    if volume >= endpoint_volume:

        st.success(
            "Endpoint reached! Permanent reddish-brown colour observed."
        )

        st.subheader("Calculation")

        if st.button("Calculate AgNO3 Normality"):

            agno3_normality = (
                nacl_n * nacl_volume
            ) / volume

            st.session_state.agno3_n = agno3_normality

            st.success(
                f"Standardized AgNO3 Normality: "
                f"{agno3_normality:.5f} N"
            )

            st.info("Formula: N1 × V1 = N2 × V2")

    else:
        st.info("Add AgNO3 gradually until the simulated endpoint.")

 
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
        st.session_state.sample_volume_used = sample_volume
        st.session_state.titre_volume_used = volume
        st.session_state.normality_used = normality

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
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    )

    st.title("Experiment Report")
    st.write("Generate and download your chloride estimation report.")

    name = st.text_input("Student Name")
    reg_no = st.text_input("Registration Number")
    section = st.text_input("Section")

    chloride = st.session_state.get("chloride_result")
    sample_volume = st.session_state.get("sample_volume_used", 10.0)
    titre_volume = st.session_state.get("titre_volume_used", 7.5)
    normality = st.session_state.get("normality_used", 0.1)

    if chloride is None:
        st.warning("Complete Titration II first to generate your result.")
    else:
        st.success(f"Chloride concentration: {chloride:.2f} mg/L")

    if st.button("Generate PDF Report"):
        if not name.strip() or not reg_no.strip() or not section.strip():
            st.error("Please enter your name, registration number, and section.")
        elif chloride is None:
            st.error("Please complete Titration II before generating the report.")
        else:
            buffer = BytesIO()

            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=2 * cm,
                leftMargin=2 * cm,
                topMargin=2 * cm,
                bottomMargin=2 * cm
            )

            styles = getSampleStyleSheet()
            story = []

            title_style = ParagraphStyle(
                "ReportTitle",
                parent=styles["Title"],
                textColor=colors.darkblue,
                alignment=1,
                spaceAfter=20
            )

            story.append(Paragraph("CHEMISTRY EXPERIMENT REPORT", title_style))
            story.append(Paragraph("<b>Experiment:</b> Estimation of Chloride", styles["Normal"]))
            story.append(Spacer(1, 15))

            story.append(Paragraph("<b>Student Details</b>", styles["Heading2"]))

            student_data = [
                ["Name", name],
                ["Registration Number", reg_no],
                ["Section", section],
            ]

            student_table = Table(student_data, colWidths=[5 * cm, 11 * cm])
            student_table.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]))
            story.append(student_table)
            story.append(Spacer(1, 15))

            sections = [
                ("Aim", "To estimate the chloride concentration in the given water sample using silver nitrate titration."),
                ("Principle", "Chloride ions react with silver ions to form a white precipitate of silver chloride. Potassium chromate is used as an indicator. At the endpoint, a reddish-brown colour appears."),
                ("Reaction", "Ag+ + Cl- → AgCl (white precipitate)"),
                ("Indicator reaction", "2Ag+ + CrO4 2- → Ag2CrO4 (reddish-brown precipitate)"),
            ]

            for heading, content in sections:
                story.append(Paragraph(heading, styles["Heading2"]))
                story.append(Paragraph(content, styles["BodyText"]))
                story.append(Spacer(1, 10))

            story.append(Paragraph("Observation Table", styles["Heading2"]))

            observation_data = [
                ["Parameter", "Value"],
                ["Sample volume", f"{sample_volume} mL"],
                ["AgNO3 normality", f"{normality} N"],
                ["Titre volume", f"{titre_volume} mL"],
            ]

            observation_table = Table(observation_data, colWidths=[8 * cm, 8 * cm])
            observation_table.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]))
            story.append(observation_table)
            story.append(Spacer(1, 15))

            story.append(Paragraph("Calculation", styles["Heading2"]))
            story.append(Paragraph(
                "Chloride concentration (mg/L) = "
                "(Titre volume × AgNO3 normality × 35.45 × 1000) "
                "/ Sample volume",
                styles["BodyText"]
            ))
            story.append(Spacer(1, 8))

            story.append(Paragraph("Result", styles["Heading2"]))
            story.append(Paragraph(
                f"The chloride concentration in the given sample is "
                f"<b>{chloride:.2f} mg/L</b>.",
                styles["BodyText"]
            ))

            story.append(Spacer(1, 25))
            story.append(Paragraph("End of Report", styles["Italic"]))

            doc.build(story)
            buffer.seek(0)

            st.download_button(
                label="Download PDF Report",
                data=buffer,
                file_name="Chloride_Estimation_Report.pdf",
                mime="application/pdf"
            )
 
