from sqlite3 import Connection
from exceptions import NotFoundError
from decimal import Decimal
from datetime import datetime

from dtos import SymbolStat
import sqlite3


class PriceRepo:
    def __init__(self, conn: Connection):
        self.__connection = conn
        self.__migrate()

    def __migrate(self):
        cur = self.__connection.cursor()
        cur.execute(
            """ 
            CREATE TABLE IF NOT EXISTS prices(
                symbol_name VARCHAR(10) NOT NULL,
                market VARCHAR(20) NOT NULL, 
                date TIMESTAMP NOT NULL,
                buy_price TEXT NOT NULL,
                sell_price TEXT NOT NULL
            )
        """
        )

    def insert_many(self, symbol_stats: SymbolStat):
        if not symbol_stats:
            raise ValueError("stats is an empty list")

        cur = self.__connection.cursor()
        count = len(symbol_stats)
        place_holders = ",".join(["(?, ?, ?, ?, ?)"] * count)
        args = []
        for i in symbol_stats:
            args.extend(
                [
                    i.name,
                    i.market,
                    i.date.isoformat(),
                    str(i.buy_price),
                    str(i.sell_price),
                ]
            )

        cur.execute(
            f"""
            INSERT INTO prices(symbol_name, market, date, buy_price, sell_price)
                VALUES {place_holders}
        """,
            args,
        )
        self.__connection.commit()

    def get_last_stat(self, symbol_name: str):
        cur = self.__connection.cursor()
        cur.execute(
            """
            SELECT symbol_name, market, date, buy_price, sell_price FROM prices
                WHERE symbol_name = ? 
                    ORDER BY date DESC LIMIT 1
        """,
            (symbol_name,),
        )
        res = cur.fetchone()
        if res is None:
            raise NotFoundError()

        ans = SymbolStat(
            name=res[0],
            market=res[1],
            date=datetime.fromisoformat(res[2]),
            buy_price=Decimal(res[3]),
            sell_price=Decimal(res[4]),
        )
        return ans
