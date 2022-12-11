Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> """ A very dirty util to recursively reply to comments in a particular post by a
...     particular target author.
...     Runs in a loop every 360 seconds.  Reparses the entire comment tree each time
...     so this is very inefficient.  However, it works just fine.
...     Not parameterized, so you have to manually edit the code, but I can extend it
...     if you start using it frequently.
...     This script is not guaranteed to work.  I have modified it since I last tested
...     it, so it probably needs some tweaks.
...     Currently, it is set to auto downvote whoever your target is, and it will only
...     reply if the target has no other replies.  Also, if it finds a comment without
...     a reply by the target, it will definitely reply.
...     I wrote this because this one idiot I was talking to wanted to get the last word
...     in no matter what.  This basically made it impossible for him to get the last
...     word in.
...     Easy improvements would be to
...         1. provide a list of comments you want to auto reply with and randomly
...            pick one
...         2. allow upvotes or downvote selection
...         3. allow upvoting and downvoting without commenting
... """
... 
... import praw
... import time
... import random
... 
... from praw import Reddit
... 
... reddit: Reddit = praw.Reddit(client_id='client id comes from signing up for api',
...                              client_secret='client secret comes from signing up for api',
...                              password='put your reddit password here',
...                              user_agent='chatbot by /u/your_username_here',
...                              username='put your username here')
... 
... 
... def reply_if_is_target_author(comment, target_author: str, reply: str):
...     """ Recursive function which finds comments by the target_author, downvotes them and
...         submits your reply.
...     """

    if comment.author == target_author:
        if comment.likes is None:
            print("downvoting comment")
            comment.downvote()

    if comment.author == target_author and len(comment.replies._comments) == 0:
        comment.reply(reply)
        print("found target - commenting")

    elif len(comment.replies._comments) == 0:
        # if this comment is mine or someone else not 'target_author'
        print(f"current child author '{comment.author}', no child comments found")

    else:
        for c in comment.replies:
            reply_if_is_target_author(c, target_author, reply)


def search(submission_id: str, follow_thread_id: str, target_author: str, reply: str):
    """ Searches for the start of the recursion.  This happens every 360 seconds, so if you
        let this run it will continue to reply.
    """

    while True:
        print("starting iteration")
        submission = reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if comment.id == follow_thread_id:
                reply_if_is_target_author(comment, target_author, reply)

        print("iteration complete")
        time.sleep(300)


if __name__ == '__main__':
    # enter the post id, thread id, target_author, and your auto reply message into
    # the following fields
    
    # the main post
    post_id = 'put_your_post_id_here'

    # a particular comment thread.  I 'think' you could use the post ID here,
    # and it might scan the entire post (untested), but I tried it by running
    # it on only a specific top level comment, and it worked fine.
    comment_thread_id = "put_your_comment_thread_id"

    target_author = "your_target_author_name"

    replies = ["put", "your", "random", "reply", "items", "in", "here", "use as many", "as you want"]

    random_reply = random.choice(replies)
    
