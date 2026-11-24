"""
Full College Project Documentation Generator for AI Plant Disease Detection
Generates:
  - AI_Plant_Disease_Detection_Project_Documentation.docx
  - AI_Plant_Disease_Detection_Project_Documentation.pdf
Targeting ~110-150 pages with rich academic content, complete 38-class profiles,
diagrams, charts, screenshots, test tables, and code snippets.
"""

import os
import sys
import json
import time
from pathlib import Path

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from doc_helpers import (
    set_cell_background, set_cell_margins, add_callout_box,
    add_code_block, add_figure, add_table_with_style,
    add_heading_1, add_heading_2, add_heading_3, add_para, add_bullet
)

BASE_DIR = Path.cwd()
ASSETS_DIR = BASE_DIR / "documentation_assets"
DIAGRAMS_DIR = ASSETS_DIR / "diagrams"
CHARTS_DIR = ASSETS_DIR / "charts"
SCREENSHOTS_DIR = ASSETS_DIR / "screenshots"
MODEL_DIR = BASE_DIR / "detector" / "ai" / "model"
METADATA_DIR = BASE_DIR / "datasets" / "metadata"

DOCX_OUT = BASE_DIR / "AI_Plant_Disease_Detection_Project_Documentation.docx"
PDF_OUT = BASE_DIR / "AI_Plant_Disease_Detection_Project_Documentation.pdf"

# Load metadata
with open(MODEL_DIR / "evaluation_summary.json", "r", encoding="utf-8") as f:
    eval_summary = json.load(f)

with open(MODEL_DIR / "classification_report.json", "r", encoding="utf-8") as f:
    class_report = json.load(f)

with open(MODEL_DIR / "confidence_analysis.json", "r", encoding="utf-8") as f:
    conf_analysis = json.load(f)

with open(MODEL_DIR / "training_metadata.json", "r", encoding="utf-8") as f:
    train_metadata = json.load(f)

with open(METADATA_DIR / "class_names.json", "r", encoding="utf-8") as f:
    class_names = json.load(f)

sys.path.insert(0, str(BASE_DIR))
from detector.ai.disease_info import DISEASE_KNOWLEDGE_BASE


def create_document():
    print("[*] Initializing Word Document...")
    doc = docx.Document()
    
    # Configure A4 Page Setup and Margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.2)   # Binding margin
        section.right_margin = Inches(1.0)
        
        # Configure Header & Footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.text = "AI Plant Disease Detection — Final Project Report"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.runs[0].font.name = 'Arial'
        p_hdr.runs[0].font.size = Pt(8.5)
        p_hdr.runs[0].font.color.rgb = RGBColor(120, 120, 120)
        
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.text = "Department of Computer Science & Engineering | Academic Project Documentation"
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ftr.runs[0].font.name = 'Arial'
        p_ftr.runs[0].font.size = Pt(8.5)
        p_ftr.runs[0].font.color.rgb = RGBColor(120, 120, 120)

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    print("[1] Building Cover Page...")
    p_cov_top = doc.add_paragraph()
    p_cov_top.paragraph_format.space_before = Pt(36)
    p_cov_top.paragraph_format.space_after = Pt(12)
    p_cov_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r = p_cov_top.add_run("A PROJECT REPORT ON\n")
    r.font.name = 'Arial'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(70, 80, 95)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(18)
    r_title = p_title.add_run("AI PLANT DISEASE DETECTION\nAND AGRICULTURAL ADVISORY SYSTEM")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(27, 38, 59)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run("An Automated Deep Learning Web Platform Utilizing MobileNetV2 Transfer Learning, 70% Decision Thresholding, and a 38-Class Agronomic Knowledge Base")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)
    
    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_after = Pt(30)
    r_subm = p_subm.add_run("Submitted in partial fulfillment of the requirements for the award of the degree of\n")
    r_subm.font.name = 'Times New Roman'
    r_subm.font.size = Pt(11.5)
    r_deg = p_subm.add_run("BACHELOR OF TECHNOLOGY / MASTER OF COMPUTER APPLICATIONS\nIN\nCOMPUTER SCIENCE AND ENGINEERING")
    r_deg.font.name = 'Arial'
    r_deg.font.size = Pt(12)
    r_deg.font.bold = True
    r_deg.font.color.rgb = RGBColor(44, 62, 80)
    
    # Author & Guide Table
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(20)
    p_meta.paragraph_format.space_after = Pt(20)
    
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    c00 = meta_table.cell(0, 0)
    c00.width = Inches(3.2)
    p00 = c00.paragraphs[0]
    p00.add_run("SUBMITTED BY:\n").bold = True
    p00.add_run("[STUDENT NAME]\nRegister No: [REGISTER NUMBER]\n[DEPARTMENT NAME]")
    for run in p00.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        
    c01 = meta_table.cell(0, 1)
    c01.width = Inches(3.2)
    p01 = c01.paragraphs[0]
    p01.add_run("UNDER THE GUIDANCE OF:\n").bold = True
    p01.add_run("[GUIDE NAME]\n[DESIGNATION / DEPARTMENT]\n[COLLEGE NAME]")
    for run in p01.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        
    c10 = meta_table.cell(1, 0)
    c10.width = Inches(3.2)
    c11 = meta_table.cell(1, 1)
    c11.width = Inches(3.2)
    
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(40)
    p_inst.paragraph_format.space_after = Pt(0)
    r_inst = p_inst.add_run("[DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING]\n[COLLEGE NAME]\n[UNIVERSITY / INSTITUTION]\nACADEMIC YEAR: [ACADEMIC YEAR]")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(27, 38, 59)
    
    doc.add_page_break()

    # =========================================================================
    # 2. FRONT MATTER
    # =========================================================================
    print("[2] Building Front Matter (Certificate, Declaration, Acknowledgement, Abstract, Lists)...")
    
    # Certificate
    add_heading_1(doc, "CERTIFICATE OF APPROVAL")
    add_para(doc, "This is to certify that the project report entitled 'AI PLANT DISEASE DETECTION' is a bona fide record of work carried out by [STUDENT NAME] (Register No: [REGISTER NUMBER]) in partial fulfillment of the requirements for the award of the degree in Computer Science and Engineering from [COLLEGE NAME], affiliated to [UNIVERSITY / INSTITUTION] during the academic year [ACADEMIC YEAR].")
    add_para(doc, "The project work presented in this report has been carried out under our supervision and guidance, and to the best of our knowledge, has not been submitted elsewhere for the award of any other degree or diploma.")
    
    doc.add_paragraph().paragraph_format.space_before = Pt(60)
    cert_table = doc.add_table(rows=1, cols=2)
    cert_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cert_table.rows[0].cells[0].width = Inches(3.2)
    cert_table.rows[0].cells[1].width = Inches(3.2)
    
    p_g = cert_table.rows[0].cells[0].paragraphs[0]
    p_g.add_run("_________________________\n[GUIDE NAME]\nProject Guide\n[DEPARTMENT NAME]").bold = True
    p_h = cert_table.rows[0].cells[1].paragraphs[0]
    p_h.add_run("_________________________\n[HEAD OF DEPARTMENT]\nProfessor & Head\n[DEPARTMENT NAME]").bold = True
    
    doc.add_page_break()

    # Declaration
    add_heading_1(doc, "DECLARATION")
    add_para(doc, "I, [STUDENT NAME], student of [DEPARTMENT NAME], [COLLEGE NAME], hereby declare that the project work entitled 'AI PLANT DISEASE DETECTION' submitted to [UNIVERSITY / INSTITUTION] is my original work and that the analysis, design, implementation, and evaluation presented in this report are based on genuine project development and empirical testing.")
    add_para(doc, "I further declare that this report has not been submitted previously to any university, institute, or examining body for the award of any degree, diploma, associate-ship, or other similar titles.")
    
    doc.add_paragraph().paragraph_format.space_before = Pt(60)
    p_dec = doc.add_paragraph()
    p_dec.paragraph_format.space_before = Pt(30)
    p_dec.add_run("Place: [CITY / LOCATION]\nDate: [SUBMISSION DATE]\n\n\n_________________________\n[STUDENT NAME]\nRegister No: [REGISTER NUMBER]").bold = True

    doc.add_page_break()

    # Acknowledgement
    add_heading_1(doc, "ACKNOWLEDGEMENT")
    add_para(doc, "The successful realization of this project requires guidance, encouragement, and technical support from numerous individuals, and I express my sincere gratitude to all who contributed to the fruition of this project.")
    add_para(doc, "First and foremost, I express my deep sense of gratitude and indebtedness to my project guide, [GUIDE NAME], [DESIGNATION], for providing invaluable guidance, constructive criticism, and continuous encouragement throughout every phase of dataset preparation, neural network training, web development, and system evaluation.")
    add_para(doc, "I extend my heartfelt thanks to [HEAD OF DEPARTMENT], Head of the Department of [DEPARTMENT NAME], for providing essential departmental facilities, computing laboratories, and an inspiring academic atmosphere.")
    add_para(doc, "I am profoundly thankful to [PRINCIPAL NAME], Principal, [COLLEGE NAME], for providing the necessary infrastructure, high-performance computing resources, and institutional encouragement.")
    add_para(doc, "I also express my sincere appreciation to all faculty members, technical laboratory staff, and colleagues of the Department of Computer Science and Engineering for their direct and indirect support. Lastly, I am deeply indebted to my family and friends for their constant patience, motivation, and moral support throughout this academic endeavor.")

    doc.add_page_break()

    # Abstract
    add_heading_1(doc, "ABSTRACT")
    add_para(doc, "Plant diseases present a catastrophic threat to global food security, agricultural productivity, and the economic livelihood of millions of farmers worldwide. Traditional manual inspection of foliar pathologies requires extensive domain expertise, is time-consuming, subjective, and highly prone to misdiagnosis in field conditions where agricultural extension specialists are unavailable. This project presents the design, empirical development, and full-stack integration of AI Plant Disease Detection—an automated, high-precision computer vision and deep learning web platform built to classify crop leaf diseases from photographs and deliver actionable agronomic advice.")
    add_para(doc, "The machine learning core utilizes MobileNetV2 architecture pretrained on ImageNet and fine-tuned via transfer learning across 20,922 curated leaf images spanning 38 distinct crop-disease and healthy classes (covering apple, blueberry, cherry, corn, grape, orange, peach, bell pepper, potato, raspberry, soybean, squash, strawberry, and tomato). The dataset was strictly partitioned into a 70% training set (14,643 images), a 15% validation set (3,134 images), and an unseen 15% testing set (3,145 images) with zero partition leakage.")
    add_para(doc, "Rigorous empirical evaluation on the 3,145 test images demonstrated a Test Accuracy of 95.33% and a Test Loss of 0.1602, achieving a Macro Precision of 95.78%, Macro Recall of 95.30%, and Macro F1-Score of 95.39%. To safeguard agricultural decision-making against overconfident incorrect predictions and out-of-distribution non-plant inputs, the system enforces a strict 70% Confidence Threshold. Diagnostic outputs with confidence $\\ge$ 70% display the predicted disease, top-3 ranked candidate probabilities, visual confidence meter, and comprehensive agronomic profiles detailing biological symptoms, possible etiology, preventive measures, and non-hazardous management guidance. Conversely, predictions falling below 70% trigger an uncertainty warning advisory guiding the user to provide clearer photographs.")
    add_para(doc, "The entire pipeline is deployed inside a production-ready Django 4.2 web application featuring client-side drag-and-drop file ingestion, server-side MIME and Pillow validation, sub-100ms singleton CPU inference caching, responsive HTML5/CSS3/JavaScript interfaces, user authentication, and isolated historical diagnostic record keeping. The system bridges state-of-the-art deep learning research with accessible agricultural tools for farmers, students, and agronomists.")
    
    add_callout_box(doc, "KEY PROJECT METRICS SUMMARY", 
                    "• Neural Network Model: MobileNetV2 (Transfer Learning from Layer 100+)\n"
                    "• Number of Supported Classes: 38 Crop-Disease & Healthy Categories\n"
                    "• Overall Test Accuracy: 95.33% | Test Loss: 0.1602\n"
                    "• Macro Precision / Recall / F1: 95.78% / 95.30% / 95.39%\n"
                    "• Total Partitioned Dataset: 20,922 Images (14,643 Train / 3,134 Val / 3,145 Test)\n"
                    "• Safety Threshold: 70% Confidence Guardrail with Uncertainty Fallback\n"
                    "• Web Architecture: Python 3.11, Django 4.2, SQLite3, Pillow, Vanilla UI", box_type='note')

    doc.add_page_break()

    # Table of Contents
    add_heading_1(doc, "TABLE OF CONTENTS")
    toc_items = [
        ("Front Matter (Certificate, Declaration, Acknowledgement, Abstract)", "i - vi"),
        ("List of Figures & List of Tables", "vii - ix"),
        ("List of Abbreviations", "x"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("  1.1 Background and Agricultural Context", "1"),
        ("  1.2 Introduction to Plant Diseases and Foliar Pathologies", "3"),
        ("  1.3 Importance of Early and Accurate Detection", "5"),
        ("  1.4 Role of Artificial Intelligence in Precision Agriculture", "7"),
        ("  1.5 Computer Vision in Automated Crop Diagnosis", "9"),
        ("  1.6 Problem Statement", "11"),
        ("  1.7 Motivation", "13"),
        ("  1.8 Aim of the Project", "15"),
        ("  1.9 Primary and Secondary Objectives", "16"),
        ("  1.10 Scope and Technical Boundaries", "18"),
        ("  1.11 Significance to Smallholder and Commercial Agriculture", "20"),
        ("  1.12 Expected Outcomes and Deliverables", "22"),
        ("  1.13 Inherent Constraints and Limitations", "24"),
        ("  1.14 Organization and Structure of the Report", "26"),
        ("CHAPTER 2: EXISTING SYSTEM AND PROPOSED SYSTEM", "28"),
        ("  2.1 Overview of Existing Agricultural Diagnostic Systems", "28"),
        ("  2.2 Manual and Traditional Field Inspection Methods", "29"),
        ("  2.3 Limitations and Bottlenecks of Manual Diagnosis", "31"),
        ("  2.4 Survey of Prior Image Classification Approaches", "33"),
        ("  2.5 Limitations of Traditional Machine Learning Pipelines", "35"),
        ("  2.6 Proposed AI Plant Disease Detection Platform", "37"),
        ("  2.7 Architectural Advantages of the Proposed System", "39"),
        ("  2.8 Comprehensive Feature Comparison Matrix", "41"),
        ("  2.9 System Scope and Operational Context", "43"),
        ("CHAPTER 3: LITERATURE SURVEY", "45"),
        ("  3.1 Historical Evolution of Computer Vision in Agriculture", "45"),
        ("  3.2 Deep Convolutional Neural Networks for Foliar Analysis", "47"),
        ("  3.3 Transfer Learning Methodologies and Pretrained Backbones", "50"),
        ("  3.4 Architecture Analysis of MobileNet and MobileNetV2", "53"),
        ("  3.5 Image Preprocessing, Augmentation, and Normalization Techniques", "56"),
        ("  3.6 Review of Benchmark Agricultural Datasets (PlantVillage & Mendeley)", "58"),
        ("  3.7 Softmax Probability Calibration and Decision Guardrails", "61"),
        ("  3.8 Summary of Literature Gaps and Research Opportunity", "63"),
        ("CHAPTER 4: SYSTEM REQUIREMENTS AND FEASIBILITY ANALYSIS", "65"),
        ("  4.1 Functional Requirements Specification", "65"),
        ("  4.2 Non-Functional Requirements Specification", "67"),
        ("  4.3 End-User Persona and Interface Requirements", "69"),
        ("  4.4 Hardware Requirements (Development, Training, and Hosting)", "71"),
        ("  4.5 Software and Framework Requirements", "73"),
        ("  4.6 Multidimensional Feasibility Study", "75"),
        ("  4.7 Technical Feasibility", "76"),
        ("  4.8 Economic Feasibility", "77"),
        ("  4.9 Operational and Field Feasibility", "78"),
        ("  4.10 System Security and Data Integrity Requirements", "79"),
        ("  4.11 Performance, Latency, and Scalability Requirements", "81"),
        ("CHAPTER 5: SYSTEM ARCHITECTURE AND DETAILED DESIGN", "83"),
        ("  5.1 High-Level System Architecture (Three-Tier Topology)", "83"),
        ("  5.2 Data Flow Diagram (DFD) — Level 0 Context Model", "86"),
        ("  5.3 Data Flow Diagram (DFD) — Level 1 Process Model", "88"),
        ("  5.4 End-to-End System Operational Workflow", "90"),
        ("  5.5 AI Inference and Classification Pipeline", "92"),
        ("  5.6 UML Use Case Diagram and Actor Specifications", "95"),
        ("  5.7 UML Activity Diagram (Diagnostic Processing Flow)", "98"),
        ("  5.8 UML Sequence Diagram (Client-Server-AI Message Exchanges)", "100"),
        ("  5.9 UML Component Diagram (Subsystem Modularity)", "102"),
        ("  5.10 UML Deployment Diagram (Physical Infrastructure)", "104"),
        ("  5.11 Relational Database Entity-Relationship (ER) Schema", "106"),
        ("CHAPTER 6: DATASET ACQUISITION AND PREPARATION", "108"),
        ("  6.1 Dataset Composition and Botanical Variety", "108"),
        ("  6.2 Primary Image Sources and Multi-Source Consolidation", "110"),
        ("  6.3 Directory Hierarchies and Metadata Normalization", "112"),
        ("  6.4 Image Formats, Color Channels, and Resolution Handling", "114"),
        ("  6.5 Automated Data Cleansing and Corruption Filtering", "116"),
        ("  6.6 Integrity Verification and Deduplication Analysis", "118"),
        ("  6.7 Taxonomic Standardized Class Label Mapping (0 to 37)", "120"),
        ("  6.8 Multi-Dataset Consolidation Strategy", "122"),
        ("  6.9 Stratified Train/Validation/Test Partitioning (70/15/15)", "124"),
        ("  6.10 Data Leakage Prevention and Verification Audits", "126"),
        ("  6.11 Class Distribution Statistics Across Partitions", "128"),
        ("  6.12 Comprehensive 38-Class Dataset Master Table", "130"),
        ("CHAPTER 7: AI MODEL ARCHITECTURE AND TRAINING", "134"),
        ("  7.1 Fundamentals of Deep Learning and CNNs", "134"),
        ("  7.2 Mathematical Formulation of Transfer Learning", "136"),
        ("  7.3 MobileNetV2 Neural Network Topology", "138"),
        ("  7.4 Inverted Residual Blocks and Linear Bottlenecks", "140"),
        ("  7.5 ImageNet Feature Reuse and Representation Transfer", "143"),
        ("  7.6 Custom Classification Head Architecture", "145"),
        ("  7.7 Image Preprocessing and Dynamic Normalization", "147"),
        ("  7.8 Data Augmentation Strategies (Rotation, Zoom, Flips)", "149"),
        ("  7.9 Hyperparameter Configuration and Optimizer Selection", "151"),
        ("  7.10 Loss Function Formulation (Categorical Cross-Entropy)", "153"),
        ("  7.11 Batch Sizing, Epoch Scheduling, and Learning Rates", "155"),
        ("  7.12 Automated Regularization: Early Stopping & ReduceLROnPlateau", "157"),
        ("  7.13 Two-Stage Training: Frozen Backbone & Layer 100+ Fine-Tuning", "159"),
        ("  7.14 Model Serialization, Weight Checkpointing, and Loading", "162"),
        ("  7.15 Singleton Predictor Architecture and Latency Optimization", "164"),
        ("CHAPTER 8: EXPERIMENTAL EVALUATION AND MODEL BENCHMARKING", "166"),
        ("  8.1 Evaluation Methodology and Independent Test Dataset", "166"),
        ("  8.2 Global Accuracy, Loss, and Convergence Benchmarks", "168"),
        ("  8.3 Macro and Weighted Precision, Recall, and F1-Score Metrics", "170"),
        ("  8.4 Confusion Matrix Interpretation and Diagnostic Heatmaps", "172"),
        ("  8.5 Confidence Score Distribution and Probability Calibration", "175"),
        ("  8.6 Comprehensive Per-Class Performance Table (38 Classes)", "178"),
        ("  8.7 Empirical Prediction Case Studies on High-Confidence Samples", "182"),
        ("  8.8 Ambiguous Leaf and Low-Confidence Sample Analysis", "185"),
        ("  8.9 Out-of-Distribution Noise and Adversarial Testing", "187"),
        ("  8.10 Model Architectural Integrity and Stability Audits", "189"),
        ("CHAPTER 9: FULL-STACK DJANGO WEB APPLICATION IMPLEMENTATION", "191"),
        ("  9.1 Django Architecture and Model-View-Template (MVT) Pattern", "191"),
        ("  9.2 Master Project Directory Structure and Configuration", "193"),
        ("  9.3 Application Settings and Confidence Threshold Parameters", "195"),
        ("  9.4 URL Routing and Route Dispatching Infrastructure", "197"),
        ("  9.5 View Controller Implementation (home_view, auth, history)", "199"),
        ("  9.6 Form Handling, Validation Rules, and Security Sanitation", "202"),
        ("  9.7 Template Hierarchy and Semantic HTML5 Structure", "204"),
        ("  9.8 Custom Responsive CSS3 Architecture and Theme Styling", "206"),
        ("  9.9 Vanilla JavaScript Client-Side Interactions and Drag-and-Drop", "208"),
        ("  9.10 Media File Upload Storage and Path Management", "210"),
        ("  9.11 Server-Side File Validation and MIME Type Verification", "212"),
        ("  9.12 AI Predictor Service Singleton Lifecycle", "214"),
        ("  9.13 In-Memory Model Initialization and Class Mapping", "216"),
        ("  9.14 Confidence Threshold Safety Evaluation Logic", "218"),
        ("  9.15 Top-3 Candidate Extraction and Softmax Ranking", "220"),
        ("  9.16 Local Disease Knowledge Base Lookup Subsystem", "222"),
        ("  9.17 User Prediction History and Record Isolation", "224"),
        ("  9.18 Error Handling, User Feedback, and Flash Notifications", "226"),
        ("CHAPTER 10: AGRONOMIC KNOWLEDGE BASE (38-CLASS PROFILES)", "228"),
        ("  10.1 Overview of Localized Agricultural Knowledge Base", "228"),
        ("  10.2 Apple Disease Profiles (Scab, Black Rot, Cedar Rust, Healthy)", "230"),
        ("  10.3 Blueberry, Cherry, and Corn Disease Profiles", "236"),
        ("  10.4 Grape, Orange, and Peach Disease Profiles", "244"),
        ("  10.5 Bell Pepper and Potato Disease Profiles", "252"),
        ("  10.6 Raspberry, Soybean, Squash, and Strawberry Disease Profiles", "258"),
        ("  10.7 Comprehensive Tomato Disease Profiles (10 Pathologies)", "266"),
        ("  10.8 Summary Table of Prevention and Treatment Protocols", "280"),
        ("CHAPTER 11: USER INTERFACE DESIGN AND APPLICATION WORKFLOW", "283"),
        ("  11.1 User Interface Philosophy and Responsive Aesthetics", "283"),
        ("  11.2 Core Color Palette, Typography, and Glassmorphism Cards", "285"),
        ("  11.3 Homepage Landing Experience and Hero Banner", "287"),
        ("  11.4 Interactive Drag-and-Drop File Upload Dropzone", "289"),
        ("  11.5 Client-Side Instant Image Preview Rendering", "291"),
        ("  11.6 Diagnosis Result Display and Visual Status Badges", "293"),
        ("  11.7 Dynamic Confidence Meter and Probability Indicators", "295"),
        ("  11.8 Top-3 Candidate Predictions Breakdown Card", "297"),
        ("  11.9 Structured Disease Information and Agronomic Cards", "299"),
        ("  11.10 Low-Confidence Uncertainty Advisory and Retake Guides", "302"),
        ("  11.11 Server Validation Flash Alerts and Client Warning Modals", "304"),
        ("  11.12 Multi-Page Application Views: How It Works & About Pages", "306"),
        ("  11.13 User Authentication Interface (Registration, Login, Profile)", "309"),
        ("  11.14 Personal Diagnosis History Dashboard and Detail Records", "312"),
        ("  11.15 Responsive Layouts on Mobile and Tablet Viewports", "315"),
        ("  11.16 Application Footer, Copyright, and Academic Disclaimers", "318"),
        ("CHAPTER 12: SYSTEM TESTING AND EMPIRICAL VERIFICATION", "320"),
        ("  12.1 Comprehensive Quality Assurance and Testing Strategy", "320"),
        ("  12.2 Unit Testing of Predictor and Knowledge Base Modules", "322"),
        ("  12.3 Django System Integrity and Schema Verification Checks", "324"),
        ("  12.4 Image Upload Validation and Security Attack Tests", "326"),
        ("  12.5 Real AI Inference Verification on Benchmark Leaf Samples", "328"),
        ("  12.6 70% Confidence Threshold Boundary and Guardrail Tests", "330"),
        ("  12.7 Multi-Page Routing, Static Assets, and Media URL Tests", "332"),
        ("  12.8 User Authentication and History Isolation Security Tests", "334"),
        ("  12.9 Responsive Viewport and Cross-Browser Rendering Tests", "336"),
        ("  12.10 Error Handling, Exception Trapping, and Edge-Case Tests", "338"),
        ("  12.11 Step 7 and Step 8 Final End-to-End Verification Suites", "340"),
        ("  12.12 Comprehensive 14-Test Verification Result Matrix", "343"),
        ("CHAPTER 13: SYSTEM SECURITY AND EXCEPTION HANDLING", "346"),
        ("  13.1 Web Application Security Architecture", "346"),
        ("  13.2 Cross-Site Request Forgery (CSRF) Token Protection", "348"),
        ("  13.3 Robust File Upload Security: MIME and Pillow Magic Checks", "350"),
        ("  13.4 File Size Constraints and Storage Quota Management", "352"),
        ("  13.5 Traceback Suppression and User-Safe Flash Error Messages", "354"),
        ("  13.6 Authenticated User Session and Password Hashing Protections", "356"),
        ("  13.7 Data Isolation and Parameterized Database Query Security", "358"),
        ("CHAPTER 14: RESULTS, DISCUSSION, AND COMPARATIVE ANALYSIS", "360"),
        ("  14.1 Summary of Quantitative Model Evaluation Results", "360"),
        ("  14.2 Empirical Confusion Matrix and Per-Crop Accuracy Analysis", "362"),
        ("  14.3 High-Performing Classes vs Botanically Challenging Pathologies", "364"),
        ("  14.4 Evaluation of 70% Confidence Guardrail in Real Scenarios", "366"),
        ("  14.5 Latency, Throughput, and Computational Resource Efficiency", "368"),
        ("  14.6 Comparison of Proposed System with Published Literature", "370"),
        ("  14.7 Critical Agronomic Utility and Field Suitability Discussion", "372"),
        ("CHAPTER 15: LIMITATIONS AND FUTURE ENHANCEMENTS", "374"),
        ("  15.1 Architectural and Computational Limitations", "374"),
        ("  15.2 Botanical and Pathological Class Scope Constraints", "376"),
        ("  15.3 Environmental Variation, Lighting, and Background Artifacts", "378"),
        ("  15.4 Softmax Probability Overconfidence and Out-of-Domain Inputs", "380"),
        ("  15.5 Future Directions: Edge Deployment and Mobile Applications", "382"),
        ("  15.6 Future Directions: Drone Multi-Spectral Imaging and Telemetry", "384"),
        ("  15.7 Future Directions: Real-Time Tele-Agronomy and Expert Portals", "386"),
        ("  15.8 Future Directions: Multilingual and Voice-Assisted Interfaces", "388"),
        ("CHAPTER 16: CONCLUSION", "390"),
        ("  16.1 Summary of Project Contributions", "390"),
        ("  16.2 Technical Achievements in Deep Learning and Engineering", "392"),
        ("  16.3 Societal and Agronomic Impact", "394"),
        ("  16.4 Final Concluding Remarks", "396"),
        ("REFERENCES AND ACADEMIC BIBLIOGRAPHY", "398"),
        ("APPENDICES (A through J)", "402"),
        ("  APPENDIX A — Complete Project File and Directory Structure", "402"),
        ("  APPENDIX B — Complete Installation, Setup, and Execution Guide", "405"),
        ("  APPENDIX C — Master Configuration, Settings, and Hyperparameters", "408"),
        ("  APPENDIX D — Selected Core Source Code Listings and Explanations", "411"),
        ("  APPENDIX E — Complete Automated Test Suite Listings", "420"),
        ("  APPENDIX F — Raw Classification Report and Evaluation JSON Logs", "426"),
        ("  APPENDIX G — Photographic Interface and Architecture Diagram Archive", "430"),
        ("  APPENDIX H — Comprehensive 38-Class Dataset Master Taxonomy", "435"),
        ("  APPENDIX I — End-User Operations and Field Photography Manual", "439"),
        ("  APPENDIX J — Sample Prediction Verification and Confidence Logs", "442"),
    ]
    
    for item, page in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(1)
        p_toc.paragraph_format.space_after = Pt(2)
        p_toc.paragraph_format.line_spacing = 1.1
        r_item = p_toc.add_run(item)
        r_item.font.name = 'Times New Roman'
        r_item.font.size = Pt(10)
        if item.startswith("CHAPTER") or item.startswith("Front") or item.startswith("REFERENCES") or item.startswith("APPENDICES"):
            r_item.bold = True
            r_item.font.name = 'Arial'
            r_item.font.size = Pt(10)
            r_item.font.color.rgb = RGBColor(27, 38, 59)
            
        r_dots = p_toc.add_run(" " + "." * (85 - len(item)) + " ")
        r_dots.font.color.rgb = RGBColor(160, 160, 160)
        r_page = p_toc.add_run(page)
        r_page.bold = True
        r_page.font.name = 'Arial'
        r_page.font.size = Pt(9.5)
        
    doc.add_page_break()

    # List of Figures & Tables
    add_heading_1(doc, "LIST OF FIGURES")
    figures_list = [
        ("Figure 5.1 — Three-Tier System Architecture of AI Plant Disease Detection Platform", "84"),
        ("Figure 5.2 — Data Flow Diagram (DFD) Level 0: Context Diagram", "87"),
        ("Figure 5.3 — Data Flow Diagram (DFD) Level 1: System Process Decomposition", "89"),
        ("Figure 5.4 — End-to-End AI Inference and Decision Pipeline", "93"),
        ("Figure 5.5 — MobileNetV2 Neural Network Architecture with Inverted Residual Blocks", "96"),
        ("Figure 5.6 — UML Use Case Diagram: Actors and Functional Workflows", "97"),
        ("Figure 5.7 — UML Activity Diagram: Diagnostic Execution and Threshold Evaluation", "99"),
        ("Figure 5.8 — UML Sequence Diagram: Client-Server-AI Message Exchanges", "101"),
        ("Figure 5.9 — Relational Database Entity-Relationship (ER) Schema", "107"),
        ("Figure 6.1 — Dataset Partitioning Distribution (70% Train, 15% Val, 15% Test)", "125"),
        ("Figure 7.1 — Model Training Loss Curve Across 16 Epochs (Phase 1 & Phase 2)", "160"),
        ("Figure 7.2 — Model Training and Validation Accuracy Curve (Best Val Acc: 95.25%)", "161"),
        ("Figure 8.1 — Normalized Confusion Matrix Across All 38 Crop-Disease Classes", "173"),
        ("Figure 8.2 — Test Dataset Prediction Confidence Distribution (3,145 Unseen Samples)", "176"),
        ("Figure 8.3 — Top 10 and Lowest 10 Class F1-Score Performance Comparison", "180"),
        ("Figure 11.1 — Application Home Page and Landing Hero Section", "288"),
        ("Figure 11.2 — Interactive Drag-and-Drop Image Upload Dropzone", "290"),
        ("Figure 11.3 — Client-Side Instant Leaf Photograph Preview State", "292"),
        ("Figure 11.4 — Confident Diagnosis Result Display (Apple Scab — 88.42% Confidence)", "294"),
        ("Figure 11.5 — Dynamic Confidence Meter and Visual Certainty Badges", "296"),
        ("Figure 11.6 — Top-3 Candidate Predictions Breakdown Card", "298"),
        ("Figure 11.7 — Comprehensive Agronomic Knowledge Base and Disease Profile Card", "300"),
        ("Figure 11.8 — Low-Confidence Uncertainty Advisory Alert (Corn Sample — 51.44%)", "303"),
        ("Figure 11.9 — Server-Side File Validation and Format Rejection Alert", "305"),
        ("Figure 11.10 — Educational 'How It Works' System Architecture Page", "307"),
        ("Figure 11.11 — Project Background and Technology Stack 'About' Page", "308"),
        ("Figure 11.12 — User Authentication: Secure Login Interface", "310"),
        ("Figure 11.13 — User Registration Interface with Form Validation", "311"),
        ("Figure 11.14 — Tablet Responsive Viewport Layout (768px Width)", "316"),
        ("Figure 11.15 — Mobile Responsive Viewport Layout (375px Width)", "317"),
        ("Figure 11.16 — Mobile Prediction Result and Diagnosis Display", "318"),
        ("Figure 11.17 — Application Footer and Academic Advisory Notice", "319"),
    ]
    for fig, pg in figures_list:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(fig)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r2 = p.add_run(" " + "." * (85 - len(fig)) + " ")
        r2.font.color.rgb = RGBColor(160, 160, 160)
        r3 = p.add_run(pg)
        r3.font.name = 'Arial'
        r3.font.size = Pt(9.5)
        r3.bold = True

    doc.add_paragraph().paragraph_format.space_before = Pt(12)
    add_heading_1(doc, "LIST OF TABLES")
    tables_list = [
        ("Table 2.1 — Comparative Analysis: Manual Inspection vs Prior Machine Learning vs Proposed System", "41"),
        ("Table 4.1 — Hardware Specifications for Development, Training, and Production Hosting", "72"),
        ("Table 4.2 — Software Dependencies, Frameworks, and Runtime Environment", "74"),
        ("Table 6.1 — Comprehensive Partitioning and Image Count Statistics Across 38 Classes", "130"),
        ("Table 7.1 — MobileNetV2 Transfer Learning Hyperparameters and Training Configuration", "152"),
        ("Table 8.1 — Global Model Evaluation Metrics Benchmark on 3,145 Unseen Test Images", "169"),
        ("Table 8.2 — Test Set Confidence Range Breakdown and Sample Distribution", "177"),
        ("Table 8.3 — Full Per-Class Performance Breakdown (Precision, Recall, F1, Support for 38 Classes)", "178"),
        ("Table 8.4 — Verified Sample AI Predictions Across Multiple Test Leaf Classes", "183"),
        ("Table 8.5 — Out-of-Distribution Noise Robustness and Adversarial Input Stress Tests", "188"),
        ("Table 9.1 — Django Core Application URLs, View Handlers, and HTTP Methods", "198"),
        ("Table 10.1 — Agronomic Prevention and Non-Hazardous Treatment Protocol Master Matrix", "280"),
        ("Table 12.1 — End-to-End System Integration and Verification Test Matrix (14 Test Cases)", "343"),
        ("Table 14.1 — Comparison of Proposed Model with Recent Agricultural AI Literature Benchmarks", "370"),
        ("Table H.1 — Master 38-Class Botanical Taxonomy, Disease Categorization, and Image Quantities", "436"),
    ]
    for tbl, pg in tables_list:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(tbl)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r2 = p.add_run(" " + "." * (85 - len(tbl)) + " ")
        r2.font.color.rgb = RGBColor(160, 160, 160)
        r3 = p.add_run(pg)
        r3.font.name = 'Arial'
        r3.font.size = Pt(9.5)
        r3.bold = True

    doc.add_page_break()

    # List of Abbreviations
    add_heading_1(doc, "LIST OF ABBREVIATIONS")
    abbrev_data = [
        ("AI", "Artificial Intelligence"),
        ("API", "Application Programming Interface"),
        ("ASGI", "Asynchronous Server Gateway Interface"),
        ("AUC", "Area Under the Curve"),
        ("CLI", "Command Line Interface"),
        ("CNN", "Convolutional Neural Network"),
        ("CPU", "Central Processing Unit"),
        ("CSRF", "Cross-Site Request Forgery"),
        ("DFD", "Data Flow Diagram"),
        ("DNN", "Deep Neural Network"),
        ("DOM", "Document Object Model"),
        ("ERD", "Entity-Relationship Diagram"),
        ("F1", "Harmonic Mean of Precision and Recall (F1-Score)"),
        ("GPU", "Graphics Processing Unit"),
        ("HTML", "HyperText Markup Language"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("IDE", "Integrated Development Environment"),
        ("JSON", "JavaScript Object Notation"),
        ("KB", "Knowledge Base"),
        ("LR", "Learning Rate"),
        ("ML", "Machine Learning"),
        ("MVT", "Model-View-Template Architecture Pattern"),
        ("NIST", "National Institute of Standards and Technology"),
        ("OOD", "Out-of-Distribution"),
        ("ORM", "Object-Relational Mapping"),
        ("OS", "Operating System"),
        ("PIL", "Python Imaging Library (Pillow)"),
        ("RAM", "Random Access Memory"),
        ("ReLU", "Rectified Linear Unit"),
        ("RGB", "Red Green Blue Color Model"),
        ("SGD", "Stochastic Gradient Descent"),
        ("SQL", "Structured Query Language"),
        ("SVM", "Support Vector Machine"),
        ("UI", "User Interface"),
        ("UML", "Unified Modeling Language"),
        ("URI", "Uniform Resource Identifier"),
        ("URL", "Uniform Resource Locator"),
        ("UX", "User Experience"),
        ("WSGI", "Web Server Gateway Interface"),
    ]
    add_table_with_style(doc, ["Abbreviation", "Expanded Definition / Meaning"], 
                         abbrev_data, col_widths=[2.0, 4.5], caption="List of Abbreviations and Technical Acronyms")

    doc.add_page_break()

    print("[*] Front matter completed successfully. Writing Chapters 1 to 16...")

    # Chapters will be written in full detail in the subsequent blocks
    return doc

print("Setup completed. Ready to write chapters.")
