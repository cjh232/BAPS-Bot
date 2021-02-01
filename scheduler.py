import schedule 
import smtplib
from main import RedditSearch
import inquirer
import secrets


flairs = [
    'CPU',
    'GPU',
    'Monitor',
    'Bundle',
    'Cables',
    'Case',
    'Controller',
    'Cooler',
    'CPU',
    'Fan',
    'Flash Drive',
    'Furniture',
    'HDD',
    'Headphones',
    'Headset',
    'HTPC',
    'Keyboard',
    'Laptop'
    'Meta',
    'Mic',
    'Mod Post',
    'Motherboard',
    'Mouse',
    'Mouse Pad',
    'Networking',
    'OS',
    'Other',
    'Optical Drive',
    'Prebuilt',
    'Printer',
    'PSU',
    'RAM',
    'Speakers',
    'SSD - Sata',
    'SSD - M.2',
    'VR',
    'Webcam'
]


def set_reoccuring_task(callable, flair, limit):
    print(f'Scheduled Task:\n\nFlair: {flair}\nLimit: {limit}\n\n')
    schedule.every(10).seconds.do(reddit_search.execute_search, flair, limit = limit)


    while True:
        schedule.run_pending()



if __name__ == "__main__":

    questions = [
        inquirer.List('flair',
                    message = 'Please select a flair',
                    choices=flairs,
        ),
        inquirer.List('limit',
                    message = "Select a limit",
                    choices = [10, 20, 40, 100]        
        ),
        inquirer.List('timeline',
                    message = 'Do you want this to be a reoccuring task?',
                    choices=['Yes', 'No']
        )
    ]

    answers = inquirer.prompt(questions)

    reddit_search = RedditSearch(secrets.client_id,
                            secrets.client_secret,
                            secrets.username,
                            secrets.password,
                            secrets.user_agent
                    )

    product_flair = answers["flair"]
    reoccuring = answers["timeline"] == 'Yes'
    limit = answers["limit"]

    if not reoccuring:
        reddit_search.execute_search(product_flair, limit=limit)
    else:
        set_reoccuring_task(reddit_search.execute_search, product_flair, limit=limit)

