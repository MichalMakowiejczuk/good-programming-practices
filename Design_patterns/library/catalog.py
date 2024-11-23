class LibraryCatalog:
    """Singleton: Manages books in the library."""
    _instance = None

    @staticmethod
    def get_instance():
        if LibraryCatalog._instance is None:
            LibraryCatalog._instance = LibraryCatalog()
        return LibraryCatalog._instance

    def __init__(self):
        if LibraryCatalog._instance is not None:
            raise Exception("LibraryCatalog is a singleton! Use get_instance().")
        self.available_books = {}  # {title: count}
        self.borrowed_books = {}  # {user: [list of borrowed books]}
        self.subscribers = {}  # {title: [list of users]}

    def add_book(self, title, count=1):
        """Adds books to the catalog."""
        self.available_books[title] = self.available_books.get(title, 0) + count

    def borrow_book(self, user, title):
        """Allows a user to borrow a book."""
        if title not in self.available_books or self.available_books[title] == 0:
            print(f"Book '{title}' is not available for borrowing.")
            return False

        if len(self.borrowed_books.get(user, [])) >= user.max_books:
            print(f"{user.name} has reached the borrowing limit ({user.max_books} books).")
            return False

        # borrow the book
        self.available_books[title] -= 1
        if user not in self.borrowed_books:
            self.borrowed_books[user] = []
        self.borrowed_books[user].append(title)
        print(f"{user.name} successfully borrowed '{title}'.")
        return True

    def subscribe(self, user, title):
        """Allows a user to subscribe for notifications about a book's availability."""
        if title not in self.subscribers:
            self.subscribers[title] = []
        self.subscribers[title].append(user)
        print(f"{user.name} has subscribed for notifications about '{title}'.")

    def notify(self, title):
        """Sends notifications to users when a book becomes available."""
        if title in self.subscribers:
            for user in self.subscribers[title]:
                print(f"Notification to {user.name}: '{title}' is now available.")
            # clear subscribers after notification
            del self.subscribers[title]

    def return_book(self, user, title):
        """Handles the return of a book by a user (with notification to subscribers)."""
        if user not in self.borrowed_books or title not in self.borrowed_books[user]:
            print(f"{user.name} has not borrowed '{title}'.")
            return False

        # return the book
        self.borrowed_books[user].remove(title)
        self.available_books[title] = self.available_books.get(title, 0) + 1
        print(f"{user.name} successfully returned '{title}'.")

        # notify subscribers
        self.notify(title)
        return True

    def list_available_books(self):
        """Displays a list of available books."""
        print("Available books:")
        for title, count in self.available_books.items():
            if count > 0:
                print(f" - {title} (x{count})")

    def list_user_borrowed_books(self, user):
        """Displays a list of books borrowed by a user."""
        borrowed = self.borrowed_books.get(user, [])
        print(f"{user.name} has borrowed: {', '.join(borrowed) if borrowed else 'none'}")