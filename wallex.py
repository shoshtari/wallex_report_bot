import logging
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

import requests
from retry import retry

import configs
import dtos

logger = logging.getLogger(__name__)


class WallexHandler:
    IGNORE_CURRENCIES = ("XTMN",)

    def __init__(self, auth_token: str):
        self.__base_url = "https://api.wallex.ir/v1"
        self.__auth = auth_token

    @retry(tries=3)
    def __send_request_to_wallex(
        self, url: str, include_auth: bool = False, method: str = "GET"
    ):
        headers = {}
        if include_auth:
            headers["Authorization"] = self.__auth

        res = requests.request(
            method, url, headers=headers, timeout=configs.REQUEST_TIMEOUT
        )
        res.raise_for_status()

        assert res.json()["success"]

        return res.json()["result"]

    def get_market_prices(self):
        url = f"{self.__base_url}/markets"
        res = self.__send_request_to_wallex(url)["symbols"]

        symbols = list(res.keys())
        ans = []
        for symbol in symbols:
            if symbol in self.IGNORE_CURRENCIES:
                continue
            symbol_data = res[symbol]["stats"]
            if "-" in (symbol_data["askPrice"], symbol_data["bidPrice"]):
                logger.warning(f"ignoring symbol {symbol} with '-' as a price")
                continue
            ans.append(
                dtos.SymbolStat(
                    name=symbol,
                    date=datetime.now(),
                    sell_price=Decimal(symbol_data["askPrice"]),
                    buy_price=Decimal(symbol_data["bidPrice"]),
                    market="wallex",
                )
            )

        return ans

    def get_running_bots(self):
        url = f"{self.__base_url}/passive-trade/runningBots"
        res = self.__send_request_to_wallex(url, include_auth=True)

        ans = []
        for bot_dict in res["bots"]:
            ans.append(
                dtos.TradeBot(
                    bot_id=bot_dict["ID"],
                    bot_handler="wallex",
                    strategy=bot_dict["strategy"]["ENName"],
                    symbols=bot_dict["symbols"],
                    original_tmn_value=Decimal(
                        bot_dict["initialInventorySnapshot"]["totalWorth"]["TMN"]
                    ),
                    current_tmn_value=Decimal(
                        bot_dict["totalWorth"]["aggregated"]["TMN"]
                    ),
                )
            )
        return ans

    def get_global_prices(self):
        url = f"{self.__base_url}/currencies/stats"
        # TODO: from here it needs development
        res = requests.get(url)
        res.raise_for_status()
        res = res.json()["result"]["symbols"]
        symbols = list(res.keys())
        ans: List[Symbol] = []
        for symbol in symbols:
            symbol_data = res[symbol]["stats"]
            ans.append(
                SymbolStat(
                    name=symbol,
                    date=datetime.now(),
                    sell_price=Decimal(symbol_data["askPrice"]),
                    buy_price=Decimal(symbol_data["bidPrice"]),
                    market="wallex",
                )
            )

        return ans
