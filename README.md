# University Course Recommendation System

A content-based university course recommendation engine that recommends the **Top 5 courses** to a student based on their interests, skills, and previously completed courses.

The system combines a transparent **rule-based baseline** with a **TF-IDF + cosine similarity** content-based recommender, and exposes the results through a FastAPI API.

---

## Project Goals

Given a `student_id`, the system returns the student's top recommended courses:

```json
{
  "student_id": 1,
  "recommendations": [
    {
      "course_id": 101,
      "course_name": "Machine Learning",
      "score": 0.92,
      "reasons": [
        "Matches your AI interest",
        "Matches your Python skills",
        "Prerequisites completed"
      ]
    }
  ]
}
```

Each recommendation includes:
- Course ID
- Course name
- Recommendation score
- Data-driven explanation / reasons

---

## Recommendation Pipeline

```text
Student ID
     ↓
Student Data
     ↓
Preprocessing
     ↓
Prerequisite Filtering
     ↓
Student Profile
     ↓
TF-IDF / Cosine Similarity
     ↓
Ranking
     ↓
Explanation
     ↓
Top 5 Recommendations
     ↓
FastAPI
```

### Phase 1 — Rule-Based Baseline

```text
Final Score =
    Interest Match       × 30%
  + Skill Match          × 30%
  + Prerequisite Match  × 20%
  + Category Match       × 10%
  + Difficulty Fit      × 10%
```

### Phase 2 — Content-Based ML Recommender

Each course is converted into a text representation built from its
name, description, category, and skills. The text is vectorized with
**TF-IDF** and compared against a student profile vector using
**cosine similarity**.

---

## Technology Stack

| Layer        | Tool                                    |
|--------------|-----------------------------------------|
| Language     | Python 3.11+                            |
| Data         | pandas, NumPy                           |
| ML           | scikit-learn (TF-IDF, cosine similarity)|
| API          | FastAPI + Uvicorn                       |
| Testing      | pytest                                 |
| Notebooks    | Jupyter (experiments)                   |

The project intentionally avoids Kubernetes, Docker, microservices,
Kafka, Redis, GraphQL, cloud infrastructure, multiple databases, and
complex MLOps platforms. The objective is a clean, understandable
recommendation system.

---

## Project Structure

```text
course-recommender/
├── data/                  # Synthetic datasets (students, courses, enrollments)
├── notebooks/             # Experiments and exploratory analysis
├── src/
│   ├── data/              # Data loading and preprocessing
│   ├── models/            # Baseline + TF-IDF recommenders
│   ├── evaluation/        # Precision@K / Recall@K metrics
│   └── utils/             # Shared helpers
├── api/                   # FastAPI application
├── tests/                 # Unit and integration tests
├── requirements.txt
├── README.md
└── .gitignore
```

> Files are created incrementally across the 10 development stages.
> Not every directory above is populated yet at this stage.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/for-tristan/student-uni-system.git
cd student-uni-system
git checkout Ai
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify the environment

```bash
python3 -c "import sys, numpy, pandas, sklearn, fastapi, uvicorn, pytest; print('Python', sys.version.split()[0]); print('numpy', numpy.__version__); print('pandas', pandas.__version__); print('scikit-learn', sklearn.__version__); print('fastapi', fastapi.__version__); print('uvicorn', uvicorn.__version__); print('pytest', pytest.__version__)"
```

Expected output (versions may differ slightly):

```text
Python 3.12.x
numpy 2.x
pandas 2.x
scikit-learn 1.x
fastapi 0.x
uvicorn 0.x
pytest 8.x
```

---

## Development Stages

This project is built incrementally across exactly **10 stages**,
each with its own Git commit:

1. Project setup
2. Synthetic dataset
3. Data preprocessing
4. Rule-based recommendation baseline
5. Content-based ML recommender (TF-IDF)
6. Recommendation explanations
7. Evaluation system (Precision@K / Recall@K)
8. FastAPI integration
9. Testing, refactoring & documentation
10. Final integration & demo

---

## Status

| Stage | Description                          | Status |
|-------|--------------------------------------|--------|
| 1     | Project setup                        | ✅ Done |
| 2     | Synthetic dataset                   | ⏳ Pending |
| 3     | Data preprocessing                   | ⏳ Pending |
| 4     | Rule-based baseline                  | ⏳ Pending |
| 5     | TF-IDF recommender                   | ⏳ Pending |
| 6     | Recommendation explanations          | ⏳ Pending |
| 7     | Evaluation system                    | ⏳ Pending |
| 8     | FastAPI integration                  | ⏳ Pending |
| 9     | Testing & documentation              | ⏳ Pending |
| 10    | Final integration & demo             | ⏳ Pending |

---

## License

This is a graduation-project academic artifact. No external license
file is bundled at this stage; one can be added in a later stage if
required by the project team.
