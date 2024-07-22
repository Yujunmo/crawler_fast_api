from app.config import get_secret
import aiohttp, asyncio

class NaverBookScraper:

    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")
    DISPLAY = 10

    @staticmethod
    async def fetch(session, url, headers):
        
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                rs = await response.json()
                return rs['items']


    def unit_url(self,keyword,start):
        return {
            "url":f"{self.NAVER_API_BOOK}?query={keyword}&display={self.DISPLAY}&start={start}",
            "headers":{
                "X-NAVER-Client-Id": self.NAVER_API_ID,
                "X-NAVER-Client-Secret" : self.NAVER_API_SECRET
            }
        }

    async def search(self, keyword:str, total_page):
        apis =  [self.unit_url(keyword,1+i*10) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            book_data = await asyncio.gather(*[self.fetch(session, api["url"],api["headers"]) for api in apis])

        result = []
        for data in book_data:
            if data:
                result.extend(data)
        return result