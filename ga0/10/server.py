from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# ✅ Enable CORS (very important for assignment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ✅ Load CSV data once when server starts
students_data = []

with open("q-fastapi.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        students_data.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })

# ✅ API endpoint
@app.get("/api")
async def get_students(class_: list[str] = Query(default=None, alias="class")):
    
    # If no filter → return all
    if class_ is None:
        return {"students": students_data}

    # Filter by class
    filtered = [
        student for student in students_data
        if student["class"] in class_
    ]

    return {"students": filtered}