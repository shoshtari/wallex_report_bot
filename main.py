from typing import List
import time
from exceptions import NotFoundError
from wallex import WallexHandler
from price_repo import PriceRepo
from dtos import SymbolStat

import configs
import sqlite3

db_conn = sqlite3.connect(configs.SQLITE_CONN_STR)

wallex_handler = WallexHandler(configs.WALLEX_AUTH_TOKEN)
price_repo = PriceRepo(db_conn)


def get_new_stats(symbol_stats: List[SymbolStat]):
    ans = []
    for stat in symbol_stats:
        last_stat = None
        try:
            last_stat = price_repo.get_last_stat(stat.name)
        except NotFoundError:
            pass

        if (
            last_stat is not None
            and last_stat.buy_price == stat.buy_price
            and last_stat.sell_price == stat.sell_price
        ):
            continue

        ans.append(stat)
    return ans


def update_stats():
    symbol_stats = wallex_handler.get_market_prices()
    new_stats = get_new_stats(symbol_stats)
    if not new_stats:
        return
    print(len(new_stats), "new stat")
    price_repo.insert_many(new_stats)

while True:
    update_stats()

