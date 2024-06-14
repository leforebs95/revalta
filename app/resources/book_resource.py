import falcon
import json

class BookResource:

    def on_get(self, req, resp):
        data = {
              "books": [
                {
                  "title": "The Great Gatsby",
                  "author": {
                    "name": "F. Scott Fitzgerald",
                    "birth_year": 1896,
                    "nationality": "American"
                  },
                  "publication_year": 1925,
                  "genre": "Fiction"
                },
                {
                  "title": "To Kill a Mockingbird",
                  "author": {
                    "name": "Harper Lee",
                    "birth_year": 1926,
                    "nationality": "American"
                  },
                  "publication_year": 1960,
                  "genre": "Fiction"
                },
                {
                  "title": "The Hobbit",
                  "author": {
                    "name": "J.R.R. Tolkien",
                    "birth_year": 1892,
                    "nationality": "British"
                  },
                  "publication_year": 1937,
                  "genre": "Fantasy"
                },
                {
                  "title": "The Catcher in the Rye",
                  "author": {
                    "name": "J.D. Salinger",
                    "birth_year": 1919,
                    "nationality": "American"
                  },
                  "publication_year": 1951,
                  "genre": "Fiction"
                }
              ]
            }

        resp.text = json.dumps(data)
        resp.status = falcon.HTTP_200