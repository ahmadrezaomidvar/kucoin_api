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

class auto_sell:
    def __init__(self):
        '''
        auto_sell pipeline
        '''

        # configuration loading
        config_path = str(Path(__file__).resolve().parents[0].joinpath('configs', 'config.yaml'))
        self.config = Config(config_path = config_path).config
        self.api_data_path = self.config['api_data_path']
        self.api_name = self.config['api_name']
        self.mode = self.config['mode']
        self.tokens_path = self.config['tokens_path']
        self.target_date = datetime.datetime.fromisoformat(self.config['target_date']).date()

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

    # tokens data loading
    def get_tokens(self):
        with open(self.tokens_path) as f:
            tokens = json.load(f)

        return tokens[self.api_name]

    # tokens meta loading
    def get_all_tokens_meta(self):
        tokens = self.get_tokens()
        tokens_meta = {}
        for token in tokens.keys():
            if tokens[token]['flag']:
                meta_data = get_token_meta(tokens[token])
                tokens_meta[token] = meta_data
        
        return tokens_meta


    def run(self):

        now = datetime.datetime.now().date()

        while now <= self.target_date:
            tokens_meta = self.get_all_tokens_meta()
            for token, data in tokens_meta.items():
                token_to_trade = data
                self._logger.info(f"investigating {token_to_trade['trade_symbol']}...")
                
                if not self.trade.check_prev_filled_date(token_to_trade['trade_symbol'], 'sell', now):                          # check if previous stop/limit order is filled
                    continue

                _, balance = self.user.get_token_balance(token)
                prev_order_data = self.trade.get_token_stop_order_data(token_to_trade['trade_symbol'], 'sell')                  # check active stop order data
                self._logger.info(f"active stop order data for {token_to_trade['trade_symbol']}: \n{prev_order_data}")

                WebsocketAPI().run(token_to_trade['trade_symbol'], save_websocket_data)                                       # getting the live data
                token_live_data = load_websocket_data()

                self.trade.auto_limit_stop_order(token_to_trade, token_live_data, balance, prev_order_data)                     # checking and placing new stop order

                sleep_time = random.uniform(8, 12)
                self._logger.info(f'sleeping for {sleep_time: .2f} seconds\n')
                time.sleep(sleep_time)
                
            now = datetime.datetime.now().date()

        self._logger.info('target date triggered. closing the bot...')
                




if __name__ == '__main__':
    auto_sell = auto_sell()
    auto_sell.run()

#TODO: 
