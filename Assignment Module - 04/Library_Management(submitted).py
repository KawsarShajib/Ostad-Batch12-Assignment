# ===================================================================
# Step : 01 # Parent Class --> (Parent of child class 'Member')
# ===================================================================
class Person:

    def __init__(self, name, age):
        self.name = name    # instance variable
        self.age = age      # instance variable

    # Instance Method : is a normal function inside a class.
    def display_info(self):
        print("Name :", self.name)
        print("Age  :", self.age)


# =====================================================================
# Step : 02 # Child Class --> (Inherits from parent class 'Person')
# =====================================================================
class Member(Person):

    # Constructor
    def __init__(self, member_id, name, age):
        # Call Person constructor
        super().__init__(name, age) 

        # New attribute
        self.member_id = member_id
        # Empty list for borrowed books
        self.borrowed_books = []

    # Borrow book
    def borrow_book(self, isbn):
        self.borrowed_books.append(isbn)

    # Return book
    def return_book(self, isbn):
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)

    # Override display_info() on 'person' class
    def display_info(self):
        print("Member ID      :", self.member_id)
        print("Name           :", self.name)
        print("Age            :", self.age)
        print("Borrowed Books :", len(self.borrowed_books))



# ===================================================================
# Step : 03 # Book Class
# ===================================================================
# Book Class
class Book:

    total_books = 0      
    # Constructor
    def __init__(self, title, author, isbn):
        self.title = title    
        self.author = author   
        self.isbn = isbn        

        self.__available = True   

        # Increase total books
        Book.total_books += 1

        # Getter
        @property
        def available(self):
            return self.__available
    
            print(book1.available)

        # Setter
        @available.setter
        def available(self, value):
            if isinstance(value, bool):
                self.__available = value
            else:
                print("Availability must be True or False.")

    # Display Book Information
    def display_book(self):
        print("ISBN      :", self.isbn)
        print("Title     :", self.title)
        print("Author    :", self.author)

        if self.available:
            print("Status    : Available")
        else:
            print("Status    : Borrowed")

    @classmethod
    def show_total_books(cls):
        print("Total Books :", cls.total_books)

    @staticmethod
    def validate_isbn(isbn):

        if isbn == "":
            return False

        return True


# ===================================================================
# Step : 04 # Library Class
# ===================================================================

# Library Class
class Library:
    # Constructor
    def __init__(self):
        # Empty list for books
        self.books = []           

        # Empty list for members
        self.members = []       

    # Find book by ISBN
    def find_book_by_isbn(self, isbn):

        for book in self.books:

            if book.isbn == isbn:
                return book

        return None

    # Add Book
    def add_book(self):

        print("\n----- Add New Book -----")

        title = input("Enter Book Title : ").strip()      
        author = input("Enter Author     : ").strip()
        isbn = input("Enter ISBN       : ").strip()

        if title == "":
            print("Error: Book title cannot be empty.")
            return
        if author == "":
            print("Error: Author name cannot be empty.")
            return
        if Book.validate_isbn(isbn) == False:
            print("Error: Invalid ISBN.")
            return

        if self.find_book_by_isbn(isbn) != None:
            print("Error: ISBN already exists.")
            return

        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        print("Book added successfully!")

    # Register Member
    def register_member(self, member):
        self.members.append(member)
        print("Member registered successfully.")

    # Show All Books
    def show_books(self):

        print("\n------------- BOOK LIST -------------")

        for book in self.books:
            book.display_book()
            print("-------------------------------------")

    # Show All Members
    def show_members(self):

        print("\n----------- MEMBER LIST ------------")

        for member in self.members:
            member.display_info()
            print("------------------------------------")

    # Find Member by ID
    def find_member_by_id(self, member_id):

        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    # Register Member
    def register_member(self):

        print("\n----- Register Member -----")

        member_id = input("Enter Member ID : ").strip()
        name = input("Enter Name      : ").strip()
        age_input = input("Enter Age       : ").strip()

        if member_id == "":
            print("Error: Member ID cannot be empty.")
            return

        if name == "":
            print("Error: Name cannot be empty.")
            return

        try:
            age = int(age_input)

        except ValueError:
            print("Error: Age must be a number.")
            return

        if age <= 0:
            print("Error: Age must be greater than 0.")
            return

        if self.find_member_by_id(member_id) != None:
            print("Error: Member ID already exists.")
            return

        new_member = Member(member_id, name, age)
        self.members.append(new_member)
        print("Member registered successfully!")

    # Borrow Book
    def borrow_book(self):
        print("\n------ Borrow Book ------")
        member_id = input("Enter Member ID : ").strip()
        isbn = input("Enter Book ISBN : ").strip()

        member = self.find_member_by_id(member_id)

        if member == None:
            print("Member not found.")
            return

        book = self.find_book_by_isbn(isbn)

        if book == None:
            print("Book not found.")
            return

        if book.available == False:
            print("Sorry! This book is currently unavailable.")
            return


        # prevent Borrowing Same Book Twice

        if book.isbn in member.borrowed_books:
            print("Member already borrowed this book.")
            return

        # Borrow Book
        member.borrow_book(book.isbn)

        # Update Book Status
        book.available = False
        print("Book borrowed successfully.")



    # Return Book
    def return_book(self):

        print("\n------ Return Book ------")
        member_id = input("Enter Member ID : ").strip()
        isbn = input("Enter Book ISBN : ").strip()
        member = self.find_member_by_id(member_id)

        if member == None:
            print("Member not found.")
            return

        book = self.find_book_by_isbn(isbn)

        if book == None:
            print("Book not found.")
            return

        if book.isbn not in member.borrowed_books:
            print("This member did not borrow this book.")
            return

        member.return_book(book.isbn)
        book.available = True
        print("Book returned successfully.")


# Search Book
    def search_book(self):

        print("\n------ Search Book ------")
        title = input("Enter Book Title : ").strip()

        if title == "":
            print("Book title cannot be empty.")
            return

        found = False

        for book in self.books:

            if book.title.lower() == title.lower():
                print("\nBook Found!")
                book.display_book()
                found = True
                break

        if found == False:
            print("Book not found.")


# Create Library

library = Library()

while True:

    print("\n=========================================")
    print("      LIBRARY MANAGEMENT SYSTEM")
    print("=========================================")

    print("1. Add Book")
    print("2. Register Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Show All Books")
    print("6. Show All Members")
    print("7. Search Book")
    print("8. Exit")

    try:
        choice = int(input("\nEnter your choice: "))

        if choice == 1:
            library.add_book()

        elif choice == 2:
            library.register_member()

        elif choice == 3:
            library.borrow_book()

        elif choice == 4:
            library.return_book()

        elif choice == 5:
            library.show_books()
            input("\nPress Enter to continue...") 

        elif choice == 6:
            library.show_members()

        elif choice == 7:
            library.search_book()

        elif choice == 8:

            print("\nThank you for using Library Management System.")
            print("Goodbye!")
            break

        else:
            print("Invalid menu choice.")

    except ValueError:
        print("Please enter a number between 1 and 8.")

    except Exception as e:
        print("Unexpected Error:", e)