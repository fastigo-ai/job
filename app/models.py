from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company_name = Column(String)
    location = Column(String)
    salary_range = Column(String)
    job_image_url = Column(String)
    applications = relationship(
    "JobApplication",
    back_populates="job",
    cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)

    # trades = relationship("Trade", back_populates="job", cascade="all, delete")
    # terms = relationship("Term", back_populates="job", uselist=False, cascade="all, delete")
class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    # trade = Column(String)
    mobile_number = Column(String)
    resume_url = Column(String)

    job_id = Column(Integer, ForeignKey("jobs.id"))

    job = relationship("Job", back_populates="applications")

# class Trade(Base):
#     __tablename__ = "trades"

#     id = Column(Integer, primary_key=True, index=True)
#     trade_name = Column(String)
#     salary = Column(String)
#     job_id = Column(Integer, ForeignKey("jobs.id"))

#     job = relationship("Job", back_populates="trades")


# class Term(Base):
#     __tablename__ = "terms"

#     id = Column(Integer, primary_key=True, index=True)
#     duty_hours = Column(String)
#     food = Column(String)
#     accommodation = Column(String)
#     ot_policy = Column(String)
#     contract = Column(String)
#     age_limit = Column(String)
#     job_id = Column(Integer, ForeignKey("jobs.id"))

#     job = relationship("Job", back_populates="terms")