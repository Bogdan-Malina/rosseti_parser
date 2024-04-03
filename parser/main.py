import datetime
import time

import schedule
import sqlalchemy

import create_map
import filter
import main_parser
from database import engine


def job():
    try:
        with engine.connect() as conn:
            print("Job запущен")
            main_parser.main(conn)
            print("Парсер отработал")
            filter.date_filter(datetime.datetime.now(), conn)
            print("Фильтр отработал")
            create_map.create_map(conn)
            print("Карта создана")
    except sqlalchemy.exc.OperationalError as e:
        print("Не удалось подключиться к базе данных")
        time.sleep(10)
        job()


schedule.every(3).minutes.do(job)


if __name__ == "__main__":
    job()
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
