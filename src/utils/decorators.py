import logging
import time

logging.basicConfig(level=logging.INFO)


def task_logger(func):
    def wrapper_with_args_kwargs(*args, **kwargs):
        func_logger = logging.getLogger(__name__)
        if args:
            for arg in args:
                func_logger.info(f'Positional argument: {arg} Type: {type(arg)}')
        if kwargs:
            for kwarg in kwargs:
                func_logger.info(f'Keyword argument: {kwarg} Type: {type(kwarg)}')

        try:
            st = time.time()
            output = func(*args, **kwargs)
            func_logger.info(f'---- {int((time.time() - st)*1000)} ms ----')

            logging.info(f'Output: {output} Type: {type(output)}')
        except Exception:
            func_logger.error('Exception', exc_info=True)

    return wrapper_with_args_kwargs
