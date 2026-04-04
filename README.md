# Spendwise — Expense Tracker with AI Advisor

Spendwise is a production-ready REST API built with Django REST Framework for tracking personal expenses. It includes JWT authentication, expense management with filtering and pagination, monthly budget tracking, CSV export, and an AI advisor powered by Groq's LLaMA 3.3 that analyzes a user's actual expense data to give personalized financial advice.

The project is containerized with Docker, connected to a MySQL database and deployed on Railway. A minimal frontend built with Bootstrap is included to demonstrate the APIs in action.

**Live Demo**: [https://expense-tracker-production-6cce.up.railway.app](https://expense-tracker-production-6cce.up.railway.app)

**API Docs**: [https://expense-tracker-production-6cce.up.railway.app/api/docs/](https://expense-tracker-production-6cce.up.railway.app/api/docs/)

---

## What it does

- Register and login securely with JWT tokens
- Add, edit and delete expenses with categories like food, transport, bills etc.
- Dashboard that shows where your money is going each month
- Set monthly budgets per category and track if you're exceeding them
- Ask the AI advisor questions like "where am I spending the most?" and get real answers based on your data
- Export your expenses to CSV and open in Excel
- Search and filter expenses by category, date, month
- Full API documentation with Swagger UI

---

## Tech Stack

**Backend**
- Python, Django, Django REST Framework
- MySQL
- JWT Authentication (SimpleJWT)
- Groq API with LLaMA 3.3 for AI advisor
- Gunicorn + Whitenoise for production

**Frontend**
- HTML, CSS, JavaScript
- Bootstrap 5

**DevOps**
- Docker and Docker Compose
- Deployed on Railway
- GitHub for version control

---

## API Endpoints

I've documented all endpoints in the Swagger UI — you can test them directly from the browser without Postman:
👉 [API Docs](https://expense-tracker-production-6cce.up.railway.app/api/docs/)

Here's a quick overview:

**Auth** — `/api/users/`
- `POST /register/` — create account
- `POST /login/` — get JWT tokens
- `GET /profile/` — get logged in user info

**Expenses** — `/api/expenses/`
- `GET /` — list expenses, supports filters like `?category=food&month=3&search=lunch`
- `POST /` — add new expense
- `PATCH /{id}/` — update an expense
- `DELETE /{id}/` — delete an expense
- `GET /summary/` — total spent per category for a month
- `GET /export/` — download as CSV

**Budgets** — `/api/budgets/`
- `GET /` — list all budgets
- `POST /` — set a budget for a category and month
- `PATCH /{id}/` — update budget amount
- `DELETE /{id}/` — remove a budget
- `GET /status/` — see how much you've spent vs your budget

**AI Advisor** — `/api/advisor/`
- `POST /ask/` — send a question, get advice based on your actual expense data
- `GET /history/` — see past conversations
---

## Running locally

You'll need Python 3.10+, MySQL and Git installed.
```bash
# Clone the repo
git clone https://github.com/Khushboo2525/expense-tracker.git
cd expense-tracker

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
DB_NAME=expense_tracker_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_secret_key
DEBUG=True
GROQ_API_KEY=your_groq_key

# Create MySQL database
CREATE DATABASE expense_tracker_db;

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

Or with Docker:
```bash
docker-compose up --build
```

---

## Project Structure
```
expense_tracker/
├── expense_tracker/     
├── users/              
├── expenses/            
├── ai_advisor/          
├── budgets/             
├── templates/           
├── static/             
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Author

**Khushboo** — Backend Developer
- GitHub: [@Khushboo2525](https://github.com/Khushboo2525)
- LinkedIn: https://www.linkedin.com/in/khushboobhagchandani