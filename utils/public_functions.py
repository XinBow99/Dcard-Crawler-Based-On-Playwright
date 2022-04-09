def loadNextPage(page, stopLoopLimit: object = None):
    times = 0
    while True:
        scrollStatus1 = page.evaluate("""async () => {
            response = document.documentElement.scrollHeight;
            return response
            }""")
        page.evaluate(
            'window.scrollTo(0, document.body.scrollHeight)')
        page.mouse.wheel(0, 100)
        page.wait_for_timeout(100)
        scrollStatus2 = page.evaluate("""async () => {
            response = document.documentElement.scrollHeight;
            return response
            }""")
        if scrollStatus1 == scrollStatus2:
            times += 1
            if times > 10:
                print('[info]scroll to the end')
                break
            else:
                page.mouse.wheel(0, 100)
        else:
            times = 0
        if stopLoopLimit is not None:
            if stopLoopLimit.stopCrawler:
                break
