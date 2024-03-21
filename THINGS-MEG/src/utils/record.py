import logging
import sys
import hydra
from omegaconf import DictConfig
import logging.config

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, message):
        # オリジナルの sys.stdout への書き込みを削除
        message = message.rstrip()
        if message:
            self.logger.log(self.log_level, message)

    def flush(self):
        # flush メソッドが要求される可能性があるが、ここでは何もしない
        pass


def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='app.log',
                        filemode='a')

    stdout_logger = logging.getLogger('STDOUT')
    sys.stdout = StreamToLogger(stdout_logger, logging.INFO)

    stderr_logger = logging.getLogger('STDERR')
    sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)








# import logging
# import sys
# import hydra
# from omegaconf import DictConfig
# import logging.config

# class StreamToLogger:
#     """
#     Fake file-like stream object that redirects writes to a logger instance
#     while also writing to the original stream.
#     """
#     def __init__(self, original_stream, logger, log_level=logging.INFO):
#         self.original_stream = original_stream
#         self.logger = logger
#         self.log_level = log_level

#     def write(self, message):
#         # Write to the original stream (IDE or CLI)
#         self.original_stream.write(message)

#         # Remove trailing newlines before logging the message
#         message = message.rstrip()
#         if message:  # Avoid logging empty messages
#             self.logger.log(self.log_level, message)

#     def flush(self):
#         # Flushing the stream is important to ensure that the output is sent to the destination
#         self.original_stream.flush()

# def setup_logging():
#     LOGGING_CONFIG = {
#         'version': 1,
#         'disable_existing_loggers': False,
#         'formatters': {
#             'standard': {
#                 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#             },
#         },
#         'handlers': {
#             'file': {
#                 'level': 'DEBUG',
#                 'formatter': 'standard',
#                 'class': 'logging.FileHandler',
#                 'filename': 'app.log',
#                 'mode': 'a'
#             },
#             'console': {
#                 'level': 'DEBUG',
#                 'formatter': 'standard',
#                 'class': 'logging.StreamHandler',
#                 'stream': 'ext://sys.stdout'
#             },
#         },
#         'loggers': {
#             '': {  # root logger
#                 'handlers': ['file', 'console'],
#                 'level': 'DEBUG',
#                 'propagate': True
#             }
#         }
#     }

#     logging.config.dictConfig(LOGGING_CONFIG)

#     # StreamToLoggerの設定をここに移動
#     stdout_logger = logging.getLogger('STDOUT')
#     sys.stdout = StreamToLogger(sys.stdout, stdout_logger, logging.INFO)

#     stderr_logger = logging.getLogger('STDERR')
#     sys.stderr = StreamToLogger(sys.stderr, stderr_logger, logging.ERROR)