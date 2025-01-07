# TalentScout Hiring Assistant Chatbot

## Project Overview

The TalentScout Hiring Assistant is an AI-powered chatbot designed for a fictional recruitment agency specializing in technology placements. The chatbot automates the initial screening of candidates by collecting essential details, prompting for a tech stack, and generating tailored technical questions to assess their proficiency.

## Features

- **Interactive UI**: Developed using Streamlit for a clean and user-friendly interface.
- **Candidate Information Collection**: Gathers essential details like name, email, years of experience, desired position, and tech stack.
- **Tech-Specific Questions**: Automatically generates technical questions based on the declared tech stack (e.g., Python, Django).
- **Context-Aware Conversations**: Maintains a coherent flow during the interaction.
- **Fallback Mechanism**: Handles unexpected inputs gracefully.
- **Conversation Conclusion**: Ends conversations politely and informs candidates about the next steps.

## Technologies Used

- **Programming Language**: Python
- **Libraries**:
  - Streamlit: Frontend development
  - LangChain: Prompt engineering and LLM integration
  - ChatGroq: LLM API
- **Model**: Llama-3.3-70b-versatile (via ChatGroq API)

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AtharvaGhodki/Hiring-Bot.git
   cd Hiring-Bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add your API key:
     ```
     GROQ_API_KEY=your_api_key
     ```
4. Run the application locally:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

1. Open the application in your browser.
2. Fill in the candidate information form, including your tech stack.
3. Interact with the chatbot for technical screening.
4. View progress and receive tailored technical questions.

## Prompt Design

- Prompts are crafted to:
  - Gather essential candidate details.
  - Generate relevant technical questions based on the tech stack.
  - Maintain conversation context and coherence.

## Challenges and Solutions

- **Challenge**: Handling diverse tech stacks and unexpected inputs.
  - **Solution**: Implemented robust prompt engineering and fallback mechanisms to ensure smooth interactions.
- **Challenge**: Maintaining conversation flow.
  - **Solution**: Used session state to preserve context across interactions.

## Acknowledgments

- Llama-3.3 model for language processing.
- Streamlit for simplifying UI development.
- LangChain and ChatGroq for enabling advanced prompt engineering.

---

For any questions or support, please contact [[your-email@example.com](mailto\:your-email@example.com)].

