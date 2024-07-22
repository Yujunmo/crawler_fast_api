from odmantic import Model

class Book(Model):
    keyword : str
    publisher : str|None = None
    price : int|None = None
    image : str|None = None

    model_config = {"collection": "books"}