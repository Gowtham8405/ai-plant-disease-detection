import os
import json
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Paths
BASE_DIR = Path.cwd()
ASSETS_DIR = BASE_DIR / "documentation_assets"
DIAGRAMS_DIR = ASSETS_DIR / "diagrams"
CHARTS_DIR = ASSETS_DIR / "charts"
MODEL_DIR = BASE_DIR / "detector" / "ai" / "model"
METADATA_DIR = BASE_DIR / "datasets" / "metadata"

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

# 1. Copy existing model training and evaluation charts
existing_charts = [
    ("training_accuracy.png", CHARTS_DIR / "training_accuracy.png"),
    ("training_loss.png", CHARTS_DIR / "training_loss.png"),
    ("confusion_matrix.png", CHARTS_DIR / "confusion_matrix.png"),
    ("evaluation_confusion_matrix.png", CHARTS_DIR / "evaluation_confusion_matrix.png"),
]

for src_name, dst_path in existing_charts:
    src_path = MODEL_DIR / src_name
    if src_path.exists():
        shutil.copy(src_path, dst_path)
        print(f"Copied {src_name} to {dst_path}")

# Load metadata
with open(MODEL_DIR / "evaluation_summary.json", "r") as f:
    eval_summary = json.load(f)

with open(MODEL_DIR / "classification_report.json", "r") as f:
    class_report = json.load(f)

with open(MODEL_DIR / "confidence_analysis.json", "r") as f:
    conf_analysis = json.load(f)

with open(METADATA_DIR / "class_names.json", "r") as f:
    class_names = json.load(f)

# Set global matplotlib styles for publication quality
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11

# =========================================================================
# CHART 1: Confidence Distribution
# =========================================================================
def plot_confidence_distribution():
    bins = ['< 50%', '50 - 60%', '60 - 70%', '70 - 80%', '80 - 90%', '90 - 100%']
    counts = [46, 110, 191, 283, 421, 2724]
    colors = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#27ae60', '#1e8449']

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    bars = ax.bar(bins, counts, color=colors, edgecolor='#2c3e50', linewidth=1.2, width=0.6)

    # Threshold indicator
    ax.axvline(x=2.5, color='#c0392b', linestyle='--', linewidth=2, label='70% Confidence Threshold')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}\n({height/3145*100:.1f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_title('Test Set Prediction Confidence Distribution (N = 3,145)', fontweight='bold', pad=15)
    ax.set_xlabel('Confidence Interval Range (%)', fontweight='bold', labelpad=10)
    ax.set_ylabel('Number of Test Samples', fontweight='bold', labelpad=10)
    ax.set_ylim(0, 3100)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', framealpha=0.9)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "confidence_distribution.png")
    plt.close()
    print("Generated confidence_distribution.png")

# =========================================================================
# CHART 2: Dataset Split Distribution
# =========================================================================
def plot_dataset_split():
    labels = ['Training Set\n(70% - 14,643)', 'Validation Set\n(15% - 3,134)', 'Test Set\n(15% - 3,145)']
    sizes = [14643, 3134, 3145]
    colors = ['#2980b9', '#27ae60', '#f39c12']
    explode = (0.05, 0.05, 0.05)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    
    # Donut Chart
    wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                      startangle=140, colors=colors, textprops=dict(color="black", fontweight='bold'),
                                      wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
    ax1.set_title('Dataset Partitioning Ratio\nTotal: 20,922 Images', fontweight='bold')

    # Bar breakdown
    ax2.bar(['Training', 'Validation', 'Testing'], sizes, color=colors, edgecolor='#2c3e50', width=0.55)
    for i, v in enumerate(sizes):
        ax2.text(i, v + 300, f"{v:,}", ha='center', fontweight='bold')
    ax2.set_ylabel('Image Count', fontweight='bold')
    ax2.set_title('Image Count per Partition', fontweight='bold')
    ax2.set_ylim(0, 16500)
    ax2.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "dataset_split_distribution.png")
    plt.close()
    print("Generated dataset_split_distribution.png")

# =========================================================================
# CHART 3: Top & Bottom Per-Class F1-Scores
# =========================================================================
def plot_class_performance():
    # Extract f1-scores for all 38 classes
    class_f1 = []
    for idx_str, name in class_names.items():
        if name in class_report:
            score = class_report[name]['f1-score'] * 100
            display_name = name.replace('___', ' - ').replace('_', ' ')
            class_f1.append((display_name, score))

    class_f1.sort(key=lambda x: x[1], reverse=True)
    top_10 = class_f1[:10]
    bottom_10 = class_f1[-10:]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), dpi=300)
    
    # Top 10
    names1 = [x[0] for x in top_10][::-1]
    scores1 = [x[1] for x in top_10][::-1]
    bars1 = ax1.barh(names1, scores1, color='#27ae60', edgecolor='#1e8449', height=0.6)
    ax1.set_title('Top 10 Classes by F1-Score (%)', fontweight='bold')
    ax1.set_xlim(90, 101)
    ax1.set_xlabel('F1-Score (%)', fontweight='bold')
    for bar in bars1:
        w = bar.get_width()
        ax1.text(w - 2.5, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='right', color='white', fontweight='bold', fontsize=8.5)
    ax1.grid(axis='x', linestyle=':', alpha=0.6)

    # Bottom 10
    names2 = [x[0] for x in bottom_10]
    scores2 = [x[1] for x in bottom_10]
    bars2 = ax2.barh(names2, scores2, color='#e67e22', edgecolor='#d35400', height=0.6)
    ax2.set_title('Lowest 10 Classes by F1-Score (%)', fontweight='bold')
    ax2.set_xlim(75, 100)
    ax2.set_xlabel('F1-Score (%)', fontweight='bold')
    for bar in bars2:
        w = bar.get_width()
        ax2.text(w - 3.0, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='right', color='white', fontweight='bold', fontsize=8.5)
    ax2.grid(axis='x', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "per_class_f1_scores.png")
    plt.close()
    print("Generated per_class_f1_scores.png")

# =========================================================================
# DIAGRAM 1: System Architecture
# =========================================================================
def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Color palette
    c_client = '#d4e6f1'
    c_app = '#d5f5e3'
    c_ai = '#fcf3cf'
    c_db = '#fadbd8'
    c_border = '#2c3e50'

    # Title
    ax.text(5.5, 7.6, "AI Plant Disease Detection - 3-Tier System Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1a5276')

    # Tier 1: Client Layer
    box_client = patches.FancyBboxPatch((0.5, 5.0), 10, 2.0, boxstyle="round,pad=0.2", fc=c_client, ec=c_border, lw=1.5)
    ax.add_patch(box_client)
    ax.text(0.8, 6.7, "Presentation Layer (Client Tier)", fontweight='bold', fontsize=11, color='#1b4f72')
    ax.text(2.0, 5.8, "Web Browser Client\n(HTML5, CSS3, JavaScript)", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#2980b9'))
    ax.text(5.5, 5.8, "Interactive Drag-and-Drop\nLeaf Image Upload Area", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#2980b9'))
    ax.text(9.0, 5.8, "Diagnosis Dashboard\nConfidence Meter & Advice", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#2980b9'))

    # Tier 2: Application Layer (Django)
    box_app = patches.FancyBboxPatch((0.5, 2.5), 6.2, 2.1, boxstyle="round,pad=0.2", fc=c_app, ec=c_border, lw=1.5)
    ax.add_patch(box_app)
    ax.text(0.8, 4.3, "Application Server (Django 4.2 / Python 3.11)", fontweight='bold', fontsize=11, color='#145a32')
    ax.text(2.0, 3.3, "URL Dispatcher &\nViews (home_view)", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#27ae60'))
    ax.text(4.0, 3.3, "LeafUploadForm &\nSecurity Validation", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#27ae60'))
    ax.text(5.8, 3.3, "Auth & History\nControllers", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#27ae60'))

    # Tier 3: AI Inference Engine
    box_ai = patches.FancyBboxPatch((7.0, 2.5), 3.5, 2.1, boxstyle="round,pad=0.2", fc=c_ai, ec=c_border, lw=1.5)
    ax.add_patch(box_ai)
    ax.text(7.3, 4.3, "AI Deep Learning Engine", fontweight='bold', fontsize=11, color='#7d6608')
    ax.text(8.75, 3.5, "MobileNetV2 Classifier\n(224x224x3 Input -> 38 Classes)", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#f39c12'))
    ax.text(8.75, 2.8, "70% Confidence Threshold Logic", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#d68910'))

    # Tier 4: Data & Knowledge Layer
    box_db = patches.FancyBboxPatch((0.5, 0.3), 10, 1.8, boxstyle="round,pad=0.2", fc=c_db, ec=c_border, lw=1.5)
    ax.add_patch(box_db)
    ax.text(0.8, 1.8, "Data & Knowledge Storage Layer", fontweight='bold', fontsize=11, color='#78281f')
    ax.text(2.0, 1.0, "SQLite3 Database\n(Uploads & History)", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#c0392b'))
    ax.text(5.5, 1.0, "Local Disease Knowledge Base\n(38 Profiles, Symptoms & Care)", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#c0392b'))
    ax.text(9.0, 1.0, "Media Storage\n(leaf_images/ & history/)", ha='center', va='center', bbox=dict(boxstyle="square", fc='white', ec='#c0392b'))

    # Connectors
    ax.annotate('', xy=(5.5, 5.0), xytext=(5.5, 4.6), arrowprops=dict(arrowstyle="<->", color='#2c3e50', lw=2))
    ax.annotate('', xy=(6.7, 3.5), xytext=(7.0, 3.5), arrowprops=dict(arrowstyle="<->", color='#2c3e50', lw=2))
    ax.annotate('', xy=(3.6, 2.5), xytext=(3.6, 2.1), arrowprops=dict(arrowstyle="<->", color='#2c3e50', lw=2))
    ax.annotate('', xy=(8.75, 2.5), xytext=(8.75, 2.1), arrowprops=dict(arrowstyle="<->", color='#2c3e50', lw=2))

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "system_architecture.png")
    plt.close()
    print("Generated system_architecture.png")

# =========================================================================
# DIAGRAM 2: DFD Level 0 (Context Diagram)
# =========================================================================
def draw_dfd_level_0():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    # Farmer / User Entity
    p1 = patches.Rectangle((0.5, 1.5), 2.2, 1.5, fc='#d4e6f1', ec='#2980b9', lw=2)
    ax.add_patch(p1)
    ax.text(1.6, 2.25, "User / Farmer\n(Client Interface)", ha='center', va='center', fontweight='bold', fontsize=10)

    # Central Process 0.0
    c0 = patches.Circle((4.5, 2.25), 1.3, fc='#d5f5e3', ec='#27ae60', lw=2.5)
    ax.add_patch(c0)
    ax.text(4.5, 2.25, "0.0\nAI Plant Disease\nDetection &\nAdvisory System", ha='center', va='center', fontweight='bold', fontsize=10)

    # Agronomist / Extension Officer Entity
    p2 = patches.Rectangle((6.3, 1.5), 2.2, 1.5, fc='#fcf3cf', ec='#f39c12', lw=2)
    ax.add_patch(p2)
    ax.text(7.4, 2.25, "Agricultural\nExtension / Admin\n(Advisory & KB)", ha='center', va='center', fontweight='bold', fontsize=10)

    # Data Flows (User to System)
    ax.annotate('1. Uploads Leaf Image (JPG/PNG)', xy=(3.2, 2.8), xytext=(1.6, 3.2),
                arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5), fontsize=8.5, fontweight='bold')
    ax.annotate('2. Diagnosis, Confidence & Care Advice', xy=(1.6, 1.3), xytext=(3.3, 1.6),
                arrowprops=dict(arrowstyle="<-", color='#1e8449', lw=1.5), fontsize=8.5, fontweight='bold', color='#145a32')

    # Data Flows (System to Agronomist)
    ax.annotate('3. Curated Disease Profiles & Remedies', xy=(5.8, 2.8), xytext=(7.4, 3.2),
                arrowprops=dict(arrowstyle="<-", color='#7d6608', lw=1.5), fontsize=8.5, fontweight='bold')
    ax.annotate('4. Unconfident Samples for Review', xy=(7.4, 1.3), xytext=(5.7, 1.6),
                arrowprops=dict(arrowstyle="->", color='#c0392b', lw=1.5), fontsize=8.5, fontweight='bold', color='#78281f')

    ax.text(4.5, 4.1, "Data Flow Diagram (DFD) - Level 0: Context Diagram", ha='center', fontweight='bold', fontsize=12, color='#1a5276')

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "dfd_level_0.png")
    plt.close()
    print("Generated dfd_level_0.png")

# =========================================================================
# DIAGRAM 3: DFD Level 1 (Decomposition)
# =========================================================================
def draw_dfd_level_1():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5.0, 5.6, "Data Flow Diagram (DFD) - Level 1: System Process Decomposition", ha='center', fontweight='bold', fontsize=12, color='#1a5276')

    # Processes
    procs = [
        (1.5, 4.0, "1.0\nUpload &\nValidate Image"),
        (4.5, 4.0, "2.0\nPreprocess Image\n(224x224 RGB)"),
        (7.5, 4.0, "3.0\nMobileNetV2\nAI Inference"),
        (7.5, 1.8, "4.0\nConfidence\nThreshold Check"),
        (4.5, 1.8, "5.0\nDisease KB &\nTreatment Lookup"),
        (1.5, 1.8, "6.0\nRender Result &\nSave History"),
    ]

    for x, y, text in procs:
        c = patches.Circle((x, y), 0.75, fc='#e8f8f5', ec='#1abc9c', lw=2)
        ax.add_patch(c)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Data Stores
    ax.text(4.5, 0.4, "D1: Local Disease Knowledge Base (38 Classes)\nD2: SQLite Database (Prediction History)", 
            ha='center', va='center', bbox=dict(boxstyle="square", fc='#fadbd8', ec='#c0392b', lw=1.5), fontsize=8.5, fontweight='bold')

    # Arrows between processes
    ax.annotate('', xy=(3.75, 4.0), xytext=(2.25, 4.0), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.text(3.0, 4.2, "Valid Image", ha='center', fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(6.75, 4.0), xytext=(5.25, 4.0), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.text(6.0, 4.2, "Tensor (1,224,224,3)", ha='center', fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(7.5, 2.55), xytext=(7.5, 3.25), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.text(8.3, 2.9, "38 Probabilities", ha='center', fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(5.25, 1.8), xytext=(6.75, 1.8), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.text(6.0, 2.0, "Conf >= 70%", ha='center', fontsize=7.5, fontweight='bold', color='#196f3d')

    ax.annotate('', xy=(2.25, 1.8), xytext=(3.75, 1.8), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.text(3.0, 2.0, "Profile & Advice", ha='center', fontsize=7.5, fontweight='bold')

    # Fallback arrow from 4.0 directly to 6.0
    ax.annotate('', xy=(2.25, 1.4), xytext=(6.75, 1.4), arrowprops=dict(arrowstyle="->", color='#c0392b', lw=1.5, linestyle='--'))
    ax.text(4.5, 1.2, "Conf < 70% (Uncertainty Warning)", ha='center', fontsize=7.5, fontweight='bold', color='#922b21')

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "dfd_level_1.png")
    plt.close()
    print("Generated dfd_level_1.png")

# =========================================================================
# DIAGRAM 4: AI Prediction Pipeline
# =========================================================================
def draw_ai_pipeline():
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)
    ax.axis('off')

    ax.text(5.5, 4.6, "MobileNetV2 AI Inference & Diagnostic Pipeline", ha='center', fontweight='bold', fontsize=13, color='#1a5276')

    steps = [
        (1.0, 2.5, "Input Image\n(JPG/PNG/WEBP)", "#d4e6f1", "#2980b9"),
        (2.8, 2.5, "Pillow Validation\n& Preprocessing\n(RGB, 224x224)", "#d5f5e3", "#27ae60"),
        (4.8, 2.5, "Tensor Conversion\n& Normalization\n([0, 1] Scaling)", "#fcf3cf", "#f39c12"),
        (6.8, 2.5, "MobileNetV2 Model\n(Inverted Residuals\n+ Softmax 38)", "#fadbd8", "#e74c3c"),
        (8.8, 2.5, "Softmax Top-3 &\nConfidence Calc\n(max prob %)", "#e8daef", "#8e44ad"),
        (10.2, 2.5, "70% Decision\nThreshold\n(Display/Warn)", "#d0ece7", "#16a085"),
    ]

    for x, y, text, fc, ec in steps:
        box = patches.FancyBboxPatch((x-0.7, y-0.8), 1.4, 1.6, boxstyle="round,pad=0.1", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

    for i in range(len(steps)-1):
        x1 = steps[i][0] + 0.7
        x2 = steps[i+1][0] - 0.7
        ax.annotate('', xy=(x2, 2.5), xytext=(x1, 2.5), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=2))

    # Bottom notes
    ax.text(5.5, 0.6, "Inference Engine Characteristics:\nSingleton model caching in RAM | Sub-100ms CPU latency | 95.33% Test Accuracy across 38 crop disease classes",
            ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", fc='#f4f6f7', ec='#bdc3c7', lw=1.2), fontsize=8.5)

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "ai_prediction_pipeline.png")
    plt.close()
    print("Generated ai_prediction_pipeline.png")

# =========================================================================
# DIAGRAM 5: MobileNetV2 Architecture
# =========================================================================
def draw_mobilenetv2_arch():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(5.5, 5.5, "MobileNetV2 Neural Network Architecture with Inverted Residuals", ha='center', fontweight='bold', fontsize=12, color='#1a5276')

    layers = [
        (1.0, 3.2, "Input Layer\n224 x 224 x 3\nRGB Image", "#ebf5fb", "#3498db"),
        (2.8, 3.2, "Standard Conv\n3x3, stride 2\n(112 x 112 x 32)", "#e8f8f5", "#1abc9c"),
        (4.8, 3.2, "16x Bottleneck\nInverted Residuals\n(Expansion-DW-Proj)", "#fef9e7", "#f1c40f"),
        (6.8, 3.2, "1x1 Conv Head\n(7 x 7 x 1280)", "#fdedec", "#e74c3c"),
        (8.6, 3.2, "Global Avg Pooling\n(1280 Features)\n+ Dropout (0.3)", "#f5eef8", "#9b59b6"),
        (10.2, 3.2, "Dense Head\n38 Units\nSoftmax Output", "#eaf2f8", "#2980b9")
    ]

    for x, y, text, fc, ec in layers:
        box = patches.FancyBboxPatch((x-0.7, y-1.0), 1.4, 2.0, boxstyle="round,pad=0.1", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

    for i in range(len(layers)-1):
        x1 = layers[i][0] + 0.7
        x2 = layers[i+1][0] - 0.7
        ax.annotate('', xy=(x2, 3.2), xytext=(x1, 3.2), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=2))

    # Inverted Residual Block Detail Box
    box_detail = patches.FancyBboxPatch((1.0, 0.4), 9.0, 1.3, boxstyle="round,pad=0.2", fc='#fdfefe', ec='#7f8c8d', lw=1.2)
    ax.add_patch(box_detail)
    ax.text(1.2, 1.4, "Inverted Residual Block Detail:", fontweight='bold', fontsize=9, color='#2c3e50')
    ax.text(5.5, 0.9, "1. 1x1 Conv (Expansion: 6x channels) + ReLU6  -->  2. 3x3 Depthwise Conv (Spatial filter) + ReLU6  -->  3. 1x1 Linear Bottleneck (Projection)\n+ Residual Skip Connection (when stride=1 and input_dim == output_dim)", 
            ha='center', va='center', fontsize=8, color='#34495e')

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "mobilenetv2_architecture.png")
    plt.close()
    print("Generated mobilenetv2_architecture.png")

# =========================================================================
# DIAGRAM 6: Use Case Diagram
# =========================================================================
def draw_use_case():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(5.0, 6.6, "UML Use Case Diagram - AI Plant Disease Detection System", ha='center', fontweight='bold', fontsize=12, color='#1a5276')

    # System boundary box
    sys_box = patches.FancyBboxPatch((2.2, 0.4), 5.6, 5.8, boxstyle="square,pad=0.1", fc='#fdfefe', ec='#2c3e50', lw=2)
    ax.add_patch(sys_box)
    ax.text(5.0, 6.0, "Plant Disease Detection System", ha='center', fontweight='bold', fontsize=10, color='#2c3e50')

    # Actor 1: Farmer / Guest User
    ax.text(1.0, 4.0, "Actor:\nGuest / Farmer", ha='center', va='center', fontweight='bold', fontsize=9, bbox=dict(boxstyle="circle", fc='#d4e6f1', ec='#2980b9', lw=1.5))
    # Actor 2: Registered User
    ax.text(1.0, 1.8, "Actor:\nRegistered User", ha='center', va='center', fontweight='bold', fontsize=9, bbox=dict(boxstyle="circle", fc='#d5f5e3', ec='#27ae60', lw=1.5))
    # Actor 3: System Admin
    ax.text(9.0, 3.0, "Actor:\nSystem Admin", ha='center', va='center', fontweight='bold', fontsize=9, bbox=dict(boxstyle="circle", fc='#fadbd8', ec='#c0392b', lw=1.5))

    # Use Cases
    use_cases = [
        (5.0, 5.3, "UC1: Upload Leaf Photo"),
        (5.0, 4.5, "UC2: View AI Diagnosis & Confidence"),
        (5.0, 3.7, "UC3: Access Prevention & Advice"),
        (5.0, 2.9, "UC4: User Registration & Login"),
        (5.0, 2.1, "UC5: View Personal History Dashboard"),
        (5.0, 1.3, "UC6: Delete / Clear History Records"),
    ]

    for x, y, text in use_cases:
        ellipse = patches.Ellipse((x, y), 3.2, 0.55, fc='#fcf3cf', ec='#f39c12', lw=1.5)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Actor Lines
    ax.plot([1.0, 3.4], [4.0, 5.3], color='#2c3e50', lw=1.2)
    ax.plot([1.0, 3.4], [4.0, 4.5], color='#2c3e50', lw=1.2)
    ax.plot([1.0, 3.4], [4.0, 3.7], color='#2c3e50', lw=1.2)

    ax.plot([1.0, 3.4], [1.8, 2.9], color='#2c3e50', lw=1.2)
    ax.plot([1.0, 3.4], [1.8, 2.1], color='#2c3e50', lw=1.2)
    ax.plot([1.0, 3.4], [1.8, 1.3], color='#2c3e50', lw=1.2)

    ax.plot([9.0, 6.6], [3.0, 5.3], color='#2c3e50', lw=1.2, linestyle=':')
    ax.plot([9.0, 6.6], [3.0, 4.5], color='#2c3e50', lw=1.2, linestyle=':')

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "use_case_diagram.png")
    plt.close()
    print("Generated use_case_diagram.png")

# =========================================================================
# DIAGRAM 7: Sequence Diagram
# =========================================================================
def draw_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(5.0, 6.6, "UML Sequence Diagram - Leaf Upload and AI Prediction Flow", ha='center', fontweight='bold', fontsize=12, color='#1a5276')

    # Lifelines
    entities = [
        (1.0, "User (Browser)"),
        (3.0, "Django View\n(home_view)"),
        (5.0, "LeafUploadForm\n(Validation)"),
        (7.0, "Predictor\n(MobileNetV2)"),
        (9.0, "Knowledge Base\n& SQLite DB")
    ]

    for x, label in entities:
        ax.text(x, 5.8, label, ha='center', va='center', fontweight='bold', fontsize=8.5, 
                bbox=dict(boxstyle="square", fc='#e8f8f5', ec='#1abc9c', lw=1.2))
        ax.plot([x, x], [0.5, 5.3], color='#95a5a6', linestyle='--', lw=1.2)

    # Messages
    msgs = [
        (1.0, 3.0, 4.8, "1. POST / (leaf image)", "->", '#2980b9'),
        (3.0, 5.0, 4.4, "2. is_valid() & Pillow check", "->", '#27ae60'),
        (5.0, 3.0, 4.0, "3. Valid Form / Image saved", "<-", '#27ae60'),
        (3.0, 7.0, 3.6, "4. predict_disease(image_path)", "->", '#e67e22'),
        (7.0, 7.0, 3.2, "5. Inference & 70% threshold check", "loop", '#d35400'),
        (7.0, 3.0, 2.8, "6. Return prediction & confidence", "<-", '#e67e22'),
        (3.0, 9.0, 2.4, "7. get_disease_info(class) / Record History", "->", '#8e44ad'),
        (9.0, 3.0, 2.0, "8. Return metadata profile", "<-", '#8e44ad'),
        (3.0, 1.0, 1.4, "9. Render HTML diagnosis response", "<-", '#2980b9')
    ]

    for x1, x2, y, text, style, col in msgs:
        if style == "loop":
            box = patches.FancyBboxPatch((x1-0.8, y-0.2), 1.6, 0.4, boxstyle="round,pad=0.05", fc='#fadbd8', ec=col, lw=1)
            ax.add_patch(box)
            ax.text(x1, y, text, ha='center', va='center', fontsize=7.5, fontweight='bold', color=col)
        elif style == "->":
            ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.5))
            ax.text((x1+x2)/2, y+0.15, text, ha='center', fontsize=8, fontweight='bold', color=col)
        elif style == "<-":
            ax.annotate('', xy=(x1, y), xytext=(x2, y), arrowprops=dict(arrowstyle="<-", color=col, lw=1.5, linestyle='--'))
            ax.text((x1+x2)/2, y+0.15, text, ha='center', fontsize=8, fontweight='bold', color=col)

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "sequence_diagram.png")
    plt.close()
    print("Generated sequence_diagram.png")

# =========================================================================
# DIAGRAM 8: Activity Diagram
# =========================================================================
def draw_activity_diagram():
    fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(4.0, 7.6, "UML Activity Diagram - Image Processing & Diagnostic Flow", ha='center', fontweight='bold', fontsize=11, color='#1a5276')

    # Start node
    start = patches.Circle((4.0, 7.0), 0.2, fc='#2c3e50')
    ax.add_patch(start)

    # Activity nodes
    acts = [
        (4.0, 6.2, "User selects/drags leaf photo"),
        (4.0, 5.2, "Django validates image format & size"),
        (4.0, 4.2, "Pillow converts RGB & resizes 224x224"),
        (4.0, 3.2, "MobileNetV2 outputs 38 Softmax probabilities"),
        (4.0, 2.0, "Confidence >= 70% ?"),
        (2.0, 1.0, "Display 'Uncertainty Warning'\nGuide clearer photo"),
        (6.0, 1.0, "Fetch Disease Knowledge Base\nDisplay symptoms, causes & care")
    ]

    for x, y, text in acts[:4]:
        b = patches.FancyBboxPatch((x-1.8, y-0.3), 3.6, 0.6, boxstyle="round,pad=0.1", fc='#e8f8f5', ec='#1abc9c', lw=1.2)
        ax.add_patch(b)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

    # Decision diamond
    diamond = patches.Polygon([[4.0, 2.4], [5.2, 2.0], [4.0, 1.6], [2.8, 2.0]], fc='#fcf3cf', ec='#f39c12', lw=1.5)
    ax.add_patch(diamond)
    ax.text(4.0, 2.0, "Confidence >= 70% ?", ha='center', va='center', fontsize=7.5, fontweight='bold')

    # Out branches
    b_no = patches.FancyBboxPatch((0.5, 0.7), 3.0, 0.6, boxstyle="round,pad=0.1", fc='#fadbd8', ec='#e74c3c', lw=1.2)
    ax.add_patch(b_no)
    ax.text(2.0, 1.0, acts[5][2], ha='center', va='center', fontsize=7.5, fontweight='bold')

    b_yes = patches.FancyBboxPatch((4.5, 0.7), 3.0, 0.6, boxstyle="round,pad=0.1", fc='#d5f5e3', ec='#27ae60', lw=1.2)
    ax.add_patch(b_yes)
    ax.text(6.0, 1.0, acts[6][2], ha='center', va='center', fontsize=7.5, fontweight='bold')

    # Connectors
    ax.annotate('', xy=(4.0, 6.5), xytext=(4.0, 6.8), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.annotate('', xy=(4.0, 5.5), xytext=(4.0, 5.9), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.annotate('', xy=(4.0, 4.5), xytext=(4.0, 4.9), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.annotate('', xy=(4.0, 3.5), xytext=(4.0, 3.9), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))
    ax.annotate('', xy=(4.0, 2.4), xytext=(4.0, 2.9), arrowprops=dict(arrowstyle="->", color='#2c3e50', lw=1.5))

    ax.annotate('', xy=(2.0, 1.3), xytext=(2.8, 2.0), arrowprops=dict(arrowstyle="->", color='#c0392b', lw=1.5))
    ax.text(2.1, 1.8, "[No: <70%]", fontweight='bold', fontsize=7.5, color='#c0392b')

    ax.annotate('', xy=(6.0, 1.3), xytext=(5.2, 2.0), arrowprops=dict(arrowstyle="->", color='#27ae60', lw=1.5))
    ax.text(5.5, 1.8, "[Yes: >=70%]", fontweight='bold', fontsize=7.5, color='#27ae60')

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "activity_diagram.png")
    plt.close()
    print("Generated activity_diagram.png")

# =========================================================================
# DIAGRAM 9: Database ERD
# =========================================================================
def draw_database_erd():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 6)
    ax.axis('off')

    ax.text(4.5, 5.5, "Entity-Relationship (ER) Diagram - Django SQLite Schema", ha='center', fontweight='bold', fontsize=12, color='#1a5276')

    # Table 1: auth_user
    box1 = patches.FancyBboxPatch((0.5, 2.2), 2.4, 2.6, boxstyle="square,pad=0.1", fc='#ebf5fb', ec='#2980b9', lw=1.5)
    ax.add_patch(box1)
    ax.text(1.7, 4.5, "auth_user (Django)", ha='center', fontweight='bold', fontsize=9, color='#1b4f72')
    ax.plot([0.5, 2.9], [4.2, 4.2], color='#2980b9', lw=1)
    ax.text(0.7, 3.8, "PK  id (Integer)\n     username (String)\n     password (Hash)\n     email (String)\n     is_active (Bool)\n     date_joined (Date)", fontsize=8, family='monospace')

    # Table 2: detector_predictionhistory
    box2 = patches.FancyBboxPatch((3.5, 1.0), 3.0, 3.8, boxstyle="square,pad=0.1", fc='#e8f8f5', ec='#1abc9c', lw=1.5)
    ax.add_patch(box2)
    ax.text(5.0, 4.5, "detector_predictionhistory", ha='center', fontweight='bold', fontsize=9, color='#145a32')
    ax.plot([3.5, 6.5], [4.2, 4.2], color='#1abc9c', lw=1)
    ax.text(3.7, 2.5, "PK  id (Integer)\nFK  user_id (Integer)\n     image (Varchar)\n     plant_name (Varchar)\n     disease_name (Varchar)\n     full_class_name (Varchar)\n     confidence_percent (Float)\n     is_confident (Bool)\n     is_healthy (Bool)\n     status_message (Varchar)\n     created_at (DateTime)", fontsize=7.5, family='monospace')

    # Table 3: detector_plantleafupload
    box3 = patches.FancyBboxPatch((7.0, 2.4), 1.8, 2.4, boxstyle="square,pad=0.1", fc='#fef9e7', ec='#f1c40f', lw=1.5)
    ax.add_patch(box3)
    ax.text(7.9, 4.5, "detector_plantleafupload", ha='center', fontweight='bold', fontsize=8, color='#7d6608')
    ax.plot([7.0, 8.8], [4.2, 4.2], color='#f1c40f', lw=1)
    ax.text(7.2, 3.2, "PK  id (Integer)\n     image (Varchar)\n     uploaded_at (Date)", fontsize=8, family='monospace')

    # Relationship connector
    ax.annotate('', xy=(3.5, 3.5), xytext=(2.9, 3.5), arrowprops=dict(arrowstyle="<|-", color='#2c3e50', lw=2))
    ax.text(3.1, 3.7, "1 : N", ha='center', fontsize=8, fontweight='bold', color='#1a5276')

    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / "database_erd.png")
    plt.close()
    print("Generated database_erd.png")

# =========================================================================
# Execute all generators
# =========================================================================
if __name__ == "__main__":
    plot_confidence_distribution()
    plot_dataset_split()
    plot_class_performance()
    draw_system_architecture()
    draw_dfd_level_0()
    draw_dfd_level_1()
    draw_ai_pipeline()
    draw_mobilenetv2_arch()
    draw_use_case()
    draw_sequence_diagram()
    draw_activity_diagram()
    draw_database_erd()
    print("\n[SUCCESS] All diagrams and charts generated successfully in documentation_assets!")
