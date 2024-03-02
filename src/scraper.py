import praw
import time
import datetime
import json
reddit = praw.Reddit(client_id='AHfet6Qwq09Yuxd5eib_wQ',
                     client_secret='ifgFCgxVZpMhKRD426jWJ_WEQLb8FA',
                     user_agent='windows:UBCStudentSimulator:v0.0.1 (by u/Frosty_Can_2796)')

##hi 


class SubredditLatest(object):
    """Get all available submissions within a subreddit newer than x."""

    def __init__(self, subreddit, dt):

        # master list of all available submissions
        self.total_list = []

        # subreddit must be a string of the subreddit name (e.g., "soccer")
        self.subreddit = subreddit

        # dt must be a utc datetime object
        self.dt = dt

    def __call__(self):
        self.get_submissions()
        return self.total_list

    def get_submissions(self, paginate=False):
        """Get limit of subreddit submissions."""
        limit = 100  # Reddit maximum limit

        if paginate is True:
            try:
                # get limit of items past the last item in the total list
                submissions = reddit.subreddit(self.subreddit).new(limit=limit, params={
                    "after": self.total_list[-1].fullname})
            except IndexError:
                print("param error")
                return
        else:
            submissions = reddit.subreddit(self.subreddit).new(limit=limit)

        submissions_list = [
            # iterate through the submissions generator object
            x for x in submissions
            # add item if item.created_utc is newer than an hour ago
            if datetime.datetime.fromtimestamp(x.created_utc) >= self.dt
        ]
        self.total_list += submissions_list

        # if you've hit the limit, recursively run this function again to get
        # all of the available items
        if len(submissions_list) == limit:
            self.get_submissions(paginate=True)
        else:
            return

#driver code

date = datetime.datetime(2023, 9, 1)

submissions = SubredditLatest("ubc",date)()
data = []

for submission in submissions:
    # Create a dictionary for the submission
    submission_dict = {k: str(getattr(submission, k)) for k in ["title","author", "author_flair_text", "likes", "ups", "downs", "upvote_ratio", "selftext"]}

    # Get the comments
    submission.comments.replace_more(limit=None)
    comments = submission.comments.list()

    # Create a list of dictionaries for the comments
    # will do recursive comment append in the future TODO
    comments_list = [comment.body for comment in comments]

    # Add the comments to the submission dictionary
    submission_dict["comments"] = comments_list

    # Add the submission dictionary to the data list
    data.append(submission_dict)

# Write the data to a JSON file
with open('./data/reddit_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


