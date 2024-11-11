import json
import sqlite3
import time
from typing import List

import configs
from dtos import SymbolStat
from exceptions import NotFoundError
from price_repo import PriceRepo
from telegram_client import TelegramClient
from wallex import WallexHandler

db_conn = sqlite3.connect(configs.SQLITE_CONN_STR)

wallex_handler = WallexHandler(configs.WALLEX_AUTH_TOKEN)
price_repo = PriceRepo(db_conn)

telegram_client = TelegramClient(configs.TELEGRAM_BOT_TOKEN, configs.TELEGRAM_CHAT_ID)


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
    price_repo.insert_many(new_stats)


async def send_trade_bot_report():
    bots = wallex_handler.get_running_bots()
    text = ""
    for bot in bots:
        text += (
            json.dumps(
                {
                    "Strategy": bot.strategy,
                    "Change Percent": float(bot.change_percent),
                    "Change Value": float(
                        bot.current_tmn_value - bot.original_tmn_value
                    )
                    // 1e4
                    / 1e2,
                }
            )
            + "\n"
        )
    text = text.strip()
    await telegram_client.send_message(text)


send_trade_bot_report()
print("DONE")
