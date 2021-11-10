import random
import time
import datetime
import logging

from kucoin.client import Market

class MarketAPI():
    def __init__(self, mode='sandbox'):
        
        # API loading
        self.mode = mode

        # logger loading
        self.logger = logging.getLogger(__name__)

        # client loading
        self.market = self._make_market()


    def _make_market(self):
        if self.mode == 'sandbox':
            while True:
                try:
                    market = Market(url='https://openapi-sandbox.kucoin.com')
                    market = Market(is_sandbox=True)
                    break
                except Exception:
                    self.logger.exception("""market object could not be checked successfully. sleeping for few time and try later""", exc_info=True)
                    sleep_time = random.uniform(8, 12)
                    time.sleep(sleep_time)
                    pass

        elif self.mode == 'main':
            while True:
                try:
                    market = Market(url='https://api.kucoin.com')
                    break
                except Exception:
                    self.logger.exception("""market object could not be checked successfully. sleeping for few time and try later""", exc_info=True)
                    sleep_time = random.uniform(8, 12)
                    time.sleep(sleep_time)
                    pass

        return market
    
    def make_klines(self, symbol, kline_type, start_time=0, end_time=0):
        '''
        Parameters
        ----------
        kline_type: str
            Type of candlestick patterns: 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
        
        start_time: str
            Start time of the candle cycle in format '2021/01/01 13:44'
        end_time: str
            End time of the candle cycle in format '2021/01/02 13:44'
        '''
        if start_time:
            start = datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M")
            start_timestamp = int(datetime.datetime.timestamp(start))
        else:
            start_timestamp = 0
        if end_time:
            end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M")
            end_timestamp = int(datetime.datetime.timestamp(end))
        else:
            end_timestamp = 0
        
        assert start_timestamp <= end_timestamp

        while True:
            try:
                klines = self.market.get_kline(symbol, kline_type, **{'startAt': start_timestamp, 'endAt': end_timestamp})
                break
            except Exception:
                self.logger.exception("""kline object could not be checked successfully. sleeping for few time and try later""", exc_info=True)
                sleep_time = random.uniform(8, 12)
                time.sleep(sleep_time)
                pass

        return klines
