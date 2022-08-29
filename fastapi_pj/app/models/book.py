from odmantic import Model


class BookModel(Model):
    keyword: str
    publisher: str
    image: str
    price: int

    class Config:
        collection = "books"
