import streamlit as st
import requests
#import json

# Page configuration
st.set_page_config(
    page_title="Figma to Code Generator",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .assistant-message {
        background-color: #e6f7ff;
    }
    .code-block {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

# Sidebar for configuration
with st.sidebar:
    st.title("Configuration")
    st.session_state.api_url = st.text_input(
        "Backend API URL",
        value="http://localhost:8000",
        help="URL of your FastAPI backend"
    )
    
    st.divider()
    st.subheader("Figma Integration")
    figma_file_id = st.text_input("Figma File ID", help="Optional: ID of your Figma file")
    
    if st.button("Generate Code from Figma") and figma_file_id:
        with st.spinner("Generating code from Figma design..."):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/api/generate-from-figma",
                    json={"file_id": figma_file_id}
                )
                
                if response.json().get("success"):
                    code_response = response.json().get("response", "")
                    st.session_state.conversation_history.append({
                        "role": "assistant", 
                        "content": f"Here's the code generated from your Figma design:\n\n{code_response}"
                    })
                    st.rerun()
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

# Main chat interface
st.title("🎨 Figma to Code Generator")
st.caption("Describe your design or connect to Figma to generate HTML/CSS code")

# Display conversation history
for message in st.session_state.conversation_history:
    with st.chat_message(message["role"]):
        if "```" in message["content"]:
            # Extract and display code blocks properly
            parts = message["content"].split("```")
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Code blocks
                    st.code(part, language="html")
                else:  # Regular text
                    st.write(part)
        else:
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Describe your design or ask a question..."):
    # Add user message to history
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/api/chat",
                    json={
                        "message": prompt,
                        "conversation_history": st.session_state.conversation_history[:-1]  # Exclude current message
                    }
                )
                
                if response.json().get("success"):
                    assistant_response = response.json().get("response", "")
                    
                    # Update conversation history
                    st.session_state.conversation_history.append({
                        "role": "assistant", 
                        "content": assistant_response
                    })
                    
                    # Display assistant response
                    if "```" in assistant_response:
                        parts = assistant_response.split("```")
                        for i, part in enumerate(parts):
                            if i % 2 == 1:  # Code blocks
                                st.code(part, language="html")
                            else:  # Regular text
                                st.write(part)
                    else:
                        st.write(assistant_response)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()
