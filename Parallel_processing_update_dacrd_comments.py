from playwright.sync_api import Playwright, sync_playwright, expect
import re
import pandas
from utils import mysql_connect_handle, parser_opt, public_functions


class dcardAuthGenerateWithMobile:
    def __init__(self) -> None:
        self.parserOptions = parser_opt.commentParserOpt()
        with sync_playwright() as playwright:
            self.run(playwright)
            print('[info] mobile auth is generated.')

    def run(self, playwright: Playwright) -> None:
        browser = playwright.webkit.launch()
        context = browser.new_context(**playwright.devices["iPhone 11"])
        print('[info] mobile auth is generating...')

        # Open new page
        page = context.new_page()

        # Go to https://www.dcard.tw/f/relationship/p/238532512
        page.goto("https://www.dcard.tw/my")
        print('[info] go to https://www.dcard.tw/my')
        page.locator("button:has-text(\"登入/註冊\")").click()
        print('[info] click login button.')
        # expect(page).to_have_url("https://id.dcard.tw/oauth/login?redirect=%2Foauth%2Fauthorize%3Fbdid%3D144f554d-48e5-4df3-aa26-a949a4e3d746%26client_id%3Dc2e76395-38a1-48f7-a9e0-af735b8f7c41%26code_challenge%3DB6UIlBembEzqwF9Nkj3jpXmSHMslZoH494Ffp_SXy-4%26code_challenge_method%3DS256%26product%3DDcard%26redirect_uri%3Dhttps%253A%252F%252Fwww.dcard.tw%252Fservice%252F_auth%252Fcallback%26region%3DTW%26response_type%3Dcode%26scope%3Dconfig%2520config%253Awrite%2520device%2520device%253Awrite%2520email%2520email%253Awrite%2520facebook%2520feed%253Asubscribe%2520forum%2520forum%253Asubscribe%2520idcard%2520member%2520member%253Awrite%2520notification%2520persona%2520phone%2520phone%253Avalidate%2520phone%253Awrite%2520photo%2520post%2520post%253Asubscribe%2520topic%2520topic%253Asubscribe%2520collection%2520collection%253Awrite%2520comment%253Awrite%2520forum%253Awrite%2520friend%2520friend%253Awrite%2520like%2520reaction%2520match%2520match%253Awrite%2520message%2520message%253Awrite%2520message%253Aprivate%2520poll%253Awrite%2520persona%253Asubscribe%2520persona%253Awrite%2520post%253Awrite%2520report%2520token%253Arevoke%2520loginVerification%2520loginVerification%253Averify%26state%3DeyJjc3JmIjoiZ2FPM0lCWEMtWC1MN3BJaUhJeHFrYjJibzN1LThpTnU1MElNIiwicmVkaXJlY3QiOiIvc2VydmljZS9zc28vY2FsbGJhY2s_cmVkaXJlY3Q9JTJGbXkifQ%26ui_locales%3Dzh-TW&ui_locales=zh-TW&product=Dcard&region=TW&bdid=144f554d-48e5-4df3-aa26-a949a4e3d746")

        # Click [placeholder="輸入信箱"]
        page.locator("[placeholder=\"輸入信箱\"]").click()
        print('[info] click email input.')

        # Fill [placeholder="輸入信箱"]
        page.locator("[placeholder=\"輸入信箱\"]").fill(
            "{}".format(self.parserOptions.email))
        print('[info] fill email input.')

        # Click [placeholder="輸入密碼"]
        page.locator("[placeholder=\"輸入密碼\"]").click()
        print('[info] click password input.')

        # Fill [placeholder="輸入密碼"]
        page.locator("[placeholder=\"輸入密碼\"]").fill(
            "{}".format(self.parserOptions.password))
        print('[info] fill password input.')

        # Click button:has-text("註冊 / 登入")
        # with page.expect_navigation(url="https://www.dcard.tw/my"):
        with page.expect_navigation():
            page.locator("button:has-text(\"註冊 / 登入\")").click()

        # Close page
        page.close()
        print('[info] close page.')

        # Open new page
        page = context.new_page()

        # Go to https://www.dcard.tw/
        page.goto("https://www.dcard.tw/")

        # Go to https://3d8e91bb5011f65988b7b6848dd909f5.safeframe.googlesyndication.com/
        page.goto(
            "https://3d8e91bb5011f65988b7b6848dd909f5.safeframe.googlesyndication.com/")

        # Go to https://tpc.googlesyndication.com/
        page.goto("https://tpc.googlesyndication.com/")

        # Go to https://www.google.com/
        page.goto("https://www.google.com/")

        # Go to https://id.dcard.tw/
        page.goto("https://id.dcard.tw/")

        # Close page
        page.close()

        # ---------------------
        context.storage_state(path="dcard_auth.json")
        print('[info] save auth state.')
        context.close()
        browser.close()


class dcardPostInformation:
    def __init__(self):
        self.dcardCrawlerDBHandler = mysql_connect_handle.labDBconnect(
            'config/mysql.yaml')
        # This parser is used to parse the command line arguments
        self.parserOptions = parser_opt.commentParserOpt()
        self.postCount = 0
        self.stopCrawler = False
        # To get all post information from dcardCrawlerDBHandler
        _postsTemp = self.fund(self.dcardCrawlerDBHandler.getDcardPosts())[self.parserOptions.spilt_process]
        self.parallel_processing(_postsTemp)

        # __next > main > div > div > article > div.sc-1eorkjw-5.hKBtVr > div > div

    def fund(self, listTemp):
        resules = [
            listTemp[:len(listTemp)//3],
            listTemp[len(listTemp)//3:len(listTemp)//3*2],
            listTemp[len(listTemp)//3*2:]
        ]
        return resules

    def parallel_processing(self,  postIds):
        for postId in postIds:
            try:
                with sync_playwright() as playwright:
                    # 'postCount' must be initialized to 0 before 'self.run()'
                    # The 'postCount' is used to count the number of comments that have been crawled
                    self.run(playwright, postId.href)
            except:
                pass

    def handleResponse(self, response):
        if '/comments?' in response.url and response.status == 200:
            try:
                for comment in response.json():
                    if not comment['hidden']:
                        _commentTemp = {
                            'postId': self.postId,
                            'author': comment['school'],
                            'content': comment['content'],
                            'comment_key': comment['id'],
                            'like': comment['likeCount'],
                            'comment_created_at': pandas.to_datetime(comment['createdAt'])
                        }
                        self.dcardCrawlerDBHandler.writeCommentToDatabase(
                            self,
                            _commentTemp)
            except Exception as e:
                print("[error]handleResponse {}".format(e))

    def parserFirstContent(self):
        # self.contentLoopTimesTemp += 1
        firstLoadComments = self.page.query_selector_all(
            "#__next > main > div > div > div > div > div > div > section > div > div")
        # First we using the firstLoadComments to get the content by querySelectorAll
        for comment in firstLoadComments:
            # A for loop to get the comment content
            try:
                if 'comment-' in comment.get_attribute('data-key'):
                    # Using comment- to filter the comment
                    commentCreatedAt = comment.query_selector(
                        'div > div > div > div > div:nth-child(3) > a > span > span:nth-child(2)').get_attribute('title').replace(' ', '')
                    commentCreatedAt = commentCreatedAt.replace(
                        "上午", ' AM').replace("下午", ' PM').replace(',', ' ')
                    commentCreatedAt = pandas.to_datetime(
                        commentCreatedAt, dayfirst=True)

                    like = comment.query_selector(
                        'div > div > div > div > div > div:nth-child(2)').inner_text().replace('\n', '')
                    if like == '':
                        like = 0
                    _commentTemp = {
                        'postId': self.postId,
                        'comment_key': comment.get_attribute('data-key').replace('comment-', ''),
                        'author': comment.query_selector('div > div > div > div > div > div:nth-child(1)').inner_text().strip().replace('\n', '').replace(' ', ''),
                        'content': comment.query_selector('div > div > div > div > div:nth-child(2) > div:nth-child(1)').inner_text().strip().replace('\n', '').replace(' ', ''),
                        'like': like,
                        'comment_created_at': commentCreatedAt
                    }
                    # And then we write the comment to database, the comment temp should have the following keys:
                    # postId(str): the postId of the comment
                    # comment_key(str): the comment_key of the comment
                    # author(str): the author of the comment
                    # content(str): the content of the comment
                    # like(int): the like of the comment
                    self.dcardCrawlerDBHandler.writeCommentToDatabase(
                        self,
                        _commentTemp)
            except Exception as e:
                print('[error]parserFirstContent!!!{}'.format(e))
        # After we get the first page's comment, we need to load the next page

    def parserMainContent(self):
        # Click main[role="main"] div:has-text("今天在ikea用餐 旁邊坐一對情侶 男生剛坐下來就開始啃他碗裡的肋排 女生則是先吃菜 原想說這男生怎麼吃相不太好看（抱歉抱歉） 當我用餐完往旁邊轉過去 看到女生") >> nth=4
        mainContent = re.sub(r'\n(?=\n)', '', self.page.query_selector(
            "#__next > main > div > div > article > div > div > div").inner_text().strip())
        mainContent = mainContent.replace(' ', ',').replace('\n', ',')
        contentCreatedAt = self.page.query_selector(
            "#__next > main > div > div > article > div:nth-child(2) > div:nth-child(2)").inner_text().strip()
        if "年" not in contentCreatedAt:
            contentCreatedAt = f"2022年{contentCreatedAt}"
        contentCreatedAt = contentCreatedAt.replace(
            "年", '-').replace("月", '-').replace("日", ' ')
        contentCreatedAt = pandas.to_datetime(contentCreatedAt)
        # call the writeContentToDatabase function to write the content to database
        self.dcardCrawlerDBHandler.writeMainContentToDatabase(
            cls=self,
            content={
                'content': mainContent,
                'contentCreatedAt': contentCreatedAt,
            })

    def run(self, playwright: Playwright, postId="") -> None:
        self.postId = postId
        browser = playwright.chromium.launch()
        context = browser.new_context(
            **playwright.devices["iPhone 11"], storage_state='dcard_auth.json')

        # Open new page
        self.page = context.new_page()
        self.page.on('response', self.handleResponse)
        # Go to https://www.dcard.tw/f/relationship/p/238532512
        self.page.goto(f"https://www.dcard.tw{postId}")
        try:
            self.parserMainContent()
            print("[info]parserFirstContent")
            self.parserFirstContent()
            print("[info]Loop page")
            public_functions.loadNextPage(self.page)
        except Exception as e:
            print(f'[error]{e}')
            print('None!')
        context.storage_state(path="dcard_auth.json")
        print('[info] save auth state.')
        context.close()
        browser.close()


if __name__ == "__main__":
    # To bypass the captcha, we need to get the auth state
    #dcardAuthGenerateWithMobile()
    # Finally we can get the content, and comments of the post
    dcardPostInformation()
    # Congratulations! You have finished the task!
