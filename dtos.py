from dataclasses import dataclass
from typing import List
from datetime import datetime
from decimal import Decimal


@dataclass
class SymbolStat:
    name: str
    date: datetime
    market: str
    sell_price: Decimal
    buy_price: Decimal


@dataclass
class TradeBot:
    bot_id: str
    bot_handler: str
    strategy: str
    symbols: List[str]
    original_tmn_value: Decimal
    current_tmn_value: Decimal

    @property
    def change_percent(self):
        return (1 - (self.current_tmn_value / self.original_tmn_value)) * 100
