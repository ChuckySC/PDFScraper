from modules.constants import Constants
from functions.universal import loadjson

from pathlib import Path
import logging
import os

class Configuration:
    config_file_path = 'pyconfig.json'
    
    CONFIG_LOCAL_STR = 'local'
    CONFIG_TEST_STR = 'test'
    CONFIG_LIVE_STR = 'live'
    
    # set config you want to use
    CONFIGTOUSE = CONFIG_LOCAL_STR
    
    logger = None
    
    description = None
    skip_line = None
    start_title = None
    title = None
    start_body = None
    body = None
    start_author = None
    author = None
    
    def __init__(self, id:int = None):
        self.logger = logging.getLogger(Constants.project_name)
        self.config_file_path = os.path.join(
            Path(os.path.dirname(__file__)).parents[0], 
            self.config_file_path
        )
        data = loadjson(self.config_file_path)
        try:
            self.loaddata(data[self.CONFIGTOUSE])
        except Exception as e:
            self.logger.exception(e)
            raise
    
    def loaddata(self, environment):
        self.description = environment['description']
        self.skip_line = environment['skip_line']
        self.start_title = environment['start_title']
        self.title = environment['title']
        self.start_body = environment['start_body']
        self.body = environment['body']
        self.start_author = environment['start_author']
        self.author = environment['author']