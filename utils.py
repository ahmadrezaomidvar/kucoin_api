import json
from pathlib import Path

def get_token_meta(token_data):
    purchase = token_data['purchase']
    total_purchase = 0
    total_qty = 0
    for qty, price in purchase.items():
        total_qty += float(qty)
        total_purchase += (float(qty) * float(price))
    avg = total_purchase / total_qty
    target = avg * (1 + token_data['target_percentage'])
    if token_data['sell_stra'] == 'tp':
        sell_amount = total_purchase / target

    elif token_data['sell_stra'] == 'total':
        sell_amount = total_qty
    
    elif token_data['sell_stra'] == 'custom':
        if token_data['base_curr'] == 'USDT':
            sell_amount = token_data['custom_sell_USDT'] / target
        else:
            sell_amount = token_data['custom_sell_token']

    meta_data = {}
    meta_data['total_qty'] = float("{0:.4f}".format(total_qty))
    meta_data['avg'] = float("{0:.4f}".format(avg))
    meta_data['total_purchase'] = float("{0:.4f}".format(total_purchase))
    meta_data['sell_amount'] = float("{0:.4f}".format(sell_amount))
    meta_data['target'] = float("{0:.4f}".format(target))
    meta_data['trade_symbol'] = token_data['trade_symbol']
    meta_data['avg_stop_percentage'] = token_data['avg_stop_percentage']
    meta_data['live_stop_limit_percentage'] = token_data['live_stop_limit_percentage']
    


    return meta_data



def get_api_data(api_data_path):
    with open(api_data_path) as f:
        data = json.load(f)

    return data


def save_websocket_data(websocket_data):
    path = Path(__file__).resolve().parents[0].joinpath('websocket_data')
    path.mkdir(parents=True, exist_ok=True)
    with open(f'{path}/websocket.json', 'w') as file:
        json.dump(websocket_data, file)


def load_websocket_data():
    path = Path(__file__).resolve().parents[0].joinpath('websocket_data', 'websocket.json')
    with open(str(path)) as f:
        msg = json.load(f)
        data = msg['data']

    return data