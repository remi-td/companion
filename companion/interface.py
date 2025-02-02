import streamlit as st
from llm_backend import LLMBackend
from config import config  # Import the configuration module

# Initialize session state
if 'backend' not in st.session_state:
    st.session_state.backend = LLMBackend()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_thread_id' not in st.session_state:
    st.session_state.current_thread_id = None

backend = st.session_state.backend

# Sidebar
with st.sidebar:
    st.title("🦅 Aether")

    # New Chat Button
    if st.button("➕ New Chat"):
        thread_id = backend.create_new_thread()
        st.session_state.current_thread_id = thread_id
        st.session_state.messages = []
        st.rerun()

    # List of Chats
    st.subheader("✨ Chats")
    threads = backend.get_all_threads()
    for thread_id, title in threads:
        if st.button(title, key=f"thread_{thread_id}"):
            backend.load_thread(thread_id)
            st.session_state.current_thread_id = thread_id
            # Load messages from the LLM instance
            st.session_state.messages = backend.llm_model.conversation_history
            st.rerun()

# Chat Interface
st.header("Chat with Aether")

if st.session_state.current_thread_id is None:
    # No chat selected, create a new one
    thread_id = backend.create_new_thread()
    st.session_state.current_thread_id = thread_id

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Input box for user message
user_input = st.chat_input("Type your message...")
if user_input:
    # Display user's message
    with st.chat_message('user'):
        st.markdown(user_input)
    # Generate assistant's response and stream it
    with st.chat_message('assistant'):
        # Generate response stream
        stream = backend.get_response_stream(user_input)
        response_placeholder = st.empty()
        full_response = ""
        for chunk in stream:
            full_response += chunk
            response_placeholder.markdown(full_response)
    # After full response is received, save to database and update session messages
    backend.save_assistant_response(full_response)
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    st.session_state.messages.append({'role': 'assistant', 'content': full_response})