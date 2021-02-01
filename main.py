import praw
from types import SimpleNamespace
import webbrowser
import secrets

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

        matching_submissions = []

        for submission in res:
            if submission.link_flair_text.lower() == product_flair.lower() and not submission.stickied:
                match_object = SimpleNamespace()
                match_object.title = submission.title
                match_object.url = submission.url
                matching_submissions.append(match_object)

        if len(matching_submissions) > 0:
            self.openLinks(matching_submissions)
        else:
            print("No submission were found...")


    def openLinks(self, submission_list):

        print("Opening submission links...")

        chrome_path = "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"

        webbrowser.register('chrome',
            None,
            webbrowser.BackgroundBrowser(chrome_path))
        
        browser = webbrowser.get('chrome')


        for submission in submission_list:
                print(submission.title)
                browser.open_new_tab(submission.url)



reddit_search = RedditSearch(secrets.client_id,
                            secrets.client_secret,
                            secrets.username,
                            secrets.password,
                            secrets.user_agent
                    )

print("Enter product flair: ")
product_flair = input()


reddit_search.execute_search(product_flair, 30)

