from reddit import RedditSearch
import inquirer
import secrets
import scheduler

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
    'Laptop',
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
                    message = 'Do you want this to be a daily task?',
                    choices=['Yes', 'No']
        )
    ]

    answers = inquirer.prompt(questions)

    reddit = RedditSearch(secrets.client_id,
                            secrets.client_secret,
                            secrets.reddit_username,
                            secrets.reddit_password,
                            secrets.user_agent
                    )

    product_flair = answers["flair"]
    reoccuring = answers["timeline"] == 'Yes'
    limit = answers["limit"]

    if not reoccuring:
        reddit.execute_search(product_flair, limit=limit)
    else:
        scheduler.set_reoccuring_task(reddit.execute_search, product_flair, limit=limit)