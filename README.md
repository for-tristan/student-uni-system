
| Area               | Technology                         | Who uses it |
| ------------------ | ---------------------------------- | ----------- |
| Mobile             | **Flutter**                 | 2 Flutter   |
| Web                | **React + TypeScript**             | 2 Frontend  |
| Backend            | **FastAPI + Python**               | Full-stack  |
| Database           | **PostgreSQL / turso sql**          | Full-stack  |
| AI                 | **Python + Hugging Face + Ollama** | 2 AI        |
| UI/UX              | **Figma Free**                     | UI/UX       |
| Version control    | **Git + GitHub Free**              | Everyone    |
| Code editor        | **VS Code**                        | Everyone    |
| Documentation      | **GitHub Wiki/Markdown**           | Everyone    |
| Project management | **GitHub Projects**                | You         |



---

# 1. Mobile — Flutter

Your two Flutter developers should use:

**Flutter**

[Flutter Documentation](https://docs.flutter.dev/?utm_source=chatgpt.com)

Teach/revise:

```text
Dart
 ↓
Flutter Widgets
 ↓
Layouts
 ↓
Navigation
 ↓
State Management
 ↓
REST APIs
 ↓
JSON
 ↓
Authentication
 ↓
Local Storage
 ↓
Testing
```

### Don't teach them 5 state-management libraries.

Pick **one**.

For your team, I'd recommend:

**Riverpod**

Then both Flutter developers use the same architecture.

---

# 2. Web — React + TypeScript

Your two frontend developers should use:

**React + TypeScript**

I'd strongly recommend TypeScript rather than plain JavaScript.

Teach:

```text
HTML/CSS
 ↓
JavaScript basics
 ↓
TypeScript
 ↓
React
 ↓
Components
 ↓
Props
 ↓
State
 ↓
React Router
 ↓
API calls
 ↓
Authentication
 ↓
Forms/validation
 ↓
Error/loading states
```

You don't need Next.js for this mini-project.

**React + Vite** is enough.

---

# 3. Backend — FastAPI

Your full-stack developer should use:

**Python + FastAPI**

[FastAPI Documentation](https://fastapi.tiangolo.com/?utm_source=chatgpt.com)

This is particularly useful because your AI engineers will already be working in Python.

Your architecture becomes:

```text
Flutter
    │
    │
    ▼
FastAPI ─────── PostgreSQL
    │
    │
    ▼
   AI
```

Teach the full-stack developer:

### Python

* Functions
* Classes
* Type hints
* Virtual environments
* Packages
* Async basics

### FastAPI

* Routes
* Request/response models
* Pydantic
* Authentication
* JWT
* Middleware
* Error handling
* File uploads
* API documentation

### Database

* SQL
* PostgreSQL
* Relationships
* Primary/foreign keys
* Indexes
* Transactions
* ORM

I'd use **SQLAlchemy**.

---

# 4. Database — PostgreSQL

Use PostgreSQL.

You have two options:

### Option A — Supabase

Probably easiest for your team.

You get:

```text
PostgreSQL
Authentication
Storage
Dashboard
```

And the free plan is sufficient for a small project. ([Supabase][3])

### Option B — Local PostgreSQL

Install PostgreSQL on the developer's machine.

This is completely free and gives your team more experience managing a real database.

### For the mini-project:

I'd use **Supabase**.

For the actual graduation project, you can decide whether you want to keep it or move to another deployment architecture.

---

# 5. AI — This is where I would be careful

You said you have **two AI engineers**.

Don't build your entire project around a paid AI API.

If you want **zero dollars**, I'd teach them:

### Python

*

### Hugging Face

*

### Ollama

Ollama lets you run models locally.

So instead of:

```text
Your app
   ↓
Paid AI API
   ↓
$$$
```

you can have:

```text
Your app
   ↓
FastAPI
   ↓
Ollama
   ↓
Local AI model
```

The downside is that **the computer running the model needs enough RAM/compute**, so this depends on your team's hardware.

---

# 6. What should the AI engineers actually learn?

This is important.

Don't tell them:

> "Learn AI."

That's way too broad.

Give them these topics:

### AI Engineer #1

Focus on:

**LLMs + RAG**

Learn:

```text
LLM
 ↓
Prompting
 ↓
Embeddings
 ↓
Vector database
 ↓
Retrieval
 ↓
RAG
```

Their practice task:

> Build a university document Q&A system.

---

### AI Engineer #2

Focus on:

**ML + recommendation/evaluation**

Learn:

```text
Python
 ↓
NumPy
 ↓
Pandas
 ↓
Scikit-learn
 ↓
Model
 ↓
Evaluation
```

Their practice task:

> Build a student/course recommendation system.

Then both AI engineers learn how to expose their work through an API.

---

# 7. Vector Database

For the RAG system, don't immediately introduce something complicated.

For the mini-project, you can use:

**FAISS**

It's free and runs locally.

Later, if the graduation project requires it, you can consider:

* pgvector
* Qdrant
* Chroma

But don't teach your team 5 technologies when one is enough.

---

# 8. UI/UX — Figma

Your designer should use:

**Figma Free**

They should learn:

```text
User research
 ↓
User flows
 ↓
Wireframes
 ↓
Components
 ↓
Design system
 ↓
High-fidelity UI
 ↓
Prototype
 ↓
Developer handoff
```

The important thing is that the designer shouldn't disappear for three days and suddenly give everyone a Figma file.

They should work closely with the developers.

---

# 9. GitHub — EVERYONE

This is actually one of the most important technologies for your team.

Use:

[GitHub](https://github.com/?utm_source=chatgpt.com)

GitHub Free gives you unlimited repositories and allows collaboration, so you don't need to pay for your mini-project. ([GitHub][2])

Everyone needs to learn:

```text
git clone
git pull
git add
git commit
git push
git branch
git checkout / switch
git merge
git rebase
```

And especially:

**Pull Requests**

Your workflow should be:

```text
Issue
 ↓
Create branch
 ↓
Write code
 ↓
Commit
 ↓
Push
 ↓
Pull Request
 ↓
Code review
 ↓
Merge
```

Nobody pushes directly to `main`.

---

# 10. Docker

I would teach Docker **only to the backend + AI people initially**.

Your architecture could eventually look like:

```text
┌─────────────────────────────┐
│          Flutter            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│           FastAPI           │
│          Backend            │
└───────┬─────────────┬───────┘
        │             │
        ▼             ▼
 ┌────────────┐  ┌────────────┐
 │ PostgreSQL │  │  AI/RAG    │
 │            │  │  Service   │
 └────────────┘  └────────────┘
        ▲             ▲
        │             │
        └──────┬──────┘
               │
        ┌──────┴──────┐
        │    React    │
        │     Web     │
        └─────────────┘
```

That's a **real software architecture**, but still manageable for students.

---

# What I would NOT teach right now

This is important.

Your team has **8 people and limited time**.

Don't overwhelm them with:

❌ Kubernetes
❌ Microservices
❌ AWS
❌ Azure
❌ Terraform
❌ GraphQL
❌ Redis
❌ Kafka
❌ Jenkins
❌ 4 different databases
❌ 3 frontend frameworks
❌ 5 AI frameworks

You don't need them.

For your practice project, **simple and integrated beats impressive and complicated.**

---

# Your final stack

I'd literally put this in your team's README:

```text
SMART UNIVERSITY ASSISTANT
==========================

Mobile
- Flutter
- Dart
- Riverpod

Web
- React
- TypeScript
- Vite

Backend
- Python
- FastAPI
- SQLAlchemy
- JWT

Database
- PostgreSQL
- Supabase

AI
- Python
- Hugging Face
- Ollama
- FAISS
- scikit-learn

Design
- Figma

Development
- VS Code
- Git
- GitHub
- Docker

Testing
- Postman
- Pytest
- Flutter testing
- React testing
```

**Estimated software cost: $0.**

The only potential issue is AI compute: running larger local models depends on the team's PCs. You can use smaller models or free hosted services where appropriate, but don't design the project around a service that unexpectedly requires a credit card.

---

## And here's what I'd teach them BEFORE assigning the project

Don't throw them directly into the mini-project.

Give them **3 days of preparation**:

### Day 1 — Git + GitHub

Everyone learns:

* clone
* branch
* commit
* push
* pull request
* merge
* resolving conflicts

Then give them a tiny exercise:

> Everyone modifies the same project and creates a PR.

---

### Day 2 — API + Database

Backend + frontend + Flutter + AI people learn:

```text
HTTP
REST
GET
POST
PUT
DELETE
JSON
Status codes
Authentication
```

Then build:

```text
GET /students
POST /students
GET /students/{id}
```

---

### Day 3 — Integration

Make:

```text
React
   ↓
FastAPI
   ↓
PostgreSQL
```

and:

```text
Flutter
   ↓
FastAPI
   ↓
PostgreSQL
```

work together.

**Only after those three days would I start the actual mini-project.**

That way you're testing your team on **software engineering**, not testing who can Google a framework fastest.

[1]: https://docs.flutter.dev/resources/faq?utm_source=chatgpt.com "FAQ"
[2]: https://github.com/pricing?utm_source=chatgpt.com "Pricing · Plans for every developer · GitHub"
[3]: https://supabase.com/pricing?utm_source=chatgpt.com "Pricing & Fees | Supabase"
