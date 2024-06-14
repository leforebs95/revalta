import falcon
from api.book import BookResource
from resources.book_resource import BookResource as TestResource

app = application = falcon.App()

app.add_route("/books/fetch", TestResource())
app.add_route("/books", BookResource())
# app.add_route("/books/add", BookResource())
