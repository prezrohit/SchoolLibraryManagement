import os
import sys
import mysql.connector as mysql


def return_book(book_id, student_id):
	cursor = db.cursor()
	query = "delete from book_student_join where book_id=%s and student_id=%s"
	args = (book_id, student_id)
	cursor.execute(query, args)
	db.commit()
	input("\nBook Returned successfully...\n")


def get_students(flag = 0):
	student_cursor = db.cursor()
	student_cursor.execute('SELECT * FROM student')
	students = student_cursor.fetchall()
	if len(students) == 0:
		print("\nNo Student Record Found. Please Register a Student First.")
		input('\nPress Enter key to Continue...')
		return -1
	else:
		print("\n\t\t\t\t\t\t**** REGISTERED STUDENTS IN LIBRARY ****\n\n")
		print('\t\t{:^10}{:^15}{:^20}{:^15}{:^15}{:^25}'.format("ID", "Roll Number", "Name", "Standard", "Section", "Admission Number"))
		print('\t\t{:^10}{:^15}{:^20}{:^15}{:^15}{:^25}'.format("", "", "", "", "", ""))
		for student in students:
			s_list = list(student)
			print('\t\t{:^10}{:^15}{:^20}{:^15}{:^15}{:^25}'.format(s_list[0], s_list[1], s_list[2], s_list[3], s_list[4], s_list[5]))
	student_cursor.close()
	if flag == 0:
		input('\nPress Enter key to Continue...')
	return 0


def get_books(flag = 0):
	db = mysql.connect(host = 'localhost', user = 'mohit', passwd = 'mohit@123', database = 'library_management')
	book_cursor = db.cursor()
	book_cursor.execute('SELECT * FROM book')
	books = book_cursor.fetchall()
	if len(books) == 0:
		print("\nNo Books Found in the Library. Please Register a Book First.")
		input('\nPress Enter key to Continue...')
		return -1
	else:
		print("\n\t\t\t\t\t\t**** BOOKS IN SGRR LIBRARY ****\n\n")
		print('\t\t{:^10}{:^40}{:^20}{:^15}{:^25}'.format("ID", "Name", "Author", "Year", "Publication"))
		print('\t\t{:^10}{:^40}{:^20}{:^15}{:^25}'.format("", "", "", "", ""))
		for book in books:
			b_list = list(book)
			print('\t\t{:^10}{:^40}{:^20}{:^15}{:^25}'.format(b_list[0], b_list[1], b_list[2], b_list[3], b_list[4]))
	book_cursor.close()
	if flag == 0:
		input('\nPress Enter key to Continue...')


def register_student(roll, name, _class, section, adm_no):
	cursor = db.cursor()

	query = 'insert into student values (%s,%s,%s,%s,%s,%s)'
	args = (None, roll,name,_class,section,adm_no)
	cursor.execute(query, args)
	db.commit()


def register_book(name, author, year, publication):
	cursor = db.cursor()
	query = 'insert into book values (%s,%s,%s,%s,%s)'
	args = (None, name, author, year, publication)
	cursor.execute(query,args)
	db.commit()


def issue_book(book_id, student_id):
	cursor = db.cursor()
	query = 'insert into book_student_join values (%s, %s, CURDATE())'
	args = (book_id, student_id)
	cursor.execute(query, args)
	db.commit()
	input("\nBook Issued successfully...\n")


def show_issued_books(student, books):
	print("\n\n\t\t\t\t\t\t **** Books Issued for {} ****\n\n".format(student[0][2]))

	print('\t\t{:^10}{:^40}{:^20}{:^15}{:^25}'.format("ID", "Name", "Author", "Year", "Publication"))
	print('\t\t{:^10}{:^40}{:^20}{:^15}{:^25}'.format("", "", "", "", ""))
	for book in books:
		b_list = list(book)
		print('\t\t{:^10}{:^40}{:^20}{:^15}{:^25}'.format(b_list[0], b_list[1], b_list[2], b_list[3], b_list[4]))


def fetch_issued_books(student_id):
	cursor = db.cursor()
	query = "SELECT * FROM student WHERE id=%s"
	cursor.execute(query, (student_id, ))
	student = cursor.fetchall()
	if len(student) == 0:
		print("\nNo Student Found with that ID...\n")
		input("Press any key to continue...\n")
		return
	else:
		cursor.execute('SELECT book_id FROM book_student_join where student_id=%s', (student_id, ))
		books_id = cursor.fetchall()
		if len(books_id) == 0:
			print("No Books Issued for Student ID {}".format(student_id))
		elif len(books_id) == 1:
			books_id = refine_list_formatting(books_id)
			cursor.execute('SELECT * FROM book WHERE id=%s', books_id)
			books = cursor.fetchall()
			show_issued_books(student, books)
		else:
			books_id = refine_list_formatting(books_id)
			cursor.execute('SELECT * FROM book WHERE id IN {}'.format(books_id))
			books = cursor.fetchall()
			show_issued_books(student, books)

		input()


def refine_list_formatting(l1):
	l2 = []
	for x in l1:
		l2.append(x[0])
	return tuple(l2)


def del_student(student_id):
	cursor = db.cursor()
	query = "delete from student where ID=%s"
	args = (student_id)
	cursor.execute(query, (args,))
	db.commit()

def del_book(book_id):
	cursor = db.cursor()
	query = "delete from book where ID=%s"
	cursor.execute(query, (book_id,))
	db.commit()


def check_if_book_exists(book_id):
	cursor.execute("SELECT * FROM book WHERE id=%s", (book_id, ))
	books = cursor.fetchall()
	if len(books) == 0:
		print('Book with ID ', book_id, " doesn't exists. Please Try Again!!!")
		input("Press any key to Continue...")
		return -1


def check_if_student_exists(student_id):
	cursor.execute("SELECT * FROM student WHERE id=%s", (student_id, ))
	students = cursor.fetchall()
	if len(students) == 0:
		print('Student with ID ', student_id, " doesn't exists. Please Try Again!!!")
		input("Press any key to Continue...")
		return -1


# main()

db = mysql.connect(host = 'localhost',user = 'mohit', passwd = 'mohit@123')
cursor = db.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS library_management')

db = mysql.connect(host = 'localhost',user = 'mohit', passwd = 'mohit@123', database = 'library_management')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS student (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, roll INT NOT NULL, name VARCHAR(50) NOT NULL, standard INT NOT NULL, section VARCHAR(1) NOT NULL, adm_no INT(6) NOT NULL)')

cursor.execute('CREATE TABLE IF NOT EXISTS book (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100) NOT NULL, author VARCHAR(100) NOT NULL, year INT NOT NULL, publication VARCHAR(100) NOT NULL)')

cursor.execute('CREATE TABLE IF NOT EXISTS book_student_join (book_id INT NOT NULL, student_id INT NOT NULL, date DATE NOT NULL)')

while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	print('\n\n\t\t\t\t\t\t***** SGRR LIBRARY MANAGEMENT SYSTEM ******\n\n')
	print('\t\t\t\t\t\t\t1. Show Students Details')
	print('\t\t\t\t\t\t\t2. Show Books')
	print('\t\t\t\t\t\t\t3. Issue Book')
	print('\t\t\t\t\t\t\t4. Return Book')
	print('\t\t\t\t\t\t\t5. Register Student')
	print('\t\t\t\t\t\t\t6. Register Book')
	print('\t\t\t\t\t\t\t7. Issued Books')
	print('\t\t\t\t\t\t\t8. Delete Student Record')
	print('\t\t\t\t\t\t\t9. Delete Book Record')
	print('\t\t\t\t\t\t\t10. Exit')
	choice = input('\n\t\t\t\t\t\t\tEnter your Choice: ')
	try:
		choice = int(choice)
	except ValueError:
		print("Input must be an Number!!!")
		print("Press any key to Continue...")
		input()
		continue

	if choice == 1:
		os.system('cls' if os.name == 'nt' else 'clear')
		get_students()

	elif choice == 2:
		os.system('cls' if os.name == 'nt' else 'clear')
		get_books()

	elif choice == 3:
		os.system('cls' if os.name == 'nt' else 'clear')
		b_result = get_books(1)
		print()
		s_result = get_students(1)
		if s_result == -1 or b_result == -1:
			continue
		else:
			print('\n\n======= Enter the following details to Issue a Book ======')
			print("\nInput 0 to go to Main Menu\n")
			book_id = input("\nBook ID: ")
			try:
				book_id = int(book_id)
				if book_id == 0:
					continue
			except ValueError:
				print("Book ID must be a Number!!!")
				print("Press any key to Continue...")
				input()
				continue
			b_result = check_if_book_exists(book_id)
			if b_result == -1:
				continue

			student_id = input('\nStudent ID: ')
			try:
				student_id = int(student_id)
				if student_id == 0:
					continue
			except ValueError:
				print("Student ID must be a Number!!!")
				print("Press any key to Continue...")
				input()
				continue
			s_result = check_if_student_exists(student_id)
			if s_result == -1:
				continue

			issue_book(book_id, student_id)

	elif choice == 4:
		os.system('cls' if os.name == 'nt' else 'clear')

		s_result = get_students(1)
		b_result = get_books(1)

		if s_result == -1 or b_result == -1:
			continue
		else:
			print('\n\n======= Enter the following details to Return a Book ======')
			print("Input 0 to go to Main Menu\n")
			book_id = input("Enter Book ID: ")
			try:
				book_id = int(book_id)
				if book_id == 0:
					continue
			except ValueError:
				print("Book ID must be a Number!!!")
				print("Press any key to Continue...")
				input()
				continue

			student_id = input('Enter Student ID: ')
			try:
				student_id = int(student_id)
				if student_id == 0:
					continue
			except ValueError:
				print("Student ID must be a Number!!!")
				print("Press any key to Continue...")
				input()
				continue

			s_result = check_if_student_exists(student_id)
			if s_result == -1:
				print("Student with id {} doesn't exist.".format(student_id))
				print("Press any key to Continue...")
				input()
				continue

			b_result = check_if_book_exists(book_id)
			if b_result == -1:
				print("Book with id {} doesn't exist.".format(book_id))
				print("Press any key to Continue...")
				input()
				continue

			return_book(book_id, student_id)

	elif choice == 5:
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\n\t\t\t***** Register a Student *****')
		print("\n Input 0 to to go to Main Menu\n")
		print("\n====== Please Enter the following Details ======")
		roll = input("\nRoll Number: ")

		try:
			roll = int(roll)
			if roll == 0:
				continue
		except ValueError:
			print("Roll Number must be a Number!!!")
			print("Press any key to Continue...")
			input()
			continue

		name = input('Name: ')
		_class = int(input("Class (in Numbers): "))
		section = input('Section: ')
		adm_no = int(input('Admission Number (6 digit): '))

		register_student(roll, name, _class, section, adm_no)

	elif choice == 6:
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\n\t\t\t***** Register a Book *****')
		print("\n====== Please Enter the following Details ======")
		print("\n Input '/q' to to go to Main Menu\n")
		name = input("\nName: ")

		if name == '/q':
			continue

		author = (input("Author: "))
		year = int(input("Year: "))
		publication = input("Publication: ")

		register_book(name, author, year, publication)

	elif choice == 7:
		os.system('cls' if os.name == 'nt' else 'clear')

		s_id = input("\nEnter your Student ID: ")
		try:
			s_id = int(s_id)
		except ValueError:
			print("Student ID must be a Number...")
			print("Press any key to Continue...")
			input()
			continue
		else:
			fetch_issued_books(s_id)

	elif choice == 8:
		os.system('cls' if os.name == 'nt' else 'clear')
		print('\n\t\t\t\t\t\t   ***** Delete a Student Record *****')
		get_students()
		student_id = input("\nEnter Student ID: ")
		del_student(student_id)

	elif choice == 9:
		os.system('cls' if os.name == 'nt' else 'clear')

		print('\n\t\t\t\t\t\t   ***** Delete a Book Record *****')
		get_books()
		book_id = input("\nEnter Book ID: ")
		del_book(book_id)

	elif choice == 10:
		sys.exit('Bye//')

	else:
		print("\n\nOops! You entered an invalid input!!! Press any key to Try Again.")
		input()