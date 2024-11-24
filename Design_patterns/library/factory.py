import random
import string


class User:
    def __init__(self, name, email, user_id):
        self.name = name
        self.email = email
        self.user_id = user_id

    def __str__(self):
        return f"{self.__class__.__name__} - Name: {self.name}, Email: {self.email}, User ID: {self.user_id}"


class Student(User):
    def __init__(self, name, user_id, max_books=3):
        email = self.generate_email(name)
        super().__init__(name, email, user_id)
        self.max_books = max_books

    def generate_email(self, name):
        return f"{name.lower().replace(' ', '')}@student.com"

    def __str__(self):
        return f"{super().__str__()}, Max Books: {self.max_books}"


class Teacher(User):
    def __init__(self, name, user_id, max_books=10):
        email = self.generate_email(name)
        super().__init__(name, email, user_id)
        self.max_books = max_books

    def generate_email(self, name):
        return f"{name.lower().replace(' ', '')}@teacher.com"

    def __str__(self):
        return f"{super().__str__()}, Max Books: {self.max_books}"


class Librarian(User):
    def __init__(self, name, user_id):
        email = self.generate_email(name)
        super().__init__(name, email, user_id)

    def generate_email(self, name):
        return f"{name.lower().replace(' ', '')}@library.com"

    def __str__(self):
        return f"{super().__str__()}"


class UserFactory:
    @staticmethod
    def generate_user_id():
        # Generuje losowy numer identyfikacyjny w formie Sxxxxxx, Txxxxxx, Lxxxxxx
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    @staticmethod
    def create_user(user_type, name):
        user_id = UserFactory.generate_user_id()
        
        if user_type == "student":
            return Student(name, user_id)
        elif user_type == "teacher":
            return Teacher(name, user_id)
        elif user_type == "librarian":
            return Librarian(name, user_id)
        else:
            raise ValueError("Unknown user type")