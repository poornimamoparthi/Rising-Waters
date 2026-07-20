import os
import sys
import subprocess

def install_reportlab():
    try:
        import reportlab
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

def create_pdf_report():
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch

    pdf_dir = 'document'
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, 'Rising_Waters_Project_Report.pdf')
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'ChapterH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        alignment=0
    )

    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=0
    )
    
    center_bold = ParagraphStyle(
        'CenterBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#ffffff'),
        alignment=1
    )

    center_text = ParagraphStyle(
        'CenterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#334155'),
        alignment=1
    )

    story = []

    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("🌊 RISING WATERS", title_style))
    story.append(Paragraph("A Machine Learning Approach to Flood Prediction", subtitle_style))
    story.append(Spacer(1, 0.4 * inch))
    
    story.append(Paragraph("<b>A guided internship project report submitted for evaluation</b>", ParagraphStyle('ReportSub', parent=center_text, fontSize=11, spaceAfter=20)))
    story.append(Spacer(1, 0.8 * inch))
    
    meta_data = [
        [Paragraph("<b>Project Domain:</b>", meta_label_style), Paragraph("Artificial Intelligence & Machine Learning", meta_val_style)],
        [Paragraph("<b>Program:</b>", meta_label_style), Paragraph("SmartInternz Long-Term Internship Program", meta_val_style)],
        [Paragraph("<b>Evaluation Platform:</b>", meta_label_style), Paragraph("SkillWallet Dashboard", meta_val_style)],
        [Paragraph("<b>Team Leader:</b>", meta_label_style), Paragraph("Doppalapudi Mohana Raghavendra", meta_val_style)],
        [Paragraph("<b>Team Members:</b>", meta_label_style), Paragraph("Moparthi Poornima<br/>Kobbari Venkata Pravalika<br/>Kamatham Naga Malleswari", meta_val_style)],
        [Paragraph("<b>Date:</b>", meta_label_style), Paragraph("July 2026", meta_val_style)],
    ]
    
    t_meta = Table(meta_data, colWidths=[2.0 * inch, 4.0 * inch])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    story.append(t_meta)
    
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("<b>State Council of Higher Education (APSCHE)</b>", ParagraphStyle('CoverFoot1', parent=center_text, fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#0f172a'))))
    story.append(Paragraph("In collaboration with SmartBridge & IBM Cloud", ParagraphStyle('CoverFoot2', parent=center_text, fontSize=10, textColor=colors.HexColor('#64748b'))))
    
    story.append(PageBreak())

    story.append(Paragraph("1. Abstract & Introduction", h1_style))
    story.append(Paragraph(
        "Floods are among the most destructive natural disasters, causing severe losses to lives, "
        "agriculture, and infrastructure annually. This project, titled Rising Waters, addresses the challenge of "
        "early flood warnings by building an intelligent machine learning-powered classification pipeline. Utilizing "
        "meteorological inputs including rainfall patterns, humidity, temperature, visibility, and atmospheric pressure, "
        "multiple models are trained, compared, and deployed. The final best-performing classifier (XGBoost) achieves "
        "an accuracy score of 96.55% and is integrated into a dynamic, responsive Flask web application to support "
        "real-time evacuation and disaster preparedness decisions.",
        body_style
    ))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph(
        "Climate change has triggered irregular weather cycles, resulting in erratic, high-volume "
        "seasonal rainfall and severe flash floods. Conventional early warning models fail to parse non-linear environmental "
        "variables in a timely manner. To solve this, predictive machine learning models can process complex weather data "
        "instantly. This report documents the end-to-end implementation of the Rising Waters system, detailing dataset generation, "
        "robust preprocessing pipelines, multi-model evaluation, and the final web deployment.",
        body_style
    ))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("2. Data Pre-Processing Pipeline", h1_style))
    story.append(Paragraph(
        "Raw environmental data is frequently incomplete or subject to sensor noise. The pre-processing pipeline in "
        "this project guarantees model stability and high accuracy through the following sequential operations:",
        body_style
    ))
    
    story.append(Paragraph("<b>2.1 Handling Missing Values:</b>", h2_style))
    story.append(Paragraph(
        "Missing data in numerical features (such as temperature and visibility) are imputed using the column median to "
        "prevent feature bias. Any missing values in categorical fields are imputed using the mode.",
        body_style
    ))
    
    story.append(Paragraph("<b>2.2 Outlier Detection and Treatment:</b>", h2_style))
    story.append(Paragraph(
        "Extreme records caused by sensor malfunctions are detected using the Interquartile Range (IQR) method. Values falling "
        "beyond 1.5 IQR limits are capped at the lower and upper bounds. This preserves the dataset size "
        "while removing gradient distortions.",
        body_style
    ))
    
    story.append(Paragraph("<b>2.3 Categorical Encoding:</b>", h2_style))
    story.append(Paragraph(
        "The meteorological category Weather_Condition (consisting of values: Sunny, Cloudy, "
        "Overcast, Rainy) is encoded into binary variables using One-Hot Encoding. This expands the input dimensions "
        "from 7 numerical features to 11 independent inputs, enabling the models to learn sky-condition coefficients.",
        body_style
    ))
    
    story.append(Paragraph("<b>2.4 Feature Scaling and Splitting:</b>", h2_style))
    story.append(Paragraph(
        "To standardize gradient descents, features are scaled to zero-mean and unit-variance using the StandardScaler. "
        "The processed dataset (consisting of 1450 records) is divided into an 80% training set (1160 samples) and a 20% test set "
        "(290 samples), stratified by the target label to maintain uniform class distributions.",
        body_style
    ))

    story.append(PageBreak())

    story.append(Paragraph("3. Model Building & Evaluation", h1_style))
    story.append(Paragraph(
        "Four classification models are trained on the stratified training set and evaluated on the test set. "
        "A summary of the model evaluation results is presented below:",
        body_style
    ))
    story.append(Spacer(1, 0.1 * inch))
    
    table_data = [
        [Paragraph("<b>Model</b>", center_bold), Paragraph("<b>Test Accuracy</b>", center_bold), Paragraph("<b>Classification Characteristics</b>", center_bold)],
        [Paragraph("Decision Tree", center_text), Paragraph("95.86%", center_text), Paragraph("Learns hierarchical splits; fast but prone to overfitting.", center_text)],
        [Paragraph("Random Forest", center_text), Paragraph("96.90%", center_text), Paragraph("Bagging ensemble; highly resilient to variance.", center_text)],
        [Paragraph("K-Nearest Neighbors", center_text), Paragraph("93.79%", center_text), Paragraph("Distance-based; slow on large dimensions.", center_text)],
        [Paragraph("<b>XGBoost (Selected)</b>", center_text), Paragraph("<b>96.55%</b>", center_text), Paragraph("<b>Gradient boosted trees; optimal trade-off and calibration.</b>", center_text)],
    ]
    
    t_style = Table(table_data, colWidths=[1.8 * inch, 1.2 * inch, 4.0 * inch])
    t_style.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(t_style)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>XGBoost Confusion Matrix:</b>", h2_style))
    story.append(Paragraph(
        "On the 290 test samples, the production-selected XGBoost model demonstrates high precision and recall, "
        "making only 1 false-positive mistake:<br/>"
        "&bull; True Negatives (No Flood): 196 samples correctly predicted.<br/>"
        "&bull; False Positives (Type I Error): 1 sample incorrectly predicted as flood.<br/>"
        "&bull; False Negatives (Type II Error): 9 samples missed.<br/>"
        "&bull; True Positives (Flood Warning): 84 samples correctly predicted.",
        body_style
    ))

    story.append(Paragraph("4. Flask Application Architecture", h1_style))
    story.append(Paragraph(
        "The finalized XGBoost classifier and the fitted StandardScaler are serialized to floods.save. "
        "We built an interactive, responsive Flask-based web application to deploy this model for production, "
        "providing real-time predictions and flood threat metrics to users.",
        body_style
    ))
    
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("5. Conclusion & Recommendations", h1_style))
    story.append(Paragraph(
        "The Rising Waters system successfully combines advanced tree-boosting architectures (XGBoost) with "
        "user-friendly web dashboards (Flask) to deliver accurate, localized flood probability outputs. Achieving a "
        "test accuracy of 96.55%, the model is highly reliable for operational planning. We recommend integrating this "
        "API with telemetry sensor grids (measuring rainfall and pressure rates) to automate flood warnings directly to the public.",
        body_style
    ))
    
    doc.build(story)
    print(f"Project report PDF successfully generated at: {pdf_path}")

if __name__ == '__main__':
    install_reportlab()
    create_pdf_report()
