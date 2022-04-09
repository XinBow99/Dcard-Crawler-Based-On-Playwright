from playwright.sync_api import Playwright, sync_playwright
from utils import mysql_connect_handle, parser_opt, public_functions



class dcardPosts:
    def __init__(self):
        print("[info]preparing to connect to database")
        print("create mysql connect")
        # Read the mysql config from mysql.yaml
        self.dcardCrawlerDBHandler = mysql_connect_handle.labDBconnect(
            'config/mysql.yaml')
        # This parser is used to parse the command line arguments
        self.parserOptions = parser_opt.parserOpt()
        self.postCount = 0
        self.stopCrawler = False
        with sync_playwright() as playwright:
            self.run(playwright)

    def handleResponse(self, response):
        # Using regex to handle the response
        if 'service/api/v2/globalPaging/page?pageKey=' in response.url and response.status == 200:
            try:
                for post in response.json()['posts']:
                    _articleTemp = {
                        'title': post['title'],
                        'forum': post['forumName'],
                        'href': '/f/{}/p/{}'.format(post['forumAlias'], post['id'])
                    }
                    self.dcardCrawlerDBHandler.writePostInformationToDatabase(
                        self, _articleTemp)
            except Exception as e:
                print("[error]handleResponse: {}".format(e))
        elif f'service/api/v2/forums/{self.parserOptions.forum}/posts?' in response.url and response.status == 200:
            try:
                for post in response.json():
                    _articleTemp = {
                        'title': post['title'],
                        'forum': post['forumName'],
                        'href': '/f/{}/p/{}'.format(post['forumAlias'], post['id'])
                    }
                    self.dcardCrawlerDBHandler.writePostInformationToDatabase(
                        self, _articleTemp)
            except Exception as e:
                print("[error]handleResponse: {}".format(e))
        elif f'service/api/v2/posts?' in response.url and response.status == 200:
            try:
                for post in response.json():
                    _articleTemp = {
                        'title': post['title'],
                        'forum': post['forumName'],
                        'href': '/f/{}/p/{}'.format(post['forumAlias'], post['id'])
                    }
                    self.dcardCrawlerDBHandler.writePostInformationToDatabase(
                        self, _articleTemp)
            except Exception as e:
                print("[error]handleResponse: {}".format(e))
        # https://www.dcard.tw/service/api/v2/forums/nkfust/posts?limit=30&before=238240372

    def parserFirstContent(self):
        # self.contentLoopTimesTemp += 1
        print("[info]start to parse the first content")
        for article in self.page.query_selector_all('#__next > div > div > div > div > div > div > div > div > div > div > div > article'):
            _articleTemp = {
                'title': article.query_selector('h2 > a').inner_text(),
                'forum': article.query_selector('div > div > div > div > div:nth-child(1)').inner_text(),
                'href': article.query_selector('h2 > a').get_attribute('href')
            }
            self.dcardCrawlerDBHandler.writePostInformationToDatabase(
                self, _articleTemp)

    def run(self, playwright: Playwright):
        print('[info]start to run')
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        # Open new page
        self.page = context.new_page()
        self.page.on('response', self.handleResponse)
        # Go to https://www.dcard.tw/f
        self.page.goto(
            f'https://www.dcard.tw/f/{self.parserOptions.forum}?latest={self.parserOptions.latest}')
        self.parserFirstContent()
        public_functions.loadNextPage(self.page, self)
        context.close()
        browser.close()


if __name__ == "__main__":
    # First we need to get the postId, and then we can get the content
    dcardPosts()
