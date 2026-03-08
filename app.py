from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2 import sql
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# PostgreSQL connection details
PG_HOST = 'localhost'
PG_USER = 'postgres'
PG_PASSWORD = '1234'

def get_connection(database='postgres'):
    """Create a connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            user=PG_USER,
            password=PG_PASSWORD,
            database=database
        )
        return conn
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def get_servers():
    """Get list of available servers (in this case, just localhost)"""
    return ['localhost', '127.0.0.1']

def get_databases(server='localhost'):
    """Get list of databases from the server"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT datname FROM pg_database 
            WHERE datistemplate = false 
            ORDER BY datname
        """)
        databases = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return databases
    except Exception as e:
        print(f"Error fetching databases: {e}")
        return []

def get_schemas(database):
    """Get list of schemas from a database"""
    conn = get_connection(database)
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT schema_name FROM information_schema.schemata 
            WHERE schema_name NOT LIKE 'pg_%' 
            AND schema_name != 'information_schema'
            ORDER BY schema_name
        """)
        schemas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return schemas
    except Exception as e:
        print(f"Error fetching schemas: {e}")
        return []

def get_tables(database, schema):
    """Get list of tables from a schema"""
    conn = get_connection(database)
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = %s 
            ORDER BY table_name
        """, (schema,))
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        print(f"Error fetching tables: {e}")
        return []

def get_table_columns(database, schema, table):
    """Get columns and their data types for a table"""
    conn = get_connection(database)
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name, data_type FROM information_schema.columns 
            WHERE table_schema = %s AND table_name = %s 
            ORDER BY ordinal_position
        """, (schema, table))
        columns = [{'name': row[0], 'type': row[1]} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return columns
    except Exception as e:
        print(f"Error fetching columns: {e}")
        return []

def get_table_data(database, schema, table, limit=5):
    """Get first N rows from a table"""
    conn = get_connection(database)
    if not conn:
        return {'columns': [], 'rows': []}
    
    try:
        cursor = conn.cursor()
        # Get columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_schema = %s AND table_name = %s 
            ORDER BY ordinal_position
        """, (schema, table))
        columns = [row[0] for row in cursor.fetchall()]
        
        # Get data
        query = sql.SQL("SELECT * FROM {schema}.{table} LIMIT %s").format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table)
        )
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'columns': columns,
            'rows': [list(row) for row in rows]
        }
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return {'columns': [], 'rows': []}

def get_data_types():
    """Get list of available PostgreSQL data types"""
    return [
        'INTEGER',
        'BIGINT',
        'SMALLINT',
        'SERIAL',
        'BIGSERIAL',
        'SMALLSERIAL',
        'NUMERIC',
        'DECIMAL',
        'REAL',
        'DOUBLE PRECISION',
        'MONEY',
        'TEXT',
        'VARCHAR',
        'CHAR',
        'CHARACTER',
        'VARCHAR(255)',
        'BOOLEAN',
        'DATE',
        'TIME',
        'TIMESTAMP',
        'TIMESTAMP WITH TIME ZONE',
        'INTERVAL',
        'UUID',
        'JSON',
        'JSONB',
        'BYTEA',
        'ARRAY'
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/databases', methods=['GET'])
def api_databases():
    """API endpoint to get databases"""
    server = request.args.get('server', 'localhost')
    databases = get_databases(server)
    return jsonify(databases)

@app.route('/api/schemas', methods=['GET'])
def api_schemas():
    """API endpoint to get schemas"""
    database = request.args.get('database', '')
    if not database:
        return jsonify([])
    schemas = get_schemas(database)
    return jsonify(schemas)

@app.route('/api/tables', methods=['GET'])
def api_tables():
    """API endpoint to get tables"""
    database = request.args.get('database', '')
    schema = request.args.get('schema', '')
    if not database or not schema:
        return jsonify([])
    tables = get_tables(database, schema)
    return jsonify(tables)

@app.route('/api/columns', methods=['GET'])
def api_columns():
    """API endpoint to get table columns"""
    database = request.args.get('database', '')
    schema = request.args.get('schema', '')
    table = request.args.get('table', '')
    if not database or not schema or not table:
        return jsonify([])
    columns = get_table_columns(database, schema, table)
    return jsonify(columns)

@app.route('/api/data-types', methods=['GET'])
def api_data_types():
    """API endpoint to get available data types"""
    return jsonify(get_data_types())

@app.route('/api/table-data', methods=['GET'])
def api_table_data():
    """API endpoint to get table data"""
    database = request.args.get('database', '')
    schema = request.args.get('schema', '')
    table = request.args.get('table', '')
    if not database or not schema or not table:
        return jsonify({'columns': [], 'rows': []})
    data = get_table_data(database, schema, table, limit=5)
    return jsonify(data)

@app.route('/api/create-table', methods=['POST'])
def create_table():
    """Create a new table"""
    data = request.json
    server = data.get('server')
    database = data.get('database')
    schema = data.get('schema')
    table_name = data.get('tableName')
    columns = data.get('columns', [])
    
    if not all([server, database, schema, table_name]):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    conn = get_connection(database)
    if not conn:
        return jsonify({'success': False, 'error': 'Failed to connect to database'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Build column definitions
        column_defs = []
        
        # Always add id primary key
        column_defs.append("id SERIAL PRIMARY KEY")
        
        # Add custom columns
        if columns:
            for col in columns:
                col_name = col.get('name', '').strip()
                col_type = col.get('type', '').strip()
                if col_name and col_type:
                    column_defs.append(f"{col_name} {col_type}")
        
        # Add created_at timestamp
        column_defs.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # Create table
        columns_sql = ', '.join(column_defs)
        create_query = sql.SQL("CREATE TABLE {schema}.{table} ({columns})").format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table_name),
            columns=sql.SQL(columns_sql)
        )
        
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': f'Table {table_name} created successfully with {len(column_defs)} columns'})
    except psycopg2.errors.DuplicateTable:
        return jsonify({'success': False, 'error': 'Table already exists'}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/insert-data', methods=['POST'])
def insert_data():
    """Insert data into a table"""
    data = request.json
    database = data.get('database')
    schema = data.get('schema')
    table = data.get('table')
    values = data.get('values')
    
    if not all([database, schema, table, values]):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    conn = get_connection(database)
    if not conn:
        return jsonify({'success': False, 'error': 'Failed to connect to database'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Get columns for the table
        columns = get_table_columns(database, schema, table)
        
        # Parse comma-separated values
        value_list = [v.strip() for v in values.split(',')]
        
        if len(value_list) != len(columns):
            return jsonify({
                'success': False, 
                'error': f'Expected {len(columns)} values but got {len(value_list)}'
            }), 400
        
        # Build insert query
        column_names = [col['name'] for col in columns]
        placeholders = ','.join(['%s'] * len(column_names))
        
        insert_query = sql.SQL("""
            INSERT INTO {schema}.{table} ({columns})
            VALUES ({values})
        """).format(
            schema=sql.Identifier(schema),
            table=sql.Identifier(table),
            columns=sql.SQL(',').join(sql.Identifier(col) for col in column_names),
            values=sql.SQL(placeholders)
        )
        
        cursor.execute(insert_query, value_list)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Data inserted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)