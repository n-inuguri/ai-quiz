from langchain_core.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    template=(
        "You are a quiz creator with a persona that is {persona_style}.\n\n"
        "Generate a {difficulty} multiple-choice question about {topic} in your persona's style.\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. Return ONLY a valid JSON object - no title, no introduction, no explanation, no extra text\n"
        "2. Do not wrap the JSON in markdown code blocks (no ```json or ```)\n"
        "3. The 'correct_answer' field MUST contain the EXACT text of one of the four options\n"
        "4. All four options must be strings in the options array\n\n"
        "Required JSON structure:\n"
        '{{\n'
        '    "question": "Your engaging question here",\n'
        '    "options": ["First option", "Second option", "Third option", "Fourth option"],\n'
        '    "correct_answer": "Second option"\n'
        '}}\n\n'
        "IMPORTANT: The correct_answer value must be EXACTLY the same as one option (same capitalization, punctuation, spacing).\n\n"
        "Example - Notice how 'Paris' appears EXACTLY the same in both options and correct_answer:\n"
        '{{\n'
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        '}}\n\n'
        "Now generate your JSON (ONLY the JSON, nothing else):"
    ),
    input_variables=["topic", "difficulty", "persona_style"]
)

fill_blank_prompt_template = PromptTemplate(
    template=(
        "You are a quiz creator with a persona that is {persona_style}.\n\n"
        "Generate a {difficulty} fill-in-the-blank question about {topic} in your persona's style.\n\n"
        "CRITICAL: You MUST return ONLY a valid JSON object. Do not include any title, introduction, or explanation.\n"
        "Do not wrap the JSON in markdown code blocks. Return ONLY the raw JSON.\n\n"
        "Required JSON format:\n"
        '{{\n'
        '    "question": "A sentence with _____ marking where the blank should be (reflect your persona in wording)",\n'
        '    "answer": "The correct word or phrase for the blank"\n'
        '}}\n\n'
        "Example:\n"
        '{{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}}\n\n'
        "Return ONLY the JSON object, nothing else:"
    ),
    input_variables=["topic", "difficulty", "persona_style"]
)