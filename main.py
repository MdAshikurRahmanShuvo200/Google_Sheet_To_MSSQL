from scheduler import Scheduler


def main():

    # 60 = 1 Minute
    scheduler = Scheduler(interval=60)

    scheduler.start()


if __name__ == "__main__":

    main()