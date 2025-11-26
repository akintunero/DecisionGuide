import json
from pathlib import Path

import streamlit as st

from utils.export import export_to_pdf, export_to_json, export_to_text, get_filename

st.set_page_config(
page_title=“DecisionGuide”,
page_icon=“🎯”,
layout=“wide”,
initial_sidebar_state=“collapsed”
)

# Exceptional Design - Modern, Bold, and Memorable

st.markdown(”””

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Reset and Base */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
    }
    
    /* Typography - Everything visible */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown span, .stMarkdown div {
        color: #ffffff !important;
    }
    
    /* Radio buttons - CRITICAL FIX */
    .stRadio > label {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    .stRadio [role="radiogroup"] {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stRadio [role="radiogroup"] label {
        color: #e5e7eb !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 1rem 1.25rem !important;
        margin: 0.5rem 0 !important;
        background: rgba(139, 92, 246, 0.08);
        border-radius: 12px;
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        display: block;
    }
    
    .stRadio [role="radiogroup"] label:hover {
        background: rgba(139, 92, 246, 0.15);
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateX(8px);
    }
    
    .stRadio [role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(59, 130, 246, 0.25));
        border-color: #8b5cf6;
        transform: translateX(12px);
    }
    
    .stRadio [role="radiogroup"] label span {
        color: #ffffff !important;
    }
    
    /* Info boxes */
    div[data-baseweb="notification"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px);
    }
    
    div[data-baseweb="notification"] * {
        color: #ffffff !important;
    }
    
    /* Success boxes */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 16px !important;
    }
    
    /* Animated Gradient Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(236, 72, 153, 0.1) 0%, transparent 50%);
        animation: gradientShift 15s ease infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes gradientShift {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.1); }
    }
    
    .block-container {
        position: relative;
        z-index: 1;
    }
    
    /* Hero Section - Cinematic */
    .hero-section {
        position: relative;
        padding: 8rem 2rem;
        text-align: center;
        margin: 2rem auto 4rem auto;
        max-width: 1400px;
        overflow: hidden;
    }
    
    .hero-glow {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 800px;
        height: 800px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
        filter: blur(80px);
        animation: pulseGlow 8s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
        50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #c4b5fd;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .hero-logo {
        font-size: 8rem;
        margin-bottom: 2rem;
        filter: drop-shadow(0 0 40px rgba(139, 92, 246, 0.6));
        animation: float 6s ease-in-out infinite;
        display: inline-block;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-20px) rotate(5deg); }
        75% { transform: translateY(-10px) rotate(-5deg); }
    }
    
    .hero-title {
        font-size: 6rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -3px;
        line-height: 1.1;
        animation: titleShine 3s ease-in-out infinite;
    }
    
    @keyframes titleShine {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #9ca3af;
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    .hero-description {
        font-size: 1.25rem;
        color: #6b7280;
        max-width: 800px;
        margin: 0 auto 3rem auto;
        line-height: 1.8;
    }
    
    .hero-cta {
        display: inline-flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .cta-primary {
        padding: 1rem 2.5rem;
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 40px rgba(139, 92, 246, 0.3);
    }
    
    .cta-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 50px rgba(139, 92, 246, 0.5);
    }
    
    /* Feature Grid - Bento Box Style */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        max-width: 1400px;
        margin: 4rem auto;
        padding: 0 2rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #8b5cf6, #3b82f6, #ec4899);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.6s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: rgba(139, 92, 246, 0.5);
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.2);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.5));
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.2) rotate(10deg);
    }
    
    .feature-title {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    .feature-text {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #9ca3af;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        max-width: 900px;
        margin: 6rem auto 4rem auto;
        padding: 0 2rem;
    }
    
    .section-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #c4b5fd;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -2px;
    }
    
    .section-subtitle {
        font-size: 1.25rem;
        color: #6b7280;
        line-height: 1.7;
    }
    
    /* Assessment Cards - Premium Design */
    .assessments-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .assessment-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .assessment-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
    }
    
    .assessment-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: rgba(139, 92, 246, 0.6);
        background: rgba(255, 255, 255, 0.06);
        box-shadow: 0 30px 80px rgba(139, 92, 246, 0.3);
    }
    
    .assessment-card:hover::after {
        opacity: 1;
    }
    
    .assessment-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.6));
        position: relative;
        z-index: 2;
    }
    
    .assessment-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #ffffff;
        position: relative;
        z-index: 2;
    }
    
    .assessment-description {
        font-size: 1.05rem;
        color: #9ca3af;
        line-height: 1.7;
        flex-grow: 1;
        position: relative;
        z-index: 2;
    }
    
    .assessment-arrow {
        font-size: 1.5rem;
        color: #8b5cf6;
        margin-top: 1.5rem;
        transition: transform 0.3s ease;
        position: relative;
        z-index: 2;
    }
    
    .assessment-card:hover .assessment-arrow {
        transform: translateX(10px);
    }
    
    /* Use Cases - Modern Cards */
    .use-cases-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .use-case-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        transition: all 0.3s ease;
    }
    
    .use-case-card:hover {
        transform: translateY(-5px);
        border-color: rgba(139, 92, 246, 0.4);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .use-case-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .use-case-card ul {
        list-style: none;
        padding: 0;
    }
    
    .use-case-card li {
        color: #9ca3af;
        margin-bottom: 1rem;
        padding-left: 1.5rem;
        position: relative;
        line-height: 1.6;
    }
    
    .use-case-card li::before {
        content: '→';
        position: absolute;
        left: 0;
        color: #8b5cf6;
        font-weight: bold;
    }
    
    /* CTA Section - Magnetic */
    .cta-section {
        max-width: 1200px;
        margin: 6rem auto;
        padding: 5rem 3rem;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.1));
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .cta-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.2) 0%, transparent 70%);
        animation: rotateCta 20s linear infinite;
    }
    
    @keyframes rotateCta {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .cta-content {
        position: relative;
        z-index: 1;
    }
    
    .cta-title {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .cta-text {
        font-size: 1.25rem;
        color: #9ca3af;
        margin-bottom: 2rem;
    }
    
    /* Footer - Minimal */
    .footer {
        max-width: 1200px;
        margin: 4rem auto 2rem auto;
        padding: 3rem 2rem;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .footer-text {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    .footer-links {
        display: flex;
        gap: 2rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    
    .footer-link {
        color: #8b5cf6;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 1.05rem;
    }
    
    .footer-link:hover {
        color: #c4b5fd;
        transform: translateY(-2px);
    }
    
    .footer-credit {
        font-size: 0.95rem;
        color: #4b5563;
    }
    
    /* Buttons - Exceptional */
    .stButton>button {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.5) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Download Buttons */
    .stDownloadButton>button {
        background: rgba(139, 92, 246, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        padding: 0.875rem 2rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }
    
    .stDownloadButton>button:hover {
        background: rgba(139, 92, 246, 0.2) !important;
        border-color: rgba(139, 92, 246, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Assessment Page Styling */
    .assessment-page-header {
        text-align: center;
        margin: 3rem auto;
        max-width: 900px;
    }
    
    .assessment-page-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .question-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 900px;
    }
    
    .question-number {
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8b5cf6;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .result-container {
        background: rgba(16, 185, 129, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 900px;
    }
    
    .result-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 1rem;
    }
    
    .path-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 900px;
    }
    
    .path-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
    }
    
    .path-step {
        color: #9ca3af;
        margin-bottom: 1rem;
        padding-left: 2rem;
        position: relative;
        line-height: 1.6;
    }
    
    .path-step::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0.5rem;
        width: 8px;
        height: 8px;
        background: #8b5cf6;
        border-radius: 50%;
    }
    
    /* Dividers */
    hr {
        margin: 3rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), transparent);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-logo {
            font-size: 5rem;
        }
        
        .hero-title {
            font-size: 3.5rem;
            letter-spacing: -2px;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
        }
        
        .section-title {
            font-size: 2.5rem;
        }
        
        .features-grid,
        .assessments-grid,
        .use-cases-grid {
            grid-template-columns: 1fr;
            padding: 0 1rem;
        }
        
        .cta-title {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
    }
    
    /* Smooth everything */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
</style>

“””, unsafe_allow_html=True)

LOGIC_DIR = Path(**file**).parent / “logic”

def load_trees():
trees = {}
for path in LOGIC_DIR.glob(”*.json”):
try:
with path.open(“r”, encoding=“utf-8”) as f:
data = json.load(f)
tree_id = data.get(“id”) or path.stem
trees[tree_id] = data
except Exception as e:
print(f”Failed to load {path}: {e}”)
return trees

def show_landing_page():
“”“Display exceptional landing page”””

```
# Hero Section
st.markdown("""
<div class='hero-section'>
    <div class='hero-glow'></div>
    <div class='hero-content'>
        <div class='hero-badge'>Open Source • Privacy First • Audit Ready</div>
        <div class='hero-logo'>🎯</div>
        <h1 class='hero-title'>DecisionGuide</h1>
        <p class='hero-subtitle'>The assessment framework that thinks like you do</p>
        <p class='hero-description'>
            Transform complex GRC assessments into clear, defensible decisions. 
            Built for professionals who refuse to compromise on quality, transparency, or privacy.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class='section-header'>
    <div class='section-badge'>Why DecisionGuide</div>
    <h2 class='section-title'>Built Different</h2>
    <p class='section-subtitle'>
        Not just another assessment tool. A complete rethinking of how GRC professionals should work.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🔍</div>
        <div class='feature-title'>Crystal Clear Logic</div>
        <div class='feature-text'>
            Every decision mapped, every path documented, every conclusion defensible. 
            See exactly how you got from question to answer.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🔒</div>
        <div class='feature-title'>Zero Trust Architecture</div>
        <div class='feature-text'>
            No uploads. No cloud storage. No data collection. Your assessments stay yours. 
            Privacy isn't a feature—it's the foundation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>⚡</div>
        <div class='feature-title'>Production Ready</div>
        <div class='feature-text'>
            Export audit trails in seconds. PDF reports that look professional. 
            JSON data for system integration. Built for real work.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Assessments Section
st.markdown("""
<div class='section-header'>
    <div class='section-badge'>Get Started</div>
    <h2 class='section-title'>Choose Your Assessment</h2>
    <p class='section-subtitle'>
        Each assessment is battle-tested, professionally crafted, and ready to use.
    </p>
</div>
""", unsafe_allow_html=True)

trees = load_trees()

assessment_styles = [
    {"icon": "🔐", "color": "#8b5cf6"},
    {"icon": "⚖️", "color": "#3b82f6"},
    {"icon": "🛡️", "color": "#ec4899"},
]

cols = st.columns(min(len(trees), 3))

for idx, (tree_id, tree_data) in enumerate(trees.items()):
    with cols[idx % 3]:
        style = assessment_styles[idx % len(assessment_styles)]
        
        st.markdown(f"""
        <div class='assessment-card'>
            <div class='assessment-icon'>{style["icon"]}</div>
            <div class='assessment-title'>{tree_data.get('title', 'Assessment')}</div>
            <div class='assessment-description'>{tree_data.get('description', '')}</div>
            <div class='assessment-arrow'>→</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Launch Assessment", key=f"start_{tree_id}", use_container_width=True):
            st.session_state.selected_tree = tree_id
            st.session_state.show_landing = False
            st.rerun()

# Use Cases Section
st.markdown("""
<div class='section-header'>
    <div class='section-badge'>Use Cases</div>
    <h2 class='section-title'>Who This Is For</h2>
    <p class='section-subtitle'>
        If you make decisions that matter, this tool is for you.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='use-case-card'>
        <div class='use-case-title'>👨‍💼 Auditors & Assessors</div>
        <ul>
            <li>Standardize assessment methodology across teams</li>
            <li>Generate defensible, documented decisions</li>
            <li>Export audit-ready reports instantly</li>
            <li>Eliminate subjective interpretation</li>
        </ul>
    </div>
    
    <div class='use-case-card'>
        <div class='use-case-title'>📊 Risk Professionals</div>
        <ul>
            <li>Classify vendors with repeatable logic</li>
            <li>Apply consistent risk tiering</li>
            <li>Document every decision's rationale</li>
            <li>Build organizational risk frameworks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='use-case-card'>
        <div class='use-case-title'>✅ Compliance Teams</div>
        <ul>
            <li>Navigate complex regulatory requirements</li>
            <li>Apply jurisdiction-specific rules accurately</li>
            <li>Maintain complete compliance trails</li>
            <li>Reduce assessment cycle time</li>
        </ul>
    </div>
    
    <div class='use-case-card'>
        <div class='use-case-title'>🛡️ Security Leaders</div>
        <ul>
            <li>Assess incident severity objectively</li>
            <li>Make confident reporting decisions</li>
            <li>Document response justifications</li>
            <li>Create consistent security protocols</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div class='cta-section'>
    <div class='cta-content'>
        <h2 class='cta-title'>Ready to Elevate Your Work?</h2>
        <p class='cta-text'>
            Join the GRC professionals who've moved beyond guesswork
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <div class='footer-title'>DecisionGuide</div>
    <p class='footer-text'>
        Making structured, defensible decisions—one assessment at a time
    </p>
    <div class='footer-links'>
        <a href='https://github.com/Adeshola3/DecisionGuide' target='_blank' class='footer-link'>
            ⭐ GitHub
        </a>
        <a href='https://github.com/Adeshola3/DecisionGuide/issues' target='_blank' class='footer-link'>
            💬 Contribute
        </a>
        <a href='https://github.com/Adeshola3/DecisionGuide#readme' target='_blank' class='footer-link'>
            📖 Documentation
        </a>
    </div>
    <p class='footer-credit'>
        Open Source • MIT License • Crafted by Adeshola
    </p>
</div>
""", unsafe_allow_html=True)
```

def show_assessment_page():
“”“Display assessment page”””
trees = load_trees()

```
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("← Back"):
        st.session_state.show_landing = True
        st.session_state.pop('selected_tree', None)
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

selected_tree_id = st.session_state.get('selected_tree')

if not selected_tree_id or selected_tree_id not in trees:
    st.error("❌ Assessment not found")
    return

tree = trees[selected_tree_id]

st.markdown(f"""
<div class='assessment-page-header'>
    <h1 class='assessment-page-title'>{tree.get('title', 'Assessment')}</h1>
</div>
""", unsafe_allow_html=True)

if tree.get("description"):
    st.info(f"ℹ️ {tree['description']}")

st.markdown("<hr>", unsafe_allow_html=True)

answers_key = f"answers_{selected_tree_id}"
result_key = f"result_{selected_tree_id}"

if answers_key not in st.session_state:
    st.session_state[answers_key] = {}

if result_key not in st.session_state:
    st.session_state[result_key] = None

answers = st.session_state[answers_key]
decision, explanation, path = traverse_tree_interactive(
    tree, 
    tree["root"], 
    answers, 
    []
)

if decision is not None:
    st.session_state[result_key] = {
        "decision": decision,
        "explanation": explanation,
        "path": path
    }

if st.session_state[result_key] is not None:
    st.success("✅ Assessment Complete!")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    result = st.session_state[result_key]
    
    st.markdown(f"""
    <div class='result-container'>
        <div class='result-title'>📊 Result</div>
        <p style='color: #ffffff; font-size: 1.1rem; margin-bottom: 0.5rem;'>
            <strong>Decision Code:</strong> {result['decision']}
        </p>
        {f"<p style='color: #9ca3af; font-size: 1rem; margin-top: 1rem;'>{result['explanation']}</p>" if result['explanation'] else ""}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='path-container'>
        <div class='path-title'>🗺️ Decision Path</div>
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(result['path'], 1):
        st.markdown(f"<div class='path-step'><strong>{i}.</strong> {step}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #ffffff; margin-bottom: 2rem;'>📥 Export Your Results</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pdf_buffer = export_to_pdf(
            tree.get("title", "Assessment"),
            result['decision'],
            result['explanation'],
            result['path']
        )
        st.download_button(
            label="📄 PDF Report",
            data=pdf_buffer,
            file_name=get_filename(tree.get("title", "Assessment"), "pdf"),
            mime="application/pdf",
            use_container_width=True
        )
    
    with col2:
        json_data = export_to_json(
            tree.get("title", "Assessment"),
            result['decision'],
            result['explanation'],
            result['path']
        )
        st.download_button(
            label="📋 JSON Data",
            data=json_data,
            file_name=get_filename(tree.get("title", "Assessment"), "json"),
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        text_data = export_to_text(
            tree.get("title", "Assessment"),
            result['decision'],
            result['explanation'],
            result['path']
        )
        st.download_button(
            label="📝 Text File",
            data=text_data,
            file_name=get_filename(tree.get("title", "Assessment"), "txt"),
            mime="text/plain",
            use_container_width=True
        )
    
    with col4:
        if st.button("🔄 New Assessment", use_container_width=True):
            st.session_state[answers_key] = {}
            st.session_state[result_key] = None
            st.rerun()
```

def traverse_tree_interactive(tree, node_id, answers, path_so_far):
“”“Interactively traverse the tree”””
nodes = tree[“nodes”]
node = nodes[node_id]

```
node_label = node.get("text", "")
node_type = node.get("type", "choice")

if node_type == "choice":
    current_question = len(answers) + 1
    
    st.markdown(f"""
    <div class='question-container'>
        <div class='question-number'>Question {current_question}</div>
    </div>
    """, unsafe_allow_html=True)
    
    options = list(node["options"].keys())
    
    if node_id in answers:
        selected = answers[node_id]
    else:
        selected = st.radio(
            node_label, 
            options, 
            key=f"{tree['id']}_{node_id}",
            index=None
        )
        
        if selected is None:
            return None, None, path_so_far
        
        answers[node_id] = selected
    
    path_entry = f"{node_label} → {selected}"
    new_path = path_so_far + [path_entry]
    
    selected_branch = node["options"][selected]
    
    if "decision" in selected_branch:
        decision = selected_branch["decision"]
        explanation = selected_branch.get("explanation", "")
        return decision, explanation, new_path
    
    next_node = selected_branch["next"]
    return traverse_tree_interactive(tree, next_node, answers, new_path)

elif node_type == "text":
    st.markdown(node_label)
    return None, None, path_so_far + [node_label]

else:
    st.warning(f"⚠️ Unknown node type: {node_type}")
    return None, None, path_so_far
```

def main():
if ‘show_landing’ not in st.session_state:
st.session_state.show_landing = True

```
if st.session_state.show_landing:
    show_landing_page()
else:
    show_assessment_page()
```

if **name** == “**main**”:
main()