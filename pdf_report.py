from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet



def generate_report(
    filename,
    score,
    matching,
    missing,
    report
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    elements = []


    # Title
    elements.append(
        Paragraph(
            "ResumeMatch AI Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )


    # Score
    elements.append(
        Paragraph(
            f"<b>Resume Match Score:</b> {score}%",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )


    # Matching Skills
    elements.append(
        Paragraph(
            "<b>Matching Skills</b>",
            styles["Heading2"]
        )
    )

    for skill in matching:

        elements.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )


    elements.append(
        Spacer(1, 15)
    )


    # Missing Skills
    elements.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    for skill in missing:

        elements.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )


    elements.append(
        Spacer(1, 15)
    )


    # AI Report
    elements.append(
        Paragraph(
            "<b>AI Analysis</b>",
            styles["Heading2"]
        )
    )

    report = report.replace("\n", "<br/>")

    elements.append(
        Paragraph(
            report,
            styles["BodyText"]
        )
    )


    pdf.build(elements)