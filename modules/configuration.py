from modules.constants import Constants
from functions.universal import load_json

from pathlib import Path
import logging
import os

class Configuration:
    config_file_path = 'pyconfig.json'

    CONFIG_LOCAL_STR = 'local'
    CONFIG_TEST_STR = 'test'
    CONFIG_LIVE_STR = 'live'

    CONFIGTOUSE = CONFIG_LOCAL_STR
    
    description = None
    secret_key = None
    upload_folder = None
    allowed_extensions = None
    max_rows = None
    parameters = None
    mapping_base = None
    
    logger = None
    
    def __init__(self, id:int = None):
        self.logger = logging.getLogger(Constants.project_name)
        self.config_file_path = os.path.join(
            Path(os.path.dirname(__file__)).parents[0], 
            self.config_file_path
        )
        data = load_json(self.config_file_path)
        try:
            self.loaddata(data[self.CONFIGTOUSE])
        except Exception as e:
            self.logger.exception(e)
            raise
    
    def loaddata(self, environment):
        self.description = environment['description']
        self.secret_key = environment['secret_key']
        self.upload_folder = environment['upload_folder']
        self.allowed_extensions = environment['allowed_extensions']
        self.max_rows = environment['max_rows']
        self.parameters = environment['parameters']
        self.mapping_base = environment['mapping_base']