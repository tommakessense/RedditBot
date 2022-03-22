from random import randint

import praw
import pdb
import re
import os


# Create the Reddit instance
reddit = praw.Reddit('bot1')

print(reddit.user.me())


# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))
# variable
locations = [" Sales of Hitler's political autobiography \"Mein Kampf\"sometimes referred to as the bible of the Nazi Party, made him a millionaire. ",
             "Hitler had dreams of playing a musical instrument. He had short but unsuccessful lessons in piano and violin and also dabbled in the flute and harmonica. In the end, he settled for whistling, which he did frequently.",
             "Though he shunned meat, Hitler was a voracious ‘sweet tooth’, consuming large amounts of cake, pastries, chocolate and sugar. He sometimes took as many as five teaspoons of sugar in his tea.", ]
# Get the top 5 values from our subreddit
subreddit = reddit.subreddit('fakehistoryporn')
for submission in subreddit.hot(limit=10):
    print(submission.title)

   # If we haven't replied to this post before
    if submission.id not in posts_replied_to:

        # Do a case insensitive search
       if re.search("(nazi|hitler|hilter|german)", submission.title, re.IGNORECASE):
            # Reply to the post
            randomnumber = randint(0, len(locations))
            submission.reply("%s" % "Did you know that:", locations[randomnumber])
            print("Bot replying to : ", submission.title)

            # Store the current id into our list
            posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")