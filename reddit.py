import praw
from types import SimpleNamespace
import secrets
from datetime import datetime
from emailer import Emailer

class RedditSearch:

    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.user_agent = user_agent

        self.reddit = self.login()
        self.subreddit = self.reddit.subreddit('buildapcsales')   

    def login(self):
        return praw.Reddit(client_id = self.client_id, 
                        client_secret = self.client_secret,
                        username = self.username,
                        password = self.password,
                        user_agent = self.user_agent
                        )


    def execute_search(self, product_flair, limit):

        res = self.subreddit.new(limit = limit)

        emailer = Emailer(secrets.sender, secrets.receiver, secrets.user, secrets.password)

        for submission in res:
            if submission.link_flair_text.lower() == product_flair.lower() and not submission.stickied:
                match_object = SimpleNamespace()
                match_object.title = submission.title
                match_object.url = submission.url
                match_object.created_utc = submission.created_utc
                emailer.appendMessage(match_object)

        if emailer.getQueueLength() > 0:
            emailer.sendEmail()
        else:
            print("No submission were found...")


    def openLinks(self, submission_list):

        print("Emailing submissions...")

        for submission in submission_list:
            time_posted = datetime.fromtimestamp(submission.created_utc)
            print(f'{submission.title}\nLink: {submission.url}\nPosted At: {time_posted}\n')


