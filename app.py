import streamlit as st
import json
from src.orchestrator import analyze_git_repo

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# --- 2. Helper Function: Render Review Cards ---
def render_review_card(review, is_low_confidence=False):
    """Renders a single review as a visual card."""
    severity = review.get("severity", "INFO").upper()
    
    # Assign icons based on severity
    if severity == "CRITICAL":
        icon = "🚨"
    elif severity == "WARNING":
        icon = "⚠️"
    else:
        icon = "ℹ️"
        
    # Handle list vs string for filename
    file_val = review.get("file", "Unknown")
    file_name = file_val[0] if isinstance(file_val, list) else file_val
    
    # The Creative Twist: Append the Verify label
    verify_label = " **[🔍 VERIFY THIS]**" if is_low_confidence else ""
    
    # Build the card UI
    with st.container(border=True):
        st.markdown(f"#### {icon} {severity} | `{file_name}` : `{review.get('scope', 'unknown')}`")
        st.markdown(f"**Line Number:** {review.get('absolute_line', 'N/A')}{verify_label}")
        st.markdown(f"> {review.get('comment', 'No comment provided.')}")
        st.caption(f"Confidence Score: {review.get('confidence_score', 0)}%")

# --- 3. Main Dashboard UI ---
st.title("🕵️‍♂️ AI Code Review Agent")
st.markdown("Autonomously clone, parse, and analyze GitHub repositories using AST and LLM reasoning.")

# Input Section
repo_url = st.text_input("Enter a public GitHub Repository URL:", placeholder="https://github.com/username/repository")

if st.button("Analyze Repository", type="primary"):
    if not repo_url:
        st.error("Please enter a valid GitHub URL.")
    else:
        # --- 4. Connect to Backend ---
        with st.spinner(f"Cloning and analyzing `{repo_url}`. This may take a minute depending on repository size..."):
            try:
                results = analyze_git_repo(repo_url)
                
                if not results:
                    st.success("Analysis complete! No issues were found in the codebase.")
                else:
                    # Store results in Streamlit session state so they don't disappear on interaction
                    st.session_state['reviews'] = results
                    st.success("Analysis complete!")
                    
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

# --- 5. Displaying Results & Filtering ---
# Check if we have results in the session state to display
if 'reviews' in st.session_state and st.session_state['reviews']:
    reviews = st.session_state['reviews']
    
    st.divider()
    
    # Header & Download Button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Review Results")
    with col2:
        json_str = json.dumps(reviews, indent=2)
        st.download_button(
            label="⬇️ Download JSON Report",
            data=json_str,
            file_name="code_review_report.json",
            mime="application/json"
        )
        
    # Severity Filter
    filter_severity = st.selectbox("Filter by Severity:", ["All", "CRITICAL", "WARNING", "INFO"])
    
    # Bucket the results (The Creative Twist)
    high_confidence = []
    low_confidence = []
    
    for r in reviews:
        # Apply severity filter
        if filter_severity != "All" and r.get("severity", "").upper() != filter_severity:
            continue
            
        score = r.get("confidence_score", 100)
        if score >= 80:
            high_confidence.append(r)
        else:
            low_confidence.append(r)

    # Render Tabs
    tab1, tab2 = st.tabs([f"✅ High Confidence ({len(high_confidence)})", f"🔍 Needs Verification ({len(low_confidence)})"])
    
    with tab1:
        if not high_confidence:
            st.info("No high-confidence reviews found for this filter.")
        for review in high_confidence:
            render_review_card(review, is_low_confidence=False)
            
    with tab2:
        if not low_confidence:
            st.info("No low-confidence reviews found for this filter.")
        for review in low_confidence:
            # Force the 'verify this' flag to True for the low confidence bucket
            render_review_card(review, is_low_confidence=True)