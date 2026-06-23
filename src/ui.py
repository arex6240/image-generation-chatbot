import streamlit as st

def inject_custom_css():
    """
    Injects custom Google Fonts and premium CSS styles into the Streamlit app.
    Implements glassmorphism, gradient buttons, glowing borders, and animations.
    """
    css = """
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    h1, h2, h3, .main-title {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Header Gradient Banner */
    .header-container {
        padding: 2.5rem 1.5rem;
        background: linear-gradient(135deg, rgba(255, 51, 102, 0.05) 0%, rgba(153, 51, 255, 0.05) 100%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 51, 102, 0.1) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .main-title {
        background: linear-gradient(135deg, #FF3366 0%, #FF9933 50%, #9933FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.05em;
    }
    
    .subtitle {
        color: #B0B3B8;
        font-size: 1.15rem;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.03);
        border-color: rgba(255, 51, 102, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    /* Gallery/History Card Styling */
    .history-card {
        border-left: 4px solid #9933FF;
    }
    
    .history-prompt {
        font-weight: 500;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    .history-meta {
        font-size: 0.75rem;
        color: #7A7C85;
        display: flex;
        gap: 1rem;
    }
    
    .badge {
        padding: 0.2rem 0.6rem;
        border-radius: 100px;
        background: rgba(153, 51, 255, 0.15);
        color: #BE93FD;
        font-weight: 600;
        font-size: 0.75rem;
    }
    
    /* Custom Footer */
    .footer {
        margin-top: 5rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        color: #7A7C85;
        font-size: 0.85rem;
    }
    
    /* Image container wrapper for animations */
    .image-wrapper {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
    }
    
    .image-wrapper:hover {
        transform: scale(1.01);
        border-color: rgba(255, 51, 102, 0.4);
        box-shadow: 0 20px 50px rgba(255, 51, 102, 0.15);
    }
    
    /* Adjust standard streamlit button rules globally for premium feel */
    div.stButton > button {
        background: linear-gradient(135deg, #FF3366 0%, #9933FF 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 15px rgba(255, 51, 102, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 6px 20px rgba(255, 51, 102, 0.4) !important;
        transform: translateY(-2px) !important;
        opacity: 0.95;
    }
    
    div.stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Quick Pill Button styling */
    .quick-pill {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        font-size: 0.85rem;
        cursor: pointer;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    .quick-pill:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 51, 102, 0.3);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_header():
    """Renders the main header banner of the application."""
    header_html = """
    <div class="header-container">
        <div class="main-title">ImagineAI</div>
        <div class="subtitle">
            Generate stunning, high-fidelity artwork instantly. Select a creative style, craft your prompt, and watch AI breathe life into your imagination.
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_footer():
    """Renders the app footer."""
    footer_html = """
    <div class="footer">
        ImagineAI • Designed with ❤️ using Streamlit & Pollinations API • © 2026 All Rights Reserved
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def render_history_card(original_prompt, final_prompt, style, provider, size):
    """Renders a beautiful history item using HTML markup."""
    card_html = f"""
    <div class="glass-card history-card">
        <div class="history-prompt">"{original_prompt}"</div>
        <div style="font-size: 0.85rem; color: #8F9199; margin-bottom: 0.5rem; font-style: italic;">
            <b>Enhanced:</b> {final_prompt}
        </div>
        <div class="history-meta">
            <span>Style: <span class="badge">{style}</span></span>
            <span>Provider: <span class="badge" style="background: rgba(51, 153, 255, 0.15); color: #82C0FF;">{provider.title()}</span></span>
            <span>Resolution: <span class="badge" style="background: rgba(51, 255, 153, 0.15); color: #82FFC0;">{size}</span></span>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
