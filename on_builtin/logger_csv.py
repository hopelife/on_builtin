import logging
import logging.handlers
import datetime # TODO: MongoHandler에 사용됨, 불필요하게 되면 삭제


class CsvLog():
    def __init__(self, path='', format=None, name='csvlog'):
        """
        Args:
            path (str, optional): csv 저장 경로path
            format (str, optional): 
            name (str, optional): log 이름
        """
        format = {
           'fmt': "%(name)s\t%(levelname)s\t%(asctime)s\t%(message)s",  # %(name)s,%(asctime)s,%(created)f,%(module)s,%(process)d,%(thread)d,%(lineno)s,%(message)s',
           'datefmt': '%Y%m%d %H:%M:%S'  
        } if format == None else format

        formatter = logging.Formatter(
            **format
        )

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(path, encoding="UTF-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self.logger = logger  # debug / info / warning / error / critical


if __name__ == "__main__":
    csvlog = CsvLog(name='csvlog', path='test.csv').logger
    msg = 'test logger csv1'
    csvlog.info(msg)
