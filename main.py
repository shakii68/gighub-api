from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="GigHub API",
    description="API for managing freelance gigs in Nairobi",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to the GigHub API!"}

gigs_db = [
    {
        "id": 1,
        "title": "Social Media Campaign",
        "description": "Manage a one-month social media campaign for a local fashion business.",
        "category": "Marketing",
        "budget": 15000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jane Wanjiku"
    },
    {
        "id": 2,
        "title": "Sales Data Analysis",
        "description": "Analyze sales data and prepare detailed monthly performance reports.",
        "category": "Data",
        "budget": 22000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Peter Mwangi"
    },
    {
        "id": 3,
        "title": "Business Growth Consulting",
        "description": "Provide consulting services to improve business operations and profitability.",
        "category": "Consulting",
        "budget": 40000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Grace Njeri"
    },
    {
        "id": 4,
        "title": "Email Marketing Strategy",
        "description": "Develop an email marketing strategy for customer engagement.",
        "category": "Marketing",
        "budget": 18000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Brian Otieno"
    },
    {
        "id": 5,
        "title": "Customer Data Cleaning",
        "description": "Clean and organize customer records for improved reporting accuracy.",
        "category": "Data",
        "budget": 25000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Mercy Achieng"
    },
    {
        "id": 6,
        "title": "Financial Consulting",
        "description": "Advise a startup on budgeting and financial planning strategies.",
        "category": "Consulting",
        "budget": 50000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "David Kariuki"
    },
    {
        "id": 7,
        "title": "SEO Optimization",
        "description": "Improve website search engine ranking using SEO best practices.",
        "category": "Marketing",
        "budget": 17000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Ann Wambui"
    },
    {
        "id": 8,
        "title": "Database Reporting",
        "description": "Generate business intelligence reports from customer databases.",
        "category": "Data",
        "budget": 27000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Samuel Kibet"
    },
    {
        "id": 9,
        "title": "HR Policy Review",
        "description": "Review HR policies and recommend improvements for compliance.",
        "category": "Consulting",
        "budget": 35000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Faith Muthoni"
    },
    {
        "id": 10,
        "title": "Digital Marketing Plan",
        "description": "Create a digital marketing plan for a small retail business.",
        "category": "Marketing",
        "budget": 20000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Kevin Maina"
    }
]

class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: str
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)

class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None  

@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):
    """
    Retrieve all gigs with optional filtering.
    """
    filtered_gigs = gigs_db

    if category:
        filtered_gigs = [
            gig for gig in filtered_gigs
            if gig["category"].lower() == category.lower()
        ]

    if min_budget is not None:
        filtered_gigs = [
            gig for gig in filtered_gigs
            if gig["budget"] >= min_budget
        ]

    if max_budget is not None:
        filtered_gigs = [
            gig for gig in filtered_gigs
            if gig["budget"] <= max_budget
        ]

    return filtered_gigs

@app.get("/gigs/search")
def search_gigs(q: str):
    """
    Search gigs by title.
    """
    results = []

    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)

    return results

@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    """
    Retrieve a single gig by its ID.
    """
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")

@app.post("/gigs")
def create_gig(gig: GigCreate):
    """
    Create a new gig.
    """

    allowed_categories = ["Marketing", "Data", "Consulting"]

    if gig.category not in allowed_categories:
        raise HTTPException(
            status_code=400,
            detail="Invalid category"
        )

    new_gig = {
        "id": max(gig["id"] for gig in gigs_db) + 1 if gigs_db else 1,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return new_gig

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update an existing gig.
    """

    allowed_status = ["Open", "In Progress", "Closed"]

    for gig in gigs_db:

        if gig["id"] == gig_id:

            if gig_update.budget is not None:
                gig["budget"] = gig_update.budget

            if gig_update.status is not None:

                if gig_update.status not in allowed_status:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid status"
                    )

                gig["status"] = gig_update.status

            return gig

    raise HTTPException(status_code=404, detail="Gig not found")

@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig.
    """
    for gig in gigs_db:
        if gig["id"] == gig_id:
            gigs_db.remove(gig)
            return {"message": "Gig deleted successfully"}

    raise HTTPException(status_code=404, detail="Gig not found")

