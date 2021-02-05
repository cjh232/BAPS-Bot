import schedule



def set_reoccuring_task(callable, flair, limit):

    print(f'Scheduled Task:\n\nFlair: {flair}\nLimit: {limit}\n\n')

    schedule.every().day.at("9:00").do(callable, flair, limit = limit)
    schedule.every().day.at("21:00").do(callable, flair, limit = limit)


    while True:
        schedule.run_pending()
