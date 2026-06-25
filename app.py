import os
import streamlit as st
from google import genai
from google.genai.errors import APIError

# Page Configuration
st.set_page_config(
    page_title="LLM Output Evaluator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean Dark Theme CSS styling injection
st.markdown("""
    <style>
    /* Styling adjustments for a cleaner dark SaaS dashboard aesthetic */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    div[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: opacity 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        opacity: 0.9 !important;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.title("🔬 LLM Output Evaluator")
st.markdown("Compare two alternative language model outputs across metric indicators including accuracy, completeness, clarity, and hallucination risk.")
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Attempt to read environment variable fallback
    env_key = os.environ.get("GEMINI_API_KEY", "")
    
    api_key_input = st.text_input(
        "Gemini API Key:", 
        value=env_key if env_key else "",
        type="password",
        help="If not set in your local system environment variables, paste your Gemini API Key here."
    )
    
    st.markdown("---")
    st.markdown("### 📊 Metrics Definitions")
    st.markdown("""
    *   **Factual Accuracy**: Veracity and correctness of facts.
    *   **Completeness**: Thoroughness in addressing all constraints of the prompt.
    *   **Clarity**: Layout, formatting structure, and general readability.
    *   **Hallucination Risk**: Presence of unsubstantiated or completely fabricated claims.
    """)

# Workspace Layout
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("❓ Target Question / Prompt")
    question = st.text_area(
        "Enter the original question prompt:", 
        height=120, 
        placeholder="e.g., Explain quantum computing in three simple sentences."
    )

with col2:
    st.subheader("📝 Candidate Responses")
    col_a, col_b = st.columns(2)
    with col_a:
        answer_a = st.text_area(
            "Answer Option A:", 
            height=200, 
            placeholder="Paste first model output response here..."
        )
    with col_b:
        answer_b = st.text_area(
            "Answer Option B:", 
            height=200, 
            placeholder="Paste second model output response here..."
        )

# Execution Action Trigger
if st.button("Analyze and Compare Outputs", use_container_width=True):
    # Validation step checks
    active_api_key = api_key_input or env_key
    
    if not active_api_key:
        st.error("Please provide a valid Gemini API key inside the sidebar or set GEMINI_API_KEY as an environment variable.")
    elif not question.strip() or not answer_a.strip() or not answer_b.strip():
        st.error("Please fill in the target prompt and both answer response blocks before initiating analysis.")
    else:
        with st.spinner("Analyzing candidate outputs..."):
            try:
                # Initialize the Google GenAI Client
                client = genai.Client(api_key=active_api_key)
                
                evaluation_prompt = f"""You are an expert LLM output evaluator. Compare these two AI answers to the same question.

QUESTION:
{question}

ANSWER A:
{answer_a}

ANSWER B:
{answer_b}

Evaluate both answers using these precise criteria on a 1-10 scale:
1. FACTUAL ACCURACY — Correctness of facts.
2. COMPLETENESS — Addresses all aspects of the prompt.
3. CLARITY — Well-structured and easy to read.
4. HALLUCINATION RISK — Fabrications present? (10 = perfect score, no hallucinations; 1 = severe hallucinations present).

For each answer, return:
- A numeric score for each criterion
- A brief explanation for the assigned score
- A clear summary identifying the overall winner (Answer A, Answer B, or Tie)
- Key differences between the two outputs

Format your response cleanly using clear headers and bullet points. End your response with a line formatted exactly as:
Winner: Answer A
Winner: Answer B
or
Winner: Tie"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=evaluation_prompt
                )
                
                evaluation_text = response.text
                
                # Rendering Results UI
                st.markdown("---")
                st.subheader("📊 Evaluation Report")
                st.markdown(evaluation_text)
                
                # Winner extraction parser
                st.markdown("---")
                st.subheader("🏆 Comparative Assessment Verdict")
                
                verdict_col_a, verdict_col_b = st.columns(2)
                text_lower = evaluation_text.lower()
                
                # Resilient string check logic
                if "winner: answer a" in text_lower or "winner is answer a" in text_lower or "winner is a" in text_lower or "winner: a" in text_lower:
                    with verdict_col_a:
                        st.success("🏆 WINNER DETERMINED: Answer A")
                elif "winner: answer b" in text_lower or "winner is answer b" in text_lower or "winner is b" in text_lower or "winner: b" in text_lower:
                    with verdict_col_b:
                        st.success("🏆 WINNER DETERMINED: Answer B")
                else:
                    st.info("🤝 Evaluation concluded with no clear single winner (Tie or mixed assessment). See the report detail above.")
                    
            except APIError as api_err:
                st.error(f"API Connection error occurred: {api_err.message}")
            except Exception as err:
                st.error(f"An unexpected error occurred during evaluation: {str(err)}")

# Footer Branding
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>"
    "LLM Output Evaluator Dashboard | Powered by Gemini 2.5 Flash & Streamlit"
    "</div>", 
    unsafe_allow_html=True
)