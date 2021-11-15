# Kucoin API customizing and automation
This module is built using Kucoin API for customizing and automation of trades. This is an unofficial Python wrapper for the [Kucoin exchanges REST and Websocket API v2](https://docs.kucoin.com/). This is not in no way affiliated with Kucoin, use at your own risk.

## Quick Start
Register an account with [KuCoin](https://www.kucoin.com/ucenter/signup).

To test on the Sandbox with [KuCoin Sandbox](https://sandbox.kucoin.com/).
[Generate an API Key](https://www.kucoin.com/account/api) or [Generate an API Key in Sandbox](https://sandbox.kucoin.com/account/api) and enable it.

### To install

```bash
make install
```

### preparing api file

an api.json file shall be created in following format:
```json
{
    "sandbox": {
        " ": {                                  #api name
            "key": " ",                         #api key
            "secret": " ",                      #api secret
            "passphrase": " ",                  #api passphrase
            "restriction": "trade"
        }
    },
    "main": {
        " ": {                           
            "key": " ",                  
            "secret": " ",               
            "passphrase": " ",          
            "restriction": "trade"
        }
    }
}
```

### preparing tokens file

a tokens.json file shall be created in following format:
```json
{
    " ": {                                      #api name
        "KCS": {                                # token name
            "flag": 1,                          # flag if automatic checking perform
            "sell_stra": "tp",                  # type of selling strategy. 'tp'= take profit
            "purchase": {                       # purchase details  
                "100": 10,                          
                "86": 11
            },
            "target_percentage": 0.8,           # N/A for this version 
            "avg_stop_percentage": 0.25,        # target percentage to perform checking start
            "live_stop_percentage": 0.10,       # percentage to place stop below live price
            "stop_limit_percentage": 0.05,      # percentage to place order below stop price
            "base_curr": "USDT",                # base currency
            "trade_symbol": "KCS-USDT",         # trade symbol
            "custom_sell_USDT": 1000,           # N/A for this version
            "custom_sell_token": 44             # N/A for this version
        }
    }
}
```
### preparing config file

a config.yaml file shall be created in ./configs/ folder in following format:
```yaml
api_data_path: "path to api.json file"
tokens_path: "path to tokens.json file"
log_dir: "path to log directory"
api_name: ''                # 'api_name in kucoin/sandbox API'
mode: ''                    # 'sandbox' or 'main'
logging_level: 'INFO'
target_date: '2021-11-11'   # target date which the code will run continuously till that date
```

### To start auto selling

```bash
make auto_sell
```