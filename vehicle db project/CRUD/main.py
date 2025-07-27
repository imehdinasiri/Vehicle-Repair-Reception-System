from crud_operations import (
    tables, create_record, read_records,
    update_record, delete_record,
    get_table_and_primary_key, input_values_for_columns
)

def main():
    while True:
        print("\n=== MAIN MENU ===")
        table_name, primary_key_column = get_table_and_primary_key()
        print(f"Selected table: {table_name}")
        print("Available operations:")
        print("1. Create")
        print("2. Read records")
        print("3. Update")
        print("4. Delete")
        print("5. Exit")

        operation = input("Choose an operation by number: ").strip()

        if operation == '1':
            column_order = tables[table_name]['columns']
            foreign_key_column = tables[table_name].get('foreign_key')
            print("Enter values:")
            values = input_values_for_columns(column_order, tables[table_name]['primary_key'], foreign_key_column)
            try:
                create_record(table_name, column_order, values)
            except Exception as e:
                print(f"Error: {e}")

        elif operation == '2':
            try:
                read_records(table_name)
            except Exception as e:
                print(f"Error: {e}")

        elif operation == '3':
            primary_key_value = input(f"Enter {primary_key_column} value to update: ").strip()
            if primary_key_value.isdigit():
                primary_key_value = int(primary_key_value)
            try:
                from db_config import get_connection
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM {table_name} WHERE {primary_key_column} = ?", (primary_key_value,))
                row = cur.fetchone()
                conn.close()
                if not row:
                    print("No record found with this primary key.")
                    continue
            except Exception as e:
                print(f"Error checking record: {e}")
                continue

            update_columns = [col for col in tables[table_name]['columns'] if col != primary_key_column]
            print("Enter new values:")
            new_values = input_values_for_columns(tables[table_name]['columns'], primary_key_column)
            try:
                update_record(table_name, primary_key_column, primary_key_value, update_columns, new_values)
            except Exception as e:
                print(f"Error: {e}")

        elif operation == '4':
            primary_key_value = input(f"Enter {primary_key_column} value to delete: ").strip()
            if primary_key_value.isdigit():
                primary_key_value = int(primary_key_value)
            try:
                from db_config import get_connection
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM {table_name} WHERE {primary_key_column} = ?", (primary_key_value,))
                row = cur.fetchone()
                conn.close()
                if not row:
                    print("No record found with this primary key.")
                    continue
            except Exception as e:
                print(f"Error checking record: {e}")
                continue

            try:
                delete_record(table_name, primary_key_column, primary_key_value)
            except Exception as e:
                print(f"Error: {e}")

        elif operation == '5':
            print("Exiting program.")
            break

        else:
            print("Invalid operation, please try again.")

if __name__ == '__main__':
    main()
