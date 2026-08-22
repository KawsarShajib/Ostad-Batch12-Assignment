# ==========================================
# PROJECT : EXPENSE TRACKER
# ==========================================


FILE_NAME = "expenses.txt"


# ===============================
# Add Expense
# ===============================
def add_expense():
    expense_id = input("Expense ID : ")
    date = input("Date (YYYY-MM-DD) : ")
    category = input("Category : ")
    description = input("Description : ")

    try:
        amount = float(input("Amount : "))

        if amount < 0:
            print("Amount cannot be negative.")
            return

    except ValueError:
        print("Invalid amount! Please enter a valid number.")
        return

    file = open(FILE_NAME, "a")
    file.write(f"{expense_id},{date},{category},{description},{amount}\n")
    file.close()

    print("Expense added successfully.")


# ===============================
# View Expenses
# ===============================
def view_expenses():

    try:
        file = open(FILE_NAME, "r")
        expenses = file.readlines()   
        file.close()  
        # readlines() reads every line from the file and stores them in a list named 'expenses'
        # The variable 'expenses' becomes
        #         [
        #         '1,2026-07-11,Food,Lunch,350\n',
        #         '2,2026-07-11,Transport,Rickshaw,80\n',
        #         '3,2026-07-12,Shopping,T-Shirt,1200\n'
        #         ]

    except FileNotFoundError:
        print("No expense records found.")
        return  # Immediately exits the function

    if len(expenses) == 0:                  # len(expenses) means "How many lines are in the list?"
        print("No expenses available.")
        return

    for expense in expenses:                # loop through every expense
        data = expense.strip().split(",")   # remove spaces by .strip()and 
                                            # cuts the string by .split() wherever it finds a comma, 
                                            # and stores them inside 'data' list

        print("-" * 40)
        print("Expense ID :", data[0])
        print("Date       :", data[1])
        print("Category   :", data[2])
        print("Description:", data[3])
        print("Amount     :", data[4])

"""
        view_expenses()
            │
            ▼
        Open expenses.txt
            │
            ▼
        Read all lines into a list
            │
            ▼
        Close file
            │
            ▼
        File found?
        │
        ├── No ──► Print "No expense records found."
        │            Return
        │
        ▼ Yes
        Is file empty?
        │
        ├── Yes ─► Print "No expenses available."
        │            Return
        │
        ▼ No
        Loop through each line
            │
            ▼
        Remove '\n'
            │
            ▼
        Split by comma
            │
            ▼
        Print each field
            │
            ▼
        Repeat until all expenses are displayed
"""




# ===============================
# Search Expense
# ===============================
def search_expense():

    try:
        file = open(FILE_NAME, "r")
        expenses = file.readlines()
        file.close()

    except FileNotFoundError:
        print("No expense records found.")
        return

    if len(expenses) == 0:
        print("No expenses available.")
        return

    search_id = input("Enter Expense ID : ")

    found = False

    for expense in expenses:
        data = expense.strip().split(",")

        if data[0] == search_id:
            print("Expense Found")
            print("Expense ID :", data[0])
            print("Date       :", data[1])
            print("Category   :", data[2])
            print("Description:", data[3])
            print("Amount     :", data[4])
            found = True
            break

    if found == False:
        print("Expense not found.")


# ===============================
# Update Expense
# ===============================
def update_expense():

    try:
        file = open(FILE_NAME, "r")
        expenses = file.readlines()
        file.close()

    except FileNotFoundError:
        print("No expense records found.")
        return

    if len(expenses) == 0:
        print("No expenses available.")
        return

    search_id = input("Enter Expense ID to Update: ")

    found = False
    new_data = []

    for expense in expenses:
        data = expense.strip().split(",")

        if data[0] == search_id:

            print("Enter New Information")

            date = input("Date : ")
            category = input("Category : ")
            description = input("Description : ")

            try:
                amount = float(input("Amount : "))

                if amount < 0:
                    print("Amount cannot be negative.")
                    return

            except ValueError:
                print("Invalid amount! Please enter a valid number.")
                return

            line = f"{search_id},{date},{category},{description},{amount}\n"
            new_data.append(line)

            found = True

        else:
            new_data.append(expense)

    if found == False:
        print("Expense not found.")
        return

  # Write all (possibly updated) records back
    with open("expenses.txt", "w") as file:
        file.writelines(new_data)
    file.close()
          
    print("Expense updated successfully.")


# ===============================
# Delete Expense
# ===============================
def delete_expense():

    try:
        file = open(FILE_NAME, "r")
        expenses = file.readlines()
        file.close()

    except FileNotFoundError:
        print("No expense records found.")
        return

    if len(expenses) == 0:
        print("No expenses available.")
        return

    search_id = input("Enter Expense ID : ")

    found = False
    new_data = []

    for expense in expenses:

        data = expense.strip().split(",")

        if data[0] == search_id:
            found = True

        else:
            new_data.append(expense)

    if found == False:
        print("Expense not found.")
        return

    file = open(FILE_NAME, "w")

    for line in new_data:
        file.write(line)

    file.close()

    print("Expense deleted successfully.")


# ===============================
# Expense Summary
# ===============================
def expense_summary():

    try:
        file = open(FILE_NAME, "r")
        expenses = file.readlines()
        file.close()

    except FileNotFoundError:
        print("No expense records found.")
        return

    if len(expenses) == 0:
        print("No expenses available.")
        return

    total = 0
    highest = float(expenses[0].strip().split(",")[4])
    # first_line = expenses[0]
    # clean_line = first_line.strip()
    # parts = clean_line.split(",")
    # amount_text = parts[4]
    # highest = float(amount_text)
    lowest = highest

    for expense in expenses:
        amount = float(expense.strip().split(",")[4])

    # for expense in expenses:
    #     # 1. Remove extra spaces/newline from the line
    #     clean_line = expense.strip()

    #     # 2. Split the line into parts using comma
    #     parts = clean_line.split(",")
    #     # parts: [id, date, category, description, amount]

    #     # 3. Take the amount part (index 4)
    #     amount_text = parts[4]

    #     # 4. Convert the amount from string to float
    #     amount = float(amount_text)

        total = total + amount

        if amount > highest:
            highest = amount

        if amount < lowest:
            lowest = amount

    count = len(expenses)
    average = total / count

    print("=" * 10, "Expense Summary", "=" * 10)
    print("Total Expenses :", count)
    print("Total Spending :", total, "BDT")
    print("Average Expense :", round(average, 2), "BDT")
    print("Highest Expense :", highest, "BDT")
    print("Lowest Expense :", lowest, "BDT")



# ===============================
# Main Function
# ===============================
def main():

    while True:

        print("\n========= Expense Tracker =========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expense")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Expense Summary")
        print("7. Exit")

        choice = input("Choose an option : ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            search_expense()

        elif choice == "4":
            update_expense()

        elif choice == "5":
            delete_expense()

        elif choice == "6":
            expense_summary()

        elif choice == "7":
            print("Thank you for using Expense Tracker.")
            break

        else:
            print("Invalid choice! Please select a valid option.")

# ===============================
# Start Program
# ===============================
main()
