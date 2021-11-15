import logging
import time
import datetime
import random
from kucoin.client import Trade
from market_kucoin import MarketAPI

class TradeAPI():
    def __init__(self, api_data, api_name, mode='sandbox'):
        
        # API loading
        self.api = api_data[mode][api_name]
        self.api_name = api_name

        self.mode = mode
        self.is_sandbox = False
        if self.mode == 'sandbox':
            self.is_sandbox = True

        self.key = self.api['key']
        self.secret = self.api['secret']
        self.passphrase = self.api['passphrase']
        self.restriction = self.api['restriction']

        # logger loading
        self.logger = logging.getLogger(__name__)
        self.trade = self._make_trade()
        self.market = MarketAPI(self.mode)

    def _make_trade(self):
        while True:
            try:
                trade = Trade(self.key, self.secret, self.passphrase, is_sandbox=self.is_sandbox)
                self.logger.info(f'trade object for {self.api_name} in {self.mode} mode created successfully...')
                break
            except Exception:
                self.logger.exception("""trade object could not be created successfully. sleeping for few seconds and try later""", exc_info=False)
                sleep_time = random.uniform(8, 12)
                time.sleep(sleep_time)
                pass


        return trade

    def auto_limit_stop_order(self, token_to_trade, token_live_data, balance, prev_order_data):
        live_price = float(token_live_data['price'])
        stop_target = ((1 + token_to_trade['avg_stop_percentage'])*token_to_trade['avg'])

        prev_order_ids = []
        prev_stop_price = []

        # loading previous stop order id and live price
        for order in prev_order_data:
            prev_order_ids.append(order['id'])
            prev_stop_price.append(float(order['stopPrice']))
        if prev_stop_price:
            prev_live_price = (prev_stop_price[0]*(1 + token_to_trade['live_stop_percentage']))*1.015
        else:
            prev_live_price = 0


        if (live_price > stop_target) and (live_price > prev_live_price):
            self.logger.warning('live price hitted the target...')

            # calculating new order details
            stop_price = float("{0:.4f}".format(live_price * (1 - token_to_trade['live_stop_percentage'])))
            order_price = float("{0:.4f}".format(stop_price * (1 - token_to_trade['stop_limit_percentage'])))
            size = float("{0:.4f}".format(token_to_trade['total_purchase'] / order_price))

            if size <= balance:
                # cancelling previous stop order
                if prev_order_ids:
                    for id in prev_order_ids:
                        while True:
                            try:
                                self.trade.cancel_stop_order(id)
                                self.logger.info(f"order {id} cancelled")
                                break
                            except Exception:
                                self.logger.exception("""previous order could not be cancelled successfully. sleeping for few seconds and try later""", exc_info=False)
                                sleep_time = random.uniform(8, 12)
                                time.sleep(sleep_time)
                                pass
                
                # placing new stop order
                size, order_price = self.data_adjustment(token_to_trade['trade_symbol'], size, order_price)
                self.logger.info(f"""order with following data will be excecuted:
                                    \nlive_price:{float("{0:.4f}".format(live_price))}, stop_price: {stop_price}, order_price: {order_price}, size: {size}""")
                
                try:
                    self.trade.create_limit_stop_order(token_to_trade['trade_symbol'], 'sell', size, order_price, stop_price)
                    self.logger.info(f"stop order for symbol {token_to_trade['trade_symbol']} created successfully...")
                except Exception:
                    self.logger.exception('new order could not be placed successfully...', exc_info=True)
                    pass

            else:
                self.logger.info(f"""balance is not sufficient to place the order for {token_to_trade['trade_symbol']}:
                                    \nbalance:{balance}, stop_price: {stop_price}, order_price: {order_price}, size: {size}""")

        else:
            self.logger.info(f"price not triggered for {token_to_trade['trade_symbol']}")


    def get_token_stop_order_data(self, symbol, side):
        while True:
            try:
                order_data = self.trade.get_all_stop_order_details(**{'symbol': symbol, 'side': side})['items']
                break
            except Exception:
                self.logger.exception("""order_data object could not be created successfully. sleeping for few seconds and try later""", exc_info=False)
                sleep_time = random.uniform(8, 12)
                time.sleep(sleep_time)
                pass
        

        return order_data


    def check_prev_filled_date(self, symbol, side, now):
        while True:
            try:
                prev_filled_data = self.trade.get_fill_list('TRADE', **{'symbol': symbol, 'side': side})['items']

                if prev_filled_data:
                    prev_filled_date = prev_filled_data[0]['createdAt']/1000
                    prev_filled_date = datetime.datetime.fromtimestamp(prev_filled_date).date()
                else:
                    prev_filled_date = now+datetime.timedelta(days=-10)

                if now <= prev_filled_date+datetime.timedelta(days=7):
                    self.logger.warning(f"""a {side} filled order found within 7 days of now on {prev_filled_date}, hence {symbol} will be skipped...""")
                    return False
                return True
                break
            except Exception:
                self.logger.exception("""prev_filled_date could not be checked successfully. sleeping for few seconds and try later""", exc_info=False)
                sleep_time = random.uniform(8, 12)
                time.sleep(sleep_time)
                pass

    def data_adjustment(self, symbol, size, price):
        while True:
            try:
                price_base_data = self.market.get_symbol_data(symbol)
                break
            except Exception:
                self.logger.exception("""symbol_data object could not be loaded successfully. sleeping for few seconds and try later""", exc_info=False)
                sleep_time = random.uniform(8, 12)
                time.sleep(sleep_time)
                pass

        baseIncrement = float(price_base_data['baseIncrement'])
        priceIncrement = float(price_base_data['priceIncrement'])
        size = int(size/baseIncrement)*baseIncrement
        price = int(price/priceIncrement)*priceIncrement

        return size, price
