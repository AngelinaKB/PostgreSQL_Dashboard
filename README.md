# PostgreSQL Database Manager

A modern web application for managing PostgreSQL databases with an intuitive interface to create tables and insert data.

## Features

✨ **Create Tables with Custom Columns**: 
- Select server, database, schema, and provide a table name
- **NEW:** Add custom columns with a + button
- Type column name and select data type from dropdown
- See real-time preview of all columns
- Automatically includes `id` (primary key) and `created_at` (timestamp) columns

📝 **Insert Data with Table Preview**:
- Select existing tables from your database
- **NEW:** View first 5 rows of data in an interactive table
- View column names and data types
- Insert comma-separated values matching column count

🎨 **Modern UI**:
- Dark theme with gradient accents
- Responsive design
- Real-time form validation
- Smooth animations and transitions
- Interactive column builder with live preview
- Beautiful data table display

## Prerequisites

- Python 3.7+
- PostgreSQL server running locally (default connection: `localhost`)
- PostgreSQL user: `postgres`
- PostgreSQL password: `1234`

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure PostgreSQL is running**:
   ```bash
   # On Linux/Mac
   brew services start postgresql
   
   # On Windows
   # Start PostgreSQL service from Services or PostgreSQL installer
   
   # Or use Docker
   docker run --name postgres -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres
   ```

3. **Verify PostgreSQL connection** (optional):
   ```bash
   psql -U postgres -h localhost -c "SELECT version();"
   ```

## Running the Application

1. **Start the Flask application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Create Table Mode

1. Select **"Create Table"** radio button
2. Choose a **Server** (localhost or 127.0.0.1)
3. Select a **Database** from the dropdown
4. Choose a **Schema** (e.g., public)
5. Enter a **Table Name**

#### Adding Custom Columns (Optional)
- Click the **+ button** to add a column
- Enter the **Column Name** (e.g., email, age, name)
- Select a **Data Type** from the dropdown:
  - Numbers: INTEGER, BIGINT, SERIAL, SMALLINT, NUMERIC, DECIMAL, REAL, DOUBLE PRECISION
  - Text: TEXT, VARCHAR, CHAR, VARCHAR(255)
  - Date/Time: DATE, TIME, TIMESTAMP, TIMESTAMP WITH TIME ZONE
  - Other: BOOLEAN, UUID, JSON, JSONB, BYTEA, ARRAY
- Click **✕** to remove a column
- See preview of all columns in real-time

6. Click **Create Table**

**Default Columns** (always included):
- `id` (SERIAL PRIMARY KEY)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### Insert Data Mode

1. Select **"Insert Data"** radio button
2. Choose a **Server**
3. Select a **Database**
4. Choose a **Schema**
5. Select a **Table** from the dropdown
6. Review **Table Columns** display showing column names and data types
7. **NEW:** View the **First 5 Rows** of existing data in the table
8. Enter **Data** as comma-separated values matching the column count
9. Click **Insert Data**

**Example**:
If your table has columns: `name`, `email`, `age`, you would enter:
```
John Doe, john@example.com, 30
```

## File Structure

```
.
├── app.py                 # Flask application and API endpoints
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # HTML template with embedded CSS and JS
└── README.md             # This file
```

## API Endpoints

- `GET /` - Main page
- `GET /api/databases?server=<server>` - Get list of databases
- `GET /api/schemas?database=<database>` - Get list of schemas
- `GET /api/tables?database=<database>&schema=<schema>` - Get list of tables
- `GET /api/columns?database=<database>&schema=<schema>&table=<table>` - Get table columns
- `GET /api/data-types` - Get available PostgreSQL data types
- `GET /api/table-data?database=<database>&schema=<schema>&table=<table>` - Get first 5 rows of table data
- `POST /api/create-table` - Create a new table with custom columns
- `POST /api/insert-data` - Insert data into a table

## Request/Response Examples

### Create Table with Custom Columns

**Request**:
```json
{
  "server": "localhost",
  "database": "mydb",
  "schema": "public",
  "tableName": "users",
  "columns": [
    {"name": "name", "type": "VARCHAR(255)"},
    {"name": "email", "type": "VARCHAR(255)"},
    {"name": "age", "type": "INTEGER"},
    {"name": "is_active", "type": "BOOLEAN"}
  ]
}
```

**Response**:
```json
{
  "success": true,
  "message": "Table users created successfully with 6 columns"
}
```

### Get Table Data

**Request**:
```
GET /api/table-data?database=mydb&schema=public&table=users
```

**Response**:
```json
{
  "columns": ["id", "name", "email", "age", "is_active", "created_at"],
  "rows": [
    [1, "John Doe", "john@example.com", 30, true, "2024-01-01T12:00:00"],
    [2, "Jane Smith", "jane@example.com", 28, true, "2024-01-01T13:00:00"]
  ]
}
```

### Insert Data

**Request**:
```json
{
  "database": "mydb",
  "schema": "public",
  "table": "users",
  "values": "Alice Smith, alice@example.com, 28, true"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Data inserted successfully"
}
```

## Supported Data Types

### Numeric
- INTEGER, BIGINT, SMALLINT, SERIAL, BIGSERIAL, SMALLSERIAL
- NUMERIC, DECIMAL, REAL, DOUBLE PRECISION
- MONEY

### Text
- TEXT, VARCHAR, CHAR, CHARACTER, VARCHAR(255)

### Date/Time
- DATE, TIME, TIMESTAMP, TIMESTAMP WITH TIME ZONE, INTERVAL

### Other
- BOOLEAN, UUID, JSON, JSONB, BYTEA, ARRAY

## Troubleshooting

**Connection Error**:
- Ensure PostgreSQL is running
- Verify credentials in `app.py` (host, user, password)
- Check if PostgreSQL is listening on localhost:5432

**Database Not Appearing**:
- Make sure the database exists in PostgreSQL
- Some databases may be system databases (they're filtered out)

**Schema Not Appearing**:
- Ensure the schema exists in your database
- System schemas starting with `pg_` are hidden

**Table Not Found**:
- Confirm the table exists in the selected schema
- Try refreshing by re-selecting the schema

**Column Mismatch Error**:
- Count the columns shown in the display
- Ensure your comma-separated values match that count exactly
- Note: `id` and `created_at` are auto-populated, don't include them in data input

**Column Creation Error**:
- Ensure column names don't contain spaces or special characters
- Use valid PostgreSQL column names (letters, numbers, underscores)
- Select a valid data type from the dropdown

## Advanced Configuration

To connect to a remote PostgreSQL server, edit `app.py`:

```python
PG_HOST = 'your-remote-host'
PG_USER = 'your-username'
PG_PASSWORD = 'your-password'
```

## Security Notes

⚠️ **For Development Only**: This application is suitable for local development. For production use:
- Use environment variables for credentials
- Implement user authentication
- Add SQL injection protection (already using parameterized queries)
- Implement role-based access control
- Use HTTPS
- Add input validation and sanitization

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify PostgreSQL connection
3. Check browser console for errors (F12)
4. Review Flask application logs in terminal

---

**Version 2.0** - Enhanced with custom column builder and table data preview
