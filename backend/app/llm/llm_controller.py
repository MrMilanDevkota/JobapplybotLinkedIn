from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv

# Import the Config class from  config.py file
from app.config.config import Config

class LLMController:
    def __init__(self):
        self.config = Config()
        os.environ["GOOGLE_API_KEY"] = self.config.GEMINI_API_KEY


    def setup_llm(self):
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.environ["GOOGLE_API_KEY"], 
            temperature=0.7
        )
        return llm
    
    def get_llm_instance(self):
        """Returns the initialized LLM instance."""
        return self.llm

    # You can add more LLM-related methods here, e.g., for generating cover letters
    def generate_cover_letter_intro(self, job_title, company, skills):
        prompt_template = PromptTemplate(
            template=(
                "Write a concise introduction for a cover letter for a {job_title} position "
                "at {company}. Highlight that I possess {skills} and am eager to contribute."
            ),
            input_variables=["job_title", "company", "skills"]
        )
        prompt = prompt_template.format(job_title=job_title, company=company, skills=skills)
        response = self.llm.invoke(prompt)
        return response