# Quick Start Guide - PostgreSQL Database Manager

## 30 Second Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start PostgreSQL (if not running)
```bash
# Docker (easiest)
docker run --name postgres -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres

# OR macOS with Homebrew
brew services start postgresql

# OR Windows - Start PostgreSQL from Services
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Open Browser
Navigate to: **http://localhost:5000**

---

## Using the Application

### 📝 **Create a Table**

1. Radio button: Select **"Create Table"**
2. Server: Choose `localhost`
3. Database: Select your database (or create one first in PostgreSQL)
4. Schema: Select `public` (or your schema)
5. Table Name: Enter any name (e.g., `users`, `products`)
6. Click: **Create Table**

✅ Table created with `id` (primary key) and `created_at` (timestamp) columns

---

### ➕ **Insert Data**

1. Radio button: Select **"Insert Data"**
2. Server: Choose `localhost`
3. Database: Select same database
4. Schema: Select same schema
5. Table: Choose your table from dropdown
6. **View the columns** displayed
7. Data Input: Enter comma-separated values matching column order
   - Example: `John Doe, 30, john@example.com`
8. Click: **Insert Data**

✅ Data inserted into table

---

## Common Errors & Solutions

| Error | Solution |
|-------|----------|
| `Connection refused` | Start PostgreSQL (Docker or brew) |
| `Database not found` | Create database first in PostgreSQL |
| `Column mismatch` | Count columns shown, match with your input values |
| `Table already exists` | Use different name or drop table in PostgreSQL |

---

## First Time Setup Example

### Create Sample Database
```bash
psql -U postgres -h localhost

CREATE DATABASE myapp;
\q
```

### Use the App
1. Open http://localhost:5000
2. Create Table mode:
   - Server: localhost
   - Database: myapp
   - Schema: public
   - Table name: users
   - Click Create Table

3. Insert Data mode:
   - Select the "users" table
   - You'll see columns: id, created_at
   - Type: `1, 2024-01-01`
   - Click Insert Data

---

## File Structure
```
your-project/
├── app.py                 ← Main Flask application
├── requirements.txt       ← Python packages
├── README.md             ← Full documentation
├── QUICKSTART.md         ← This file
└── templates/
    └── index.html        ← Web interface
```

---

## Accessing PostgreSQL Directly

```bash
# Connect to postgres
psql -U postgres -h localhost

# List databases
\l

# Connect to database
\c myapp

# List tables
\dt

# View table
SELECT * FROM public.users;

# Drop table if needed
DROP TABLE public.users;
```

---

## Support

- **Port**: 5000 (Flask app)
- **Database**: localhost:5432 (PostgreSQL)
- **Username**: postgres
- **Password**: 1234

If issues persist, check:
1. PostgreSQL running: `psql -U postgres -c "SELECT 1"`
2. Flask running: Check terminal for errors
3. Browser console: Press F12 and check for errors

---

## Next Steps

- ✅ Add more columns to tables manually in PostgreSQL
- ✅ Create indexes for performance
- ✅ Set up daily backups
- ✅ Explore PostgreSQL documentation for advanced features
