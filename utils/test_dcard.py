from playwright.sync_api import Playwright, sync_playwright, expect


class dcardPosts:
    def __init__(self):
        print("[info]preparing to connect to database")
        self.contentLoopTimes = 1000000
        self.contentLoopTimesTemp = 0
        # self.testMySQL()
        with sync_playwright() as playwright:
            self.run(playwright)
        print('[info] forum content is parsed with 10 loops.')

    def loadNextPage(self, times=0):
        for _ in range(times):
            self.page.mouse.wheel(0, 100000)
            self.contentLoopTimesTemp += 1

    def parserFirstContent(self):
        _hrefTemp = []
        self.contentLoopTimesTemp += 1
        for article in self.page.query_selector_all('#__next > div > div > div > div > div > div > div > div > div > div > div > article'):
            _articleTemp = {
                'title': article.query_selector('h2 > a').inner_text(),
                'forum': article.query_selector('div > div > div > div > div:nth-child(1)').inner_text(),
                'href': article.query_selector('h2 > a').get_attribute('href')
            }
            print(_articleTemp)
            if _articleTemp['href'] not in _hrefTemp:
                _hrefTemp.append(_articleTemp['href'])

    def run(self, playwright: Playwright):
        print('[info]start to run')
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        # Open new page
        self.page = context.new_page()
        # Go to https://www.dcard.tw/f
        self.page.goto(
            "https://www.dcard.tw/f?listKey=latest_TW&listType=globalPaging")
        

        input()
        self.loadNextPage(self.contentLoopTimes - 1)
        context.close()
        browser.close()


if __name__ == "__main__":
    dcardPosts()
    # dcardAuthGenerateWithMobile()
    # dcardPostInformation()
