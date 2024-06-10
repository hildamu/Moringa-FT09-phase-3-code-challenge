from database.connection import get_db_connection


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self._title = None
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.title}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a type str")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be between 5 and 50 characters, inclusive")
        if self._title is not None:
            raise ValueError(
                "Title should not be able to change after the article is instantiated"
            )
        self._title = value

    def get_author(self):
        """
        Returns the author of the article.
        """
        from models.author import Author  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT authors.id, authors.name FROM authors "
            "JOIN articles ON authors.id = articles.author_id "
            "WHERE articles.id = ?",
            (self.id,),
        )
        author_data = cursor.fetchone()
        conn.close()
        if author_data:
            return Author(author_data["id"], author_data["name"])
        else:
            return None

    def get_magazine(self):
        """
        Returns the magazine of the article.
        """
        from models.magazine import Magazine  

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT magazines.id, magazines.name, magazines.category FROM magazines "
            "JOIN articles ON magazines.id = articles.magazine_id "
            "WHERE articles.id = ?",
            (self.id,),
        )
        magazine_data = cursor.fetchone()
        conn.close()
        if magazine_data:
            return Magazine(
                magazine_data["id"], magazine_data["name"], magazine_data["category"]
            )
        else:
            return None