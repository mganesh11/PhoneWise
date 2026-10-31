"""
PhoneWise - Smart Smartphone Suitability & Comparison Guide
------------------------------------------------------------
A modern, elegant light-themed web application that helps users
evaluate, score, and compare smartphones based on their specific
needs and budget.

Technologies: Python, Streamlit, Pandas, Plotly.
Theme: Clean Light Tech (Soft White, Sky Blue, Lavender, Mint Green, Dark Navy text)
"""

import os
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# 1. CONSTANTS & DATA MANAGEMENT
# ==============================================================================
SAMPLE_CSV_PATH = os.path.join(os.path.dirname(__file__), "sample_phones.csv")

# Processor tier baseline capabilities (0 - 100)
PROCESSOR_TIER_SCORES = {
    "Entry": 45,
    "Budget": 60,
    "Mid-range": 75,
    "Upper Mid-range": 88,
    "Flagship": 100
}

def get_default_phones() -> pd.DataFrame:
    """Returns initial fictional sample dataframe in case CSV is absent."""
    return pd.DataFrame([
        {
            "name": "NovaLite 5G",
            "brand": "NovaTech",
            "price": 199,
            "ram_gb": 6,
            "storage_gb": 128,
            "battery_mah": 5000,
            "charging_w": 18,
            "processor_tier": "Budget",
            "processor_name": "Helio G99 Octa-Core",
            "main_camera_mp": 50,
            "front_camera_mp": 8,
            "has_ois": False,
            "screen_type": "LCD",
            "screen_refresh_hz": 90
        },
        {
            "name": "Apex Stellar Pro",
            "brand": "Apex",
            "price": 899,
            "ram_gb": 12,
            "storage_gb": 256,
            "battery_mah": 4800,
            "charging_w": 80,
            "processor_tier": "Flagship",
            "processor_name": "Snapdragon 8 Gen 3",
            "main_camera_mp": 50,
            "front_camera_mp": 32,
            "has_ois": True,
            "screen_type": "AMOLED",
            "screen_refresh_hz": 120
        },
        {
            "name": "Veloce Cyber Gaming 8",
            "brand": "Veloce",
            "price": 499,
            "ram_gb": 16,
            "storage_gb": 256,
            "battery_mah": 6000,
            "charging_w": 67,
            "processor_tier": "Upper Mid-range",
            "processor_name": "Snapdragon 7+ Gen 3",
            "main_camera_mp": 64,
            "front_camera_mp": 16,
            "has_ois": False,
            "screen_type": "AMOLED",
            "screen_refresh_hz": 144
        },
        {
            "name": "Lumina PhotoMaster X",
            "brand": "Lumina",
            "price": 649,
            "ram_gb": 8,
            "storage_gb": 256,
            "battery_mah": 4600,
            "charging_w": 65,
            "processor_tier": "Upper Mid-range",
            "processor_name": "Dimensity 8200",
            "main_camera_mp": 108,
            "front_camera_mp": 32,
            "has_ois": True,
            "screen_type": "OLED",
            "screen_refresh_hz": 120
        },
        {
            "name": "Echo Daily M2",
            "brand": "Echo",
            "price": 139,
            "ram_gb": 4,
            "storage_gb": 64,
            "battery_mah": 5000,
            "charging_w": 10,
            "processor_tier": "Entry",
            "processor_name": "Unisoc T616 Octa-Core",
            "main_camera_mp": 13,
            "front_camera_mp": 5,
            "has_ois": False,
            "screen_type": "LCD",
            "screen_refresh_hz": 60
        },
        {
            "name": "Aura Balance 7",
            "brand": "Aura",
            "price": 349,
            "ram_gb": 8,
            "storage_gb": 128,
            "battery_mah": 5000,
            "charging_w": 33,
            "processor_tier": "Mid-range",
            "processor_name": "Snapdragon 6 Gen 1",
            "main_camera_mp": 50,
            "front_camera_mp": 16,
            "has_ois": True,
            "screen_type": "AMOLED",
            "screen_refresh_hz": 120
        },
        {
            "name": "Horizon Max Ultra",
            "brand": "Horizon",
            "price": 1099,
            "ram_gb": 16,
            "storage_gb": 512,
            "battery_mah": 5400,
            "charging_w": 100,
            "processor_tier": "Flagship",
            "processor_name": "Snapdragon 8 Gen 3 Extreme",
            "main_camera_mp": 200,
            "front_camera_mp": 50,
            "has_ois": True,
            "screen_type": "LTPO AMOLED",
            "screen_refresh_hz": 120
        }
    ])

def load_phones_dataset() -> pd.DataFrame:
    """Load sample phones from CSV or fallback to defaults."""
    if os.path.exists(SAMPLE_CSV_PATH):
        try:
            df = pd.read_csv(SAMPLE_CSV_PATH, encoding="utf-8")
            if "has_ois" in df.columns:
                df["has_ois"] = df["has_ois"].astype(bool)
            return df
        except Exception:
            return get_default_phones()
    return get_default_phones()


# ==============================================================================
# 2. TRANSPARENT SUITABILITY SCORING ENGINE (PRESERVED)
# ==============================================================================
def compute_component_scores(phone: dict, budget: int = None) -> dict:
    """
    Computes 5 foundational hardware sub-scores (0-100 each):
    1. Performance: Processor tier + RAM capacity
    2. Camera: Main sensor resolution + Front camera + OIS optical stabilization
    3. Battery: Capacity (mAh) + Fast charging speed
    4. Storage: Internal flash capacity
    5. Value: Hardware capability relative to retail price and user's budget
    """
    # 1. Performance score (0-100)
    proc_score = PROCESSOR_TIER_SCORES.get(phone.get("processor_tier", "Mid-range"), 70)
    ram = float(phone.get("ram_gb", 6))
    ram_score = min(100.0, max(30.0, (ram / 16.0) * 100))
    perf_score = (0.55 * proc_score) + (0.45 * ram_score)

    # 2. Camera score (0-100)
    main_mp = float(phone.get("main_camera_mp", 50))
    front_mp = float(phone.get("front_camera_mp", 8))
    has_ois = bool(phone.get("has_ois", False))
    
    cam_base = min(80.0, (main_mp / 108.0) * 65.0 + (front_mp / 32.0) * 15.0)
    cam_bonus = 20.0 if has_ois else 5.0
    cam_score = min(100.0, cam_base + cam_bonus)

    # 3. Battery score (0-100)
    battery_mah = float(phone.get("battery_mah", 5000))
    charging_w = float(phone.get("charging_w", 18))
    
    capacity_score = min(100.0, max(40.0, (battery_mah / 6000.0) * 100))
    charging_score = min(100.0, max(35.0, (charging_w / 80.0) * 100))
    battery_score = (0.70 * capacity_score) + (0.30 * charging_score)

    # 4. Storage score (0-100)
    storage_gb = float(phone.get("storage_gb", 128))
    if storage_gb <= 64:
        storage_score = 50.0
    elif storage_gb <= 128:
        storage_score = 75.0
    elif storage_gb <= 256:
        storage_score = 92.0
    else:
        storage_score = 100.0

    # 5. Value for Money / Budget Fit (0-100)
    price = float(phone.get("price", 300))
    raw_hardware_power = (perf_score + cam_score + battery_score + storage_score) / 4.0
    baseline_expected_price = 100 + (raw_hardware_power * 7)
    price_ratio = baseline_expected_price / max(100.0, price)
    value_base = min(100.0, max(30.0, price_ratio * 70.0))

    if budget and budget > 0:
        if price <= budget:
            budget_factor = min(100.0, 85.0 + (1.0 - (price / budget)) * 15.0)
        else:
            over_pct = (price - budget) / budget
            budget_factor = max(10.0, 80.0 - (over_pct * 120.0))
        value_score = (0.5 * value_base) + (0.5 * budget_factor)
    else:
        value_score = value_base

    return {
        "Performance": round(perf_score, 1),
        "Camera": round(cam_score, 1),
        "Battery": round(battery_score, 1),
        "Storage": round(storage_score, 1),
        "Value": round(value_score, 1)
    }

def calculate_suitability_score(phone: dict, selected_needs: list, budget: int = None) -> tuple:
    """
    Computes weighted final suitability score (0 - 100) based on user's requirements.
    Transparently shifts weight based on user selections:
    - Gaming -> High Performance & Battery
    - Photography -> High Camera & Storage
    - Online Classes -> High Battery & Performance
    - Everyday Use -> High Battery & Value
    - Multitasking -> High Performance & Storage
    """
    sub_scores = compute_component_scores(phone, budget)
    
    needs_weights = {
        "Gaming": {
            "Performance": 0.40,
            "Battery": 0.25,
            "Storage": 0.15,
            "Camera": 0.05,
            "Value": 0.15
        },
        "Photography": {
            "Performance": 0.15,
            "Camera": 0.45,
            "Storage": 0.20,
            "Battery": 0.10,
            "Value": 0.10
        },
        "Online classes and studying": {
            "Performance": 0.25,
            "Battery": 0.35,
            "Storage": 0.15,
            "Camera": 0.15,
            "Value": 0.10
        },
        "Everyday use": {
            "Performance": 0.20,
            "Battery": 0.30,
            "Value": 0.30,
            "Camera": 0.10,
            "Storage": 0.10
        },
        "Multitasking": {
            "Performance": 0.45,
            "Storage": 0.20,
            "Battery": 0.15,
            "Value": 0.15,
            "Camera": 0.05
        }
    }

    if selected_needs:
        combined_weights = {"Performance": 0.0, "Camera": 0.0, "Battery": 0.0, "Storage": 0.0, "Value": 0.0}
        for need in selected_needs:
            weights = needs_weights.get(need, needs_weights["Everyday use"])
            for k in combined_weights:
                combined_weights[k] += weights[k]
        
        total_w = sum(combined_weights.values())
        for k in combined_weights:
            combined_weights[k] /= total_w
    else:
        combined_weights = {
            "Performance": 0.25,
            "Battery": 0.25,
            "Camera": 0.20,
            "Storage": 0.15,
            "Value": 0.15
        }

    final_score = 0.0
    for dim, weight in combined_weights.items():
        final_score += sub_scores[dim] * weight

    final_score = round(min(100.0, max(0.0, final_score)), 1)
    return final_score, sub_scores, combined_weights


# ==============================================================================
# 3. ADVANTAGES & DISADVANTAGES (PROS & CONS) GENERATOR (PRESERVED)
# ==============================================================================
def generate_pros_and_cons(phone: dict, budget: int = None, selected_needs: list = None) -> tuple:
    """
    Dynamically deduces clear advantages (pros) and disadvantages (weaknesses)
    based on the phone's hardware parameters and active user context.
    """
    pros = []
    cons = []

    ram = float(phone.get("ram_gb", 6))
    storage = float(phone.get("storage_gb", 128))
    battery = float(phone.get("battery_mah", 5000))
    charging = float(phone.get("charging_w", 18))
    proc_tier = phone.get("processor_tier", "Mid-range")
    main_cam = float(phone.get("main_camera_mp", 50))
    has_ois = bool(phone.get("has_ois", False))
    price = float(phone.get("price", 300))
    refresh_hz = float(phone.get("screen_refresh_hz", 60))
    screen_type = phone.get("screen_type", "LCD")

    # RAM & Processor
    if ram >= 12:
        pros.append(f"Massive {int(ram)}GB RAM ensures buttery-smooth multitasking and long-term future proofing.")
    elif ram >= 8:
        pros.append(f"Generous {int(ram)}GB RAM handles heavy background apps with ease.")
    elif ram <= 4:
        cons.append(f"Limited {int(ram)}GB RAM may reload apps frequently during multitasking or high-end gaming.")

    if proc_tier == "Flagship":
        pros.append(f"Top-tier flagship processor ({phone.get('processor_name')}) delivers maximum gaming and app speeds.")
    elif proc_tier == "Entry":
        cons.append(f"Entry-level chipset ({phone.get('processor_name')}) is tailored for light tasks, not intensive 3D gaming.")

    # Storage
    if storage >= 256:
        pros.append(f"Spacious {int(storage)}GB storage provides ample room for 4K video, heavy games, and thousands of photos.")
    elif storage <= 64:
        cons.append(f"Constrained {int(storage)}GB storage can fill up rapidly with system updates and downloaded media.")

    # Battery & Charging
    if battery >= 5500:
        pros.append(f"High-capacity {int(battery)} mAh battery provides multi-day endurance for travel and heavy work.")
    elif battery >= 5000:
        pros.append(f"Reliable {int(battery)} mAh battery comfortably powers through a full day of active usage.")
    elif battery < 4700:
        cons.append(f"Modest {int(battery)} mAh battery capacity may require an afternoon top-up under heavy screen-on time.")

    if charging >= 65:
        pros.append(f"Super-fast {int(charging)}W charging quickly restores battery in under 35-45 minutes.")
    elif charging <= 15:
        cons.append(f"Standard {int(charging)}W charging is relatively slow compared to modern fast-charging standards.")

    # Camera
    if main_cam >= 108:
        pros.append(f"Ultra-high-resolution {int(main_cam)}MP main sensor captures crisp detail and sharp crops.")
    elif main_cam >= 50 and has_ois:
        pros.append("Main camera features Optical Image Stabilization (OIS) for sharper low-light photos and steady video.")
    elif main_cam <= 16:
        cons.append(f"Basic {int(main_cam)}MP camera sensor produces modest clarity, especially in dimly lit environments.")

    if not has_ois and price > 400:
        cons.append("Lacks Optical Image Stabilization (OIS), which is commonly expected at this price point.")

    # Display
    if refresh_hz >= 120 and "OLED" in screen_type.upper():
        pros.append(f"Vibrant {screen_type} display with smooth {int(refresh_hz)}Hz refresh rate gives a premium visual experience.")
    elif refresh_hz <= 60:
        cons.append("Standard 60Hz screen refresh rate feels less fluid compared to 90Hz or 120Hz displays.")

    # Budget Alignment
    if budget and budget > 0:
        if price <= budget:
            savings = budget - price
            if savings >= 50:
                pros.append(f"Comfortably within budget: leaves you with ${savings:.0f} in savings!")
            else:
                pros.append(f"Fits neatly inside your ${budget} budget ceiling.")
        else:
            diff = price - budget
            cons.append(f"Exceeds your preferred budget by ${diff:.0f} ({((diff/budget)*100):.0f}% above target).")

    if not pros:
        pros.append("Solid balanced hardware offering consistent daily baseline performance.")
    if not cons:
        cons.append("No major technical shortcomings found for its hardware tier.")

    return pros, cons


# ==============================================================================
# 4. ROBUST HTML & VECTOR SVG RENDERING HELPERS
# ==============================================================================
def render_html(html_str: str):
    """
    Renders HTML safely in Streamlit without CommonMark indented code-block interference.
    Strips leading whitespace from every line so markdown never treats lines with 4+ spaces as code blocks.
    """
    if not html_str:
        return
    cleaned_lines = [line.lstrip() for line in html_str.strip().splitlines()]
    clean_code = "\n".join(cleaned_lines)
    st.markdown(clean_code, unsafe_allow_html=True)

def render_phone_svg(phone: dict, width: int = 140, height: int = 240) -> str:
    """
    Renders an elegant, scalable, vector smartphone mockup SVG encoded as a base64 image.
    This guarantees 100% valid HTML rendering without raw tag leakage.
    """
    brand = str(phone.get("brand", "Phone")).upper()
    name = str(phone.get("name", "Smartphone"))
    proc_tier = phone.get("processor_tier", "Mid-range")
    
    if proc_tier == "Flagship":
        grad_def = '<linearGradient id="grad_theme" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#1E1B4B"/><stop offset="50%" stop-color="#312E81"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient>'
        accent = "#A5B4FC"
    elif "Gaming" in name or proc_tier == "Upper Mid-range":
        grad_def = '<linearGradient id="grad_theme" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#022C22"/><stop offset="50%" stop-color="#065F46"/><stop offset="100%" stop-color="#10B981"/></linearGradient>'
        accent = "#6EE7B7"
    elif proc_tier == "Entry":
        grad_def = '<linearGradient id="grad_theme" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0F172A"/><stop offset="50%" stop-color="#334155"/><stop offset="100%" stop-color="#64748B"/></linearGradient>'
        accent = "#CBD5E1"
    else:
        grad_def = '<linearGradient id="grad_theme" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0369A1"/><stop offset="50%" stop-color="#0284C7"/><stop offset="100%" stop-color="#38BDF8"/></linearGradient>'
        accent = "#BAE6FD"

    ram_str = f"{phone.get('ram_gb', 8)}GB"
    storage_str = f"{phone.get('storage_gb', 128)}GB"
    battery_str = f"{phone.get('battery_mah', 5000)} mAh"
    charging_str = f"{phone.get('charging_w', 33)}W"
    clean_name = name[:16].replace("<", "").replace(">", "").replace("&", "")
    clean_brand = brand[:12].replace("<", "").replace(">", "").replace("&", "")

    svg_content = (
        f'<svg viewBox="0 0 160 270" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;max-width:100%;height:auto;">'
        f'<defs>{grad_def}<linearGradient id="chassis_metal" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#CBD5E1"/><stop offset="100%" stop-color="#64748B"/></linearGradient></defs>'
        f'<rect x="6" y="6" width="148" height="258" rx="26" fill="#0F172A" stroke="url(#chassis_metal)" stroke-width="2.5"/>'
        f'<rect x="11" y="11" width="138" height="248" rx="22" fill="url(#grad_theme)"/>'
        f'<path d="M 11 30 Q 80 85 149 30 L 149 11 L 11 11 Z" fill="rgba(255,255,255,0.1)"/>'
        f'<rect x="68" y="14" width="24" height="2.5" rx="1.2" fill="#334155"/>'
        f'<circle cx="80" cy="23" r="3.5" fill="#020617" stroke="#1E293B" stroke-width="1"/>'
        f'<text x="80" y="58" font-size="16" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-weight="700" fill="#FFFFFF" text-anchor="middle" letter-spacing="-0.5">10:30</text>'
        f'<text x="80" y="73" font-size="8.5" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-weight="500" fill="rgba(255,255,255,0.8)" text-anchor="middle">Wednesday, Oct 31</text>'
        f'<rect x="24" y="96" width="112" height="76" rx="14" fill="rgba(255, 255, 255, 0.12)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1"/>'
        f'<circle cx="80" cy="120" r="13" fill="{accent}" fill-opacity="0.25" stroke="{accent}" stroke-width="1.5"/>'
        f'<text x="80" y="125" font-size="12" font-family="sans-serif" text-anchor="middle" fill="#FFFFFF">&#9889;</text>'
        f'<text x="80" y="148" font-size="9" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-weight="700" fill="#FFFFFF" text-anchor="middle">{ram_str} &#8226; {storage_str}</text>'
        f'<text x="80" y="161" font-size="7.5" font-family="-apple-system,BlinkMacSystemFont,sans-serif" fill="rgba(255,255,255,0.85)" text-anchor="middle">{battery_str} &#8226; {charging_str}</text>'
        f'<text x="80" y="234" font-size="9.5" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-weight="800" fill="rgba(255,255,255,0.9)" text-anchor="middle" letter-spacing="1">{clean_brand}</text>'
        f'<text x="80" y="246" font-size="8" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-weight="500" fill="rgba(255,255,255,0.7)" text-anchor="middle">{clean_name}</text>'
        f'<rect x="62" y="252" width="36" height="2.5" rx="1.2" fill="rgba(255, 255, 255, 0.6)"/>'
        f'</svg>'
    )
    b64 = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" height="{height}" style="display:block;margin:0 auto;max-width:100%;height:auto;filter:drop-shadow(0 6px 16px rgba(15,23,42,0.12));border-radius:18px;" alt="{clean_name}" />'

def render_circular_score(score: float, size: int = 68) -> str:
    """Renders a colorful circular match indicator as a clean single-line HTML element."""
    val = int(round(score))
    if val >= 80:
        color, bg, border, label = "#059669", "#ECFDF5", "#10B981", "High Match"
    elif val >= 65:
        color, bg, border, label = "#D97706", "#FFFBEB", "#F59E0B", "Good Match"
    else:
        color, bg, border, label = "#DC2626", "#FEF2F2", "#EF4444", "Fair Match"

    return (
        f'<div style="display:inline-flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">'
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{bg};border:3.5px solid {border};display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(15,23,42,0.05);">'
        f'<span style="font-size:{size*0.35:.0f}px;font-weight:800;color:{color};line-height:1;">{val}</span>'
        f'<span style="font-size:{size*0.17:.0f}px;font-weight:600;color:#64748B;margin-top:2px;">/100</span>'
        f'</div>'
        f'<span style="font-size:0.72rem;font-weight:700;color:{color};text-transform:uppercase;margin-top:4px;letter-spacing:0.04em;">{label}</span>'
        f'</div>'
    )


# ==============================================================================
# 5. DATA VISUALIZATION FUNCTIONS (PLOTLY LIGHT THEME)
# ==============================================================================
def create_radar_chart(categories: list, values: list, title: str = "Hardware Pillars Breakdown") -> go.Figure:
    """Creates an elegant light-themed tech radar chart for sub-scores."""
    r_vals = values + [values[0]]
    theta_vals = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_vals,
        theta=theta_vals,
        fill='toself',
        fillcolor='rgba(2, 132, 199, 0.16)',
        line=dict(color='#0284C7', width=2.5),
        marker=dict(size=6, color='#8B5CF6')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='#64748B', size=9),
                linecolor='#CBD5E1',
                gridcolor='#E2E8F0'
            ),
            angularaxis=dict(
                tickfont=dict(color='#0F172A', size=11, family='sans-serif'),
                linecolor='#CBD5E1',
                gridcolor='#E2E8F0'
            ),
            bgcolor='#F8FAFC'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=35, r=35, t=35, b=35),
        height=320,
        showlegend=False,
        title=dict(text=title, font=dict(color='#0F172A', size=14, family='sans-serif'))
    )
    return fig

def create_gauge_chart(score: float, title: str = "Suitability Score") -> go.Figure:
    """Creates a clean light-themed circular gauge meter for overall suitability."""
    if score >= 80:
        bar_color = "#10B981"
    elif score >= 60:
        bar_color = "#F59E0B"
    else:
        bar_color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix': "/100", 'font': {'size': 32, 'color': "#0F172A", 'family': "sans-serif"}},
        title={'text': title, 'font': {'size': 14, 'color': "#475569", 'family': "sans-serif"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#CBD5E1", 'tickfont': {'color': "#64748B"}},
            'bar': {'color': bar_color, 'thickness': 0.25},
            'bgcolor': "#F1F5F9",
            'borderwidth': 1,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.10)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.10)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.12)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=210,
        margin=dict(l=20, r=20, t=30, b=10)
    )
    return fig

def create_comparison_radar(phone_a_data: dict, phone_b_data: dict, phone_a_name: str, phone_b_name: str) -> go.Figure:
    """Creates a dual radar chart comparing two phones in the light theme."""
    categories = ["Performance", "Camera", "Battery", "Storage", "Value"]
    
    vals_a = [phone_a_data[c] for c in categories] + [phone_a_data[categories[0]]]
    vals_b = [phone_b_data[c] for c in categories] + [phone_b_data[categories[0]]]
    thetas = categories + [categories[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=vals_a,
        theta=thetas,
        fill='toself',
        name=phone_a_name,
        fillcolor='rgba(2, 132, 199, 0.18)',
        line=dict(color='#0284C7', width=2.5)
    ))

    fig.add_trace(go.Scatterpolar(
        r=vals_b,
        theta=thetas,
        fill='toself',
        name=phone_b_name,
        fillcolor='rgba(139, 92, 246, 0.18)',
        line=dict(color='#8B5CF6', width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#64748B', size=9), gridcolor='#E2E8F0'),
            angularaxis=dict(tickfont=dict(color='#0F172A', size=11, family='sans-serif'), gridcolor='#E2E8F0'),
            bgcolor='#F8FAFC'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#0F172A")),
        margin=dict(l=35, r=35, t=30, b=45),
        height=360
    )
    return fig


# ==============================================================================
# 6. STREAMLIT APPLICATION (LIGHT THEME)
# ==============================================================================
def main():
    st.set_page_config(
        page_title="PhoneWise - Smartphone Decision Assistant",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Global CSS: Light Theme & Responsive Layout
    render_html("""
    <style>
        /* Viewport & Scrolling Fix */
        html, body, [data-testid="stAppViewContainer"], .main {
            overflow-x: hidden !important;
            max-width: 100vw;
        }

        *, *::before, *::after {
            box-sizing: border-box !important;
        }

        /* Light Theme Foundation */
        .stApp {
            background-color: #F8FAFC;
            color: #0F172A;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Main Container Spacing */
        .main .block-container {
            max-width: 1200px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* Gradient Text Highlights */
        .gradient-brand {
            background: linear-gradient(135deg, #0284C7 0%, #6366F1 50%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
            box-shadow: 2px 0 14px rgba(148, 163, 184, 0.08);
        }

        /* Standard White Tech Card */
        .phone-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 20px;
            width: 100%;
            max-width: 100%;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.02);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            overflow-wrap: break-word;
            word-break: break-word;
        }
        .phone-card:hover {
            border-color: #BAE6FD;
            box-shadow: 0 10px 25px -3px rgba(2, 132, 199, 0.1), 0 4px 6px -2px rgba(2, 132, 199, 0.05);
        }

        /* Soft Grey Inner Section */
        .inner-card-grey {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px;
            width: 100%;
            max-width: 100%;
            overflow-wrap: break-word;
        }

        /* Best Recommendation Highlight Card (Mint Green) */
        .best-rec-card {
            background: linear-gradient(135deg, #ECFDF5 0%, #F0FDF4 100%);
            border: 2px solid #10B981;
            border-radius: 16px;
            padding: 22px;
            width: 100%;
            max-width: 100%;
            box-shadow: 0 8px 24px -4px rgba(16, 185, 129, 0.15);
            overflow-wrap: break-word;
        }

        /* Best Value Pick Card (Sky Blue) */
        .value-pick-card {
            background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
            border: 2px solid #0284C7;
            border-radius: 16px;
            padding: 22px;
            width: 100%;
            max-width: 100%;
            box-shadow: 0 8px 24px -4px rgba(2, 132, 199, 0.15);
            overflow-wrap: break-word;
        }

        /* Specification Pills */
        .spec-pill-light {
            display: inline-flex;
            align-items: center;
            background-color: #F1F5F9;
            color: #334155;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.84rem;
            margin: 3px 4px 3px 0;
            border: 1px solid #CBD5E1;
        }
        .spec-pill-light strong {
            color: #0F172A;
            margin-left: 4px;
        }

        /* Pros and Cons Boxes */
        .pro-box {
            background: #ECFDF5;
            border-left: 4px solid #10B981;
            padding: 12px 16px;
            margin-bottom: 10px;
            border-radius: 0 10px 10px 0;
            font-size: 0.92rem;
            color: #065F46;
            font-weight: 500;
            width: 100%;
            overflow-wrap: break-word;
        }
        .con-box {
            background: #FFF1F2;
            border-left: 4px solid #F43F5E;
            padding: 12px 16px;
            margin-bottom: 10px;
            border-radius: 0 10px 10px 0;
            font-size: 0.92rem;
            color: #9F1239;
            font-weight: 500;
            width: 100%;
            overflow-wrap: break-word;
        }

        /* Price Badge */
        .price-badge {
            display: inline-block;
            background: #F1F5F9;
            color: #0F172A;
            font-size: 1.4rem;
            font-weight: 800;
            padding: 4px 14px;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
        }

        /* Disclaimer Card */
        .disclaimer-card {
            background: #FFFBEB;
            border: 1px solid #FDE68A;
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 0.88rem;
            color: #92400E;
            line-height: 1.5;
            margin-top: 24px;
            width: 100%;
            overflow-wrap: break-word;
        }

        /* Responsive Images */
        img {
            max-width: 100%;
            height: auto;
        }

        /* Streamlit Button Styling */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
            color: #FFFFFF;
            font-weight: 600;
            border-radius: 10px;
            border: none;
            padding: 8px 20px;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
            transition: all 0.2s ease;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #0369A1 0%, #0284C7 100%);
            box-shadow: 0 6px 16px rgba(2, 132, 199, 0.35);
            transform: translateY(-1px);
        }

        /* Mobile Media Queries */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.75rem;
                padding-right: 0.75rem;
            }
            .phone-card, .best-rec-card, .value-pick-card {
                padding: 16px !important;
            }
            h1 {
                font-size: 1.7rem !important;
            }
            h2 {
                font-size: 1.35rem !important;
            }
        }
    </style>
    """)

    # Initialize phone catalog in session state
    if "phones_df" not in st.session_state:
        st.session_state.phones_df = load_phones_dataset()

    # ==========================================================================
    # SIDEBAR: LOGO, NAVIGATION & USER PROFILE CONTROLS
    # ==========================================================================
    with st.sidebar:
        # Beautiful PhoneWise Logo Header
        render_html("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 6px 0 18px 0; border-bottom: 1px solid #E2E8F0;">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #0284C7, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 24px; color: white; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3);">
                📱
            </div>
            <div>
                <span style="font-size: 1.4rem; font-weight: 800; background: linear-gradient(135deg, #0284C7, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PhoneWise</span>
                <div style="font-size: 0.74rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Smart Phone Guide</div>
            </div>
        </div>
        """)

        render_html("<p style='font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-top: 14px; margin-bottom: 6px; letter-spacing: 0.05em;'>Navigation</p>")
        
        # Navigation Options
        page_selected = st.radio(
            "Go to page:",
            ["Home", "Add Smartphone", "Compare Phones", "Recommendations", "About"],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("### 🎯 Your Priorities & Budget")
        render_html("<p style='font-size:0.84rem; color:#475569;'>Customize your budget and needs to dynamically update suitability scores.</p>")

        user_budget = st.slider(
            "Max Target Budget ($ USD)",
            min_value=100,
            max_value=1500,
            value=500,
            step=25,
            help="Phones within this budget receive a positive score boost. Phones exceeding this budget are penalized."
        )

        st.markdown("#### Primary Activities:")
        user_needs = []
        
        gaming = st.checkbox("🎮 Gaming (3D games, high FPS)", value=False)
        if gaming: user_needs.append("Gaming")
        
        photography = st.checkbox("📸 Photography & Video", value=False)
        if photography: user_needs.append("Photography")
        
        classes = st.checkbox("📚 Online Classes & Studying", value=False)
        if classes: user_needs.append("Online classes and studying")
        
        everyday = st.checkbox("☕ Everyday Use (Browsing, Calls)", value=True)
        if everyday: user_needs.append("Everyday use")
        
        multitasking = st.checkbox("⚡ Heavy Multitasking & Work", value=False)
        if multitasking: user_needs.append("Multitasking")

        st.markdown("---")
        st.markdown("#### 📊 Active Weights")
        if user_needs:
            for n in user_needs:
                render_html(f"<span class='spec-pill-light' style='background:#E0F2FE; color:#0369A1; border-color:#BAE6FD;'>✓ {n}</span>")
        else:
            st.info("Using balanced all-rounder weights.")

        render_html("""
        <div style='margin-top: 24px; padding: 12px; background: #F1F5F9; border-radius: 10px; font-size: 0.78rem; color: #475569;'>
            💡 <b>Tip:</b> Changing your budget or priorities recalculates recommendations across all pages in real time!
        </div>
        """)

    # ==========================================================================
    # PAGE 1: HOME (DISCOVER & EVALUATE)
    # ==========================================================================
    if page_selected == "Home":
        # Hero Banner
        render_html(f"""
        <div class="phone-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 50%, #FAF5FF 100%); border-color: #BAE6FD;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                <div style="max-width: 650px;">
                    <span style="background: #E0F2FE; color: #0284C7; font-weight: 700; font-size: 0.78rem; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;">
                        ✨ Smart Smartphone Decision Engine
                    </span>
                    <h1 style="margin: 8px 0 6px 0; font-size: 2.2rem;">
                        Find the <span class="gradient-brand">Perfect Smartphone</span> for You
                    </h1>
                    <p style="color: #475569; font-size: 1.02rem; line-height: 1.5; margin: 0;">
                        Personalized suitability scoring based on your specific requirements and budget ceiling. 
                        Transparent, objective, and beginner-friendly.
                    </p>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 14px 22px; border-radius: 14px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04); text-align: right;">
                    <div style="font-size: 0.8rem; color: #64748B; font-weight: 600;">ACTIVE BUDGET</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #0284C7;">${user_budget}</div>
                    <div style="font-size: 0.78rem; color: #10B981; font-weight: 600;">{len(st.session_state.phones_df)} Models in Catalog</div>
                </div>
            </div>
        </div>
        """)

        # Single Smartphone Evaluation Section
        st.markdown("### 🔍 Evaluate a Smartphone's Suitability")
        st.write("Select any smartphone from the catalog to see its comprehensive match evaluation, circular score, and pros/cons.")

        all_names = st.session_state.phones_df["name"].tolist()
        col_select1, col_select2 = st.columns([3, 1])
        with col_select1:
            selected_name = st.selectbox("Choose a Phone to Inspect:", all_names, index=0)
        with col_select2:
            render_html("<div style='height: 28px;'></div>")
            quick_compare_btn = st.button("⚖️ Compare This Phone", use_container_width=True)

        phone_series = st.session_state.phones_df[st.session_state.phones_df["name"] == selected_name].iloc[0]
        selected_phone = phone_series.to_dict()

        # Calculate scores
        suitability, sub_scores, weights_used = calculate_suitability_score(selected_phone, user_needs, user_budget)
        pros, cons = generate_pros_and_cons(selected_phone, user_budget, user_needs)

        # Verdict message
        if suitability >= 80:
            verdict_badge = "<span style='background:#ECFDF5; color:#059669; border:1px solid #10B981; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.85rem;'>🌟 Highly Recommended Match</span>"
        elif suitability >= 65:
            verdict_badge = "<span style='background:#FFFBEB; color:#D97706; border:1px solid #F59E0B; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.85rem;'>👍 Solid Balanced Choice</span>"
        else:
            verdict_badge = "<span style='background:#FEF2F2; color:#DC2626; border:1px solid #EF4444; padding:4px 12px; border-radius:20px; font-weight:700; font-size:0.85rem;'>⚠️ Better Options Available for Budget</span>"

        # Main Evaluation Showcase Card
        col_mockup, col_details = st.columns([1, 2.5])
        with col_mockup:
            render_html(f"""
            <div class="phone-card" style="text-align: center; padding: 20px 10px;">
                {render_phone_svg(selected_phone, width=140, height=240)}
                <div style="margin-top: 14px;">
                    {render_circular_score(suitability, size=68)}
                </div>
            </div>
            """)

        with col_details:
            render_html(f"""
            <div class="phone-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span style="color: #0284C7; font-weight: 700; text-transform: uppercase; font-size: 0.82rem; letter-spacing: 0.05em;">
                            {selected_phone.get('brand', 'Tech')}
                        </span>
                        <h2 style="margin: 4px 0 6px 0; font-size: 1.8rem;">{selected_phone['name']}</h2>
                        <div style="margin-bottom: 8px;">{verdict_badge}</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="price-badge">${selected_phone['price']}</span>
                        <div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">
                            Target Budget: <strong>${user_budget}</strong>
                        </div>
                    </div>
                </div>
                <hr style="border-color: #E2E8F0; margin: 14px 0;">
                <div>
                    <span class="spec-pill-light">🧠 RAM: <strong>{selected_phone['ram_gb']} GB</strong></span>
                    <span class="spec-pill-light">💾 Storage: <strong>{selected_phone['storage_gb']} GB</strong></span>
                    <span class="spec-pill-light">🔋 Battery: <strong>{selected_phone['battery_mah']} mAh</strong></span>
                    <span class="spec-pill-light">⚡ Fast Charge: <strong>{selected_phone['charging_w']}W</strong></span>
                    <span class="spec-pill-light">⚙️ Processor: <strong>{selected_phone['processor_name']}</strong> ({selected_phone['processor_tier']})</span>
                    <span class="spec-pill-light">📸 Main Camera: <strong>{selected_phone['main_camera_mp']} MP</strong> {'(OIS)' if selected_phone.get('has_ois') else ''}</span>
                    <span class="spec-pill-light">🤳 Front: <strong>{selected_phone['front_camera_mp']} MP</strong></span>
                    <span class="spec-pill-light">🖥️ Display: <strong>{selected_phone.get('screen_type', 'OLED')} {selected_phone.get('screen_refresh_hz', 120)}Hz</strong></span>
                </div>
            </div>
            """)

            # Sub-scores mini cards
            st.markdown("#### 📐 Hardware Dimension Sub-Scores")
            sc1, sc2, sc3, sc4, sc5 = st.columns(5)
            sc1.metric("🚀 Performance", f"{sub_scores['Performance']}/100", f"Weight: {int(weights_used['Performance']*100)}%")
            sc2.metric("📸 Camera", f"{sub_scores['Camera']}/100", f"Weight: {int(weights_used['Camera']*100)}%")
            sc3.metric("🔋 Battery", f"{sub_scores['Battery']}/100", f"Weight: {int(weights_used['Battery']*100)}%")
            sc4.metric("💾 Storage", f"{sub_scores['Storage']}/100", f"Weight: {int(weights_used['Storage']*100)}%")
            sc5.metric("💰 Value / Fit", f"{sub_scores['Value']}/100", f"Weight: {int(weights_used['Value']*100)}%")

        # Visualizations: Gauge & Radar
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(create_gauge_chart(suitability, f"{selected_phone['name']} Match Meter"), use_container_width=True)
        with col_g2:
            radar_cats = list(sub_scores.keys())
            radar_vals = list(sub_scores.values())
            st.plotly_chart(create_radar_chart(radar_cats, radar_vals, f"{selected_phone['name']} Capability Radar"), use_container_width=True)

        # Pros and Cons
        st.markdown("### ⚖️ Good & Weak Points")
        col_pro, col_con = st.columns(2)
        with col_pro:
            st.markdown("#### ✅ Advantages (Pros)")
            for p in pros:
                render_html(f'<div class="pro-box">✓ {p}</div>')
        with col_con:
            st.markdown("#### ❌ Disadvantages (Cons)")
            for c in cons:
                render_html(f'<div class="con-box">✗ {c}</div>')

        st.markdown("---")
        # Quick Catalog Grid
        st.markdown("### 📱 Browse All Models in Catalogue")
        st.write("Click any model in the dropdown above or inspect key specs below:")

        grid_cols = st.columns(3)
        for idx, row in st.session_state.phones_df.iterrows():
            p_dict = row.to_dict()
            p_score, _, _ = calculate_suitability_score(p_dict, user_needs, user_budget)
            col_target = grid_cols[idx % 3]
            with col_target:
                is_selected = (p_dict["name"] == selected_name)
                border_style = "border: 2px solid #0284C7;" if is_selected else "border: 1px solid #E2E8F0;"
                render_html(f"""
                <div class="phone-card" style="{border_style} padding: 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.78rem; font-weight: 700; color: #0284C7; text-transform: uppercase;">
                            {p_dict.get('brand', 'Tech')}
                        </span>
                        <span style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">
                            ${p_dict['price']}
                        </span>
                    </div>
                    <h4 style="margin: 4px 0 8px 0; font-size: 1.15rem;">{p_dict['name']}</h4>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
                        <div>
                            <div style="font-size: 0.82rem; color: #475569;">RAM: <b>{p_dict['ram_gb']}GB</b></div>
                            <div style="font-size: 0.82rem; color: #475569;">Storage: <b>{p_dict['storage_gb']}GB</b></div>
                            <div style="font-size: 0.82rem; color: #475569;">Battery: <b>{p_dict['battery_mah']}mAh</b></div>
                        </div>
                        <div>
                            {render_circular_score(p_score, size=52)}
                        </div>
                    </div>
                </div>
                """)

    # ==========================================================================
    # PAGE 2: ADD SMARTPHONE
    # ==========================================================================
    elif page_selected == "Add Smartphone":
        render_html("""
        <div class="phone-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%);">
            <span style="background: #E0F2FE; color: #0284C7; font-weight: 700; font-size: 0.78rem; padding: 4px 12px; border-radius: 20px; text-transform: uppercase;">
                ➕ Device Registration
            </span>
            <h1 style="margin: 8px 0 4px 0;">Add Custom Smartphone</h1>
            <p style="color: #475569; margin: 0;">
                Add any phone specifications to evaluate and compare it immediately against the catalogue.
            </p>
        </div>
        """)

        with st.form("add_phone_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.markdown("#### 📱 Identity & Memory")
                new_name = st.text_input("Smartphone Model Name*", placeholder="e.g. Pixel 8a or Galaxy A55")
                new_brand = st.text_input("Brand", placeholder="e.g. Google, Samsung, Xiaomi")
                new_price = st.number_input("Retail Price ($ USD)*", min_value=50, max_value=2500, value=399, step=10)
                new_ram = st.selectbox("RAM (GB)*", [4, 6, 8, 12, 16, 24], index=2)
                new_storage = st.selectbox("Internal Storage (GB)*", [64, 128, 256, 512, 1024], index=1)
                new_battery = st.number_input("Battery Capacity (mAh)*", min_value=2000, max_value=8000, value=5000, step=100)

            with col_f2:
                st.markdown("#### ⚡ Processor, Camera & Display")
                new_proc_tier = st.selectbox("Processor Tier*", ["Entry", "Budget", "Mid-range", "Upper Mid-range", "Flagship"], index=2)
                new_proc_name = st.text_input("Processor Name / Chipset*", placeholder="e.g. Snapdragon 7s Gen 2")
                new_main_cam = st.number_input("Main Camera Resolution (MP)*", min_value=8, max_value=200, value=50, step=2)
                new_front_cam = st.number_input("Front Camera (MP)", min_value=5, max_value=64, value=16, step=1)
                new_charging = st.number_input("Charging Speed (Watts)", min_value=10, max_value=240, value=33, step=5)
                
                col_sub_ois, col_sub_screen = st.columns(2)
                with col_sub_ois:
                    new_ois = st.checkbox("Optical Image Stabilization (OIS)", value=True)
                with col_sub_screen:
                    new_screen = st.selectbox("Screen Type", ["AMOLED", "OLED", "LCD", "LTPO AMOLED"], index=0)
                
                new_refresh = st.selectbox("Screen Refresh Rate", [60, 90, 120, 144, 165], index=2)

            submitted = st.form_submit_button("🚀 Save Smartphone & Calculate Score", use_container_width=True)

            if submitted:
                if not new_name.strip() or not new_proc_name.strip():
                    st.error("Please enter a valid Phone Model Name and Processor Name.")
                else:
                    new_entry = {
                        "name": new_name.strip(),
                        "brand": new_brand.strip() if new_brand.strip() else "Custom",
                        "price": int(new_price),
                        "ram_gb": int(new_ram),
                        "storage_gb": int(new_storage),
                        "battery_mah": int(new_battery),
                        "charging_w": int(new_charging),
                        "processor_tier": new_proc_tier,
                        "processor_name": new_proc_name.strip(),
                        "main_camera_mp": int(new_main_cam),
                        "front_camera_mp": int(new_front_cam),
                        "has_ois": bool(new_ois),
                        "screen_type": new_screen,
                        "screen_refresh_hz": int(new_refresh)
                    }

                    existing_names = st.session_state.phones_df["name"].str.lower().tolist()
                    if new_name.strip().lower() in existing_names:
                        idx = st.session_state.phones_df[st.session_state.phones_df["name"].str.lower() == new_name.strip().lower()].index[0]
                        for k, v in new_entry.items():
                            st.session_state.phones_df.at[idx, k] = v
                        st.success(f"Updated existing phone **{new_name.strip()}** with new specifications!")
                    else:
                        new_df = pd.DataFrame([new_entry])
                        st.session_state.phones_df = pd.concat([st.session_state.phones_df, new_df], ignore_index=True)
                        st.success(f"🎉 **{new_name.strip()}** successfully added! It is now available for evaluation and comparison across all pages.")

    # ==========================================================================
    # PAGE 3: COMPARE PHONES
    # ==========================================================================
    elif page_selected == "Compare Phones":
        render_html("""
        <div class="phone-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F5F3FF 100%);">
            <span style="background: #EDE9FE; color: #7C3AED; font-weight: 700; font-size: 0.78rem; padding: 4px 12px; border-radius: 20px; text-transform: uppercase;">
                ⚖️ Head-to-Head Showdown
            </span>
            <h1 style="margin: 8px 0 4px 0;">Side-by-Side Smartphone Comparison</h1>
            <p style="color: #475569; margin: 0;">
                Compare specifications, multi-dimension radar capabilities, pros/cons, and final suitability verdicts.
            </p>
        </div>
        """)

        all_names = st.session_state.phones_df["name"].tolist()
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            phone_a_name = st.selectbox("Select Phone A:", all_names, index=0, key="nav_cmp_a")
        with col_c2:
            default_b_idx = 1 if len(all_names) > 1 else 0
            phone_b_name = st.selectbox("Select Phone B:", all_names, index=default_b_idx, key="nav_cmp_b")

        phone_a = st.session_state.phones_df[st.session_state.phones_df["name"] == phone_a_name].iloc[0].to_dict()
        phone_b = st.session_state.phones_df[st.session_state.phones_df["name"] == phone_b_name].iloc[0].to_dict()

        # Compute scores & pros/cons
        score_a, sub_a, _ = calculate_suitability_score(phone_a, user_needs, user_budget)
        score_b, sub_b, _ = calculate_suitability_score(phone_b, user_needs, user_budget)
        pros_a, cons_a = generate_pros_and_cons(phone_a, user_budget, user_needs)
        pros_b, cons_b = generate_pros_and_cons(phone_b, user_budget, user_needs)

        # Side-by-side Product Cards
        col_card_a, col_card_b = st.columns(2)
        with col_card_a:
            render_html(f"""
            <div class="phone-card" style="border-top: 5px solid #0284C7;">
                <div style="display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">
                    <div style="flex-shrink: 0;">
                        {render_phone_svg(phone_a, width=100, height=170)}
                    </div>
                    <div style="flex-grow: 1; min-width: 150px;">
                        <span style="color: #0284C7; font-weight: 800; font-size: 0.8rem; text-transform: uppercase;">PHONE A</span>
                        <h3 style="margin: 2px 0 6px 0;">{phone_a['name']}</h3>
                        <div class="price-badge" style="font-size: 1.3rem;">${phone_a['price']}</div>
                        <div style="margin-top: 10px;">
                            {render_circular_score(score_a, size=58)}
                        </div>
                    </div>
                </div>
            </div>
            """)

        with col_card_b:
            render_html(f"""
            <div class="phone-card" style="border-top: 5px solid #8B5CF6;">
                <div style="display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">
                    <div style="flex-shrink: 0;">
                        {render_phone_svg(phone_b, width=100, height=170)}
                    </div>
                    <div style="flex-grow: 1; min-width: 150px;">
                        <span style="color: #8B5CF6; font-weight: 800; font-size: 0.8rem; text-transform: uppercase;">PHONE B</span>
                        <h3 style="margin: 2px 0 6px 0;">{phone_b['name']}</h3>
                        <div class="price-badge" style="font-size: 1.3rem;">${phone_b['price']}</div>
                        <div style="margin-top: 10px;">
                            {render_circular_score(score_b, size=58)}
                        </div>
                    </div>
                </div>
            </div>
            """)

        # Multi-dimension Radar Comparison
        st.markdown("#### 📊 Capability Radar Comparison (Phone A vs Phone B)")
        st.plotly_chart(create_comparison_radar(sub_a, sub_b, phone_a['name'], phone_b['name']), use_container_width=True)

        # Specification Showdown Table
        st.markdown("#### 📋 Detailed Specification Showdown")
        spec_rows = [
            ("Retail Price", f"${phone_a['price']}", f"${phone_b['price']}", "Cheaper" if phone_a['price'] < phone_b['price'] else ("Cheaper" if phone_b['price'] < phone_a['price'] else "Equal")),
            ("Suitability Score", f"{score_a} / 100", f"{score_b} / 100", phone_a['name'] if score_a > score_b else (phone_b['name'] if score_b > score_a else "Tie")),
            ("RAM", f"{phone_a['ram_gb']} GB", f"{phone_b['ram_gb']} GB", phone_a['name'] if phone_a['ram_gb'] > phone_b['ram_gb'] else (phone_b['name'] if phone_b['ram_gb'] > phone_a['ram_gb'] else "Tie")),
            ("Storage", f"{phone_a['storage_gb']} GB", f"{phone_b['storage_gb']} GB", phone_a['name'] if phone_a['storage_gb'] > phone_b['storage_gb'] else (phone_b['name'] if phone_b['storage_gb'] > phone_a['storage_gb'] else "Tie")),
            ("Battery Capacity", f"{phone_a['battery_mah']} mAh", f"{phone_b['battery_mah']} mAh", phone_a['name'] if phone_a['battery_mah'] > phone_b['battery_mah'] else (phone_b['name'] if phone_b['battery_mah'] > phone_a['battery_mah'] else "Tie")),
            ("Fast Charging", f"{phone_a['charging_w']} W", f"{phone_b['charging_w']} W", phone_a['name'] if phone_a['charging_w'] > phone_b['charging_w'] else (phone_b['name'] if phone_b['charging_w'] > phone_a['charging_w'] else "Tie")),
            ("Processor Tier", f"{phone_a['processor_tier']}", f"{phone_b['processor_tier']}", "-"),
            ("Processor Name", f"{phone_a['processor_name']}", f"{phone_b['processor_name']}", "-"),
            ("Main Camera", f"{phone_a['main_camera_mp']} MP", f"{phone_b['main_camera_mp']} MP", phone_a['name'] if phone_a['main_camera_mp'] > phone_b['main_camera_mp'] else (phone_b['name'] if phone_b['main_camera_mp'] > phone_a['main_camera_mp'] else "Tie")),
            ("Selfie Camera", f"{phone_a['front_camera_mp']} MP", f"{phone_b['front_camera_mp']} MP", phone_a['name'] if phone_a['front_camera_mp'] > phone_b['front_camera_mp'] else (phone_b['name'] if phone_b['front_camera_mp'] > phone_a['front_camera_mp'] else "Tie")),
            ("OIS Stabilization", "Yes" if phone_a.get('has_ois') else "No", "Yes" if phone_b.get('has_ois') else "No", "-"),
            ("Screen Type", f"{phone_a.get('screen_type', 'AMOLED')}", f"{phone_b.get('screen_type', 'AMOLED')}", "-"),
            ("Refresh Rate", f"{phone_a.get('screen_refresh_hz', 120)} Hz", f"{phone_b.get('screen_refresh_hz', 120)} Hz", phone_a['name'] if phone_a.get('screen_refresh_hz', 60) > phone_b.get('screen_refresh_hz', 60) else (phone_b['name'] if phone_b.get('screen_refresh_hz', 60) > phone_a.get('screen_refresh_hz', 60) else "Tie"))
        ]

        cmp_df = pd.DataFrame(spec_rows, columns=["Specification", phone_a_name, phone_b_name, "Edge / Leader"])
        st.dataframe(cmp_df, use_container_width=True, hide_index=True)

        # Side-by-side Pros and Cons
        st.markdown("#### ⚖️ Side-by-Side Pros and Cons")
        col_p_a, col_p_b = st.columns(2)
        with col_p_a:
            st.markdown(f"**Strengths of {phone_a['name']}:**")
            for p in pros_a[:3]:
                render_html(f'<div class="pro-box">✓ {p}</div>')
            st.markdown(f"**Weaknesses of {phone_a['name']}:**")
            for c in cons_a[:2]:
                render_html(f'<div class="con-box">✗ {c}</div>')

        with col_p_b:
            st.markdown(f"**Strengths of {phone_b['name']}:**")
            for p in pros_b[:3]:
                render_html(f'<div class="pro-box">✓ {p}</div>')
            st.markdown(f"**Weaknesses of {phone_b['name']}:**")
            for c in cons_b[:2]:
                render_html(f'<div class="con-box">✗ {c}</div>')

        # Comparative Verdict
        diff_score = abs(score_a - score_b)
        winner_name = phone_a['name'] if score_a >= score_b else phone_b['name']
        winner_score = max(score_a, score_b)
        runner_up = phone_b['name'] if score_a >= score_b else phone_a['name']

        render_html(f"""
        <div class="phone-card" style="background: linear-gradient(135deg, #F0F9FF 0%, #EDE9FE 100%); border: 2px solid #8B5CF6;">
            <h4 style="color: #6D28D9; margin: 0 0 8px 0; font-size: 1.15rem;">🎯 Head-to-Head PhoneWise Recommendation</h4>
            <p style="font-size: 1.05rem; line-height: 1.6; color: #1E293B; margin-bottom: 0;">
                For your target budget of <b>${user_budget}</b> and priorities (<b>{", ".join(user_needs) if user_needs else "Everyday use"}</b>), 
                <span style="color: #0284C7; font-weight: 800;">{winner_name}</span> is the more suitable choice with a score of 
                <b>{winner_score}/100</b> (a <b>{diff_score:.1f} point</b> advantage over {runner_up}).
            </p>
        </div>
        """)

    # ==========================================================================
    # PAGE 4: RECOMMENDATIONS
    # ==========================================================================
    elif page_selected == "Recommendations":
        render_html(f"""
        <div class="phone-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #ECFDF5 100%);">
            <span style="background: #D1FAE5; color: #065F46; font-weight: 700; font-size: 0.78rem; padding: 4px 12px; border-radius: 20px; text-transform: uppercase;">
                🎯 Smart Decision Engine
            </span>
            <h1 style="margin: 8px 0 4px 0;">Budget & Needs Recommendations</h1>
            <p style="color: #475569; margin: 0;">
                Ranked results across all smartphones for your <b>${user_budget}</b> budget ceiling.
            </p>
        </div>
        """)

        all_evaluated = []
        for idx, row in st.session_state.phones_df.iterrows():
            p_dict = row.to_dict()
            f_score, s_scores, _ = calculate_suitability_score(p_dict, user_needs, user_budget)
            all_evaluated.append({
                "name": p_dict["name"],
                "brand": p_dict.get("brand", "Generic"),
                "price": p_dict["price"],
                "suitability_score": f_score,
                "performance_score": s_scores["Performance"],
                "camera_score": s_scores["Camera"],
                "battery_score": s_scores["Battery"],
                "value_score": s_scores["Value"],
                "ram_gb": p_dict["ram_gb"],
                "storage_gb": p_dict["storage_gb"],
                "battery_mah": p_dict["battery_mah"],
                "in_budget": p_dict["price"] <= user_budget,
                "price_diff": p_dict["price"] - user_budget
            })

        eval_df = pd.DataFrame(all_evaluated)
        eval_df["Budget Status"] = eval_df["in_budget"].map({True: "Within Budget", False: "Exceeds Budget"})

        within_budget_df = eval_df[eval_df["in_budget"]].copy().sort_values(by="suitability_score", ascending=False)
        all_ranked_df = eval_df.sort_values(by="suitability_score", ascending=False)

        if not within_budget_df.empty:
            best_phone = within_budget_df.iloc[0]
            within_budget_df["value_ratio"] = within_budget_df["suitability_score"] / within_budget_df["price"]
            best_value_phone = within_budget_df.sort_values(by="value_ratio", ascending=False).iloc[0]

            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                render_html(f"""
                <div class="best-rec-card">
                    <span style="color: #065F46; font-weight: 800; font-size: 0.8rem; letter-spacing: 0.05em; text-transform: uppercase;">
                        👑 BEST OVERALL MATCH (IN BUDGET)
                    </span>
                    <h2 style="margin: 6px 0 2px 0; font-size: 1.8rem; color: #064E3B !important;">{best_phone['name']}</h2>
                    <div style="color: #047857; font-size: 0.9rem; font-weight: 500;">
                        {best_phone['brand']} &bull; {best_phone['ram_gb']}GB RAM &bull; {best_phone['battery_mah']}mAh Battery
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px;">
                        <span class="price-badge" style="background: #FFFFFF; color: #065F46; border-color: #A7F3D0;">
                            ${best_phone['price']}
                        </span>
                        {render_circular_score(best_phone['suitability_score'], size=56)}
                    </div>
                </div>
                """)

            with col_rec2:
                render_html(f"""
                <div class="value-pick-card">
                    <span style="color: #0369A1; font-weight: 800; font-size: 0.8rem; letter-spacing: 0.05em; text-transform: uppercase;">
                        💎 BEST VALUE FOR MONEY
                    </span>
                    <h2 style="margin: 6px 0 2px 0; font-size: 1.8rem; color: #0C4A6E !important;">{best_value_phone['name']}</h2>
                    <div style="color: #0284C7; font-size: 0.9rem; font-weight: 500;">
                        {best_value_phone['brand']} &bull; Maximum hardware performance delivered per dollar
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px;">
                        <span class="price-badge" style="background: #FFFFFF; color: #0369A1; border-color: #BAE6FD;">
                            ${best_value_phone['price']}
                        </span>
                        {render_circular_score(best_value_phone['suitability_score'], size=56)}
                    </div>
                </div>
                """)
        else:
            st.warning(f"No phones in the catalog are currently under your ${user_budget} budget. Consider adjusting your budget slider.")

        # Ranked Bar Chart
        st.markdown("#### 📊 Ranked Suitability Scores")
        fig_bar = px.bar(
            eval_df.sort_values(by="suitability_score", ascending=True),
            x="suitability_score",
            y="name",
            orientation="h",
            color="Budget Status",
            color_discrete_map={"Within Budget": "#10B981", "Exceeds Budget": "#94A3B8"},
            text="suitability_score",
            labels={"suitability_score": "Suitability Score (0-100)", "name": "Smartphone"},
            title="All Smartphones Evaluated for Your Profile"
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0F172A', family='sans-serif'),
            xaxis=dict(range=[0, 105], gridcolor='#E2E8F0'),
            yaxis=dict(gridcolor='#E2E8F0'),
            height=380,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Full Table
        st.markdown("#### 📑 Complete Phone Catalogue & Suitability Table")
        filter_budget_only = st.checkbox("Show only phones within budget ceiling", value=False)
        
        table_source = within_budget_df if filter_budget_only else all_ranked_df
        display_df = table_source[[
            "name", "brand", "price", "suitability_score", "ram_gb", "storage_gb", "battery_mah", "Budget Status"
        ]].rename(columns={
            "name": "Phone Name",
            "brand": "Brand",
            "price": "Price ($)",
            "suitability_score": "Suitability (/100)",
            "ram_gb": "RAM (GB)",
            "storage_gb": "Storage (GB)",
            "battery_mah": "Battery (mAh)"
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # ==========================================================================
    # PAGE 5: ABOUT
    # ==========================================================================
    elif page_selected == "About":
        render_html("""
        <div class="phone-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);">
            <span style="background: #E2E8F0; color: #334155; font-weight: 700; font-size: 0.78rem; padding: 4px 12px; border-radius: 20px; text-transform: uppercase;">
                ℹ️ About PhoneWise
            </span>
            <h1 style="margin: 8px 0 4px 0;">Methodology, Scoring & Principles</h1>
            <p style="color: #475569; margin: 0;">
                PhoneWise is an open, transparent smartphone purchasing decision assistant built with Python, Streamlit, Pandas, and Plotly.
            </p>
        </div>
        """)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            render_html("""
            <div class="inner-card-grey">
                <h4 style="color:#0284C7 !important;">📐 1. Five Foundation Dimensions (0-100 each)</h4>
                <ul style="color: #334155; font-size: 0.92rem; line-height: 1.6;">
                    <li><b>Performance (🚀):</b> Combines Processor Tier (Entry: 45, Budget: 60, Mid-range: 75, Upper Mid: 88, Flagship: 100) with RAM capacity (scaled up to 16GB).</li>
                    <li><b>Camera (📸):</b> Main camera resolution + Selfie camera + 20-point bonus for Optical Image Stabilization (OIS).</li>
                    <li><b>Battery (🔋):</b> Battery capacity (scaled up to 6,000 mAh) + fast charging wattage.</li>
                    <li><b>Storage (💾):</b> Evaluates onboard internal capacity (64GB=50, 128GB=75, 256GB=92, 512GB+=100).</li>
                    <li><b>Value for Money (💰):</b> Hardware capability delivered per dollar compared against the user's budget target.</li>
                </ul>
            </div>
            """)

        with col_m2:
            render_html("""
            <div class="inner-card-grey">
                <h4 style="color:#8B5CF6 !important;">⚖️ 2. Dynamic Priority Weighting</h4>
                <ul style="color: #334155; font-size: 0.92rem; line-height: 1.6;">
                    <li><b>Gaming:</b> Performance (40%), Battery (25%), Storage (15%), Value (15%), Camera (5%).</li>
                    <li><b>Photography:</b> Camera (45%), Storage (20%), Performance (15%), Battery (10%), Value (10%).</li>
                    <li><b>Online Classes:</b> Battery (35%), Performance (25%), Camera (15%), Storage (15%), Value (10%).</li>
                    <li><b>Everyday Use:</b> Battery (30%), Value (30%), Performance (20%), Camera (10%), Storage (10%).</li>
                    <li><b>Multitasking:</b> Performance (45%), Storage (20%), Battery (15%), Value (15%), Camera (5%).</li>
                </ul>
            </div>
            """)

        render_html("""
        <div class="disclaimer-card">
            <strong>⚠️ IMPORTANT TRANSPARENCY DISCLAIMER:</strong><br>
            All suitability scores, pillar ratings, and recommendations produced by PhoneWise are estimated 
            heuristic scores derived mathematically from manufacturer hardware specifications and user-selected priorities. 
            They do <strong>not</strong> represent physical laboratory benchmark measurements (such as AnTuTu, Geekbench, or DxOMark) 
            and should be used as educational purchasing guidance rather than absolute lab metrics.
        </div>
        """)

    # ==========================================================================
    # GLOBAL FOOTER
    # ==========================================================================
    render_html("<br><hr style='border-color: #E2E8F0;'>")
    col_foot1, col_foot2 = st.columns([2, 1])
    with col_foot1:
        render_html("<span style='color: #64748B; font-size: 0.84rem;'>PhoneWise &copy; 2026 &bull; Built with Python, Streamlit, Pandas & Plotly</span>")
    with col_foot2:
        render_html("<div style='text-align: right; color: #64748B; font-size: 0.84rem;'>No external paid APIs required &bull; 100% Offline</div>")

if __name__ == "__main__":
    main()
