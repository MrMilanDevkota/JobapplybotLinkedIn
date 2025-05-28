
class PromptTemplate:

    def generate_answer_with_llm(llm, question, resume_data, job_title, company):
        """Generate an appropriate answer to a custom question using the LLM with improved error handling"""
        try:
            print(f"Generating answer for question: {question}")
            
            # Check if question is empty or too short
            if not question or len(question) < 5:
                print("Question text too short, skipping LLM generation")
                return ""
                
            # Extract skills and experience from resume data for use in the prompt
            skills = ", ".join(resume_data["skills"][:5]) if "skills" in resume_data else ""
            experience_summary = ""
            if "work_experience" in resume_data and resume_data["work_experience"]:
                latest_job = resume_data["work_experience"][0]
                experience_summary = f"{latest_job.get('title', '')} at {latest_job.get('company', '')} - {latest_job.get('description', '')}"
            
            # Build a more focused prompt template
            from langchain import PromptTemplate
            prompt_template = PromptTemplate(
                input_variables=["question", "job_title", "company", "skills", "experience", "profile"],
                template="""
                You are helping a job applicant answer a question on a LinkedIn job application form.
                
                JOB: {job_title} at {company}
                
                QUESTION: {question}
                
                APPLICANT INFO:
                - Skills: {skills}
                - Recent Experience: {experience}
                - Additional Profile Info: {profile}
                
                Write a concise, professional response that directly answers the question. 
                Make it specific to the job position and highlight relevant skills or experience.
                Keep it under 100 words, using first-person perspective. Just write the very short answer directly, and if the answer is numbers then answer in digits.
                Don't start with phrases like "As a [job title]" or "Based on my experience" - just answer directly.
                Only output the answer text with no quotation marks or additional commentary.
                """
            )
            
            # Extract a compact profile summary for the prompt
            profile_summary = f"Education: {resume_data['education'][0]['degree'] if 'education' in resume_data and resume_data['education'] else 'Not specified'}, "
            profile_summary += f"Years of experience: {resume_data['questions'].get('years_of_experience', 'Not specified')}, "
            profile_summary += f"Willing to relocate: {resume_data['questions'].get('willing_to_relocate', 'Not specified')}"
            
            # Format the prompt with our data
            formatted_prompt = prompt_template.format(
                question=question,
                job_title=job_title,
                company=company,
                skills=skills,
                experience=experience_summary,
                profile=profile_summary
            )
            print(formatted_prompt)
            
            # Generate the answer with timeout handling
            try:
                response = llm.invoke(formatted_prompt)
                answer = response.strip()
                
                # Handle common edge cases
                if "As an AI assistant" in answer or "As an AI language model" in answer:
                    answer = answer.split("\n", 1)[1] if "\n" in answer else ""
                
                # Remove any quotation marks around the answer
                answer = answer.strip('"\'')
                
                print(f"Generated answer: {answer[:100]}...")
                return answer
            except Exception as e:
                print(f"LLM timeout or error: {e}")
                # Fall through to simple fallback
            
        except Exception as e:
            print(f"Error generating answer with LLM: {e}")
        
        # Simple fallback - let the LLM handle everything, no pattern matching
        skills_list = resume_data.get('skills', ['problem-solving', 'communication', 'teamwork'])
        top_skills = ', '.join(skills_list[:3])
        experience_years = resume_data.get('questions', {}).get('years_of_experience', '3+')
        
        return f"Based on my {experience_years} years of experience with {top_skills}, I believe I would be able to make strong contributions to this {job_title} role. I'm excited about the opportunity to bring my skills to {company} and help achieve your team's goals."
