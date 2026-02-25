from http.client import HTTPException
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import json
from app.database import get_db
from app.models import Job, Trade, Term
from app.schemas import JobResponse,JobDetailResponse
from app.dependencies import get_current_admin
from app.services.cloudinary_service import upload_image

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", dependencies=[Depends(get_current_admin)])
def create_job(
    title: str = Form(...),
    company_name: str = Form(...),
    location: str = Form(...),
    salary_range: str = Form(...),
    trades: str = Form(...),
    terms: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_url = upload_image(image.file)

    job = Job(
        title=title,
        company_name=company_name,
        location=location,
        salary_range=salary_range,
        job_image_url=image_url
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    trades_list = json.loads(trades)
    for t in trades_list:
        db.add(Trade(trade_name=t["trade_name"], salary=t["salary"], job_id=job.id))

    terms_data = json.loads(terms)
    db.add(Term(job_id=job.id, **terms_data))

    db.commit()
    return {"message": "Job created successfully"}


@router.get("/", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


@router.get("/{job_id}", response_model=JobDetailResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}", dependencies=[Depends(get_current_admin)])
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    db.delete(job)
    db.commit()
    return {"message": "Deleted"}
@router.put("/{job_id}", dependencies=[Depends(get_current_admin)])
def update_job(
    job_id: int,
    title: str = Form(...),
    company_name: str = Form(...),
    location: str = Form(...),
    salary_range: str = Form(...),
    trades: str = Form(...),
    terms: str = Form(...),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.title = title
    job.company_name = company_name
    job.location = location
    job.salary_range = salary_range

    # Delete old trades & terms
    db.query(Trade).filter(Trade.job_id == job_id).delete()
    db.query(Term).filter(Term.job_id == job_id).delete()

    # Add new trades
    trades_list = json.loads(trades)
    for t in trades_list:
        db.add(
            Trade(
                trade_name=t["trade_name"],
                salary=t["salary"],
                job_id=job.id
            )
        )

    # Add new terms
    terms_data = json.loads(terms)
    db.add(Term(job_id=job.id, **terms_data))

    db.commit()

    return {"message": "Job updated successfully"}