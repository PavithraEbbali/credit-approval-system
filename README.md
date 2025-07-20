# 🏦 Credit Approval System

A Django-based credit approval backend system that calculates credit scores, checks loan eligibility, creates and manages loans, records EMI payments, and provides customer insights with RESTful APIs and PostgreSQL integration.

---

## 📚 API Documentation

### Available Endpoints

| Endpoint                    | Method | Description                      |
|-----------------------------|--------|----------------------------------|
| `/register`                 | POST   | Register a new customer          |
| `/check-eligibility`        | POST   | Check loan eligibility           |
| `/create-loan`              | POST   | Create a new loan                |
| `/view-loan/<loan_id>`      | GET    | View specific loan details       |
| `/view-loans/<customer_id>` | GET    | View all loans for a customer    |

---

## 📌 Features

- Register new customers with salary-based credit limits  
- Check loan eligibility dynamically  
- Create and manage loans with EMI schedules  
- View customer and loan details  
- Make payments and track EMIs  
- Asynchronous background task support using Celery + Redis  
- Unit tests for core endpoints  
- Dockerized for easy deployment

---

## 🧰 Technologies Used

| Category       | Technologies Used         |
|----------------|---------------------------|
| Backend        | Python 3.10, Django, DRF  |
| Database       | PostgreSQL                |
| Async          | Celery + Redis            |
| Data Handling  | pandas (Excel import)     |
| Deployment     | Docker, Docker Compose    |
| Testing        | Django Test Runner        |

---

## ✅ Prerequisites

- Docker & Docker Compose installed  
- Git  

---

## 🚀 Setup Instructions

### 📁 Step 1: Clone the Repository

```bash
git clone https://github.com/PavithraEbbali/credit-approval-system.git
cd credit-approval-system
```
---

### ⚙️ Step 2: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Add the following content to .env:

```bash
POSTGRES_DB=credit_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
---

### ⚙️ Step 3: Start Docker Containers

Run the following command to build and start the backend, PostgreSQL, and Redis containers:

```bash
docker-compose up --build
```
---

### ⚙️ Step 4: Load Initial Data from Excel

Once the containers are running, open a Django shell inside the backend container:

```bash
docker-compose run backend python manage.py shell
```
Then execute the following Python commands:

```bash
from core.utils import load_initial_data
load_initial_data()
exit()
```
This loads sample customer and loan data from:

backend/data/customer_data.xlsx
backend/data/loan_data.xlsx

---

### ⚙️ Step5: Run Unit Tests

To run the automated unit tests:

```bash
docker-compose run backend python manage.py test
```
---

### 📂 Project Structure

credit-approval-system/
├── backend/
│ ├── config/
│ ├── core/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ ├── tests.py
│ ├── data/
│ │ ├── customer_data.xlsx
│ │ ├── loan_data.xlsx
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore

---

## 📌 Key Notes

### Credit Limit Calculation
`Approved Limit = 36 × Monthly Salary` (rounded to nearest lakh)

### Loan Approval Rules
- **EMI Threshold**: Loan approved only if `EMI ≤ 50% of monthly salary`
- **Credit Score Requirements**:

  | Credit Score | Interest Rate | Approval Status |
  |--------------|---------------|-----------------|
  | ≥ 750        | 12%           | Approved        |
  | 600-749      | 16%           | Approved        |
  | < 600        | N/A           | Rejected        |

### Data Import
Initial data loaded from:
- `backend/data/customer_data.xlsx`
- `backend/data/loan_data.xlsx`
---
