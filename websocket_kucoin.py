import logging
import asyncio
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient

class WebsocketAPI():
    def __init__(self):
        
        
        # logger loading
        self.logger = logging.getLogger(__name__)

        self.loop = self.get_loop()
    
    def get_loop(self):
        loop = asyncio.get_event_loop()

        return loop


    async def _get_data(self, token_pair, function=None):

        async def deal_msg(msg):
            if msg['topic'] == f'/market/ticker:{token_pair}':
                if function:
                    function(msg)
                    self.logger.info(f'{msg}')
                else:
                    print(msg)
                self.loop.close()
        
        client = WsToken()
        ws_client = await KucoinWsClient.create(self.loop, client, deal_msg, private=False)
        
        await ws_client.subscribe(f'/market/ticker:{token_pair}')

        while True:
            await asyncio.sleep(8, loop=self.loop)
            break


    def run(self, token_pair, function=None):
        ws_client = self._get_data(token_pair, function)
        self.loop.run_until_complete(ws_client)









