import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Enhanced Streamlit page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1fae5;
        color: #065f46;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e0f2fe;
        color: #075985;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.title("📊 Interview Statistics")
    if "total_interviews" not in st.session_state:
        st.session_state.total_interviews = 0
    
    st.metric("Total Interviews Conducted", st.session_state.total_interviews)
    
    st.markdown("---")
    st.subheader("🎯 About TalentScout")
    st.markdown("""
    TalentScout is an AI-powered hiring assistant that:
    - Collects candidate information
    - Conducts technical screenings
    - Provides immediate feedback
    - Maintains conversation context
    """)

# Main function for response generation with enhanced prompt
def get_response(user_query, chat_history, tech_stack=""):
    template = """
    You are TalentScout, an advanced AI Hiring Assistant for a recruitment agency.
    
    Your responsibilities:
    1. Maintain a professional yet friendly tone
    2. Ask relevant technical questions based on the candidate's tech stack: {tech_stack}
    3. Evaluate responses and provide constructive feedback
    4. Keep questions focused on practical scenarios and problem-solving
    5. Maintain context throughout the conversation
    6. Your responses must be complete and under 300-350 tokens.

    Current chat history: {chat_history}
    Latest input: {user_question}
    
    Provide a detailed, engaging response while staying focused on the technical assessment.
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.7,
        max_tokens=400
    )

    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({
        "chat_history": chat_history,
        "user_question": user_query,
        "tech_stack": tech_stack
    })

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="👋 Welcome to TalentScout! I'm your AI Hiring Assistant. Let's start with your details.")
    ]
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0
if "submitted_form" not in st.session_state:
    st.session_state.submitted_form = False
if "tech_stack" not in st.session_state:
    st.session_state.tech_stack = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# Main title with custom styling
st.title("🤖 TalentScout Hiring Assistant")
st.markdown("*Your AI-powered technical screening partner*")

# Enhanced candidate details form
if not st.session_state.submitted_form:
    with st.form("candidate_form", clear_on_submit=True):
        st.subheader("📝 Candidate Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
        
        with col2:
            experience = st.number_input("Years of Experience", min_value=0, step=1)
            position = st.text_input("Desired Position")
            location = st.text_input("Current Location")
        
        tech_stack = st.text_area("Technical Skills (Please list your primary technologies)", 
                                 placeholder="e.g., Python, Django, React, PostgreSQL")
        
        # Additional preferences
        st.subheader("💼 Additional Preferences")
        col3, col4 = st.columns(2)
        with col3:
            work_type = st.selectbox("Preferred Work Type", 
                                   ["Remote", "Hybrid", "On-site"])
            availability = st.date_input("Available From", 
                                       min_value=datetime.today())
        with col4:
            salary_range = st.select_slider("Expected Salary Range (K USD)", 
                                          options=['40-60', '60-80', '80-100', '100-120', '120+'])
            notice_period = st.number_input("Notice Period (in weeks)", 
                                          min_value=0, max_value=12, step=1)

        submitted = st.form_submit_button("Begin Technical Assessment")

        if submitted:
            if not name or not email or not phone or not tech_stack:
                st.error("⚠️ Please fill in all required fields!")
            else:
                st.session_state.submitted_form = True
                st.session_state.tech_stack = tech_stack
                st.session_state.candidate_name = name
                welcome_message = f"Thank you, {name}! 🎉 I see you're experienced with {tech_stack}. Let's proceed with the technical assessment."
                st.session_state.chat_history.append(AIMessage(content=welcome_message))
                st.session_state.total_interviews += 1
                st.rerun()

# Enhanced chat interface
if st.session_state.submitted_form:
    st.markdown("---")
    st.subheader("🤖 Technical Assessment")
    
    # Progress indicator
    progress = min(st.session_state.questions_asked / 3, 1.0)  # Now between 0 and 1
    st.progress(progress)
    st.markdown(f"Progress: {int(progress * 100)}% complete")

    # Chat display with enhanced styling
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI", avatar="🤖"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human", avatar="👤"):
                st.write(message.content)

    # Start button with animation
    if st.session_state.questions_asked == 0:
        if st.button("🎯 Start Technical Questions", key="start_button"):
            with st.spinner("Preparing your first question..."):
                response = get_response("", st.session_state.chat_history, st.session_state.tech_stack)
                st.session_state.chat_history.append(AIMessage(content=response))
                st.session_state.questions_asked += 1
                st.rerun()

    # Enhanced chat input and response handling
    if 0 < st.session_state.questions_asked <= 3:
        user_query = st.chat_input("Your response...")
        
        if user_query:
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            
            with st.spinner("Analyzing your response..."):
                # If this is the third question's response, send a concluding message
                if st.session_state.questions_asked == 3:
                    concluding_message = (
                        "Thank you for your detailed responses throughout this technical assessment. "
                        "I appreciate your thorough explanations and technical knowledge demonstrated. "
                    )
                    st.session_state.chat_history.append(AIMessage(content=concluding_message))
                    st.session_state.questions_asked = 4  # Set to 4 to trigger the feedback section
                else:
                    # For first and second questions, continue with normal response
                    response = get_response(user_query, st.session_state.chat_history, st.session_state.tech_stack)
                    st.session_state.chat_history.append(AIMessage(content=response))
                    st.session_state.questions_asked += 1
                st.rerun()

    # Enhanced completion message
    if st.session_state.questions_asked > 3:
        st.markdown("""
        <div class="success-message">
            ✨ Technical assessment completed! Thank you for your time.
            We will review your responses and get back to you soon.
        </div>
        """, unsafe_allow_html=True)
        
        # Feedback section
        if "feedback_submitted" not in st.session_state:
            st.session_state.feedback_submitted = False
            
        if not st.session_state.feedback_submitted:
            st.subheader("📝 Your Feedback")
            feedback = st.slider("How would you rate this interview experience?", 1, 5, 3)
            feedback_text = st.text_area("Any additional comments?")
            
            if st.button("Submit Feedback"):
                st.session_state.feedback.append({
                    "rating": feedback,
                    "comment": feedback_text,
                    "timestamp": datetime.now()
                })
                st.session_state.feedback_submitted = True
                st.success("Thank you for your feedback! 🙏")

        # Restart option
        if st.button("📝 Start New Interview"):
            st.session_state.chat_history = [
                AIMessage(content="👋 Welcome to TalentScout! I'm your AI Hiring Assistant. Let's start with your details.")
            ]
            st.session_state.questions_asked = 0
            st.session_state.submitted_form = False
            st.session_state.tech_stack = ""
            st.session_state.feedback_submitted = False
            st.rerun()