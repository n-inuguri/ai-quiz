from langchain_core.output_parsers import PydanticOutputParser
from src.models.question_schemas import MCQQuestion,FillBlankQuestion
from src.prompts.templates import mcq_prompt_template,fill_blank_prompt_template
from src.llm.llm_factory import get_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    def __init__(self, provider: str = None, api_key: str = None, model: str = None, persona_style: str = None):
        """
        Initialize QuestionGenerator with dynamic LLM provider and persona.
        
        Args:
            provider: Model provider ('Groq' or 'OpenAI')
            api_key: API key for the selected provider
            model: Model name
            persona_style: Persona style description for question generation
        """
        if provider and api_key and model:
            self.llm = get_llm(provider, api_key, model)
        else:
            # Fallback to default Groq for backward compatibility
            from src.llm.groq_client import get_groq_llm
            self.llm = get_groq_llm()
        
        self.persona_style = persona_style or "neutral and educational"
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self, prompt, parser, topic, difficulty):

        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty} and persona {self.persona_style}")

                response = self.llm.invoke(prompt.format(
                    topic=topic,
                    difficulty=difficulty,
                    persona_style=self.persona_style
                ))

                # Clean the response content - remove markdown code blocks if present
                content = response.content.strip()
                
                # Remove markdown code block markers if they exist
                if content.startswith("```json"):
                    content = content[7:]  # Remove ```json
                elif content.startswith("```"):
                    content = content[3:]  # Remove ```
                
                if content.endswith("```"):
                    content = content[:-3]  # Remove closing ```
                
                content = content.strip()
                
                self.logger.info(f"Cleaned response content: {content[:100]}...")

                parsed = parser.parse(content)

                self.logger.info("Sucesfully parsed the question")

                return parsed
            
            except Exception as e:
                self.logger.error(f"Error coming (attempt {attempt + 1}/{settings.MAX_RETRIES}): {str(e)}")
                self.logger.error(f"Response content was: {response.content if 'response' in locals() else 'No response'}")
                if attempt==settings.MAX_RETRIES-1:
                    raise CustomException(f"Generation failed after {settings.MAX_RETRIES} attempts", e)
                
    
    def generate_mcq(self,topic:str,difficulty:str='medium') -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)

            question = self._retry_and_parse(mcq_prompt_template,parser,topic,difficulty)

            # Detailed validation logging
            self.logger.info(f"MCQ validation - Options count: {len(question.options)}, Options: {question.options}, Correct answer: {question.correct_answer}")
            
            if len(question.options) != 4:
                raise ValueError(f"Invalid MCQ Structure: Expected 4 options, got {len(question.options)}")
            
            if question.correct_answer not in question.options:
                raise ValueError(f"Invalid MCQ Structure: Correct answer '{question.correct_answer}' not found in options {question.options}")
            
            self.logger.info("Generated a valid MCQ Question")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ : {str(e)}")
            raise CustomException("MCQ generation failed" , e)
        
    
    def generate_fill_blank(self,topic:str,difficulty:str='medium') -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)

            question = self._retry_and_parse(fill_blank_prompt_template,parser,topic,difficulty)

            if "___" not in question.question:
                raise ValueError("Fill in blanks should contain '___'")
            
            self.logger.info("Generated a valid Fill in Blanks Question")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate fillups : {str(e)}")
            raise CustomException("Fill in blanks generation failed" , e)

