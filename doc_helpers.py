"""
Comprehensive College Project Documentation Generator
Project: AI Plant Disease Detection
Output: AI_Plant_Disease_Detection_Project_Documentation.docx & PDF
Target Page Count: ~110-150 Pages
"""

import os
import sys
import json
import docx
from pathlib import Path
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

# Load metadata & data
with open(MODEL_DIR / "evaluation_summary.json", "r", encoding="utf-8") as f:
    eval_summary = json.load(f)

with open(MODEL_DIR / "classification_report.json", "r", encoding="utf-8") as f:
    class_report = json.load(f)

with open(MODEL_DIR / "training_metadata.json", "r", encoding="utf-8") as f:
    train_metadata = json.load(f)

with open(METADATA_DIR / "class_names.json", "r", encoding="utf-8") as f:
    class_names = json.load(f)

# Import the 38-class knowledge base
sys.path.insert(0, str(BASE_DIR))
from detector.ai.disease_info import DISEASE_KNOWLEDGE_BASE


# XML / Styling Helpers
def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout_box(doc, title, text, box_type='note'):
    colors = {
        'note': ('#EBF5FB', '#2980B9', 'NOTE / ADVISORY'),
        'important': ('#FEF9E7', '#F39C12', 'IMPORTANT REQUIREMENT'),
        'warning': ('#FADBD8', '#C0392B', 'WARNING / CAUTION'),
        'tip': ('#E8F8F5', '#27AE60', 'OPTIMIZATION / BEST PRACTICE')
    }
    bg_col, border_col, default_title = colors.get(box_type, colors['note'])
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_col.replace('#', ''))
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    # Left border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_col.replace("#", "")}"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"[{title or default_title}]\n")
    run_t.bold = True
    run_t.font.name = 'Arial'
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor.from_string(border_col.replace('#', ''))
    
    run_b = p.add_run(text)
    run_b.font.name = 'Times New Roman'
    run_b.font.size = Pt(10.5)
    run_b.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, caption=None):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(2)
        r_cap = p_cap.add_run(f"Listing: {caption}")
        r_cap.bold = True
        r_cap.font.name = 'Arial'
        r_cap.font.size = Pt(9.5)
        r_cap.font.color.rgb = RGBColor(70, 80, 95)
        
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F4F6F7")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="D5D8DC"/>\n'
        f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="34495E"/>\n'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="D5D8DC"/>\n'
        f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="D5D8DC"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(33, 37, 41)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_path, caption, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.keep_with_next = True
        run = p_img.add_run()
        run.add_picture(str(img_path), width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption)
        run_cap.font.name = 'Arial'
        run_cap.font.size = Pt(9.5)
        run_cap.font.italic = True
        run_cap.bold = True
        run_cap.font.color.rgb = RGBColor(60, 64, 67)
    else:
        p_err = doc.add_paragraph(f"[Image Placeholder: {caption} - File: {img_path}]")
        p_err.italic = True

def add_table_with_style(doc, headers, rows, col_widths=None, caption=None):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(8)
        p_cap.paragraph_format.space_after = Pt(4)
        p_cap.paragraph_format.keep_with_next = True
        run_cap = p_cap.add_run(caption)
        run_cap.font.name = 'Arial'
        run_cap.font.size = Pt(10)
        run_cap.bold = True
        run_cap.font.color.rgb = RGBColor(27, 38, 59)
        
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Format header
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1B263B")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    # Format rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_col = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(40, 40, 40)
                
    # Apply column widths if provided
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                if i < len(row.cells):
                    row.cells[i].width = Inches(w)
                    
    # Subtle borders
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            borders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>\n'
                f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="D5D8DC"/>\n'
                f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="D5D8DC"/>\n'
                f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D5D8DC"/>\n'
                f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="D5D8DC"/>\n'
                f'</w:tcBorders>'
            )
            tcPr.append(borders)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(8)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = 'Arial'
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(27, 38, 59)
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = 'Arial'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(44, 62, 80)
    return h

def add_heading_3(doc, text):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = 'Arial'
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(52, 73, 94)
    return h

def add_para(doc, text, bold_prefix="", italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(11)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(20, 20, 20)
    r_body = p.add_run(text)
    r_body.font.name = 'Times New Roman'
    r_body.font.size = Pt(11)
    r_body.italic = italic
    r_body.font.color.rgb = RGBColor(35, 35, 35)
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(11)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(20, 20, 20)
    r_body = p.add_run(text)
    r_body.font.name = 'Times New Roman'
    r_body.font.size = Pt(11)
    r_body.font.color.rgb = RGBColor(35, 35, 35)
    return p

print("Loaded all formatting and helper functions.")
