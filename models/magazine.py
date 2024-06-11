from models.__init__ import CONN, CURSOR
 
from models.author import Author

class Magazine:
    def __init__(self, id=None, name="", category=None):
        self._id = id
        self._name = name
        self._category = category

    def create_magazines_table(self):
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS magazines
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT)''')
        CONN.commit()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value
        CURSOR.execute("INSERT OR REPLACE INTO magazines (name, category) VALUES (?,?)", (value, self.category))
        CONN.commit()
        self._id = CURSOR.lastrowid

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Category must be a string or None")
        if value is not None and len(value) == 0:
            raise ValueError("Category cannot be empty")
        self._category = value
        CURSOR.execute("INSERT OR REPLACE INTO magazines (name, category) VALUES (?,?)", (self.name, value))
        CONN.commit()
        self._id = CURSOR.lastrowid

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def articles(self):
        CURSOR.execute('''SELECT a.title 
                          FROM magazines 
                          JOIN articles a ON magazines.id = a.magazine_id 
                          WHERE magazines.id =?''', (self.id,))
        results = CURSOR.fetchall()
        return [row[0] for row in results]

    def contributors(self):
        CURSOR.execute('''SELECT a.name 
                          FROM magazines 
                          JOIN articles art ON magazines.id = art.magazine_id 
                          JOIN authors a ON art.author_id = a.id 
                          WHERE magazines.id =?''', (self.id,))
        results = CURSOR.fetchall()
        return [row[0] for row in results]
    
    def article_titles(self):
        CURSOR.execute('''SELECT a.title 
                          FROM magazines 
                          JOIN articles a ON magazines.id = a.magazine_id 
                          WHERE magazines.id =?''', (self.id,))
        results = CURSOR.fetchall()
        if results:
            return [row[0] for row in results]
        return None

    def contributing_authors(self):
        CURSOR.execute('''SELECT a.id, a.name 
                          FROM magazines 
                          JOIN articles art ON magazines.id = art.magazine_id 
                          JOIN authors a ON art.author_id = a.id 
                          WHERE magazines.id =? 
                          GROUP BY a.id, a.name 
                          HAVING COUNT(art.id) > 2''', (self.id,))
        results = CURSOR.fetchall()
        if results:
            authors = []
            for row in results:
                author = Author(id=row[0], name=row[1])
                authors.append(author)
            return authors
        return None
