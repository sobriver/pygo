import asyncio, tkinter, traceback
from pyppeteer import launch

"""
pyppeteer框架爬虫
"""

class PyppeteerBrowser:
    def __init__(self):
        # self.hash = Hash_Utils()
        self.url = None
        self.ua = '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'


    # """使用tkinter获取屏幕大小"""）--OK--
    def screen_size(self):
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()
        return width, height


        # 构造一个浏览器对象； --OK--


    async def getbrowser(self, headless=True):
        # 'dumpio': True：解决chromium浏览器多开页面卡死问题。
        '''
            参数：
            ignoreHTTPSErrors (bool): 是否要忽略 HTTPS 的错误，默认是 False。
            headless (bool): 是否启用 Headless 模式，即无界面模式，如果 devtools 这个参数是 True 的话，那么该参数就会被设置为 False，否则为 True，即默认是开启无界面模式的。
            executablePath (str): 可执行文件的路径，如果指定之后就不需要使用默认的 Chromium 了，可以指定为已有的 Chrome 或 Chromium。
            slowMo (int|float): 通过传入指定的时间，可以减缓 Pyppeteer 的一些模拟操作。
            args (List[str]): 在执行过程中可以传入的额外参数。
            ignoreDefaultArgs (bool): 不使用 Pyppeteer 的默认参数，如果使用了这个参数，那么最好通过 args 参数来设定一些参数，否则可能会出现一些意想不到的问题。这个参数相对比较危险，慎用。
            handleSIGINT (bool): 是否响应 SIGINT 信号，也就是可以使用 Ctrl + C 来终止浏览器程序，默认是 True。
            handleSIGTERM (bool): 是否响应 SIGTERM 信号，一般是 kill 命令，默认是 True。
            handleSIGHUP (bool): 是否响应 SIGHUP 信号，即挂起信号，比如终端退出操作，默认是 True。
            dumpio (bool): 是否将 Pyppeteer 的输出内容传给 process.stdout 和 process.stderr 对象，默认是 False。
            userDataDir (str): 即用户数据文件夹，即可以保留一些个性化配置和操作记录。(比如登录信息等；可以在以后打开时自动登录；)
            env (dict): 环境变量，可以通过字典形式传入。
            devtools (bool): 是否为每一个页面自动开启调试工具，默认是 False。如果这个参数设置为 True，那么 headless 参数就会无效，会被强制设置为 False。
            logLevel  (int|str): 日志级别，默认和 root logger 对象的级别相同。
            autoClose (bool): 当一些命令执行完之后，是否自动关闭浏览器，默认是 True。
            loop (asyncio.AbstractEventLoop): 时间循环对象。
        '''
        '''
        launch_kwargs = {
        # 控制是否为无头模式
        "headless": False,
        # chrome启动命令行参数
        "args": [
            # 浏览器代理 配合某些中间人代理使用
            "--proxy-server=http://127.0.0.1:8008",
            # 最大化窗口
            "--start-maximized",
            # 取消沙盒模式 沙盒模式下权限太小
            "--no-sandbox",
            # 不显示信息栏  比如 chrome正在受到自动测试软件的控制 ...
            "--disable-infobars",
            # log等级设置 在某些不是那么完整的系统里 如果使用默认的日志等级 可能会出现一大堆的warning信息
            "--log-level=3",
            # 设置UA
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        ],
        # 用户数据保存目录 这个最好也自己指定一个目录
        # 如果不指定的话，chrome会自动新建一个临时目录使用，在浏览器退出的时候会自动删除临时目录
        # 在删除的时候可能会删除失败（不知道为什么会出现权限问题，我用的windows） 导致浏览器退出失败
        # 然后chrome进程就会一直没有退出 CPU就会狂飙到99%
        "userDataDir": "",
        }
        '''
        print("构造浏览器对象开始...")
        ##注意：同一个用户目录（userDataDir）不能被两个chrome进程使用，如果你要多开，记得分别指定用户目录。否则会报编码错误。
        self.browser = await launch({'headless': headless,
                                     'args': ['--no-sandbox', "--log-level=3", "--no-sandbox", "--disable-infobars",
                                              '--start-maximized', '--disable-infobars']})

        self.page = await self.browser.newPage()  # 在此浏览器上创建新页面并返回其对象。

        width, height = self.screen_size()
        # 设置网页可视区域大小
        await self.page.setViewport({
            "width": width,
            "height": height
        })

        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)

        # 设置请求头userAgent
        await self.page.setUserAgent(self.ua)

        await self.preventCheckWebdriver(self.page)
        print("构造浏览器对象完毕....", self.page)


    # 获取当前操作的界面    --OK--
    async def getPage(self):
        return self.page


    # 获取当前page对象的链接；
    async def getCurUrl(self, page):
        if page == None:
            page = self.page
        return page.url


    # 打开一个新的界面；）--OK--
    async def getnewpage(self):
        return await self.browser.newPage()


    # 获取当前操作的界面重新加载    ??????????
    async def reload(self):
        await self.page.reload()


    # 当前操作界面返回    ??????????
    async def goBack(self):
        await self.page.goBack()


    # 获取当前操作的界面的URL   ??????????
    async def getPageUrl(self):
        await self.page.url()


    # 打开连接；--OK--
    async def open(self, url, timeout=60):
        if url == None:
            print("当前传入的【url】不能为空，参数错误！！")
        self.url = url
        print("打开网页：" + (url))
        self.res = await self.page.goto(url, options={'timeout': int(timeout * 1000)})  # 打开连接；
        await asyncio.sleep(2)  # 强行等待3秒
        status = self.res.status
        curUrl = self.page.url
        await self.preventCheckWebdriver(self.page)
        return status, curUrl


    # 防止 webdriver 检测，如淘宝登录。其实淘宝主要通过 window.navigator.webdriver 来对 webdriver 进行检测，所以我们只需要使用 JavaScript 将它设置为 false 即可
    async def preventCheckWebdriver(self, page):
        if page == None:
            page = self.page
        # 替换淘宝在检测浏览时采集的一些参数。
        # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
        # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator
        await page.evaluate(
            '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
        await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')


    # 关闭当前打开的浏览器；--OK--
    async def closeBrowser(self, browser):
        if browser == None:
            browser = self.browser
        try:
            await browser.close()
        except:
            pass


    # 关闭当前打开的浏览器中的一个界面；--OK--
    async def closePage(self, page):
        if page == None:
            page = self.page
        await page.close()


    # 关闭当前打开的浏览器中的某一个界面；--OK--
    async def closeNumPage(self, number: "号码从0开始"):
        pages = await self.browser.pages()
        await pages[number].close()
        return True


    # 关闭除了最后一个所有的界面；--OK--
    async def retainLastPage(self):
        pages = await self.browser.pages()
        num = 0
        for page in pages:
            if num != (len(pages) - 1):
                await page.close()
            else:
                self.page = page
            num += 1


    # 获取当前打开页面的响应状态        --OK--
    async def gerReponseStatus(self):
        try:
            return self.res.status  # 响应状态
        except:
            return 200


    # 截个图
    async def screenshot(self, page):
        hashCode = self.hash.getMd5Hash(self.url)
        if page == None:
            page = self.page
        await page.screenshot({'path': './screenshots/' + str(hashCode) + '.png'})


    # 得到响应头；            --OK--
    async def getHeader(self):
        return self.res.headers  # 响应头；


    # 滚动到页面底部            --OK--
    async def scrollToButtom(self, page):
        if page == None:
            page = self.page
        await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        print("滑动到当前界面底部【完毕】")


    # 获取当前页面的cookie
    async def getCookies(self, page):
        if page == None:
            page = self.page
        return await page.cookies()


    # 获取当前页面的cookie
    async def setCookies(self, page, cookies):
        if page == None:
            page = self.page
        return await page.setCookie(*cookies)


    # 获取所有 html源码        --OK--
    async def getHtml(self, page):
        if page == None:
            page = self.page
        return (await page.content())


    # 当前页标题                 --OK--
    async def getCurPageTitle(self, page):
        if page == None:
            page = self.page
        return (await page.title())


    # 获取对象属性值；
    async def getElementFieldValue(self, page, element, field):
        if element == None:
            print("当前传入的【element】不能为空，参数错误！！")
            return None
        if field == None:
            print("当前传入的【field】不能为空，参数错误！！")
            return None
        if page == None:
            page = self.page
        if str(type(element)) == "<class 'list'>":
            print("当前传入的【element】不是单个对象，为list集合，参数错误！！")
            return None
        fieldValue = await (await element.getProperty(field)).jsonValue()
        return fieldValue


    # 获取当前界面的宽、高、像素大小比率三个值    --OK--
    async def getPageWidthHight(self, page):
        if page == None:
            page = self.page
        return await page.evaluate('''() => {
                    return {
                        width: document.documentElement.clientWidth,
                        height: document.documentElement.clientHeight,
                        deviceScaleFactor: window.devicePixelRatio,
                    }
                }''')


    # 获取当前浏览器的所有界面集合；        --OK--
    async def getCurBrowserAllPages(self):
        return await self.browser.pages()


    # 获取当前界面中某个元素的内容；   :'如：//div[@class="title-box"]/a'      --OK--
    async def getElementsByXpaths(self, page, xpath):
        if xpath == None:
            print("当前传入的【xpath】不能为空，参数错误！！")
            return None
        if page == None:
            page = self.page
        elemList = None
        try:
            elemList = await page.xpath(xpath)
        except:
            print("获取xpath路径为【" + str(xpath) + "】的标签对象异常...")
        return elemList  # 返回类型为：list集合；


    # 获取当前界面的所有内容；（效果较差；）---OK---
    async def getPageText(self, page):
        if page == None:
            page = self.page
        return await page.evaluate('document.body.textContent', force_expr=True)


    # 获取元素内容；                        ---OK---
    async def getElementText(self, page, element):
        if element == None:
            print("当前传入的【element】不能为空，参数错误！！")
            return None
        if page == None:
            page = self.page
        if str(type(element)) == "<class 'list'>":
            print("当前传入的【element】不是单个对象，为list集合，参数错误！！")
            return None
        return await page.evaluate('(element) => element.textContent', element)


    # 通过selector获取元素内容；                        ---OK---
    async def getElementBySelector(self, page, selector):
        if selector == None:
            print("当前传入的【selector】不能为空，参数错误！！")
            return None
        if page == None:
            page = self.page
        return await page.querySelector(selector)


    # 向输入框输入数据                ---OK---
    # async def inputKw(self, page, selector: "如：'input#kw.s_ipt':获取input标签中id='kw',class='s_ipt'的对象。不可用xpath路径",
    #                   kw: '待输入的关键词'):
    #     if kw == None:
    #         print("当前传入的【kw】不能为空，参数错误！！")
    #         return None
    #     if selector == None:
    #         print("当前传入的【selector】不能为空，参数错误！！")
    #         return None
    #     if page == None:
    #         page = self.page
    #     mylist = [1.55, 0.798, 1.187]
    #     if len(kw) <= 5:
    #         mylist = [0.695, 0.798, 1.087, 0.343, 0.4067]
    #     else:
    #         mylist = [1.095, 0.798, 1.127, 1.0543, 1.1267, 0.8067]
    #     for i in str(kw):  # 逐个字符输入，减少被识别为机器的改了；
    #         await page.type(selector, i)
    #         time.sleep(random.choice(mylist))
    #     return None


    # 鼠标单击某一个元素；        ---OK---
    # async def clickElement(self, page, selector: "如：'input#kw.s_ipt':获取input标签中id='kw',class='s_ipt'的对象。。不可用xpath路径"):
    #     if selector == None:
    #         print("当前传入的【selector】不能为空，参数错误！！")
    #     if page == None:
    #         page = self.page
    #     await page.click(selector)  # 如果selector获取的对象是list集合，则执行第一个元素的点击；
    #

    # 清空某个input的值
    async def removeInputValue(self, page, idValue):
        if idValue == None:
            print("当前传入的【idValue】不能为空，参数错误！！")
        if page == None:
            page = self.page
        await page.evaluate("document.querySelector('#" + str(idValue) + "').value=''")
        print("清空【" + str(idValue) + "】的内容")


    # --OK--
    async def clickByEle(self, ele):
        if ele == None:
            return
        return ele.click()


    # 获取当前浏览器打开的【最后一个】界面对象    --OK--
    async def getLastPage(self):
        pages = await self.browser.pages()
        return pages[-1]


    # 获取当前浏览器打开的【最后一个】界面对象    --OK--
    async def getPageTotal(self):
        pages = await self.browser.pages()
        return len(pages)


    # 获取当前浏览器打开的【最一个】界面对象 --OK--
    async def getFirstPage(self):
        pages = await self.browser.pages()
        return pages[0]


    # 获取当前界面中所有的frame对象        --OK--
    async def getAllFrames(self, page):
        if page == None:
            page = self.page
        return page.frames


    # async def getScreenshotByEle(self, page, ele, screenshotFilePath: "目前测试只有.png图片可正常生成，jpg异常；"):
    #     picture = ''
    #     try:
    #         fu = File_Utils(None)
    #         fu = File_Utils(fu.getParentDir(screenshotFilePath))
    #         if not fu.exists(fu.getParentDir(screenshotFilePath)): fu.makeDirs()  # 如果图片的保存目录不存在，则创建；
    #         # 进行截图
    #         time.sleep(3)
    #         print("验证码路径:", screenshotFilePath)
    #         try:
    #             for _ in range(6):
    #                 clip = await ele.boundingBox()
    #                 picture = base64.b64encode(await page.screenshot({
    #                     'path': screenshotFilePath,  # 图片路径, 不指定就不保存
    #                     'clip': clip,  # 指定图片位置,大小
    #                     # 'encoding': 'base64',                           #  返回的图片格式, 默认二进制
    #                 }))
    #                 if picture != '':
    #                     break
    #         except Exception as e:
    #             print('截图获取失败')
    #             print(traceback.print_exc())
    #     except Exception as e:
    #         print('截图获取失败')
    #         print(traceback.print_exc())
    #     return picture