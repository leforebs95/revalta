import falcon

from resources import data


class BookResource:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        print(req)
        title = req.get_param("title")
        print(title)
        book_data = data.get_book_from_title(title)
        resp.text = book_data.to_json()

    def on_post(self, req, resp):
        data = req.media
        title = data.get("title")
        author = data.get("author")
        year = data.get("year")
        genre = data.get("genre")
        # book_data = data.add_book_to_library(title, author, year, genre)
        print(title, author, year, genre)
        resp.text = "Added new book: \n" + title + " by " + author
        resp.status = falcon.HTTP_201
        resp.content_type = falcon.MEDIA_JSON
