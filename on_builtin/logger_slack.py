import logging
import logging.handlers
import datetime # TODO: MongoHandler에 사용됨, 불필요하게 되면 삭제


# - [조금 더 체계적인 Python Logging](https://hwangheek.github.io/2019/python-logging/)
# - [LogRecord 어트리뷰트](https://docs.python.org/ko/3/library/logging.html#logrecord-attributes)
# - [logging.handlers — 로깅 처리기](https://docs.python.org/ko/3/library/logging.handlers.html)
# - [logging — 파이썬 로깅](https://docs.python.org/ko/3/library/logging.html)
# - [Logging to MongoDB (로그 남기기)](http://blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=222033147585)

# https://docs.python.org/ko/3/library/logging.html
# https://sematext.com/blog/logging-levels/
## https://www.webfx.com/tools/emoji-cheat-sheet/

## TODO: load log setting(yml), 

SLACK_TOKEN = ''


class SlackHandler(logging.handlers.HTTPHandler):
    def __init__(self, name, token, channel='#stock', format=None, emoji=True):
        """SlackHandler 초기화

        Args:
            name (str, optional): log 이름
            token (str, optional): slack token
            channel (str, optional): slack channel. Defaults to '#stock'.
            emoji (bool, optional): log에 emoji를 사용하는지 여부. Defaults to True.
        """
        super().__init__(host='slack.com', method='POST', url='/api/chat.postMessage', secure=True)
        self.token = token
        self.channel = channel
        self.emoji = emoji

        logger = logging.getLogger(name)

        self.logger = logger

        format = {
           'fmt': '%(name)s,%(asctime)s,%(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S'  
        } if format == None else format

        self.formatter = logging.Formatter(
            **format
        )


    # 수준	숫자 값
    # CRITICAL	50
    # ERROR	40
    # WARNING	30
    # INFO	20
    # DEBUG	10
    # NOTSET	0
    def mapLogRecord(self, record):
        """log record 매핑

        Args:
            record (obj): log record

        Returns:
            [dict]: {'token': '', 'channel': '', 'text': '', 'as_user': True}
        """
        if self.formatter is None:    # Formatter가 설정되지 않은 경우
            text = record.msg
        else:
            text = self.formatter.format(record)
        
        emoji = (
            '' if self.emoji == False else
            ':bug:' if record.levelname == 'DEBUG' else
            ':pencil2:' if record.levelname == 'INFO' else
            ':warning:' if record.levelname == 'WARNING' else
            ':fire:' if record.levelname == 'ERROR' else
            ':rotating_light:' if record.levelname == 'CRITICAL' else
            ':pushpin:'
        )

        return {
            'token': self.token,
            'channel': self.channel,
            'text': f'{emoji} {text}',
            'as_user': True,
        }


class SlackLog():
    def __init__(self, name, token, channel="#stock", format=None, emoji=True):
        """SlackLog 초기화

        Args:
            name (str, optional): log 이름
            token (str, optional): slack token
            channel (str, optional): slack channel. Defaults to '#stock'.
        """

        # formatter = logging.Formatter(
        #     fmt='%(asctime)s *%(module)s* : %(message)s',
        #     datefmt='%H:%M:%S',
        # )

        slack_handler = SlackHandler(name, token, channel=channel, format=format, emoji=emoji)
        slack_handler.setFormatter(slack_handler.formatter)
        slack_handler.logger.addHandler(slack_handler)

        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

        self.logger = slack_handler.logger
        self.logger.setLevel(logging.DEBUG) # Note: logger level 설정


def log_slack(msg, level='info', name='slacklog', token=SLACK_TOKEN, channel='#stock', format=None, emoji=True):
    """slack으로 log 메시지를 보냄

    Args:
        msg (str): 메시지
        level (str): debug / info / warning / error
        name (str, optional): log 이름. Defaults to 'slacklog'.
        token (str, optional): slack token. Defaults to SLACK_TOKEN.
        channel (str, optional): slack channel. Defaults to '#stock'.
    """

    slacklog = SlackLog(name=name, token=token, channel=channel, format=format, emoji=emoji)

    if level == 'debug':
        slacklog.logger.debug(msg)
    elif level == 'info':
        slacklog.logger.info(msg)
    elif level == 'warning':
        slacklog.logger.warning(msg)
    elif level == 'error':
        slacklog.logger.error(msg)
    elif level == 'critical':
        slacklog.logger.critical(msg)
    else:
        slacklog.logger.debug(msg)              


if __name__ == "__main__":
    level = 'critical'
    msg = f'slack logger test({level})'
    log_slack(msg, level)


# # -*- coding: utf-8 -*-
# import logging.handlers

# # http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
# def Logger(name):
#     """파일 로그 클래스
#         :param name: 로그 이름
#             log = Logger(__name__)
#     """

#     # 로거 인스턴스를 만든다
#     log = logging.getLogger(name)

#     # 환경변수를 읽어서 로깅 레벨과 로그를 남길 파일의 경로를 변수에 저장한다
#     if LoggerSetting.LEVEL == 'DEBUG':
#         fomatter = logging.Formatter("%(asctime)s[%(levelname)s|%(name)s,%(lineno)s] %(message)s")
#         loggerLevel = logging.DEBUG
#     else:
#         fomatter = logging.Formatter("%(asctime)s[%(name)s] %(message)s")
#         if LoggerSetting.LEVEL == 'INFO':
#             loggerLevel = logging.INFO
#         else:
#             loggerLevel = logging.ERROR

#     log.setLevel(loggerLevel)
#     # 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
#     fileHandler = logging.handlers.RotatingFileHandler(LoggerSetting.FILE, maxBytes=1024 * 1024 * LoggerSetting.MAX_MBYTE, backupCount=LoggerSetting.BACK_COUNT, encoding="utf-8")
#     streamHandler = logging.StreamHandler()
#     # 각 핸들러에 포매터를 지정한다.
#     fileHandler.setFormatter(fomatter)
#     streamHandler.setFormatter(fomatter)
#     # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
#     log.addHandler(fileHandler)
#     log.addHandler(streamHandler)
#     return log


# class LoggerSetting:
#     """파일 로그 환경을 설정하는 클래스
#             LoggerSetting.LEVEL = "INFO"
#             LoggerSetting.FILE = "logfile.log"
#     """
#     LEVEL = "DEBUG"
#     """로그 레벨
#     """
#     FILE = "__Trader.log"
#     """로그 파일명
#     """
#     MAX_MBYTE = 10
#     """로그 파일 하나의 최대 크기 (MByte)
#     """
#     BACK_COUNT = 10
#     """로그 파일 유지 개수
#     """