# GigHub API

## Description

GigHub API is a FastAPI application for managing freelance gig listings. It allows users to create, view, search, update, and delete gigs.

## Features

- View all gigs
- Filter gigs by category and budget
- Search gigs by title
- View a gig by ID
- Create a new gig
- Update a gig's budget or status
- Delete a gig

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic

## Running the API

1. Activate the virtual environment.
2. Run:

```bash
uvicorn main:app --reload
```

3. Open:

```
http://127.0.0.1:8000/docs
```

to access the Swagger UI.