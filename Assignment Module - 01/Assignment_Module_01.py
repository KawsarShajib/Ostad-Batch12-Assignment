# ==========================================
# PROJECT : STUDENT RESULT MANAGEMENT SYSTEM
# ==========================================

# --------------------------------
# 1. Student Information
# --------------------------------
student_name = input("Enter Student Name: ")
student_id = input("Enter Student ID: ")
department = input("Enter Department: ")

print()

# --------------------------------
# 2. Subject Marks
# --------------------------------
# declaring the subjects list:
subjects = ["Python", "Math", "English", "Physics", "ICT"]

marks = {}          # initiating an empty dictionary named marks

print("Enter Marks:")

for subject in subjects:
    mark = float(input(f"Marks obtained in {subject}: "))
    marks[subject] = mark       # Dictionary Syntax : dictionary[key] = value
    # here, subject = key, mark = value
print()

# --------------------------------
# 3. Calculate Result
# --------------------------------
total = sum(marks.values())
average = total / len(marks)
highest = max(marks.values())
lowest = min(marks.values())

# --------------------------------
# 4. Grade Calculation
# --------------------------------
if average >= 80 and average <= 100:
    grade = "A+"
elif average >= 70 and average <= 79:
    grade = "A"
elif average >= 60 and average <= 69:
    grade = "A-"
elif average >= 50 and average <= 59:
    grade = "B"
elif average >= 40 and average <= 49:
    grade = "C"
else:
    grade = "F"
# Easy alternative : 
# ------------------------------------
# if average >= 80:
#     grade = "A+"
# elif average >= 70:
#     grade = "A"
# elif average >= 60:
#     grade = "A-"
# elif average >= 50:
#     grade = "B"
# elif average >= 40:
#     grade = "C"
# else:
#     grade = "F"

# --------------------------------
# 5. Pass or Fail
# --------------------------------
status = "Passed"

for mark in marks.values():
    if mark < 40:
        status = "Failed"
        break
# It means:
#     Assume the student has Passed.
#     Check each subject mark.
#     If any mark is below 40, change the status to Failed and stop checking.

# --------------------------------
# 6. Password Verification
# --------------------------------
correct_password = "python123"

password = input("\nEnter Password: ")

while password != correct_password:
    print("Incorrect Password! Try Again.")
    password = input("Enter Password: ")

print("Password Verified Successfully!")

# --------------------------------
# 7. String Operations
# --------------------------------
print("\n========== STRING OPERATIONS ==========")
print("Uppercase       :", student_name.upper())
print("Lowercase       :", student_name.lower())
print("Length          :", len(student_name))
print("First 3 Letters :", student_name[:3])
print("Last 3 Letters  :", student_name[-3:])

# --------------------------------
# 8. Set Example
# --------------------------------
sports = {"Football", "Cricket", "Badminton"}
clubs = {"Programming", "Cricket", "Photography"}

print("\n========== SET OPERATIONS ==========")
print("Common Items :", sports.intersection(clubs))
print("All Unique Items :", sports.union(clubs))

# --------------------------------
# 9. Tuple Example
# --------------------------------
weekdays = (
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
)

print("\n========== TUPLE EXAMPLE ==========")
print("First Day :", weekdays[0])
print("Last Day  :", weekdays[-1])
print("Total Days:", len(weekdays))

# --------------------------------
# 10. Final Report
# --------------------------------
print("\n" + "=" * 35)
print("          STUDENT REPORT")
print("=" * 35)

print(f"Name       : {student_name}")
print(f"ID         : {student_id}")
print(f"Department : {department}")

print("-" * 35)

for subject, mark in marks.items():
    print(f"{subject:<10} : {mark}")
# {subject:<10} meaning : 
# 'subject' prints the value of the variable 
# '<' means left-align the text
# '10' means use a field width of 10 characters.

# Alternative code : 
#-------------------
# for subject in marks:
#     print(subject, ":", marks[subject])

# Explanation :   
# -------------
    # To access a value from a dictionary, we write
    # dictionary[key] 
    # here, marks[subject]
    # Python looks for the key--> subject 
    # in the dictionary--> marks and 
    # returns its value.


print("-" * 35)

print(f"Total      : {total}")
print(f"Average    : {average:.2f}")    
# ':' means "I want to format this value"
# '.2' means "Show 2 digits after the decimal point"
# 'f' means "Display the number as a floating-point number."
print(f"Highest    : {highest}")
print(f"Lowest     : {lowest}")
print(f"Grade      : {grade}")
print(f"Status     : {status}")

print("=" * 35)