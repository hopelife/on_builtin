import sys, os
import logging
import logging.handlers
import datetime # TODO: MongoHandler에 사용됨, 불필요하게 되면 삭제

##------------------------------------------------------------
## User 모듈
##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '.')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from api_google_gspread import (api, write_sheet_add)

## TODO: load log setting(yml), 

class GoogleHandler(logging.Handler):
    # def __init__(self, level=logging.NOTSET, spreadsheet='test_write', worksheet='test_sheet', path="configs/google_account_mats.yml", format=None, name='googlelog'):
    def __init__(self, spreadsheet='test_write1', worksheet='test_sheet', path="configs/google_account_mats.yml", format=None, name='googlelog'):
        # logging.Handler.__init__(self, level) #// 부모 생성자 호출
        logging.Handler.__init__(self, logging.NOTSET) #// 부모 생성자 호출
        # self.api = api
        self.name = name
        self.path = path
        self.spreadsheet = spreadsheet
        self.worksheet = worksheet

        logger = logging.getLogger(name)
        self.logger = logger

    def emit(self, record):
        self.record = record
        data = {
            'name' : self.name,       #// 로그 이름
            'when' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),       #// 현재일시
            # 'threadName': record.threadName,        #// 쓰레드명
            # 'functionName': record.funcName,        #// 함수명
            # 'levelNumber': record.levelno,          #// 로그레벨(ex. 10)
            'level': record.levelname,          #// 로그레벨명(ex. DEBUG)
            'message': record.msg,                  #// 오류 메시지
        }

        _api = api(path=self.path)
        write_sheet_add([data], spreadsheet_title=self.spreadsheet, worksheet_title=self.worksheet, api=_api)


class GoogleLog():
    # def __init__(self, level='info', spreadsheet='test_write', worksheet='test_sheet', path="configs/google_account_mats.yml", format=None, name='googlelog'):
    def __init__(self, spreadsheet='test_write', worksheet='test_sheet', path="configs/google_account_mats.yml", format=None, name='googlelog'):

        # formatter = logging.Formatter(
        #     fmt='%(asctime)s *%(module)s* : %(message)s',
        #     datefmt='%H:%M:%S',
        # )

        google_handler = GoogleHandler(spreadsheet=spreadsheet, worksheet=worksheet, path=path, format=format, name=name)
        # google_handler.setFormatter(google_handler.formatter)
        google_handler.logger.addHandler(google_handler)

        self.logger = google_handler.logger
        self.logger.setLevel(logging.DEBUG) # Note: logger level 설정


def log_google(msg, level='info', spreadsheet='test_write', worksheet='test_sheet', path="configs/google_account_mats.yml", format=None, name='googlelog'):
    """google으로 log 메시지를 보냄

    Args:
        msg (str): 메시지
        name (str, optional): log 이름
        path (str, optional): google 저장 경로path
    """

    googlelog = GoogleLog(spreadsheet=spreadsheet, worksheet=worksheet, path=path, name=name)

    print(f"googlelog.logger: {googlelog.logger}")
    if level == 'debug':
        googlelog.logger.debug(msg)
    elif level == 'info':
        googlelog.logger.info(msg)
    elif level == 'warning':
        googlelog.logger.warning(msg)
    elif level == 'error':
        googlelog.logger.error(msg)
    elif level == 'critical':
        googlelog.logger.critical(msg)
    else:
        googlelog.logger.debug(msg)   


if __name__ == "__main__":
    # googlelog = CsvLog("log.google")
    msg = 'test logger google'
    log_google(msg, level='info', spreadsheet='google_log', worksheet='test3', name='googlelog')