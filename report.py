from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import os
from datetime import datetime

def generate_pdf_report(
    df: pd.DataFrame,
    actions: dict,
    summary: dict,
    plot_dir: str,
    output_file="Data_Analysis_Report.pdf"
):
    """
    Generates a PDF report containing:
    - Dataset preview
    - Cleaning actions
    - Numeric and categorical summary
    - Plots saved in plot_dir
    """
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("Data Analysis Report", styles['Title']))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Dataset preview
    elements.append(Paragraph("Dataset Preview (first 10 rows)", styles['Heading2']))
    preview_table = Table([df.columns.tolist()] + df.head(10).values.tolist())
    preview_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    elements.append(preview_table)
    elements.append(Spacer(1, 12))

    # Cleaning actions
    elements.append(Paragraph("Cleaning Actions", styles['Heading2']))
    action_data = [["Tool", "Column", "Strategy/Action"]]
    for act in actions.get("actions", []):
        tool = act.get("tool", "")
        col = act.get("column", "")
        strat = act.get("strategy", act.get("action", ""))
        action_data.append([tool, col, strat])
    action_table = Table(action_data)
    action_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    elements.append(action_table)
    elements.append(Spacer(1, 12))

    # Numeric summary
    elements.append(Paragraph("Numeric Summary", styles['Heading2']))
    for col, stats in summary.get("numeric", {}).items():
        elements.append(Paragraph(col, styles['Heading3']))
        stats_df = pd.DataFrame(stats, index=[0]).T.rename(columns={0: 'Value'})
        table = Table([stats_df.index.tolist()] + [stats_df['Value'].tolist()])
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 6))

    # Categorical summary
    elements.append(Paragraph("Categorical Summary", styles['Heading2']))
    for col, counts in summary.get("categorical", {}).items():
        elements.append(Paragraph(col, styles['Heading3']))
        counts_df = pd.DataFrame(list(counts.items()), columns=['Category', 'Count'])
        table = Table([counts_df.columns.tolist()] + counts_df.values.tolist())
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 6))

    # Plots
    elements.append(Paragraph("Plots", styles['Heading2']))
    if os.path.exists(plot_dir):
        for file in sorted(os.listdir(plot_dir)):
            if file.endswith(".png"):
                img_path = os.path.join(plot_dir, file)
                elements.append(Paragraph(file, styles['Heading3']))
                elements.append(Image(img_path, width=400, height=300))
                elements.append(Spacer(1, 12))

    # Build PDF
    doc.build(elements)
    print(f"✅ PDF report generated: {output_file}")
