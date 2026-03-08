# PostgreSQL Manager - Feature Guide v2.0

## New Features Overview

### 1. Custom Column Builder (Create Table Mode)

#### How It Works:
When you select "Create Table" mode, you'll see an "Add Columns" section with a **+ button**.

```
┌─────────────────────────────────────────┐
│ Add Columns (Optional)        [+]       │
├─────────────────────────────────────────┤
│ Column Name    │  Data Type     │  ✕    │
├─────────────────────────────────────────┤
│ [email      ]  │ [VARCHAR(255)] │ ✕    │
│ [age        ]  │ [INTEGER]      │ ✕    │
│ [is_active  ]  │ [BOOLEAN]      │ ✕    │
└─────────────────────────────────────────┘
```

#### Step-by-Step Example:

**Creating a "users" table:**

1. Click the **+** button to add a column
2. Type column name: `email`
3. Select data type: `VARCHAR(255)`
4. Click **+** again for next column
5. Type: `age`, Select: `INTEGER`
6. Click **+** for another column
7. Type: `is_active`, Select: `BOOLEAN`
8. Click **+** for one more
9. Type: `created_at`, Select: `TIMESTAMP`
10. Click **Create Table**

**Result**: A table with these columns:
- `id` (SERIAL PRIMARY KEY) ✓ Auto-added
- `email` (VARCHAR(255))
- `age` (INTEGER)
- `is_active` (BOOLEAN)
- `created_at` (TIMESTAMP) ✓ Auto-added (note: column names can be duplicated, so you can name a custom one the same)

#### Removing Columns:
Click the **✕** button next to any column to remove it.

#### Column Preview:
As you add columns, you'll see a real-time preview showing all columns including the auto-generated `id` and `created_at`.

---

### 2. Table Data Preview (Insert Data Mode)

#### How It Works:
When you select a table in "Insert Data" mode, the first 5 rows are automatically displayed in a formatted table.

```
┌────────────────────────────────────────┐
│ First 5 Rows                           │
├───┬──────────┬─────────────────┬────────┤
│ id│ name     │ email           │ age    │
├───┼──────────┼─────────────────┼────────┤
│ 1 │ John Doe │ john@example... │ 30     │
│ 2 │ Jane Sm. │ jane@example... │ 28     │
│ 3 │ Bob Joh. │ bob@example.... │ 35     │
│ 4 │ Alice W. │ alice@example.. │ 27     │
│ 5 │ Charlie  │ charlie@exam... │ 32     │
└───┴──────────┴─────────────────┴────────┘
```

#### Features:
- Shows actual data from your table
- Displays all columns
- Truncates long values to prevent overflow
- Shows "(null)" for empty values
- If table is empty, shows "No data in this table yet"
- If table has fewer than 5 rows, shows all available rows

#### When Empty Table:
```
┌────────────────────────────────────────┐
│ First 5 Rows                           │
├────────────────────────────────────────┤
│ No data in this table yet              │
└────────────────────────────────────────┘
```

---

## Available Data Types

### Numeric Types
- `INTEGER` - Standard 32-bit integer (-2,147,483,648 to 2,147,483,647)
- `BIGINT` - 64-bit integer (for very large numbers)
- `SMALLINT` - 16-bit integer (-32,768 to 32,767)
- `SERIAL` - Auto-incrementing integer (like MySQL AUTO_INCREMENT)
- `BIGSERIAL` - Auto-incrementing big integer
- `SMALLSERIAL` - Auto-incrementing small integer
- `NUMERIC` - Exact decimal number with precision
- `DECIMAL` - Same as NUMERIC
- `REAL` - Floating-point number (6 decimal digits)
- `DOUBLE PRECISION` - Floating-point number (15 decimal digits)
- `MONEY` - Currency amount (for money values)

### Text Types
- `TEXT` - Variable unlimited length text
- `VARCHAR` - Variable length up to limit
- `VARCHAR(255)` - Variable length up to 255 characters
- `CHAR` - Fixed length single character
- `CHARACTER` - Fixed length text

### Date/Time Types
- `DATE` - Date only (YYYY-MM-DD)
- `TIME` - Time only (HH:MM:SS)
- `TIMESTAMP` - Date and time (YYYY-MM-DD HH:MM:SS)
- `TIMESTAMP WITH TIME ZONE` - Timestamp with timezone
- `INTERVAL` - Time interval/duration

### Other Types
- `BOOLEAN` - True/False
- `UUID` - Universally unique identifier
- `JSON` - JSON data structure
- `JSONB` - Binary JSON (faster, supports indexing)
- `BYTEA` - Binary data
- `ARRAY` - Array of any type

---

## Common Use Cases

### Example 1: E-commerce Product Table

**Columns to add:**
1. `product_name` → VARCHAR(255)
2. `description` → TEXT
3. `price` → NUMERIC
4. `stock_quantity` → INTEGER
5. `is_available` → BOOLEAN
6. `category` → VARCHAR(100)

**Result table structure:**
```
id (SERIAL PK)
product_name (VARCHAR)
description (TEXT)
price (NUMERIC)
stock_quantity (INTEGER)
is_available (BOOLEAN)
category (VARCHAR)
created_at (TIMESTAMP)
```

### Example 2: User Authentication Table

**Columns to add:**
1. `username` → VARCHAR(100)
2. `email` → VARCHAR(255)
3. `password_hash` → TEXT
4. `last_login` → TIMESTAMP WITH TIME ZONE
5. `is_verified` → BOOLEAN
6. `verification_token` → UUID

**Result table structure:**
```
id (SERIAL PK)
username (VARCHAR)
email (VARCHAR)
password_hash (TEXT)
last_login (TIMESTAMP WITH TZ)
is_verified (BOOLEAN)
verification_token (UUID)
created_at (TIMESTAMP)
```

### Example 3: Blog Post Table

**Columns to add:**
1. `title` → VARCHAR(255)
2. `content` → TEXT
3. `author` → VARCHAR(100)
4. `tags` → JSON
5. `view_count` → INTEGER
6. `published_date` → DATE
7. `is_published` → BOOLEAN

**Result table structure:**
```
id (SERIAL PK)
title (VARCHAR)
content (TEXT)
author (VARCHAR)
tags (JSON)
view_count (INTEGER)
published_date (DATE)
is_published (BOOLEAN)
created_at (TIMESTAMP)
```

---

## Tips & Tricks

### ✅ Best Practices

1. **Use descriptive column names**
   - ✓ `customer_email` (good)
   - ✗ `ce` (bad)

2. **Choose appropriate data types**
   - Use BIGINT for very large numbers
   - Use BOOLEAN for true/false values
   - Use JSON for complex structures
   - Use TEXT for unlimited length strings

3. **Plan your schema first**
   - Think about what data you'll store
   - Consider future growth
   - Add all needed columns upfront

4. **Don't include auto-columns manually**
   - `id` and `created_at` are added automatically
   - You don't need to add them yourself

### ⚡ Quick Shortcuts

- **To clear form**: Click "Clear" button
- **To remove column**: Click "✕" button next to it
- **To see preview**: As you add columns, preview updates in real-time
- **To refresh data**: Click on table dropdown again

### 🔍 When Inserting Data

Remember:
- Column order matters
- Don't include `id` values (auto-generated)
- Don't include `created_at` (auto-generated with current time)
- Separate values with commas
- Text values don't need quotes in the interface

**Example input:**
```
John Doe, john@example.com, 30, true
```

(For: name, email, age, is_active)

---

## Troubleshooting New Features

### Column Builder Issues

**Problem: Column not appearing**
- Make sure you typed a column name AND selected a data type
- Both fields must have values

**Problem: Can't remove column**
- Click the ✕ button on the right side of the column
- If not visible, scroll right or resize window

**Problem: Data type list empty**
- The page may still be loading
- Try refreshing your browser
- Check browser console for errors (F12)

### Table Preview Issues

**Problem: No data displayed**
- Table might be empty (shows "No data in this table yet")
- This is normal for newly created tables

**Problem: Some columns not showing**
- Scroll horizontally in the table
- Or view the table in a wider window

**Problem: Values appear truncated**
- This is by design to prevent overflow
- Full data is in the database, just displayed shortened
- Hover over values for tooltip (browser dependent)

---

## What's New in Version 2.0

✨ **Enhanced Features:**
- ✅ Custom column builder with live preview
- ✅ Support for 26+ PostgreSQL data types
- ✅ Real-time column preview display
- ✅ First 5 rows table display in insert mode
- ✅ Better error messages
- ✅ Improved form validation
- ✅ More responsive design

🚀 **Performance:**
- Faster data loading
- Optimized database queries
- Smoother animations

🎨 **UI/UX:**
- Better visual feedback
- More intuitive column management
- Clearer data presentation

---

## API Changes (For Developers)

### New Endpoints

**GET /api/data-types**
Returns list of available PostgreSQL data types.

**Response:**
```json
[
  "INTEGER",
  "BIGINT",
  "VARCHAR",
  "TEXT",
  ...
]
```

**GET /api/table-data**
Returns first 5 rows from a table.

**Parameters:**
- `database` - Database name
- `schema` - Schema name
- `table` - Table name

**Response:**
```json
{
  "columns": ["id", "name", "email"],
  "rows": [
    [1, "John", "john@example.com"],
    [2, "Jane", "jane@example.com"]
  ]
}
```

### Updated Endpoints

**POST /api/create-table**
Now accepts custom columns.

**Request:**
```json
{
  "server": "localhost",
  "database": "mydb",
  "schema": "public",
  "tableName": "users",
  "columns": [
    {"name": "email", "type": "VARCHAR(255)"},
    {"name": "age", "type": "INTEGER"}
  ]
}
```

---

## Need Help?

- 📖 Read the full README.md
- 💬 Check browser console (F12) for errors
- 🔧 Verify PostgreSQL is running
- 📧 Review logs in Flask terminal output
