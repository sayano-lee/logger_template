import os
from logger import make_logger


if __name__ == "__main__":
    # Initialize logger
    logger_path = '/path/to/logger'
    os.makedirs(logger_path, exist_ok=True)
    logger = make_logger('Description of logger', logger_path, 'name of logging file')

    # Save argparser into  logging file
    logger.info('information to be saved') 
    for k, v in parser.__dict__.items():
        logger.info('\t----- {}: {}'.format(k, v))

    logger.info('some information to be saved')
