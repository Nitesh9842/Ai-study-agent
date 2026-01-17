import streamlit as st
import json
from agent import InputUnderstanding, StateTracker, TaskPlanner, OutputGenerator


# Initialize session state
def init_session_state():
    if "agent_state" not in st.session_state:
        st.session_state.agent_state = StateTracker()
    if "input_handler" not in st.session_state:
        st.session_state.input_handler = InputUnderstanding()
    if "planner" not in st.session_state:
        st.session_state.planner = TaskPlanner()
    if "generator" not in st.session_state:
        st.session_state.generator = OutputGenerator()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_debug_info" not in st.session_state:
        st.session_state.last_debug_info = {}


def process_query(user_input: str) -> dict:
    """Process query and return all intermediate steps."""
    debug_info = {}
    
    # Step 1: Input Understanding
    parsed = st.session_state.input_handler.parse_input(user_input)
    intent = st.session_state.input_handler.classify_intent(user_input)
    debug_info["input_understanding"] = {
        "raw_input": user_input,
        "classified_intent": intent,
        "parsed_analysis": parsed.get("parsed", "")
    }
    
    # Step 2: State Tracking
    st.session_state.agent_state.set_topic(user_input)
    debug_info["state_tracker"] = {
        "current_topic": st.session_state.agent_state.current_topic,
        "difficulty_level": st.session_state.agent_state.difficulty_level,
        "topics_covered": st.session_state.agent_state.topics_covered.copy(),
        "interaction_count": len(st.session_state.agent_state.conversation_history)
    }
    
    # Step 3: Task Planning
    plan = st.session_state.planner.create_plan(
        intent=intent,
        topic=user_input,
        difficulty=st.session_state.agent_state.difficulty_level
    )
    debug_info["task_planner"] = {
        "task_type": plan["task_type"],
        "steps": plan["steps"],
        "prompt_template": plan["prompt_template"]
    }
    
    # Step 4: Output Generation
    context = st.session_state.agent_state.get_context()
    response = st.session_state.generator.generate_response(plan, context)
    formatted = st.session_state.generator.format_response(response, plan["task_type"])
    debug_info["output_generator"] = {
        "context_used": len(context),
        "response_length": len(response)
    }
    
    # Step 5: Update State
    st.session_state.agent_state.update_state(user_input, parsed, response)
    
    return {
        "response": formatted,
        "raw_response": response,
        "debug_info": debug_info
    }


def main():
    st.set_page_config(
        page_title="AI Study Buddy Agent",
        page_icon="🎓",
        layout="wide"
    )
    
    init_session_state()
    
    # Header
    st.title("🎓 AI Study Buddy Agent")
    st.markdown("*Your intelligent learning companion powered by AI*")
    
    # Sidebar - Agent Components & Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Difficulty selector
        difficulty = st.selectbox(
            "📊 Difficulty Level",
            ["beginner", "intermediate", "advanced"],
            index=["beginner", "intermediate", "advanced"].index(
                st.session_state.agent_state.difficulty_level
            )
        )
        if difficulty != st.session_state.agent_state.difficulty_level:
            st.session_state.agent_state.set_difficulty(difficulty)
            st.success(f"Difficulty set to: {difficulty}")
        
        st.divider()
        
        # Session Info
        st.header("📊 Session Info")
        session_info = st.session_state.agent_state.get_session_summary()
        st.metric("Total Interactions", session_info["total_interactions"])
        st.metric("Topics Covered", len(session_info["topics_covered"]))
        st.text(f"Duration: {str(session_info['session_duration']).split('.')[0]}")
        
        if session_info["topics_covered"]:
            with st.expander("📚 Topics Covered"):
                for topic in session_info["topics_covered"][-5:]:
                    st.markdown(f"• {topic[:50]}...")
        
        st.divider()
        
        # Reset button
        if st.button("🔄 Reset Session", use_container_width=True):
            st.session_state.agent_state.reset()
            st.session_state.messages = []
            st.session_state.last_debug_info = {}
            st.rerun()
    
    # Main content area - Two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat")
        
        # Chat container
        chat_container = st.container(height=400)
        
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your studies..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Process and get response
            with st.spinner("🤔 Thinking..."):
                result = process_query(prompt)
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["raw_response"]
            })
            
            # Store debug info
            st.session_state.last_debug_info = result["debug_info"]
            
            st.rerun()
    
    with col2:
        st.header("🔍 Agent Pipeline")
        
        if st.session_state.last_debug_info:
            debug = st.session_state.last_debug_info
            
            # Input Understanding
            with st.expander("🧠 Input Understanding", expanded=True):
                st.markdown("**Classified Intent:**")
                intent = debug.get("input_understanding", {}).get("classified_intent", "N/A")
                intent_colors = {
                    "explain": "🟢", "summarize": "🔵", "quiz": "🟡",
                    "define": "🟣", "compare": "🟠", "practice": "🔴", "general": "⚪"
                }
                st.markdown(f"{intent_colors.get(intent, '⚪')} **{intent.upper()}**")
                
                with st.container():
                    st.markdown("**Parsed Analysis:**")
                    try:
                        parsed = debug.get("input_understanding", {}).get("parsed_analysis", "")
                        st.code(parsed, language="json")
                    except:
                        st.text("Analysis complete")
            
            # State Tracker
            with st.expander("📍 State Tracker", expanded=True):
                state = debug.get("state_tracker", {})
                st.markdown(f"**Difficulty:** {state.get('difficulty_level', 'N/A')}")
                st.markdown(f"**Interactions:** {state.get('interaction_count', 0)}")
                st.markdown(f"**Topics:** {len(state.get('topics_covered', []))}")
            
            # Task Planner
            with st.expander("📋 Task Planner", expanded=True):
                planner = debug.get("task_planner", {})
                st.markdown(f"**Task Type:** `{planner.get('task_type', 'N/A')}`")
                st.markdown("**Execution Steps:**")
                for i, step in enumerate(planner.get("steps", []), 1):
                    st.markdown(f"{i}. {step}")
            
            # Output Generator
            with st.expander("✨ Output Generator", expanded=True):
                output = debug.get("output_generator", {})
                st.markdown(f"**Context Messages:** {output.get('context_used', 0)}")
                st.markdown(f"**Response Length:** {output.get('response_length', 0)} chars")
        else:
            st.info("💡 Send a message to see the agent pipeline in action!")
    
    # Bottom section - Quick Actions
    st.divider()
    st.subheader("⚡ Quick Actions")
    
    quick_cols = st.columns(6)
    quick_prompts = [
        ("📚 Explain", "Explain the concept of"),
        ("📝 Summarize", "Summarize the topic of"),
        ("❓ Quiz Me", "Quiz me on"),
        ("📖 Define", "Define"),
        ("⚖️ Compare", "Compare and contrast"),
        ("✏️ Practice", "Give me practice problems for")
    ]
    
    for col, (label, prefix) in zip(quick_cols, quick_prompts):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.quick_prefix = prefix
                st.toast(f"Type your topic after: '{prefix}'")


if __name__ == "__main__":
    main()
