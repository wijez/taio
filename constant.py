class TaioConstant:
    def __init__(self):
        self.flag = False
        self.PAGE = None
        self.BUTTON_ACTION = None
        self.ROW = None
        self.NEXT_5_PAGE = None
        self.index = 2
        self.page_numbers = 3
        self.release_date = None
        self.declaration_period = None
        self.update_next_5_page(isActivate=None)
        self.update_next_page(isActivate=None, next_5_page=None)
        self.update_row(isActivate=None)

    def update_next_5_page(self, isActivate):
        if isActivate == 0:
            self.NEXT_5_PAGE = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/ul/li[8]'
        else:
            self.NEXT_5_PAGE='//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/ul/li[10]'

    def update_next_page(self, isActivate, next_5_page):
        if next_5_page == 0:
            if isActivate < 3:
                self.PAGE = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/ul/li[10]'
            elif isActivate == 4:
                self.PAGE = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/ul/li[11]'
        else:
            self.PAGE = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/ul/li[12]'

    def update_row(self, isActivate):
        self.ROW = (f'//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div/div['
                    f'3]/div/div/div/div/div[2]/table/tbody/tr[{isActivate}]')

    BUTTON_DOWNLOAD = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/button[1]/span'
    NUMBER = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/button[2]/span'
    ID = '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr[3]/td[1]/span[2]'
    SUPPILER = '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr[4]/td/span[2]'
    FIELD_ACCOUNT = '//*[@id="username"]'
    FIELD_PASSWORD = '//*[@id="password"]'

    BUTTON_LOGIN = '//*[@id="root"]/div/div/div[3]/form/div[4]/button'
    BUTTON_BILL = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div/div[1]/div/div/div[1]'
    FIRST_ROW = ('//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div/div/div/div/div['
                 '2]/table/tbody/tr[2]')
    NEXT_PAGE = '//*[@id="primaryLayout"]/main/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/button[3]'
    BUTTON_DOWNLOAD = '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/button[8]'

    URL = "https://hoadon.taio.vn/"
    CORE_NAME = "TAIO"

    META_DATA = {
        'URL': URL,
        'RPA_NAME': CORE_NAME,
        'DRIVER_NAME': 'edge'

    }
    VERSIONS = {
        'v1': {
            'URL': URL,
            'RPA_NAME': CORE_NAME
        }
    }
    LATEST_VERSION = 'v1'
    DELAY_OPEN_MAXIMUM_BROWSER = 2
    DELAY_TIME_LOAD_PAGE = 10
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 4
    RETRY_MAX = 2
    SLEEP = 5


taio_constant = TaioConstant()
