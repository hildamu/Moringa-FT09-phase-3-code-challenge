import sqlite3
import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from models.__init__ import CURSOR, CONN

def get_db_connection():
    return sqlite3.connect(':memory:')


class TestModels(unittest.TestCase):
    
    def test_author_creation(self):
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly")
        self.assertEqual(magazine.name, "Tech Weekly")


    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(':memory:')
        cls.conn.row_factory = sqlite3.Row
        cls.cursor = cls.conn.cursor()
        global CONN, CURSOR
        CONN = cls.conn
        CURSOR = cls.cursor
        
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS authors
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)''')
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS magazines
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT)''')
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT, author_id INTEGER, magazine_id INTEGER)''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def tearDown(self):
        CURSOR.execute('DELETE FROM authors')
        CURSOR.execute('DELETE FROM magazines')
        CURSOR.execute('DELETE FROM articles')
        CONN.commit()

    def test_create_magazine(self):
        magazine = Magazine(name="Tech Monthly", category="Technology")
        magazine.create_magazines_table()
        magazine.name = "Tech Monthly"
        self.assertIsNotNone(magazine.id)
        self.assertEqual(magazine.name, "Tech Monthly")
        self.assertEqual(magazine.category, "Technology")

    def test_update_magazine_name(self):
        magazine = Magazine(name="Old Name", category="Category")
        magazine.create_magazines_table()
        magazine.name = "Old Name"
        magazine.name = "New Name"
        self.assertEqual(magazine.name, "New Name")

    def test_invalid_magazine_name_length(self):
        magazine = Magazine()
        with self.assertRaises(ValueError):
            magazine.name = "A"
        with self.assertRaises(ValueError):
            magazine.name = "A" * 17

    def test_create_author(self):
        author = Author(name="Jane Doe")
        author.create_authors_table()
        author.insert_author("Jane Doe")
        self.assertIsNotNone(author.id)
        self.assertEqual(author.name, "Jane Doe")

    def test_invalid_author_name_change(self):
        author = Author(name="John Doe")
        with self.assertRaises(AttributeError):
            author.name = "New Name"

    def test_get_author_articles(self):
        author = Author(name="Author 1")
        author.create_authors_table()
        author.insert_author("Author 1")
        author_id = CURSOR.lastrowid
        
        CURSOR.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       ("Article 1", "Content 1", author_id, 1))
        CURSOR.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       ("Article 2", "Content 2", author_id, 1))
        CONN.commit()

        articles = author.articles()
        self.assertEqual(articles, ["Article 1", "Article 2"])

    def test_get_author_magazines(self):
        author = Author(name="Author 1")
        author.create_authors_table()
        author.insert_author("Author 1")
        author_id = CURSOR.lastrowid

        CURSOR.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', ("Magazine 1", "Tech"))
        magazine_id = CURSOR.lastrowid
        CURSOR.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       ("Article 1", "Content 1", author_id, magazine_id))
        CONN.commit()

        magazines = author.magazines()
        self.assertEqual(magazines, ["Magazine 1"])

    def test_create_article(self):
        article = Article(id=None, title="Innovations in AI", content="AI Content", author_id=1, magazine_id=1)
        article.create_articles_table()
        self.assertIsNotNone(article.id)
        self.assertEqual(article.title, "Innovations in AI")
        self.assertEqual(article.content, "AI Content")

    def test_invalid_article_title_length(self):
        article = Article(id=None, title="Short", content="Content", author_id=1, magazine_id=1)
        with self.assertRaises(ValueError):
            article.title = "A"
        with self.assertRaises(ValueError):
            article.title = "A" * 51

    def test_get_article_author(self):
        CURSOR.execute('INSERT INTO authors (name) VALUES (?)', ("Author 1",))
        author_id = CURSOR.lastrowid
        CURSOR.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       ("Test Article", "Content", author_id, 1))
        article_id = CURSOR.lastrowid
        CONN.commit()

        article = Article(article_id, "Test Article", "Content", author_id, 1)
        author = article.get_author()
        self.assertIsNotNone(author)
        self.assertEqual(author.id, author_id)
        self.assertEqual(author.name, "Author 1")

    def test_get_article_magazine(self):
        CURSOR.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', ("Magazine 1", "Tech"))
        magazine_id = CURSOR.lastrowid
        CURSOR.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       ("Test Article", "Content", 1, magazine_id))
        article_id = CURSOR.lastrowid
        CONN.commit()

        article = Article(article_id, "Test Article", "Content", 1, magazine_id)
        magazine = article.get_magazine()
        self.assertIsNotNone(magazine)
        self.assertEqual(magazine.id, magazine_id)
        self.assertEqual(magazine.name, "Magazine 1")
        self.assertEqual(magazine.category, "Tech")

if __name__ == '__main__':
    unittest.main()
