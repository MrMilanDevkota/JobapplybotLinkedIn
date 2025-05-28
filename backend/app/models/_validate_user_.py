from pydantic import BaseModel, EmailStr, Field, constr


class UserValidation(BaseModel):
    LINKEDIN_EMAIL : str
    LINKEDIN_PASSWORD : str
    JOB_TITLE : str
    JOB_LOCATION : str
    RESUME_PATH : str
    PHONE_NUMBER : int
    USER_WEBSITE : str
    MAX_APPLICATIONS : int = Field(gt=0, lt=20)
