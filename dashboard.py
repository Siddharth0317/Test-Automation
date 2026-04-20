import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from ai.testcase_generator import generate_testcases
from core.executor import execute_test
from core.storage import (
    save_testcases,
    load_testcases,
    save_test_run,
    load_history
)
from core.pdf_report import (
    save_testcases_pdf,
    save_execution_report
)

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI Testing Tool", layout="wide")

# -------- SESSION STATE --------
if "testcases" not in st.session_state:
    st.session_state.testcases = load_testcases()

if "user_story" not in st.session_state:
    st.session_state.user_story = ""

if "base_url" not in st.session_state:
    st.session_state.base_url = ""

# -------- SIDEBAR NAV --------
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "📜 Test History"]
)

# -------- SIDEBAR CONFIG --------
st.sidebar.markdown("### 🌐 Website Config")

base_url = st.sidebar.text_input(
    "Base URL",
    value=st.session_state.base_url
)

if st.sidebar.button("Save URL"):
    st.session_state.base_url = base_url
    st.success("URL Saved")

# ================= DASHBOARD =================
if page == "🏠 Dashboard":

    st.title("🤖 AI Test Automation Dashboard")

    # -------- STEP 1 --------
    st.header("Step 1: Enter User Story")

    user_story = st.text_area(
        "Describe your test scenario",
        value=st.session_state.user_story
    )

    if st.button("Save User Story"):
        st.session_state.user_story = user_story
        st.success("User story saved")

    # -------- STEP 2 --------
    if st.session_state.user_story:

        st.header("Step 2: Generate Test Cases")

        if st.button("Generate Test Cases"):
            with st.spinner("Generating..."):
                testcases = generate_testcases(st.session_state.user_story)
                st.session_state.testcases = testcases
                save_testcases(testcases)

                # Save PDF
                pdf_path = save_testcases_pdf(testcases)

                st.success("Test cases generated!")

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📄 Download Test Cases PDF",
                        f,
                        file_name="testcases.pdf"
                    )

    # -------- SHOW TESTS --------
    if st.session_state.testcases:

        st.subheader("Generated Test Cases")
        st.json(st.session_state.testcases)

        # -------- STEP 3 --------
        st.header("Step 3: Execute Tests")

        if st.button("Run Tests"):

            results = []
            progress = st.progress(0)

            for i, test in enumerate(st.session_state.testcases):

                st.write(f"Running: {test.get('test_name', 'Unnamed Test')}")

                try:
                    execute_test(test, st.session_state.base_url)
                    st.success("✅ Passed")

                    results.append({
                        "name": test.get('test_name', 'Unnamed Test'),
                        "status": True
                    })

                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")

                    results.append({
                        "name": test.get('test_name', 'Unnamed Test'),
                        "status": False
                    })

                progress.progress((i + 1) / len(st.session_state.testcases))

            # -------- SAVE HISTORY --------
            save_test_run(results)

            # -------- SAVE REPORT --------
            report_path = save_execution_report(results)

            with open(report_path, "rb") as f:
                st.download_button(
                    "📊 Download Execution Report",
                    f,
                    file_name="execution_report.pdf"
                )

    # -------- STEP 4 --------
    st.header("Step 4: Screenshots")

    if os.path.exists("reports"):
        files = os.listdir("reports")

        for file in files:
            if file.endswith(".png"):
                st.image(f"reports/{file}", caption=file)

# ================= HISTORY =================
elif page == "📜 Test History":

    st.title("📜 Test Execution History")

    history = load_history()

    if not history:
        st.info("No test history available")
    else:
        for run in reversed(history):

            st.subheader(f"Run at {run['timestamp']}")

            for result in run["results"]:
                if result["status"]:
                    st.success(f"{result['name']} - PASSED")
                else:
                    st.error(f"{result['name']} - FAILED")

            st.markdown("---")