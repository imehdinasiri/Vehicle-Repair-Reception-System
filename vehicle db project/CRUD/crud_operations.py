import pyodbc
from db_config import get_connection

tables = {
    'Customer': {
        'columns': ['FullName', 'NationalCode', 'Mobile', 'Phone', 'Address', 'PostalCode'],
        'primary_key': 'CustomerID'
    },
    'Car': {
        'columns': ['LicensePlate', 'ChassisNumber', 'EngineNumber', 'Color', 'GearboxType', 'BodyType', 'EngineType'],
        'primary_key': 'CarID',
        'foreign_keys': ['ModelID', 'CustomerID']
    },
    'Reception': {
        'columns': ['ReceptionDate', 'Status', 'KilometerIn', 'KilometerOut', 'EstimatedCost'],
        'primary_key': 'ReceptionID',
        'foreign_keys': ['CarID']
    },
    'RepairOrder': {
        'columns': ['OrderDate', 'Status', 'Description'],
        'primary_key': 'RepairOrderID',
        'foreign_keys': ['ReceptionID']
    },
    'Goods': {
        'columns': ['GoodsName', 'Brand', 'UnitPrice'],
        'primary_key': 'GoodsID'
    },
    'Service': {
        'columns': ['ServiceName', 'Description', 'Cost'],
        'primary_key': 'ServiceID'
    },
    'Staff': {
        'columns': ['FullName', 'Role', 'NationalCode'],
        'primary_key': 'StaffID'
    },
    'CarBrand': {
        'columns': ['BrandName', 'Country'],
        'primary_key': 'BrandID'
    },
    'CarModel': {
        'columns': ['ModelName', 'ProductionYear'],
        'primary_key': 'ModelID',
        'foreign_keys': ['BrandID']
    },
    'Part_Used': {
        'columns': ['QuantityUsed'],
        'primary_key': 'UsedPartID',
        'foreign_keys': ['RepairOrderID', 'GoodsID']
    }
}

def create_record(table_name, columns, foreign_keys=[]):
    conn = get_connection()
    cur = conn.cursor()
    input_values = []
    for col in columns:
        val = input(f"{col}: ").strip()
        if val.isdigit():
            val = int(val)
        input_values.append(val)
    for fk in foreign_keys:
        val = input(f"{fk}: ").strip()
        if val.isdigit():
            val = int(val)
        input_values.append(val)
    full_columns = columns + foreign_keys
    placeholders = ', '.join(['?' for _ in full_columns])
    query = f"INSERT INTO {table_name} ({', '.join(full_columns)}) VALUES ({placeholders})"
    try:
        cur.execute(query, input_values)
        conn.commit()
        print(f"Record added to {table_name}")
    except Exception as e:
        print(f"Insert Error: {e}")
    finally:
        cur.close()
        conn.close()

def read_records(table_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        if not rows:
            print("No records found.")
            return
        columns = [desc[0] for desc in cur.description]
        print("\t".join(columns))
        for row in rows:
            print("\t".join(str(cell) for cell in row))
    except Exception as e:
        print(f"Read Error: {e}")
    finally:
        cur.close()
        conn.close()

def update_record(table_name, primary_key_column, columns):
    conn = get_connection()
    cur = conn.cursor()
    pk_value = input(f"{primary_key_column}: ")
    if pk_value.isdigit():
        pk_value = int(pk_value)

    try:
        cur.execute(f"SELECT 1 FROM {table_name} WHERE {primary_key_column} = ?", (pk_value,))
        if not cur.fetchone():
            print("No record found with this primary key.")
            return

        new_values = []
        for col in columns:
            val = input(f"New {col}: ").strip()
            if val.isdigit():
                val = int(val)
            new_values.append(val)

        set_clause = ", ".join([f"{col} = ?" for col in columns])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key_column} = ?"
        cur.execute(query, new_values + [pk_value])
        conn.commit()
        print(f"Record updated in {table_name}")
    except Exception as e:
        print(f"Update Error: {e}")
    finally:
        cur.close()
        conn.close()

def delete_record(table_name, primary_key_column):
    conn = get_connection()
    cur = conn.cursor()
    pk_value = input(f"{primary_key_column}: ")
    if pk_value.isdigit():
        pk_value = int(pk_value)

    try:
        cur.execute(f"SELECT 1 FROM {table_name} WHERE {primary_key_column} = ?", (pk_value,))
        if not cur.fetchone():
            print("No record found with this primary key.")
            return

        cur.execute(f"DELETE FROM {table_name} WHERE {primary_key_column} = ?", (pk_value,))
        conn.commit()
        print(f"Record deleted from {table_name}")
    except Exception as e:
        print(f"Delete Error: {e}")
    finally:
        cur.close()
        conn.close()

def get_table_and_primary_key():
    print("Select a Table:")
    for idx, table in enumerate(tables.keys(), start=1):
        print(f"{idx}. {table}")
    table_index = int(input("Choose a table by number: ")) - 1
    table_name = list(tables.keys())[table_index]
    primary_key_column = tables[table_name]['primary_key']
    return table_name, primary_key_column

def input_values_for_columns(column_order, primary_key_column, foreign_key_column=None):
    values = []
    for col in column_order:
        if col != primary_key_column and (foreign_key_column is None or col != foreign_key_column):
            val = input(f"Enter value for '{col}': ").strip()
            if val.isdigit():
                val = int(val)
            elif not val:
                val = None
            values.append(val)
    return values
