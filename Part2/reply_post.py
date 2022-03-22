from random import randint

import praw
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
locations = [
    " Sales of Hitler's political autobiography \"Mein Kampf\"sometimes referred to as the bible of the Nazi Party, made him a millionaire. ",
    "Hitler had dreams of playing a musical instrument. He had short but unsuccessful lessons in piano and violin and also dabbled in the flute and harmonica. In the end, he settled for whistling, which he did frequently.",
    "Though he shunned meat, Hitler was a voracious ‘sweet tooth’, consuming large amounts of cake, pastries, chocolate and sugar. He sometimes took as many as five teaspoons of sugar in his tea.",
    "When the regime came into power in 1933, they passed a comprehensive set of laws for animal protection. When all of these were in place, Hitler said something about animal cruelty. With the new Reich, there will be no grounds for any form of animal abuse and cruelty.",
    "It’s already a known fact that during Hitler’s reign, their main objective was to free the world of Jews. However, Hilter unknowingly had a Jewish chauffeur. Emil Maurice was also his friend and personal chauffeur. When it got known to many, Heinrich Himmler was ready to target Maurice for expulsion. Hitler came to the rescue and made an exception for him and his brothers. He called them “honorary Aryans”.",
    "In a pre-cursor to modern stances and laws in this area, the Nazi party were the first people to ban smoking. Nazi doctors were the first to establish a link between smoking and lung cancer which meant that a fierce anti-smoking campaign began under Hitler. The Nazi leadership strongly condemned smoking and advised the general population to give it up.",
    "During the Second World War, German doctors came up with a methamphetamine based experimental drug to increase soldier’s performance. This was very successful in trials when tested and made the troops super tough. It was found that they could march 55 miles without any tiredness which is pretty amazing. The plan was to roll it out to all soldiers serving in the war but the German’s lost before it could be put into place."]
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
            submission.reply(f"Did you know that: {locations[randomnumber]}")
            print(f"Bot replying to: {submission.title} https://www.reddit.com/r/fakehistoryporn/comments/{submission.id}")

            # Store the current id into our list
            posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
