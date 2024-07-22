from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import Book
from app.book_scraper import NaverBookScraper
#absolute path. path of this main.py file
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})
    


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q:str):
    keyword = q

    if not keyword:
        return templates.TemplateResponse("index.html",
                                        {"request":request,
                                        "title":"book collector"
                                        })

    if await mongodb.engine.find_one(Book, Book.keyword == keyword):
        print("read DB ")
        # book model
        books = await mongodb.engine.find(Book, Book.keyword == keyword)
        

    else:
        print("scrap data ")
        naver_book_scraper = NaverBookScraper()

        # scraped dictionary data
        books = await naver_book_scraper.search(keyword, 10)
        book_models = []
        for book in books:
            # dict data -> model data  (ORD)
            book_model = Book(
                keyword= keyword,
                publisher= book['publisher'],
                price = book['discount'],
                image = book['image']
            )
            book_models.append(book_model)

        # insert data into DB
        await mongodb.engine.save_all(book_models)

    # data visualization
    return templates.TemplateResponse("index.html",
                                      {"request":request,
                                       "title":"book collector",
                                       "books":books})


@app.on_event("startup")
async def on_app_start():
    # just before app starts
    mongodb.connect()
    

@app.on_event("shutdown")
async def on_app_shutdown():
    # just before app shuts down
    mongodb.close()
    
