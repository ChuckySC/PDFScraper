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
    skip = None
    title_start = None
    title = None
    content_start = None
    content = None
    author_start = None
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
        self.skip = environment['skip']
        self.title_start = environment['title-start']
        self.title = environment['title']
        self.content_start = environment['content-start']
        self.content = environment['content']
        self.author_start = environment['author-start']
        self.author = environment['author']