import datetime
import time
import schedule
from parser import create_map, filter, main_parser


def job():
    try:
        main_parser.main()
        filter.date_filter(datetime.datetime.now())
        create_map.create_map()
    except Exception as e:
        print(e)


schedule.every(3).minutes.do(job)


if __name__ == "__main__":
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)
