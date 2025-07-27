import report_generator

def main():
    while True:
        print("\n==> REPORT MENU")
        print("1. Total Income from Services and Parts")
        print("2. Number of Car Receptions")
        print("3. Repairs by Type and Income")
        print("4. Repair Costs by Car Plate")
        print("5. Top 20 Frequent Customers")
        print("6. Exit")

        choice = input("Select a report number: ")

        if choice == "1":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            result = report_generator.get_income_by_services_and_parts(start_date, end_date)
            print("\n--- Total Income from Services and Parts ---")
            for row in result:
                print(row)

        elif choice == "2":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            result = report_generator.get_acceptance_count(start_date, end_date)
            print("\n--- Number of Car Receptions ---")
            for row in result:
                print(row)

        elif choice == "3":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            result = report_generator.get_repairs_by_type_and_income(start_date, end_date)
            print("\n--- Repairs by Type and Income ---")
            for row in result:
                print(row)

        elif choice == "4":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            result = report_generator.get_repair_costs_by_plate(start_date, end_date)
            print("\n--- Repair Costs by Car Plate ---")
            for row in result:
                print(row)

        elif choice == "5":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            result = report_generator.get_top_customers(start_date, end_date)
            print("\n--- Top 20 Frequent Customers ---")
            for row in result:
                print(row)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
