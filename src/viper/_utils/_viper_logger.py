 #   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


viper_logger_name = 'viper'
import sys
import logging
from datetime import datetime
formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
from dask.distributed import get_worker
from dask.distributed import WorkerPlugin
import dask

def _get_viper_logger(name = viper_logger_name):
    '''
    Will fisrt try to get worker logger. If this fails graph construction logger is returned.
    '''
    from dask.distributed import get_worker
    try:
        worker = get_worker()
    except:
        return logging.getLogger(name)
    
    try:
        logger = worker.plugins['viper_worker'].get_logger()
        return logger
    except:
        return logging.getLogger()

def _setup_viper_logger(log_to_term=False,log_to_file=True,log_file='viper_', log_level='INFO', name=viper_logger_name):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(log_level))
    
    if log_to_term:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    if log_to_file:
        log_file = log_file+datetime.today().strftime('%Y%m%d_%H%M%S')+'.log'
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
    
def _get_viper_worker_logger_name(name=viper_logger_name):
    worker_log_name = name + '_' + str(get_worker().id)
    return worker_log_name

'''
class _viper_worker_logger_plugin(WorkerPlugin):
    def __init__(self,log_parms):
        self.log_to_term=log_parms['log_to_term']
        self.log_to_file=log_parms['log_to_file']
        self.log_file=log_parms['log_file']
        self.level=log_parms['log_level']
        self.logger = None
        print(self.log_to_term,self.log_to_file,self.log_file,self.log_level)
        
    def get_logger(self):
        return self.logger
        
    def setup(self, worker: dask.distributed.Worker):
        "Run when the plugin is attached to a worker. This happens when the plugin is registered and attached to existing workers, or when a worker is created after the plugin has been registered."
        self.logger = _setup_viper_worker_logger(self.log_to_term,self.log_to_file,self.log_file,self.level)
'''

def _setup_viper_worker_logger(log_to_term,log_to_file,log_file, log_level):
    parallel_logger_name = _get_viper_worker_logger_name()
    
    logger = logging.getLogger(parallel_logger_name)
    logger.setLevel(logging.getLevelName(log_level))
    
    if log_to_term:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    if log_to_file:
        log_file = log_file + '_' + str(get_worker().id) + '_' + datetime.today().strftime('%Y%m%d_%H%M%S') + '.log'
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
