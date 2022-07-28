import aiohttp
import asyncio

from app.config import NAVER_API_SECRET, get_secret


class NaverBookScraper:

    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.NAVER_API_BOOK}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-NAVER-Client-ID": self.NAVER_API_ID,
                "X-NAVER-Client-SECRET": self.NAVER_API_SECRET,
            },
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[
                    NaverBookScraper.fetch(session, api["url"], api["headers"])
                    for api in apis
                ]
            )

        print(all_data)
        result = []
        for data in all_data:
            if data is not None:
                for book in data:
                    result.append(book)

        return result

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))


if __name__ == "__main__":

    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(main())

    scraper = NaverBookScraper()
    print(scraper.run("파이썬", 2))
