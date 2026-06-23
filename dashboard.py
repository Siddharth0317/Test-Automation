import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from ai.testcase_generator import generate_testcases
from core.executor import execute_test
from core.storage import save_testcases, save_test_run, load_history
from core.pdf_report import save_testcases_pdf, save_execution_report

st.set_page_config(page_title="AI Testing Tool", layout="wide")

# -------- SESSION STATE --------
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

if "testcases" not in st.session_state:
    st.session_state.testcases = []

if "user_story" not in st.session_state:
    st.session_state.user_story = ""

if "base_url" not in st.session_state:
    st.session_state.base_url = ""

# -------- SIDEBAR --------
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "📜 Test History"]
)

# RESET
if st.sidebar.button("🔄 Reset"):
    st.session_state.current_step = 0
    st.session_state.testcases = []
    st.session_state.user_story = ""
    st.session_state.base_url = ""
    st.rerun()

# ================= DASHBOARD =================
if page == "🏠 Dashboard":

    st.title("🤖 AI Test Automation Dashboard")

    step = st.session_state.current_step
    st.progress((step + 1) / 4)
    st.write(f"Step {step + 1} of 4")

    # ================= STEP 0 =================
    if step == 0:
        st.header("🌐 Step 1: Enter Website URL")

        base_url = st.text_input(
            "Website URL",
            value=st.session_state.base_url,
            placeholder="https://example.com"
        )

        if st.button("Next →"):
            if base_url.startswith("http"):
                st.session_state.base_url = base_url
                st.session_state.current_step = 1
                st.rerun()
            else:
                st.error("Enter valid URL (must start with http/https)")

    # ================= STEP 1 =================
    elif step == 1:
        st.header("📝 Step 2: Enter User Story")

        user_story = st.text_area(
            "Describe your test scenario",
            value=st.session_state.user_story
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Back"):
                st.session_state.current_step = 0
                st.rerun()

        with col2:
            if st.button("Next →"):
                if user_story:
                    st.session_state.user_story = user_story
                    st.session_state.current_step = 2
                    st.rerun()
                else:
                    st.error("Please enter user story")

    # ================= STEP 2 =================
    elif step == 2:
        st.header("⚙️ Step 3: Generate Test Cases")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Back"):
                st.session_state.current_step = 1
                st.rerun()

        with col2:
            if st.button("Generate Test Cases"):
                with st.spinner("Generating..."):
                    testcases = generate_testcases(st.session_state.user_story)
                    st.session_state.testcases = testcases
                    save_testcases(testcases)

                    pdf_path = save_testcases_pdf(testcases)

                    st.success("Test cases generated!")

                    # ✅ FIXED DOWNLOAD
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📄 Download Test Cases PDF",
                            data=f.read(),
                            file_name="testcases.pdf",
                            mime="application/pdf"
                        )

        if st.session_state.testcases:
            st.subheader("Generated Test Cases")
            st.json(st.session_state.testcases)

            if st.button("Next →"):
                st.session_state.current_step = 3
                st.rerun()

    # ================= STEP 3 =================
    elif step == 3:
        st.header("🚀 Step 4: Execute Tests")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Back"):
                st.session_state.current_step = 2
                st.rerun()

        if st.button("Run Tests"):

            results = []
            progress = st.progress(0)

            for i, test in enumerate(st.session_state.testcases):

                name = test.get("test_name", "Unnamed Test")
                st.write(f"Running: {name}")

                try:
                    execute_test(test, st.session_state.base_url)
                    st.success("✅ Passed")
                    results.append({"name": name, "status": True})

                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")
                    results.append({"name": name, "status": False})

                progress.progress((i + 1) / len(st.session_state.testcases))

            save_test_run(results)

            report_path = save_execution_report(results)

            # ✅ FIXED DOWNLOAD
            with open(report_path, "rb") as f:
                st.download_button(
                    label="📊 Download Execution Report",
                    data=f.read(),
                    file_name="execution_report.pdf",
                    mime="application/pdf"
                )


# ================= HISTORY =================
else:
    st.title("📜 Test History")

    history = load_history()

    if not history:
        st.info("No history yet")
    else:
        for run in reversed(history):
            st.subheader(run["timestamp"])

            for r in run["results"]:
                if r["status"]:
                    st.success(f"{r['name']} - PASSED")
                else:
                    st.error(f"{r['name']} - FAILED")

            st.markdown("---")