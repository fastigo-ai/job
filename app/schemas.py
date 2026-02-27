from pydantic import BaseModel
from typing import List, Optional


# class TradeCreate(BaseModel):
#     trade_name: str
#     salary: str


# class TermCreate(BaseModel):
#     duty_hours: str
#     food: str
#     accommodation: str
#     ot_policy: str
#     contract: str
#     age_limit: str


class JobCreate(BaseModel):
    title: str
    company_name: str
    location: str
    salary_range: str
    # trades: List[TradeCreate]
    # terms: TermCreate

# class TradeResponse(BaseModel):
#     id: int
#     trade_name: str
#     salary: str

#     model_config = {
#         "from_attributes": True
    # }   
# class TermResponse(BaseModel):
#     id: int
#     duty_hours: str
#     food: str
#     accommodation: str
#     ot_policy: str
#     contract: str
#     age_limit: str

#     model_config = {
#         "from_attributes": True
#     }
        
class JobResponse(BaseModel):
    id: int
    title: str
    company_name: str
    location: str
    salary_range: str
    job_image_url: str

    class Config:
        orm_mode = True
        
class JobDetailResponse(BaseModel):
    id: int
    title: str
    company_name: str
    location: str
    salary_range: str
    job_image_url: str
    # trades: List[TradeResponse]
    # terms: Optional[TermResponse]

    model_config = {
        "from_attributes": True 
    }
class ApplicationResponse(BaseModel):
    id: int
    # trade: str
    mobile_number: str
    resume_url: str

    model_config = {
        "from_attributes": True
    }