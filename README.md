# 📱 PhoneWise — Smart Smartphone Suitability & Comparison Guide

**PhoneWise** is a modern, beginner-friendly web application designed to help users evaluate whether a smartphone is suitable for their everyday needs and budget. Built with Python, Streamlit, Pandas, and Plotly, it features an elegant **Light Theme** (soft white background, sky blue accents, lavender highlights, mint green recommendation cards, and crisp dark navy typography).

---

## 🎨 Design & Theme

- **Background:** Soft white (`#F8FAFC`) with subtle, comfortable spacing.
- **Accents:** Sky blue (`#0284C7`), lavender & light purple (`#8B5CF6`).
- **Recommendations:** Vibrant mint green (`#10B981`, `#ECFDF5`) for top matches.
- **Cards:** Crisp white cards with soft grey inner sections and subtle drop shadows.
- **Typography:** Dark navy (`#0F172A`) for optimal readability.
- **Visuals:** Vector SVG smartphone mockups and circular suitability score indicators.

---

## 📄 Application Pages

1. **🏠 Home (Discover & Evaluate)**
   - Welcome hero banner with active budget and catalog count.
   - Deep smartphone evaluator with vector phone mockup, price badge, circular match ring (`/100`), and spec pills.
   - Animated Plotly gauge meter and multi-dimensional radar chart.
   - Dynamic pros (mint green) and cons (soft coral) tailored to selected activities and budget.
   - Quick-browse grid cards of all models in the catalog.

2. **➕ Add Smartphone**
   - Clean, rounded two-column form to add custom smartphones into the session.
   - Live spec inputs (RAM, Storage, Battery, Charging Speed, Processor Tier & Name, Camera MP, OIS, Display).
   - Instantly persists in the session for evaluation, comparison, and ranking.

3. **⚖️ Compare Phones**
   - Head-to-head showdown between any two selected smartphones (Phone A vs Phone B).
   - Side-by-side product cards with phone mockups and circular score badges.
   - Dual-radar chart comparing capabilities across Performance, Camera, Battery, Storage, and Value.
   - Detailed specification showdown table with alternating rows and "Winner / Edge" highlights.
   - Comparative strengths and weaknesses.
   - Algorithmic PhoneWise comparative verdict card.

4. **🎯 Recommendations**
   - Highlighted **👑 Best Overall Match (In Budget)** card with mint green styling.
   - Highlighted **💎 Best Value for Money** card with sky blue styling.
   - Plotly horizontal bar chart of all phones ranked by suitability score (color-coded by budget status).
   - Filterable, searchable catalog table with full technical specs.

5. **ℹ️ About & Transparency**
   - Overview of PhoneWise's mission and architecture.
   - Full mathematical explanation of the 5 hardware pillars and dynamic use-case weights.
   - Prominent transparency disclaimer stating scores are educational estimates based on hardware specifications, not physical lab benchmark scores.

---

## 🛠️ Technology Stack

- **Python 3.9+** (Tested on Python 3.11)
- **Streamlit** — Web interface and reactive state management
- **Pandas** — Data parsing and tabular comparisons
- **Plotly** — Interactive radar, gauge, and bar charts

---

## 🚀 Running PhoneWise on Windows

Follow these simple steps to run PhoneWise on your Windows machine:

### Step 1: Open Terminal (PowerShell or Command Prompt)
Press `Win + R`, type `powershell` or `cmd`, and press **Enter**.

Navigate to the project directory:
```powershell
cd "c:\Users\mamid\OneDrive\Desktop\my projects\PhoneWise"
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```powershell
# In PowerShell:
$env:PYTHONUTF8=1
streamlit run app.py

# Or in Windows Command Prompt (CMD):
set PYTHONUTF8=1
streamlit run app.py
```

### Step 5: Open in Your Browser
Streamlit will automatically open your default browser to:
```text
http://localhost:8501
```

*(To stop the server, press `Ctrl + C` in the terminal).*

---

## 📂 Project Structure

```text
PhoneWise/
│
├── app.py                 # Main Streamlit application with modern light UI
├── sample_phones.csv      # Fictional smartphone dataset with 7 distinct models
├── requirements.txt       # Python package dependencies
├── README.md              # Project documentation and setup guide
└── .streamlit/
    └── config.toml        # Light theme configuration
```

---

## 📊 How the Suitability Score is Calculated

1. **Hardware Pillars (0 – 100 each):**
   - **Performance:** Processor Tier (Entry: 45, Budget: 60, Mid-range: 75, Upper Mid-range: 88, Flagship: 100) + RAM capacity (scaled up to 16GB).
   - **Camera:** Main sensor resolution + Front camera resolution + 20-point bonus for Optical Image Stabilization (OIS).
   - **Battery:** Battery capacity (scaled up to 6,000 mAh) + charging speed (Watts).
   - **Storage:** Internal flash capacity (64GB=50, 128GB=75, 256GB=92, 512GB+=100).
   - **Value / Budget Fit:** Spec-to-price ratio adjusted by user's budget ceiling.

2. **Priority Weight Distribution:**
   - **Gaming:** Performance (40%), Battery (25%), Storage (15%), Value (15%), Camera (5%).
   - **Photography:** Camera (45%), Storage (20%), Performance (15%), Battery (10%), Value (10%).
   - **Online Classes:** Battery (35%), Performance (25%), Storage (15%), Camera (15%), Value (10%).
   - **Everyday Use:** Battery (30%), Value (30%), Performance (20%), Camera (10%), Storage (10%).
   - **Multitasking:** Performance (45%), Storage (20%), Battery (15%), Value (15%), Camera (5%).

---

## ⚠️ Disclaimer
All suitability scores, pillar ratings, and recommendations produced by PhoneWise are estimated heuristic scores derived mathematically from manufacturer hardware specifications and user priorities. They do **not** represent physical laboratory benchmark measurements (such as AnTuTu, Geekbench, or DxOMark) and do not invent physical benchmark metrics. They are designed for educational decision assistance.
