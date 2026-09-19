from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Dict, List

# --- Determinism -----------------------------------------------------------
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# --- Paths -----------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

STUDENTS_CSV = DATA_DIR / "students.csv"
COURSES_CSV = DATA_DIR / "courses.csv"
ENROLLMENTS_CSV = DATA_DIR / "enrollments.csv"


# ===========================================================================
# COURSE CATALOG
# ===========================================================================
# Each course dict: name, category, description, skills, prerequisites,
# difficulty, credits. Prerequisites reference course NAMES (resolved to
# course_id after catalog is built) to keep the taxonomy human-readable.
# ---------------------------------------------------------------------------
COURSE_CATALOG: List[Dict] = [
    # --- AI (5 courses) -----------------------------------------------------
    {"name": "Introduction to Artificial Intelligence",
     "category": "AI",
     "description": "Overview of AI: search, knowledge representation, reasoning, and agents.",
     "skills": ["Python", "Algorithms", "Logic"],
     "prerequisites": [],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Machine Learning",
     "category": "AI",
     "description": "Supervised and unsupervised learning methods, model evaluation, and regularization.",
     "skills": ["Python", "Statistics", "Algorithms"],
     "prerequisites": ["Introduction to Artificial Intelligence"],
     "difficulty": "Advanced", "credits": 3},
    {"name": "Deep Learning",
     "category": "AI",
     "description": "Neural networks, backpropagation, CNNs, RNNs, and modern architectures.",
     "skills": ["Python", "Linear Algebra", "Machine Learning"],
     "prerequisites": ["Machine Learning"],
     "difficulty": "Advanced", "credits": 4},
    {"name": "Computer Vision",
     "category": "AI",
     "description": "Image processing, feature detection, and visual recognition systems.",
     "skills": ["Python", "Linear Algebra", "Machine Learning"],
     "prerequisites": ["Machine Learning"],
     "difficulty": "Advanced", "credits": 3},
    {"name": "Natural Language Processing",
     "category": "AI",
     "description": "Text processing, language models, sequence labelling, and transformers.",
     "skills": ["Python", "Machine Learning", "Linguistics"],
     "prerequisites": ["Machine Learning"],
     "difficulty": "Advanced", "credits": 3},

    # --- Data Science (5 courses) -----------------------------------------
    {"name": "Statistics for Data Science",
     "category": "Data Science",
     "description": "Descriptive and inferential statistics for data analysis.",
     "skills": ["Statistics", "Python", "Probability"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Database Systems",
     "category": "Data Science",
     "description": "Relational model, SQL, normalization, transactions, and indexing.",
     "skills": ["SQL", "Databases", "Data Modeling"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Data Mining",
     "category": "Data Science",
     "description": "Mining and analyzing large datasets for patterns and insights.",
     "skills": ["Python", "SQL", "Statistics"],
     "prerequisites": ["Database Systems", "Statistics for Data Science"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Big Data Analytics",
     "category": "Data Science",
     "description": "Distributed data processing, MapReduce, and large-scale pipelines.",
     "skills": ["Python", "SQL", "Distributed Systems"],
     "prerequisites": ["Data Mining"],
     "difficulty": "Advanced", "credits": 4},
    {"name": "Data Visualization",
     "category": "Data Science",
     "description": "Principles and tools for effective visual communication of data.",
     "skills": ["Python", "Statistics", "Design"],
     "prerequisites": ["Statistics for Data Science"],
     "difficulty": "Intermediate", "credits": 3},

    # --- Web (5 courses) ---------------------------------------------------
    {"name": "Web Development Fundamentals",
     "category": "Web",
     "description": "HTML, CSS, and modern web page structure and styling.",
     "skills": ["HTML", "CSS", "JavaScript"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Frontend Development",
     "category": "Web",
     "description": "Modern frontend frameworks, component design, and state management.",
     "skills": ["JavaScript", "React", "CSS"],
     "prerequisites": ["Web Development Fundamentals"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Backend Development",
     "category": "Web",
     "description": "Server-side development, REST APIs, authentication, and databases.",
     "skills": ["Python", "REST", "Databases"],
     "prerequisites": ["Web Development Fundamentals", "Database Systems"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Full Stack Development",
     "category": "Web",
     "description": "End-to-end web applications integrating frontend and backend systems.",
     "skills": ["JavaScript", "React", "Python", "REST"],
     "prerequisites": ["Frontend Development", "Backend Development"],
     "difficulty": "Advanced", "credits": 4},
    {"name": "Cloud Web Applications",
     "category": "Web",
     "description": "Deploying and scaling web applications on cloud platforms.",
     "skills": ["Cloud", "Docker", "DevOps"],
     "prerequisites": ["Backend Development"],
     "difficulty": "Advanced", "credits": 3},

    # --- Cybersecurity (5 courses) -----------------------------------------
    {"name": "Introduction to Cybersecurity",
     "category": "Cybersecurity",
     "description": "Core security principles, threats, vulnerabilities, and defense strategies.",
     "skills": ["Security", "Linux", "Networking"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Network Fundamentals",
     "category": "Cybersecurity",
     "description": "Computer networks, protocols, routing, and the OSI model.",
     "skills": ["Networking", "Linux"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Network Security",
     "category": "Cybersecurity",
     "description": "Securing computer networks: firewalls, IDS/IPS, VPNs, and monitoring.",
     "skills": ["Networking", "Linux", "Security"],
     "prerequisites": ["Introduction to Cybersecurity", "Network Fundamentals"],
     "difficulty": "Advanced", "credits": 3},
    {"name": "Ethical Hacking",
     "category": "Cybersecurity",
     "description": "Penetration testing methodologies and offensive security techniques.",
     "skills": ["Linux", "Security", "Networking"],
     "prerequisites": ["Network Security"],
     "difficulty": "Advanced", "credits": 3},
    {"name": "Cryptography",
     "category": "Cybersecurity",
     "description": "Symmetric and asymmetric cryptography, hashing, and protocols.",
     "skills": ["Mathematics", "Security", "Python"],
     "prerequisites": ["Introduction to Cybersecurity"],
     "difficulty": "Advanced", "credits": 3},

    # --- Software Engineering (5 courses) ----------------------------------
    {"name": "Programming Fundamentals",
     "category": "Software Engineering",
     "description": "Introduction to programming with Python: variables, control flow, functions.",
     "skills": ["Python", "Algorithms"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Data Structures",
     "category": "Software Engineering",
     "description": "Lists, trees, graphs, hash tables, and complexity analysis.",
     "skills": ["Python", "Algorithms", "Data Structures"],
     "prerequisites": ["Programming Fundamentals"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Algorithms",
     "category": "Software Engineering",
     "description": "Design and analysis of algorithms: sorting, searching, graphs, dynamic programming.",
     "skills": ["Algorithms", "Python", "Data Structures"],
     "prerequisites": ["Data Structures"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Software Engineering Principles",
     "category": "Software Engineering",
     "description": "Software lifecycle, design patterns, testing, and project management.",
     "skills": ["Software Design", "Testing", "Git"],
     "prerequisites": ["Data Structures"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Distributed Systems",
     "category": "Software Engineering",
     "description": "Consensus, replication, fault tolerance, and distributed algorithms.",
     "skills": ["Algorithms", "Distributed Systems", "Networking"],
     "prerequisites": ["Algorithms", "Network Fundamentals"],
     "difficulty": "Advanced", "credits": 4},

    # --- Math & Foundations (5 courses) ------------------------------------
    {"name": "Calculus I",
     "category": "Mathematics",
     "description": "Limits, derivatives, and applications of differentiation.",
     "skills": ["Mathematics", "Calculus"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 4},
    {"name": "Linear Algebra",
     "category": "Mathematics",
     "description": "Vectors, matrices, eigenvalues, and linear transformations.",
     "skills": ["Linear Algebra", "Mathematics"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Discrete Mathematics",
     "category": "Mathematics",
     "description": "Logic, sets, combinatorics, graph theory, and proofs.",
     "skills": ["Logic", "Mathematics", "Proofs"],
     "prerequisites": [],
     "difficulty": "Beginner", "credits": 3},
    {"name": "Probability Theory",
     "category": "Mathematics",
     "description": "Probability spaces, random variables, distributions, and limit theorems.",
     "skills": ["Probability", "Mathematics", "Calculus"],
     "prerequisites": ["Calculus I"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Numerical Methods",
     "category": "Mathematics",
     "description": "Numerical algorithms for solving mathematical problems on computers.",
     "skills": ["Python", "Mathematics", "Linear Algebra"],
     "prerequisites": ["Linear Algebra", "Calculus I"],
     "difficulty": "Intermediate", "credits": 3},

    # --- Mobile (3 courses) ------------------------------------------------
    {"name": "Mobile App Development",
     "category": "Mobile",
     "description": "Building mobile applications for Android and iOS platforms.",
     "skills": ["Mobile", "Dart", "UI Design"],
     "prerequisites": ["Programming Fundamentals"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "iOS Development",
     "category": "Mobile",
     "description": "Native iOS development with Swift and the iOS SDK.",
     "skills": ["Swift", "Mobile", "UI Design"],
     "prerequisites": ["Mobile App Development"],
     "difficulty": "Advanced", "credits": 3},
    {"name": "Android Development",
     "category": "Mobile",
     "description": "Native Android development with Kotlin and the Android SDK.",
     "skills": ["Kotlin", "Mobile", "UI Design"],
     "prerequisites": ["Mobile App Development"],
     "difficulty": "Advanced", "credits": 3},

    # --- Systems (3 courses) -----------------------------------------------
    {"name": "Operating Systems",
     "category": "Systems",
     "description": "Processes, threads, memory management, file systems, and scheduling.",
     "skills": ["Linux", "C", "Systems"],
     "prerequisites": ["Data Structures"],
     "difficulty": "Intermediate", "credits": 4},
    {"name": "Computer Networks",
     "category": "Systems",
     "description": "Architecture and protocols of the Internet and modern computer networks.",
     "skills": ["Networking", "Linux", "Systems"],
     "prerequisites": ["Operating Systems"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Compilers",
     "category": "Systems",
     "description": "Lexing, parsing, semantic analysis, and code generation.",
     "skills": ["Algorithms", "Data Structures", "Compilers"],
     "prerequisites": ["Algorithms"],
     "difficulty": "Advanced", "credits": 4},

    # --- Theory (4 courses) ------------------------------------------------
    {"name": "Theory of Computation",
     "category": "Theory",
     "description": "Automata, formal languages, and computability.",
     "skills": ["Logic", "Proofs", "Theory"],
     "prerequisites": ["Discrete Mathematics"],
     "difficulty": "Intermediate", "credits": 3},
    {"name": "Database Theory",
     "category": "Theory",
     "description": "Relational algebra, query optimization, and database internals.",
     "skills": ["Databases", "Logic", "Theory"],
     "prerequisites": ["Database Systems", "Discrete Mathematics"],
     "difficulty": "Advanced", "credits": 3},
    {"name": "Algorithm Analysis",
     "category": "Theory",
     "description": "Advanced techniques for analyzing algorithm complexity and efficiency.",
     "skills": ["Algorithms", "Proofs", "Theory"],
     "prerequisites": ["Algorithms"],
     "difficulty": "Advanced", "credits": 3},
    {"name": "Quantum Computing",
     "category": "Theory",
     "description": "Quantum bits, gates, algorithms, and quantum information theory.",
     "skills": ["Linear Algebra", "Physics", "Theory"],
     "prerequisites": ["Linear Algebra", "Probability Theory"],
     "difficulty": "Advanced", "credits": 4},
]


# ===========================================================================
# STUDENT POOL
# ===========================================================================
# Predefined profiles give realistic interest/skill/major combinations.
# ---------------------------------------------------------------------------
STUDENT_PROFILES: List[Dict] = [
    {"name": "Aisha", "year": 3, "major": "Computer Science",
     "interests": ["AI", "Machine Learning", "Data Science"],
     "skills": ["Python", "SQL", "Algorithms"]},
    {"name": "Marco", "year": 2, "major": "Computer Science",
     "interests": ["Web Development", "Cloud"],
     "skills": ["JavaScript", "React", "HTML", "CSS"]},
    {"name": "Salma", "year": 4, "major": "Cybersecurity",
     "interests": ["Cybersecurity", "Networks"],
     "skills": ["Linux", "Python", "Networking"]},
    {"name": "John", "year": 3, "major": "Data Science",
     "interests": ["Data Science", "Statistics", "AI"],
     "skills": ["Python", "Statistics", "SQL"]},
    {"name": "Fatima", "year": 1, "major": "Computer Science",
     "interests": ["Programming", "Algorithms"],
     "skills": ["Python"]},
    {"name": "Omar", "year": 3, "major": "Software Engineering",
     "interests": ["Software Engineering", "Systems"],
     "skills": ["Python", "C", "Linux", "Git"]},
    {"name": "Lina", "year": 4, "major": "Computer Science",
     "interests": ["AI", "NLP", "Deep Learning"],
     "skills": ["Python", "Machine Learning", "Linear Algebra"]},
    {"name": "David", "year": 2, "major": "Information Systems",
     "interests": ["Databases", "Data Mining"],
     "skills": ["SQL", "Python", "Data Modeling"]},
    {"name": "Mona", "year": 3, "major": "Computer Science",
     "interests": ["Mobile", "UI Design"],
     "skills": ["Dart", "JavaScript", "UI Design"]},
    {"name": "Karim", "year": 4, "major": "Computer Science",
     "interests": ["Systems", "Operating Systems", "Networks"],
     "skills": ["C", "Linux", "Networking", "Systems"]},
    {"name": "Sara", "year": 2, "major": "Mathematics",
     "interests": ["Mathematics", "Cryptography"],
     "skills": ["Mathematics", "Calculus", "Proofs"]},
    {"name": "Youssef", "year": 3, "major": "Computer Science",
     "interests": ["Theory", "Algorithms", "Compilers"],
     "skills": ["Python", "Algorithms", "Proofs"]},
    {"name": "Hana", "year": 1, "major": "Computer Science",
     "interests": ["Web Development", "Design"],
     "skills": ["HTML", "CSS"]},
    {"name": "Tarek", "year": 4, "major": "Data Science",
     "interests": ["Big Data", "Data Science", "Cloud"],
     "skills": ["Python", "SQL", "Distributed Systems"]},
    {"name": "Nour", "year": 2, "major": "Cybersecurity",
     "interests": ["Security", "Ethical Hacking"],
     "skills": ["Linux", "Security", "Python"]},
    {"name": "Ali", "year": 3, "major": "Software Engineering",
     "interests": ["Software Engineering", "Cloud", "DevOps"],
     "skills": ["Python", "Docker", "Git", "Cloud"]},
    {"name": "Maya", "year": 4, "major": "Computer Science",
     "interests": ["AI", "Computer Vision", "Deep Learning"],
     "skills": ["Python", "Machine Learning", "Linear Algebra"]},
    {"name": "Bilal", "year": 2, "major": "Computer Science",
     "interests": ["Algorithms", "Competitive Programming"],
     "skills": ["Python", "Algorithms", "Data Structures"]},
    {"name": "Yara", "year": 3, "major": "Information Technology",
     "interests": ["Networks", "Cloud"],
     "skills": ["Networking", "Linux", "Cloud"]},
    {"name": "Ziad", "year": 1, "major": "Computer Science",
     "interests": ["Programming", "Mathematics"],
     "skills": ["Python"]},
    {"name": "Reem", "year": 4, "major": "Computer Science",
     "interests": ["AI", "Deep Learning", "Quantum Computing"],
     "skills": ["Python", "Linear Algebra", "Machine Learning"]},
    {"name": "Hassan", "year": 3, "major": "Cybersecurity",
     "interests": ["Cryptography", "Security", "Mathematics"],
     "skills": ["Python", "Mathematics", "Security"]},
    {"name": "Layla", "year": 2, "major": "Data Science",
     "interests": ["Data Visualization", "Statistics"],
     "skills": ["Python", "Statistics", "Design"]},
    {"name": "Adel", "year": 4, "major": "Software Engineering",
     "interests": ["Distributed Systems", "Systems"],
     "skills": ["Python", "Algorithms", "Distributed Systems"]},
    {"name": "Dina", "year": 1, "major": "Computer Science",
     "interests": ["AI", "Robotics"],
     "skills": ["Python", "Mathematics"]},
]


# ===========================================================================
# GENERATION
# ===========================================================================
def _join(items: List[str]) -> str:
    """Join a list of tags into a single CSV cell string."""
    return ",".join(items) if items else ""


def write_courses() -> Dict[str, int]:
    """Write ``courses.csv`` and return a name→course_id lookup table."""
    name_to_id: Dict[str, int] = {}
    rows: List[Dict] = []

    for course_id, course in enumerate(COURSE_CATALOG, start=101):
        name_to_id[course["name"]] = course_id
        rows.append({
            "course_id": course_id,
            "name": course["name"],
            "category": course["category"],
            "description": course["description"],
            "skills": _join(course["skills"]),
            "prerequisites": _join(course["prerequisites"]),  # names, resolved below
            "difficulty": course["difficulty"],
            "credits": course["credits"],
        })

    # Resolve prerequisite names to comma-separated course IDs.
    for row in rows:
        if not row["prerequisites"]:
            continue
        prereq_names = [p.strip() for p in row["prerequisites"].split(",") if p.strip()]
        prereq_ids = [str(name_to_id[name]) for name in prereq_names if name in name_to_id]
        row["prerequisites"] = _join(prereq_ids)

    _write_csv(COURSES_CSV, rows, fieldnames=[
        "course_id", "name", "category", "description",
        "skills", "prerequisites", "difficulty", "credits",
    ])
    print(f"  courses.csv     → {len(rows)} courses")
    return name_to_id


def write_students() -> None:
    """Write ``students.csv`` from STUDENT_PROFILES."""
    rows: List[Dict] = []
    for sid, profile in enumerate(STUDENT_PROFILES, start=1):
        rows.append({
            "student_id": sid,
            "name": profile["name"],
            "year": profile["year"],
            "major": profile["major"],
            "interests": _join(profile["interests"]),
            "skills": _join(profile["skills"]),
        })
    _write_csv(STUDENTS_CSV, rows, fieldnames=[
        "student_id", "name", "year", "major", "interests", "skills",
    ])
    print(f"  students.csv    → {len(rows)} students")


def write_enrollments(name_to_id: Dict[str, int]) -> None:
    """Write ``enrollments.csv`` with realistic, prerequisite-aware statuses."""
    course_by_id: Dict[int, Dict] = {}
    for course in COURSE_CATALOG:
        cid = name_to_id[course["name"]]
        course_by_id[cid] = {
            "course_id": cid,
            "name": course["name"],
            "category": course["category"],
            "difficulty": course["difficulty"],
            "prerequisite_ids": [
                name_to_id[p] for p in course["prerequisites"] if p in name_to_id
            ],
            "prerequisite_names": [p for p in course["prerequisites"] if p in name_to_id],
        }

    rows: List[Dict] = []

    for sid, profile in enumerate(STUDENT_PROFILES, start=1):
        skills = set(profile["skills"])
        interests = set(profile["interests"])

        # Score every course for this student to drive enrollment decisions.
        scored: List[tuple] = []
        for cid, course in course_by_id.items():
            course_skills = set()
            for c in COURSE_CATALOG:
                if name_to_id[c["name"]] == cid:
                    course_skills = set(c["skills"])
                    break

            skill_overlap = len(skills & course_skills)
            interest_tags = {course["category"]} | course_skills
            interest_overlap = len(interests & interest_tags)

            year = profile["year"]
            difficulty = course["difficulty"]
            difficulty_fit = 0
            if year == 1 and difficulty == "Beginner":
                difficulty_fit = 2
            elif year == 2 and difficulty in ("Beginner", "Intermediate"):
                difficulty_fit = 1
            elif year >= 3:
                difficulty_fit = 1

            score = skill_overlap * 3 + interest_overlap * 2 + difficulty_fit
            scored.append((score, cid))

        scored.sort(reverse=True, key=lambda x: (x[0], x[1]))

        target = random.randint(5, 8) if profile["year"] >= 2 else random.randint(4, 6)

        completed_by_student: set = set()
        added_courses: set = set()

        for _, cid in scored:
            if len(added_courses) >= target:
                break
            if cid in added_courses:
                continue

            course = course_by_id[cid]
            prereqs = course["prerequisite_ids"]

            # Enroll in prerequisites first (one level deep — our catalog
            # only has 1–2 levels of prereqs).
            for pid in prereqs:
                if pid not in completed_by_student and pid not in added_courses:
                    if random.random() < 0.85:
                        grade = random.randint(60, 99)
                        rows.append({
                            "student_id": sid,
                            "course_id": pid,
                            "grade": grade,
                            "status": "completed",
                        })
                        completed_by_student.add(pid)
                        added_courses.add(pid)
                        if len(added_courses) >= target:
                            break

            if len(added_courses) >= target:
                break
            if cid in added_courses:
                continue

            year = profile["year"]
            if year == 4:
                status_choice = random.choices(
                    ["completed", "failed", "dropped", "in_progress"],
                    weights=[0.70, 0.10, 0.10, 0.10])[0]
            elif year == 3:
                status_choice = random.choices(
                    ["completed", "in_progress", "failed", "dropped"],
                    weights=[0.45, 0.35, 0.10, 0.10])[0]
            elif year == 2:
                status_choice = random.choices(
                    ["completed", "in_progress", "failed", "dropped"],
                    weights=[0.30, 0.50, 0.10, 0.10])[0]
            else:  # year 1
                status_choice = random.choices(
                    ["in_progress", "completed", "dropped"],
                    weights=[0.70, 0.20, 0.10])[0]

            grade = random.randint(60, 99) if status_choice in ("completed", "failed") else ""
            rows.append({
                "student_id": sid,
                "course_id": cid,
                "grade": grade,
                "status": status_choice,
            })
            added_courses.add(cid)
            if status_choice == "completed":
                completed_by_student.add(cid)

    _write_csv(ENROLLMENTS_CSV, rows, fieldnames=[
        "student_id", "course_id", "grade", "status",
    ])
    print(f"  enrollments.csv → {len(rows)} enrollment records")


# ===========================================================================
# CSV HELPERS
# ===========================================================================
def _write_csv(path: Path, rows: List[Dict], fieldnames: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ===========================================================================
# MAIN
# ===========================================================================
def main() -> None:
    print(f"Generating synthetic dataset into: {DATA_DIR}")
    write_students()
    name_to_id = write_courses()
    write_enrollments(name_to_id)
    print("Done.")


if __name__ == "__main__":
    main()
