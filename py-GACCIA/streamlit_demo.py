import streamlit as st
import asyncio
import os
from pathlib import Path
from gaccia_main import GACCIAComplete, EXAMPLE_CODES
from gaccia_with_images import EnhancedGACCIAOrchestrator

st.title("🥊 GACCIA: Code Competition Arena")
st.subheader("Generative Adversarial Competitive Code Improvement")

# Add option for image generation
st.sidebar.header("Battle Mode")
with_images = st.sidebar.checkbox("🎨 Generate Battle Images", value=False, help="Creates epic images during the coding battle (requires OpenAI API key)")

# Show API key status
if with_images:
    if os.getenv("OPENAI_API_KEY"):
        st.sidebar.success("✅ OpenAI API key detected")
    else:
        st.sidebar.error("❌ OpenAI API key required for image generation")
        st.sidebar.info("Set OPENAI_API_KEY environment variable")

# Sidebar controls
st.sidebar.header("Competition Settings")
example = st.sidebar.selectbox("Choose Example", list(EXAMPLE_CODES.keys()))
language = st.sidebar.selectbox("Starting Language", ["python", "typescript"])
rounds = st.sidebar.slider("Competition Rounds", 1, 5, 2)

# Battle button
button_text = "🎨 Start Epic Battle!" if with_images else "🚀 Start Competition"
if st.sidebar.button(button_text):
    code = EXAMPLE_CODES[example][language]
    
    if with_images and os.getenv("OPENAI_API_KEY"):
        # Run with image generation
        with st.spinner("🎬 Running epic coding battle with live image generation..."):
            try:
                orchestrator = EnhancedGACCIAOrchestrator()
                completed_session, images = orchestrator.run_complete_competition_with_images(code, language, rounds)
                
                # Display battle start image
                if "battle_start" in images and Path(images["battle_start"]).exists():
                    st.image(images["battle_start"], caption="🎬 Battle Begins!", use_column_width=True)
                
                # Display results
                st.success("🎉 Epic Battle Complete!")
                
                # Show round images in a gallery
                if any("round_" in key for key in images.keys()):
                    st.subheader("⚔️ Battle Highlights")
                    
                    # Create columns for round images
                    round_images = {k: v for k, v in images.items() if "round_" in k}
                    if round_images:
                        cols = st.columns(min(len(round_images), 3))
                        for i, (key, image_path) in enumerate(round_images.items()):
                            if Path(image_path).exists():
                                with cols[i % 3]:
                                    st.image(image_path, caption=f"🥊 {key.replace('_', ' ').title()}", use_column_width=True)
                
                # Display final battle image
                if "battle_finale" in images and Path(images["battle_finale"]).exists():
                    st.image(images["battle_finale"], caption="🏁 Battle Finale!", use_column_width=True)
                
                # Show strategy and action images
                strategy_images = {k: v for k, v in images.items() if "strategy" in k or "thinking" in k or "coding_action" in k}
                if strategy_images:
                    st.subheader("🧠 Behind the Scenes")
                    for key, image_path in strategy_images.items():
                        if Path(image_path).exists():
                            st.image(image_path, caption=f"💭 {key.replace('_', ' ').title()}", use_column_width=True)
                
            except Exception as e:
                st.error(f"Failed to run battle with images: {str(e)}")
                st.info("Falling back to standard competition...")
                # Fallback to standard competition
                with st.spinner("Running standard competitive coding session..."):
                    gaccia = GACCIAComplete()
                    completed_session = gaccia.run_complete_competition(code, language, rounds)
    else:
        # Run standard competition
        with st.spinner("Running competitive coding session..."):
            gaccia = GACCIAComplete()
            completed_session = gaccia.run_complete_competition(code, language, rounds)
        
        st.success("Competition Complete!")
    
    # Display scores and results (common for both modes)
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🐍 Python Score", f"{completed_session.evaluation.python_total_score:.1f}/10")
        with st.expander("Python's Trash Talk"):
            st.write(completed_session.evaluation.python_snark)
    
    with col2:
        st.metric("📘 TypeScript Score", f"{completed_session.evaluation.typescript_total_score:.1f}/10")
        with st.expander("TypeScript's Trash Talk"):
            st.write(completed_session.evaluation.typescript_snark)
    
    # Winner announcement
    winner = completed_session.evaluation.winner
    if winner == "Python":
        st.success(f"🏆 Winner: {winner} 🐍")
    elif winner == "TypeScript":
        st.success(f"🏆 Winner: {winner} 📘")
    else:
        st.info(f"🤝 Result: {winner}")
    
    # Battle Statistics
    st.subheader("📊 Battle Statistics")
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        python_rounds = len(completed_session.session.python_implementations)
        st.metric("Python Rounds", python_rounds)
    
    with stats_col2:
        typescript_rounds = len(completed_session.session.typescript_implementations)
        st.metric("TypeScript Rounds", typescript_rounds)
    
    with stats_col3:
        total_rounds = max(python_rounds, typescript_rounds)
        st.metric("Total Rounds", total_rounds)
    
    # Show final codes in tabs
    if completed_session.get_final_python_code() and completed_session.get_final_typescript_code():
        tab1, tab2 = st.tabs(["🐍 Final Python Code", "📘 Final TypeScript Code"])
        
        with tab1:
            st.code(completed_session.get_final_python_code(), language="python")
        
        with tab2:
            st.code(completed_session.get_final_typescript_code(), language="typescript")
    
    elif completed_session.get_final_python_code():
        st.subheader("🐍 Final Python Implementation")
        st.code(completed_session.get_final_python_code(), language="python")
    
    elif completed_session.get_final_typescript_code():
        st.subheader("📘 Final TypeScript Implementation") 
        st.code(completed_session.get_final_typescript_code(), language="typescript")

# Add some information about the app
st.sidebar.markdown("---")
st.sidebar.markdown("### About GACCIA")
st.sidebar.info("""
🥊 **GACCIA** pits Python against TypeScript in competitive coding battles!

🎯 **How it works:**
- Choose a starting code example
- Watch as agents convert between languages
- See which implementation wins!

🎨 **With Images:**
- Epic battle visuals
- Round-by-round highlights
- Behind-the-scenes strategy images
""")