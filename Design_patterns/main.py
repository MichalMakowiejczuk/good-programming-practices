from library.factory import UserFactory
from library.catalog import LibraryCatalog
from library.facade import LibraryInterface
from library.adapter import BookDataAdapter
from library.iterator import BookIterator


def main():
    # Setting up the interface and catalog
    library = LibraryInterface()
    catalog = LibraryCatalog.get_instance()

    # Example of using BookDataAdapter: loading data from JSON
    json_data = '[{"title": "The Last Wish", "author": "Andrzej Sapkowski"}, {"title": "The Painted Man", "author": "Peter V. Brett"}]'
    json_adapter = BookDataAdapter("JSON")
    books_from_json = json_adapter.parse(json_data)
    
    # Adding books from JSON to the catalog
    for book in books_from_json:
        library.add_book(book["title"], 1)
    
    # Example of using BookDataAdapter: loading data from XML
    xml_data = """<library>
        <book><title>Lord of Destruction</title><author>Richard A. Knaak</author></book>
        <book><title>Arthas: Rise of the Lich King</title><author>Christie Golden</author></book>
    </library>"""
    xml_adapter = BookDataAdapter("XML")
    books_from_xml = xml_adapter.parse(xml_data)
    
    # Adding books from XML to the catalog
    for book in books_from_xml:
        library.add_book(book["title"], 2)

    # Example of using BookIterator: iterating through books
    books = catalog.available_books.keys()  # Get a list of book titles
    book_iterator = BookIterator(list(books))

    print("\nBooks in the catalog:")
    for book in book_iterator:
        print(f" - {book}")

    # Creating users
    geralt = UserFactory.create_user("student", "Geralt of Rivia")
    vesemir = UserFactory.create_user("teacher", "Vesemir of Kaer Morhen")

    # Displaying the list of available books
    library.list_available_books()

    # Borrowing books
    library.borrow_book(geralt, "The Last Wish")
    library.borrow_book(vesemir, "The Last Wish")

    # Subscribing to notifications
    library.subscribe_to_book(geralt, "Lord of Destruction")

    # Returning a book by Vesemir
    library.return_book(vesemir, "The Last Wish")

    # Displaying the list of books borrowed by Geralt
    library.list_user_borrowed_books(geralt)

    # Displaying the list of available books after a return
    library.list_available_books()


if __name__ == "__main__":
    main()

