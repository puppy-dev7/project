import sqlite3

DB_NAME = "library.db"


# Подключение к базе данных с поддержкой внешних ключей
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Создание таблиц и заполнение стартовыми данными
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS readers ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "first_name TEXT NOT NULL, "
            "last_name TEXT NOT NULL, "
            "age INTEGER NOT NULL)"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, "
            "author TEXT NOT NULL, "
            "year INTEGER NOT NULL, "
            "is_available INTEGER DEFAULT 1, "
            "reader_id INTEGER DEFAULT NULL, "
            "FOREIGN KEY (reader_id) REFERENCES readers(id) ON DELETE SET NULL)"
        )

        # Добавляем книги, если таблица пустая
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone() == (0,):
            sample_books = [
                ("Белый пароход", "Чингиз Айтматов", 1970, 1, None),
                ("Мастер и Маргарита", "Михаил Булгаков", 1967, 1, None),
                ("Преступление и наказание", "Фёдор Достоевский", 1866, 1, None),
                ("1984", "Джордж Оруэлл", 1949, 1, None),
                ("Гарри Поттер и философский камень", "Джоан Роулинг", 1997, 1, None),
            ]
            cursor.executemany(
                "INSERT INTO books (title, author, year, is_available, reader_id) VALUES (?, ?, ?, ?, ?)",
                sample_books
            )

        # Добавляем читателей, если таблица пустая
        cursor.execute("SELECT COUNT(*) FROM readers")
        if cursor.fetchone() == (0,):
            sample_readers = [
                ("Азамат", "Токтогулов", 24),
                ("Айгерим", "Асанова", 19),
                ("Бекзат", "Жумабеков", 21),
            ]
            cursor.executemany(
                "INSERT INTO readers (first_name, last_name, age) VALUES (?, ?, ?)",
                sample_readers
            )


def print_books(books):
    if not books:
        print("\nКниги не найдены.")
        return

    print("\n" + "-" * 80)
    print(f"{'ID':<4} | {'Название':<32} | {'Автор':<20} | {'Год':<6} | {'Статус'}")
    print("-" * 80)
    for b in books:
        book_id, title, author, year, is_available, reader_info = b
        status = "Доступна" if is_available == 1 else f"Выдана ({reader_info})"
        print(f"{book_id:<4} | {title:<32} | {author:<20} | {year:<6} | {status}")
    print("-" * 80)


# Просмотр всех или только доступных книг (с присоединением имени читателя)
def show_all_books(only_available=False):
    with get_connection() as conn:
        cursor = conn.cursor()
        query = (
            "SELECT b.id, b.title, b.author, b.year, b.is_available, "
            "(r.first_name || ' ' || r.last_name) "
            "FROM books b "
            "LEFT JOIN readers r ON b.reader_id = r.id"
        )
        if only_available:
            query += " WHERE b.is_available = 1"

        cursor.execute(query)
        print_books(cursor.fetchall())


# Поиск книг по названию или автору
def search_books(by_author=False):
    search_term = input("Введите запрос для поиска: ").strip()
    column = "author" if by_author else "title"

    with get_connection() as conn:
        cursor = conn.cursor()
        query = (
            "SELECT b.id, b.title, b.author, b.year, b.is_available, "
            "(r.first_name || ' ' || r.last_name) "
            "FROM books b "
            "LEFT JOIN readers r ON b.reader_id = r.id "
            f"WHERE b.{column} LIKE ?"
        )
        cursor.execute(query, (f"%{search_term}%",))
        print_books(cursor.fetchall())


def add_book():
    title = input("Введите название книги: ").strip()
    author = input("Введите автора: ").strip()
    try:
        year = int(input("Введите год выпуска: "))
    except ValueError:
        print("Ошибка: год должен быть числом.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year)
        )
        print(f"Книга '{title}' добавлена.")


def update_book():
    show_all_books()
    try:
        book_id = int(input("Введите ID книги для изменения: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    title = input("Новое название (Enter — оставить старое): ").strip()
    author = input("Новый автор (Enter — оставить старого): ").strip()
    year_str = input("Новый год выпуска (Enter — оставить старый): ").strip()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, author, year FROM books WHERE id = ?", (book_id,))
        current = cursor.fetchone()
        if not current:
            print("Ошибка: книга с таким ID не найдена.")
            return

        old_title, old_author, old_year = current
        new_title = title if title else old_title
        new_author = author if author else old_author
        new_year = int(year_str) if year_str.isdigit() else old_year

        cursor.execute(
            "UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?",
            (new_title, new_author, new_year, book_id)
        )
        print("Данные книги обновлены.")


def delete_book():
    show_all_books()
    try:
        book_id = int(input("Введите ID книги для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        if cursor.rowcount > 0:
            print("Книга удалена.")
        else:
            print("Ошибка: книга с таким ID не найдена.")


# --- Работа с читателями и выдачей ---

def add_reader():
    first_name = input("Имя читателя: ").strip()
    last_name = input("Фамилия читателя: ").strip()
    try:
        age = int(input("Возраст: "))
    except ValueError:
        print("Ошибка: возраст должен быть числом.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO readers (first_name, last_name, age) VALUES (?, ?, ?)",
            (first_name, last_name, age)
        )
        print(f"Читатель {first_name} {last_name} добавлен.")


def show_readers():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, age FROM readers")
        readers = cursor.fetchall()
        print("\n--- Список читателей ---")
        for reader_id, first_name, last_name, age in readers:
            print(f"ID: {reader_id} | {first_name} {last_name} ({age} лет)")
        print("------------------------")


# Выдача доступной книги читателю по ID
def issue_book():
    show_all_books(only_available=True)
    try:
        book_id = int(input("Введите ID книги для выдачи: "))
        show_readers()
        reader_id = int(input("Введите ID читателя: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_available FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        if not book or book == (0,):
            print("Ошибка: книга недоступна или не существует.")
            return

        cursor.execute("SELECT id FROM readers WHERE id = ?", (reader_id,))
        if not cursor.fetchone():
            print("Ошибка: читатель не найден.")
            return

        cursor.execute(
            "UPDATE books SET is_available = 0, reader_id = ? WHERE id = ?",
            (reader_id, book_id)
        )
        print("Книга выдана читателю.")


# Возврат книги в библиотеку
def return_book():
    show_all_books()
    try:
        book_id = int(input("Введите ID книги для возврата: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET is_available = 1, reader_id = NULL WHERE id = ? AND is_available = 0",
            (book_id,)
        )
        if cursor.rowcount > 0:
            print("Книга возвращена в библиотеку.")
        else:
            print("Ошибка: книга не найдена или уже в библиотеке.")


# Главное меню программы
def main():
    init_db()
    while True:
        print("\n=== БИБЛИОТЕКА ===")
        print("1. Все книги")
        print("2. Доступные книги")
        print("3. Поиск по названию")
        print("4. Поиск по автору")
        print("5. Добавить книгу")
        print("6. Изменить книгу")
        print("7. Удалить книгу")
        print("8. Добавить читателя")
        print("9. Выдать книгу")
        print("10. Вернуть книгу")
        print("0. Выход")

        choice = input("\nВыберите пункт: ").strip()

        if choice == "1":
            show_all_books()
        elif choice == "2":
            show_all_books(only_available=True)
        elif choice == "3":
            search_books(by_author=False)
        elif choice == "4":
            search_books(by_author=True)
        elif choice == "5":
            add_book()
        elif choice == "6":
            update_book()
        elif choice == "7":
            delete_book()
        elif choice == "8":
            add_reader()
        elif choice == "9":
            issue_book()
        elif choice == "10":
            return_book()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
