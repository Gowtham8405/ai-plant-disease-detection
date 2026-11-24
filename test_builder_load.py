import os
import sys
import json
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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

with open(MODEL_DIR / "training_metadata.json", "r", encoding="utf-8") as f:
    train_metadata = json.load(f)

with open(METADATA_DIR / "class_names.json", "r", encoding="utf-8") as f:
    class_names = json.load(f)

from detector.ai.disease_info import DISEASE_KNOWLEDGE_BASE

print(f"Loaded knowledge base for {len(DISEASE_KNOWLEDGE_BASE)} classes.")
print(f"Loaded metadata for {len(class_names)} classes.")
