from .catalog import LibraryCatalog

class LibraryInterface:
    def __init__(self):
        self.catalog = LibraryCatalog.get_instance()

    def add_book(self, title, count=1):
        self.catalog.add_book(title, count)

    def borrow_book(self, user, title):
        self.catalog.borrow_book(user, title)

    def return_book(self, user, title):
        self.catalog.return_book(user, title)

    def subscribe_to_book(self, user, title):
        self.catalog.subscribe(user, title)

    def list_available_books(self):
        self.catalog.list_available_books()

    def list_user_borrowed_books(self, user):
        self.catalog.list_user_borrowed_books(user)