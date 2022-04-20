from pathlib import Path
import json
import datetime
import time
import random
from parse_config import Config
from logging_utils import Logger
from utils import get_token_meta, get_api_data, load_websocket_data, save_websocket_data
from user_kucoin import UserAPI
from trade_kucoin import TradeAPI
from websocket_kucoin import WebsocketAPI
from market_kucoin import MarketAPI

class TimeBasedSell:
    def __init__(self):
        '''
        Time Based Sell pipeline
        '''

        # configuration loading
        config_path = str(Path(__file__).resolve().parents[0].joinpath('configs', 'config.yaml'))
        self.config = Config(config_path = config_path).config
        self.api_data_path = self.config['api_data_path']
        self.api_name = self.config['api_name']
        self.mode = self.config['mode']
        self.target_time = datetime.datetime.fromisoformat(self.config['time_based_target_time'])
        self.trade_symbol = self.config['time_based_trade_symbol']
        self.size = self.config['time_based_amount']
        self.price = self.config['time_based_price']

        # logger loading
        self.log_dir = Path(self.config['log_dir']).joinpath('logs')
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logging_level = self.config['logging_level'].lower()
        self._logger = self._make_logger(log_dir=self.log_dir, logging_level=self.logging_level)

        # loading api data
        self.api_data = get_api_data(self.api_data_path)

        # main object creation
        self.trade = TradeAPI(self.api_data, self.api_name, self.mode)
        self.user = UserAPI(self.api_data, self.api_name, self.mode)
        self.market = MarketAPI(self.mode)


    def _make_logger(self, log_dir, logging_level='INFO', console_logger=True, multi_module=True):
        '''
        module to make the logger:

        Parameters
        ----------
        log_dir: string
            path to the the log directory

        logging_level: str
            level to be logged
        
        console_logger: bool
            boolean to specify if needed the log be shown in console.
            
        multi_module: bool
            boolean to be specified True in case of the logger is going to be used in multiple script.

        Returns
        ----------
        logger: logger 
            logger object
        '''

        logger = Logger(log_dir, logging_level=logging_level, console_logger=console_logger, multi_module=multi_module).make_logger()
        return logger


    def run(self):

        self._logger.info(f"checking {self.trade_symbol}...")
        now = datetime.datetime.now()
        price_base_data = self.market.get_symbol_data(self.trade_symbol)
        self._logger.info(f'price base data: {price_base_data}')

        while now <= self.target_time:
            now = datetime.datetime.now()

        while True:
            try:
                self.trade.trade.create_limit_order(self.trade_symbol, 'sell', str(self.size), str(self.price))
                self._logger.info(f'order for {self.trade_symbol}, amount: {self.size} in price: {self.price} created successfully')
                break
            except Exception:
                self._logger.exception("""order could not be created""", exc_info=True)
                pass
                
        

if __name__ == '__main__':
    time_based_sell = TimeBasedSell()
    time_based_sell.run()

#TODO: 
