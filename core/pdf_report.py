from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def save_testcases_pdf(testcases):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    file_path = "reports/testcases.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    for i, test in enumerate(testcases):

        # ✅ SAFE NAME
        name = test.get("test_name", f"Test Case {i+1}")

        content.append(Paragraph(f"<b>{name}</b>", styles["Heading2"]))
        content.append(Spacer(1, 10))

        for step in test.get("steps", []):
            content.append(Paragraph(str(step), styles["Normal"]))
            content.append(Spacer(1, 5))

        content.append(Spacer(1, 20))

    doc.build(content)

    return file_path

def save_execution_report(results):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import os

    if not os.path.exists("reports"):
        os.makedirs("reports")

    file_path = "reports/execution_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>Execution Report</b>", styles["Heading1"]))
    content.append(Spacer(1, 20))

    for i, result in enumerate(results):
        name = result.get("name", f"Test {i+1}")
        status = "PASSED" if result.get("status") else "FAILED"

        content.append(
            Paragraph(f"{name} - {status}", styles["Normal"])
        )
        content.append(Spacer(1, 10))

    doc.build(content)

    return file_path