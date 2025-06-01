import streamlit as st
import asyncio
from gaccia_main import GACCIAComplete, EXAMPLE_CODES

st.title("🥊 GACCIA: Code Competition Arena")
st.subtitle("Generative Adversarial Competitive Code Improvement")

# Sidebar controls
st.sidebar.header("Competition Settings")
example = st.sidebar.selectbox("Choose Example", list(EXAMPLE_CODES.keys()))
language = st.sidebar.selectbox("Starting Language", ["python", "typescript"])
rounds = st.sidebar.slider("Competition Rounds", 1, 5, 2)

if st.sidebar.button("🚀 Start Competition"):
    with st.spinner("Running competitive coding session..."):
        gaccia = GACCIAComplete()
        code = EXAMPLE_CODES[example][language]
        
        # Run competition
        completed_session = gaccia.run_complete_competition(code, language, rounds)
        
        # Display results
        st.success("Competition Complete!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Python Score", f"{completed_session.evaluation.python_total_score:.1f}/10")
            st.text(completed_session.evaluation.python_snark)
        
        with col2:
            st.metric("TypeScript Score", f"{completed_session.evaluation.typescript_total_score:.1f}/10")
            st.text(completed_session.evaluation.typescript_snark)
        
        st.header(f"🏆 Winner: {completed_session.evaluation.winner}")
        
        # Show final codes
        if completed_session.get_final_python_code():
            st.subheader("Final Python Implementation")
            st.code(completed_session.get_final_python_code(), language="python")
        
        if completed_session.get_final_typescript_code():
            st.subheader("Final TypeScript Implementation") 
            st.code(completed_session.get_final_typescript_code(), language="typescript")