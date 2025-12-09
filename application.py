import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator
from src.config.settings import settings
load_dotenv()


def main():
    st.set_page_config(page_title="AI Quiz" , page_icon="🎧🎧")

    if 'quiz_manager'not in st.session_state:
        st.session_state.quiz_manager = QuizManager()

    if 'quiz_generated'not in st.session_state:
        st.session_state.quiz_generated = False

    if 'quiz_submitted'not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger'not in st.session_state:
        st.session_state.rerun_trigger = False
    
    if 'groq_api_key' not in st.session_state:
        st.session_state.groq_api_key = ""
    
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
    
    if 'selected_provider' not in st.session_state:
        st.session_state.selected_provider = "Groq"
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = settings.GROQ_MODELS[0]
    
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = "Friendly Tutor"
    
    if 'custom_persona' not in st.session_state:
        st.session_state.custom_persona = ""
        

    st.title("AI QUIZ GENERATOR ")

    st.sidebar.header("Model Configuration")

    # Model Provider Selection
    model_provider = st.sidebar.selectbox(
        "Select Model Provider",
        settings.MODEL_PROVIDERS,
        index=settings.MODEL_PROVIDERS.index(st.session_state.selected_provider)
    )

    # Update provider in session state
    if model_provider != st.session_state.selected_provider:
        st.session_state.selected_provider = model_provider
        # Reset model selection when provider changes
        if model_provider == "Groq":
            st.session_state.selected_model = settings.GROQ_MODELS[0]
        else:
            st.session_state.selected_model = settings.OPENAI_MODELS[0]

    # Model Selection based on Provider
    if model_provider == "Groq":
        available_models = settings.GROQ_MODELS
        api_key_label = "Groq API Key"
        api_key_help = "Enter your Groq API key (required)"
        current_api_key = st.session_state.groq_api_key
    else:
        available_models = settings.OPENAI_MODELS
        api_key_label = "OpenAI API Key"
        api_key_help = "Enter your OpenAI API key (required)"
        current_api_key = st.session_state.openai_api_key

    selected_model = st.sidebar.selectbox(
        "Select Model",
        available_models,
        index=available_models.index(st.session_state.selected_model) if st.session_state.selected_model in available_models else 0
    )
    st.session_state.selected_model = selected_model

    # API Key Input - Store in provider-specific session variable
    api_key = st.sidebar.text_input(
        api_key_label,
        type="password",
        value=current_api_key,
        help=api_key_help,
        placeholder=f"Enter your {model_provider} API key"
    )
    
    # Update the appropriate session variable based on provider (strip whitespace)
    if model_provider == "Groq":
        st.session_state.groq_api_key = api_key.strip() if api_key else ""
    else:
        st.session_state.openai_api_key = api_key.strip() if api_key else ""

    st.sidebar.markdown("---")
    st.sidebar.header("Quiz Settings")

    # Persona Selection
    persona_options_display = [f"{settings.PERSONAS[p]['icon']} {p}" for p in settings.PERSONA_OPTIONS]
    selected_persona_display = st.sidebar.selectbox(
        "Select Quiz Persona",
        persona_options_display,
        index=persona_options_display.index(f"{settings.PERSONAS[st.session_state.selected_persona]['icon']} {st.session_state.selected_persona}")
    )
    
    # Extract persona name without icon
    selected_persona = selected_persona_display.split(" ", 1)[1]
    st.session_state.selected_persona = selected_persona
    
    # Show custom persona input if Custom is selected
    custom_persona_description = ""
    if selected_persona == "Custom":
        st.sidebar.markdown("**Define Your Custom Persona:**")
        custom_persona_description = st.sidebar.text_area(
            "Custom Persona Description",
            value=st.session_state.custom_persona,
            placeholder="e.g., A sports commentator explaining science, A detective investigating historical events, A pirate teaching navigation",
            help="Describe the persona/character that will create your quiz questions",
            height=100
        )
        st.session_state.custom_persona = custom_persona_description
    else:
        # Show description of selected persona
        st.sidebar.info(settings.PERSONAS[selected_persona]['description'])

    question_type = st.sidebar.selectbox(
        "Select Question Type" ,
        ["Multiple Choice" , "Fill in the Blank"],
        index=0
    )

    topic = st.sidebar.text_input("Ennter Topic" , placeholder="Indian History, geography", value="Cricket")

    difficulty = st.sidebar.selectbox(
        "Dificulty Level",
        ["Easy" , "Medium" , "Hard"],
        index=1
    )

    num_questions = st.sidebar.number_input(
        "Number of Questions",
        min_value=1, max_value=10, value=3
    )

    
    if st.sidebar.button("Generate Quiz"):
        # Get the appropriate API key based on provider
        if model_provider == "Groq":
            active_api_key = st.session_state.groq_api_key
        else:
            active_api_key = st.session_state.openai_api_key
        
        # Strip whitespace
        active_api_key = active_api_key.strip() if active_api_key else ""
        
        # Validate API key
        if not active_api_key:
            st.sidebar.error(f"⚠️ Please enter your {model_provider} API key!")
            return
        
        if not topic:
            st.sidebar.error("⚠️ Please enter a topic!")
            return
        
        # Validate custom persona if selected
        if selected_persona == "Custom" and not custom_persona_description.strip():
            st.sidebar.error("⚠️ Please describe your custom persona!")
            return

        # Determine persona style
        if selected_persona == "Custom":
            persona_style = custom_persona_description
        else:
            persona_style = settings.PERSONAS[selected_persona]['style']

        # Debug info (will appear in terminal/logs, not in UI)
        import logging
        logging.info(f"Provider: {st.session_state.selected_provider}, Model: {st.session_state.selected_model}")
        logging.info(f"API Key length: {len(active_api_key)}, First 10 chars: {active_api_key[:10] if len(active_api_key) > 10 else 'TOO_SHORT'}")

        st.session_state.quiz_submitted = False

        # Create generator with selected provider, API key, model, and persona
        generator = QuestionGenerator(
            provider=st.session_state.selected_provider,
            api_key=active_api_key,
            model=st.session_state.selected_model,
            persona_style=persona_style
        )
        
        succces = st.session_state.quiz_manager.generate_questions(
            generator,
            topic,question_type,difficulty,num_questions
        )

        st.session_state.quiz_generated= succces
        rerun()

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count/total_questions)*100
            st.write(f"Score : {score_percentage}")

            for _, result in results_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:
                    st.success(f"✅ Question {question_num} : {result['question']}")
                else:
                    st.error(f"❌ Question {question_num} : {result['question']}")
                    st.write(f"Your answer : {result['user_answer']}")
                    st.write(f"Correct answer : {result['correct_answer']}")
                
                st.markdown("-------")

            
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file,'rb') as f:
                        st.download_button(
                            label="Downlaod Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime='text/csv'
                        )
                else:
                    st.warning("No results avialble")

if __name__=="__main__":
    main()

        
