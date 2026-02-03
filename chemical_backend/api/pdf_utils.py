from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import tempfile
import os
import matplotlib
matplotlib.use("Agg")  



def _generate_type_distribution_chart(type_distribution):
    """Generate pie chart image and return file path"""
    labels = list(type_distribution.keys())
    values = list(type_distribution.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title("Equipment Type Distribution")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name, bbox_inches="tight")
    plt.close(fig)

    return temp_file.name


def _generate_average_chart(statistics):
    """Generate bar chart image and return file path"""
    labels = ["Flowrate", "Pressure", "Temperature"]
    values = [
        statistics["flowrate"]["avg"],
        statistics["pressure"]["avg"],
        statistics["temperature"]["avg"],
    ]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=["#22c55e", "#f97316", "#a855f7"])
    ax.set_title("Average Equipment Parameters")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name, bbox_inches="tight")
    plt.close(fig)

    return temp_file.name


def build_pdf_report(file_path, summary, user):
    """
    Build a complete PDF report with:
    - Project info
    - User info
    - Dataset summary
    - Tables
    - Charts
    """

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ===================== TITLE =====================
    elements.append(Paragraph(
        "<b>Chemical Equipment Parameter Visualizer</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "A comprehensive analytical report generated from uploaded "
        "chemical equipment data.",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    # ===================== USER INFO =====================
    elements.append(Paragraph("<b>User Information</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    user_table = Table([
        ["Username", user.username],
        ["Report Generated For", "Chemical Equipment Dataset"],
    ])
    user_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(user_table)
    elements.append(Spacer(1, 20))

    # ===================== DATASET SUMMARY =====================
    elements.append(Paragraph("<b>Dataset Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    summary_table = Table([
        ["Total Equipment Count", summary["total_count"]],
    ])
    summary_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # ===================== TYPE DISTRIBUTION =====================
    elements.append(Paragraph(
        "<b>Equipment Type Distribution</b>",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 8))

    dist_data = [["Equipment Type", "Count"]]
    for k, v in summary["type_distribution"].items():
        dist_data.append([k, v])

    dist_table = Table(dist_data)
    dist_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(dist_table)
    elements.append(Spacer(1, 20))

    # ===================== TYPE CHART =====================
    type_chart_path = _generate_type_distribution_chart(
        summary["type_distribution"]
    )
    elements.append(Image(type_chart_path, width=4*inch, height=4*inch))
    elements.append(Spacer(1, 20))

    # ===================== STATISTICS =====================
    elements.append(Paragraph(
        "<b>Statistical Analysis</b>",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 8))

    stats = summary["statistics"]

    stats_table = Table([
        ["Parameter", "Average", "Minimum", "Maximum"],
        ["Flowrate", stats["flowrate"]["avg"],
         stats["flowrate"]["min"], stats["flowrate"]["max"]],
        ["Pressure", stats["pressure"]["avg"],
         stats["pressure"]["min"], stats["pressure"]["max"]],
        ["Temperature", stats["temperature"]["avg"],
         stats["temperature"]["min"], stats["temperature"]["max"]],
    ])
    stats_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 20))

    # ===================== AVERAGE CHART =====================
    avg_chart_path = _generate_average_chart(stats)
    elements.append(Image(avg_chart_path, width=4*inch, height=3*inch))
    elements.append(Spacer(1, 30))

    # ===================== FOOTER =====================
    elements.append(Paragraph(
        "This report was automatically generated using the "
        "Chemical Equipment Parameter Visualizer system.",
        styles["Italic"]
    ))

    # ===================== BUILD PDF =====================
    doc.build(elements)

    # Cleanup temp files
    os.remove(type_chart_path)
    os.remove(avg_chart_path)
