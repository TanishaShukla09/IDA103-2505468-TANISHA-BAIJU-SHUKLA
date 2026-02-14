import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# OpenRouter API Configuration
OPENROUTER_API_KEY = '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'
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Page configuration
st.set_page_config(
    page_title="ArtRestorer AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for museum-quality aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Cinzel:wght@400;600;700&family=Crimson+Text:wght@400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f1e8 0%, #e8dcc4 100%);
        background-attachment: fixed;
    }
    * { color: #2c1810 !important; }
    .main-header {
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #2c1810 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 3px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        font-weight: 300;
        color: #2c1810 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c1810 !important;
        font-family: 'Cinzel', serif !important;
    }
    p, span, div, li, a {
        color: #2c1810 !important;
        font-family: 'Crimson Text', serif !important;
    }
    .element-container, .stMarkdown, div[data-testid="stMarkdownContainer"] {
        background: transparent !important;
    }
    .custom-card {
        background: linear-gradient(145deg, rgba(248, 246, 240, 0.7) 0%, rgba(245, 241, 232, 0.7) 100%);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(44, 24, 16, 0.15);
        margin-bottom: 2rem;
        border: 1px solid rgba(139, 115, 85, 0.3);
    }
    .section-header {
        font-family: 'Cinzel', serif !important;
        font-size: 1.8rem !important;
        color: #2c1810 !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #8b7355 !important;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #2c1810 !important;
        color: #f5f1e8 !important;
        border: 1px solid #8b7355 !important;
        border-radius: 8px !important;
    }
    /* Force white text + dark bg on focus/active — prevents grey flash */
    .stTextArea > div > div > textarea,
    .stTextArea > div > div > textarea:focus,
    .stTextArea > div > div > textarea:active,
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:focus,
    .stTextInput > div > div > input:active {
        background-color: #2c1810 !important;
        color: #f5f1e8 !important;
        -webkit-text-fill-color: #f5f1e8 !important;
        -webkit-box-shadow: 0 0 0px 1000px #2c1810 inset !important;
        box-shadow: 0 0 0px 1000px #2c1810 inset !important;
    }
    /* Selectbox closed box — dark background, white text */
    .stSelectbox > div > div {
        background-color: #2c1810 !important;
        border: 1px solid #8b7355 !important;
        border-radius: 8px !important;
    }
    /* Force all text inside closed selectbox to be white */
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] input,
    .stSelectbox div[data-baseweb="select"] p {
        background-color: #2c1810 !important;
        color: #f5f1e8 !important;
        -webkit-text-fill-color: #f5f1e8 !important;
    }

    /* Open dropdown list — beige background, dark text */
    div[data-baseweb="popover"] { background-color: #f5f1e8 !important; }
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #f5f1e8 !important;
        border: 1px solid #8b7355 !important;
        border-radius: 8px !important;
    }
    div[role="option"],
    li[role="option"] {
        background-color: #f5f1e8 !important;
        color: #2c1810 !important;
        -webkit-text-fill-color: #2c1810 !important;
    }
    div[role="option"]:hover,
    li[role="option"]:hover {
        background-color: #e8dcc4 !important;
        color: #2c1810 !important;
    }
    label, .stMarkdown label, div[data-testid="stWidgetLabel"] {
        color: #2c1810 !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    .output-container {
        background: linear-gradient(to bottom, rgba(253, 252, 250, 0.9) 0%, rgba(245, 241, 232, 0.9) 100%);
        border-left: 4px solid #8b7355;
        padding: 2rem;
        border-radius: 8px;
        margin-top: 1rem;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
    }
    .output-text {
        font-family: 'Crimson Text', serif !important;
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
        color: #2c1810 !important;
    }
    .stButton > button {
        font-family: 'Cinzel', serif !important;
        background: linear-gradient(135deg, #8b7355 0%, #5a4a3a 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 115, 85, 0.3) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a4a3a 0%, #2c1810 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(139, 115, 85, 0.4) !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c1810 0%, #5a4a3a 100%) !important;
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f5f1e8 !important;
    }
    .prompt-section-title {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        color: #2c1810 !important;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #8b7355;
    }
    .prompt-card {
        background: linear-gradient(145deg, #fdfdfc 0%, #f8f6f0 100%);
        border-left: 4px solid #8b7355;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(44, 24, 16, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .prompt-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(44, 24, 16, 0.15);
    }
    .prompt-card strong {
        display: block;
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        color: #2c1810 !important;
        margin-bottom: 0.5rem;
    }
    .prompt-card .desc {
        display: block;
        font-family: 'Crimson Text', serif;
        font-size: 1rem;
        color: #5a4a3a !important;
        margin-bottom: 0.3rem;
        font-style: italic;
    }
    .prompt-card .example {
        display: block;
        font-family: 'Crimson Text', serif;
        font-size: 0.9rem;
        color: #8b7355 !important;
        padding-left: 1rem;
        border-left: 2px solid #e8dcc4;
        margin-top: 0.5rem;
    }
    .custom-divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #8b7355, transparent);
        margin: 2rem 0;
    }
    div[data-testid="stExpander"] {
        background: linear-gradient(145deg, #fdfdfc 0%, #f8f6f0 100%);
        border: 1px solid #8b7355;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏛️ ArtRestorer AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional Art Restoration & Analysis Assistant</p>', unsafe_allow_html=True)

if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []

# Sidebar configuration
with st.sidebar:
    st.markdown('<h2 style="color: #f5f1e8 !important;">⚙️ AI Configuration</h2>', unsafe_allow_html=True)
    
    temperature = st.slider(
        "Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values = more creative suggestions"
    )
    
    max_tokens = st.slider(
        "Response Length",
        min_value=500,
        max_value=3000,
        value=1500,
        step=100,
        help="Maximum length of AI response"
    )
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #f5f1e8 !important;">📊 Quick Stats</h3>', unsafe_allow_html=True)
    st.metric("Analyses Generated", len(st.session_state.generation_history))
    st.metric("Available Prompts", "12+")

tab1, tab2, tab3, tab4 = st.tabs([
    "🎨 Restoration Studio",
    "📚 Prompt Library",
    "🔍 History",
    "ℹ️ Guide"
])

# ─────────────────────────────────────────────────────────────
# TAB 1 — Restoration Studio
# ─────────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">Artwork Information</h2>', unsafe_allow_html=True)
        
        artwork_type = st.selectbox(
            "Artwork Type",
            ["Oil Painting", "Watercolor", "Fresco", "Sculpture", "Tapestry", "Manuscript", "Photography", "Mixed Media", "Other"],
            key="artwork_type"
        )
        
        period = st.selectbox(
            "Art Period/Style",
            ["Renaissance", "Baroque", "Gothic", "Byzantine", "Islamic", "Medieval", "Impressionist", "Modern", "Contemporary", "Ancient", "Mughal", "Japanese", "Chinese", "African", "Other"],
            key="period"
        )
        
        artist = st.text_input(
            "Artist (if known)",
            placeholder="e.g., leonardo da vinci",
            key="artist"
        )
        
        artwork_desc = st.text_area(
            "Artwork Description",
            placeholder="Describe the subject, colors, composition, style elements...",
            height=150,
            key="artwork_desc"
        )
        
        damage_desc = st.text_area(
            "Damage Description",
            placeholder="Detail the type, location, and extent of damage...",
            height=150,
            key="damage_desc"
        )
    
    with col2:
        st.markdown('<h2 class="section-header">Select Analysis Type</h2>', unsafe_allow_html=True)
        
        prompt_options = {
            "1. Comprehensive Restoration Suggestion": """Complete restoration plan with style-consistent reconstruction""",
            
            "2. Period-Specific Technique Analysis": """Authentic restoration methods from the artwork's historical period""",
            
            "3. Color Palette Reconstruction": """Scientific color matching and pigment analysis""",
            
            "4. Texture & Brushwork Recreation": """Reproduce the artist's unique techniques and materials""",
            
            "5. Damage Assessment & Priority": """Systematic damage evaluation and action planning""",
            
            "6. Material-Specific Conservation": """Tailored guidance for different art materials""",
            
            "7. Digital Reconstruction Strategy": """Modern digital workflow for restoration""",
            
            "8. Symbolic & Cultural Interpretation": """Decode meanings and cultural significance""",
            
            "9. Historical Context & Background": """Period, movement, and influence analysis""",
            
            "10. Cross-Cultural Comparison": """Compare with global artistic traditions""",
            
            "11. Inscription/Text Restoration": """Restore and interpret historical writing""",
            
            "12. Museum Visitor Summary": """Engaging explanations for general audiences"""
        }
        
        selected_prompt = st.selectbox(
            "Choose Analysis Type",
            list(prompt_options.keys()),
            format_func=lambda x: x,
            key="selected_prompt"
        )
        
        st.info(f"**Description:** {prompt_options[selected_prompt]}")
        
        include_history = st.checkbox("Include Historical References", value=True)
        include_materials = st.checkbox("Include Material Specifications", value=True)
        suggest_timeline = st.checkbox("Suggest Restoration Timeline", value=False)
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        if st.button("🎨 Generate AI Analysis"):
            if artwork_desc and damage_desc:
                with st.spinner("🔮 AI is analyzing the artwork..."):
                    try:
                        # Build the system prompt
                        system_prompt = f"""You are ArtRestorer AI, a world-class art restoration expert with deep knowledge of:
- Historical and contemporary art restoration techniques
- Period-specific materials and methods
- Cultural and symbolic interpretations across civilizations
- Conservation science and modern digital tools

Provide detailed, actionable guidance for restoring artworks while respecting their historical and cultural integrity."""

                        # Build the user prompt
                        user_prompt = f"""**ARTWORK DETAILS:**
- Type: {artwork_type}
- Period/Style: {period}
- Artist: {artist if artist else 'Unknown'}
- Description: {artwork_desc}

**DAMAGE DETAILS:**
{damage_desc}

**ANALYSIS REQUEST:**
{selected_prompt}
{prompt_options[selected_prompt]}

"""
                        if include_history:
                            user_prompt += "\n- Include relevant historical references and context"
                        if include_materials:
                            user_prompt += "\n- Specify materials, tools, and chemical compounds needed"
                        if suggest_timeline:
                            user_prompt += "\n- Provide a realistic restoration timeline with phases"
                        
                        user_prompt += "\n\nProvide comprehensive, professional restoration guidance."

                        # Make the API call with corrected headers
                        headers = {
                            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                            'Content-Type': 'application/json',
                            'HTTP-Referer': 'https://artrestorer.app',  # Optional but recommended
                            'X-Title': 'ArtRestorer AI'  # Optional but recommended
                        }
                        
                        payload = {
                            'model': 'openai/gpt-4o',
                            'messages': [
                                {'role': 'system', 'content': system_prompt},
                                {'role': 'user', 'content': user_prompt}
                            ],
                            'temperature': temperature,
                            'max_tokens': max_tokens
                        }
                        
                        response = requests.post(
                            OPENROUTER_API_URL,
                            headers=headers,
                            json=payload,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            ai_response = result['choices'][0]['message']['content']
                            st.session_state.generation_history.append({
                                'prompt_type': selected_prompt,
                                'artwork': f"{artwork_type} - {period}",
                                'response': ai_response,
                                'timestamp': 'Just now'
                            })
                            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                            st.markdown('<div class="output-container">', unsafe_allow_html=True)
                            st.markdown(f'<h3 class="section-header">AI Analysis: {selected_prompt}</h3>', unsafe_allow_html=True)
                            st.markdown(f'<div class="output-text">{ai_response}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.success("✅ Analysis complete! See results above.")
                        else:
                            st.error(f"❌ API Error: {response.status_code}")
                            if response.status_code == 401:
                                st.error("⚠️ **Authentication Failed**: Invalid API key or the key may have expired.")
                                st.info("**Troubleshooting:**\n- Verify your API key at https://openrouter.ai/keys\n- Ensure the key has sufficient credits\n- Check if the key has been revoked")
                            elif response.status_code == 402:
                                st.warning("⚠️ **Insufficient Credits**: Your OpenRouter API key needs credits.")
                            else:
                                st.error(f"Details: {response.text}")
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timed out. Please try again.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Network Error: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please provide both artwork description and damage description.")

# ─────────────────────────────────────────────────────────────
# TAB 2 — Prompt Library  (uses HTML cards instead of expanders)
# ─────────────────────────────────────────────────────────────
with tab2:
    st.header("📚 Specialized Prompt Library")
    st.info("ArtRestorer AI features 12+ specialized prompts designed for different restoration scenarios.")

    # ── Restoration Techniques ──────────────────────────────
    st.markdown('<p class="prompt-section-title">🎨 Restoration Techniques</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="prompt-card">
        <strong>Comprehensive Restoration Suggestion</strong>
        <span class="desc">Complete end-to-end restoration planning with style consistency</span>
        <span class="example">Example: Renaissance oil painting with water damage</span>
    </div>
    <div class="prompt-card">
        <strong>Period-Specific Technique Analysis</strong>
        <span class="desc">Authentic methods from the artwork's historical period</span>
        <span class="example">Example: Mughal miniature with faded borders</span>
    </div>
    <div class="prompt-card">
        <strong>Color Palette Reconstruction</strong>
        <span class="desc">Scientific color matching and pigment analysis</span>
        <span class="example">Example: Impressionist painting with sun-faded sections</span>
    </div>
    <div class="prompt-card">
        <strong>Texture &amp; Brushwork Recreation</strong>
        <span class="desc">Reproduce the artist's unique techniques</span>
        <span class="example">Example: Van Gogh-style painting with missing impasto</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Analysis & Assessment ───────────────────────────────
    st.markdown('<p class="prompt-section-title">🔍 Analysis &amp; Assessment</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="prompt-card">
        <strong>Damage Assessment &amp; Priority</strong>
        <span class="desc">Systematic damage evaluation and action planning</span>
        <span class="example">Example: Medieval fresco with multiple damage types</span>
    </div>
    <div class="prompt-card">
        <strong>Material-Specific Conservation</strong>
        <span class="desc">Tailored guidance for different art materials</span>
        <span class="example">Example: Gothic tapestry with fiber degradation</span>
    </div>
    <div class="prompt-card">
        <strong>Digital Reconstruction Strategy</strong>
        <span class="desc">Modern digital workflow for restoration</span>
        <span class="example">Example: Illuminated manuscript needing digital work</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Cultural & Historical ───────────────────────────────
    st.markdown('<p class="prompt-section-title">📖 Cultural &amp; Historical</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="prompt-card">
        <strong>Symbolic &amp; Cultural Interpretation</strong>
        <span class="desc">Decode meanings and cultural significance</span>
        <span class="example">Example: Byzantine icon with damaged symbolic elements</span>
    </div>
    <div class="prompt-card">
        <strong>Historical Context &amp; Background</strong>
        <span class="desc">Period, movement, and influence analysis</span>
        <span class="example">Example: Gothic cathedral sculpture fragment</span>
    </div>
    <div class="prompt-card">
        <strong>Cross-Cultural Comparison</strong>
        <span class="desc">Compare with global artistic traditions</span>
        <span class="example">Example: Japanese Ukiyo-e woodblock print</span>
    </div>
    <div class="prompt-card">
        <strong>Inscription/Text Restoration</strong>
        <span class="desc">Restore and interpret historical writing</span>
        <span class="example">Example: Medieval manuscript with faded Latin text</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Communication ───────────────────────────────────────
    st.markdown('<p class="prompt-section-title">👥 Communication</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="prompt-card">
        <strong>Museum Visitor Summary</strong>
        <span class="desc">Engaging explanations for general audiences</span>
        <span class="example">Example: Recently restored Baroque painting</span>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<h2 class="section-header">🔍 Analysis History</h2>', unsafe_allow_html=True)
    
    if st.session_state.generation_history:
        for idx, entry in enumerate(reversed(st.session_state.generation_history)):
            with st.expander(f"Analysis #{len(st.session_state.generation_history) - idx}: {entry['artwork']}"):
                st.markdown(f"**Prompt Type:** {entry['prompt_type']}")
                st.markdown(f"**Timestamp:** {entry['timestamp']}")
                st.markdown("**Response:**")
                st.markdown(entry['response'])
    else:
        st.info("No analyses yet. Use the Restoration Studio to generate your first analysis!")
    
    if st.session_state.generation_history:
        if st.button("Clear History"):
            st.session_state.generation_history = []
            st.rerun()

with tab4:
    st.markdown('<h2 class="section-header">ℹ️ User Guide</h2>', unsafe_allow_html=True)
    st.markdown("""
    ### 🚀 Getting Started
    
    1. **Configure AI Settings** (Sidebar) — Adjust creativity level and response length
    2. **Enter Artwork Details** — Select type, period, and describe the artwork and damage
    3. **Choose Analysis Type** — Select from 12+ specialized prompts
    4. **Generate Analysis** — Click "Generate AI Analysis" and review guidance
    
    ### 💡 Tips for Best Results
    
    - **Be Specific**: Include details about colors, composition, style elements
    - **Describe Damage Precisely**: Location, type, extent, and cause if known
    - **Use Cultural References**: Mention regional styles, traditions, periods
    - **Iterate**: Try different prompts for comprehensive insights
    
    ### 🎯 Example Workflows
    
    **Scenario 1: Renaissance Painting**  
    Start with "Comprehensive Restoration Suggestion" → "Period-Specific Technique Analysis" → "Color Palette Reconstruction" → "Museum Visitor Summary"
    
    **Scenario 2: Ancient Manuscript**  
    Begin with "Damage Assessment & Priority" → "Inscription/Text Restoration" → "Symbolic & Cultural Interpretation" → "Historical Context & Background"
    
    ### ⚙️ AI Parameters Explained
    
    **Temperature (Creativity Level)**
    - 0.0–0.3: Conservative, factual restoration suggestions
    - 0.4–0.6: Balanced approach with some creativity
    - 0.7–1.0: Imaginative interpretations and bold suggestions
    
    **Response Length**
    - 500–1000: Concise, focused guidance
    - 1000–2000: Detailed, comprehensive analysis
    - 2000–3000: Exhaustive, research-grade documentation
    """)

# Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #5a4a3a; font-family: 'Cormorant Garamond', serif; padding: 2rem;">
    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">🏛️ ArtRestorer AI</p>
    <p style="font-size: 0.9rem; font-style: italic;">Bridging Heritage and Technology</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">Powered by OpenRouter AI (GPT-4o) | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)