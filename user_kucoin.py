import logging
import time
import random

from kucoin.client import User

class UserAPI():
    def __init__(self, api_data, api_name, mode='sandbox'):
        
        # API loading
        self.data = api_data
        self.api = self.data[mode][api_name]
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
        self.user = self._make_user()

    def _make_user(self):
        while True:
            try:
                user = User(self.key, self.secret, self.passphrase, is_sandbox=self.is_sandbox, )
                self.logger.info(f'{self.api_name} user in {self.mode} mode created successfully...')
                break
            except Exception:
                self.logger.exception("""user object could not be created successfully. sleeping for few time and try later""", exc_info=True)
                sleep_time = random.uniform(8, 12)
                time.sleep(sleep_time)
                pass


        return user

    def get_ledger(self):
        while True:
            try:
                lst = self.user.get_account_list()
                ledger = []
                for token in lst:
                    if token['balance'] == '0':
                        continue
                    ledger.append(token)
                self.logger.info(f'ledger for {self.api_name} loaded successfully...')
                break
            except Exception:
                self.logger.exception("""ledger object could not be created successfully. sleeping for few time and try later""", exc_info=True)
                sleep_time = random.uniform(8, 12)
                time.sleep(sleep_time)
                pass

        return ledger


    def get_token_balance(self, token_name):
        ledger = self.get_ledger()
        token_list = []
        balance = 0
        for token in ledger:
            if (token['currency'] == token_name) and (token['type'] == 'trade'):
                token_list.append(token)
                balance += float(token['balance'])

        self.logger.info(f'{token_name} balance for {self.api_name} loaded successfully...')

        return token_list, balance


# TODO: