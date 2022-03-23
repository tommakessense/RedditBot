from json import loads, dumps
from random import randint
import stanza
import praw
import re
import os

from stanza import Pipeline

def log_into_reddit():
    reddit = praw.Reddit('bot1')
    print(reddit.user.me())
    return reddit

def get_posts_replied_to():
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
    return posts_replied_to

# variable
LOCATIONS = [
    " Sales of Hitler's political autobiography \"Mein Kampf\"sometimes referred to as the bible of the Nazi Party, made him a millionaire. ",
    "Hitler had dreams of playing a musical instrument. He had short but unsuccessful lessons in piano and violin and also dabbled in the flute and harmonica. In the end, he settled for whistling, which he did frequently.",
    "Though he shunned meat, Hitler was a voracious ‘sweet tooth’, consuming large amounts of cake, pastries, chocolate and sugar. He sometimes took as many as five teaspoons of sugar in his tea.",
    "When the regime came into power in 1933, they passed a comprehensive set of laws for animal protection. When all of these were in place, Hitler said something about animal cruelty. With the new Reich, there will be no grounds for any form of animal abuse and cruelty.",
    "It’s already a known fact that during Hitler’s reign, their main objective was to free the world of Jews. However, Hilter unknowingly had a Jewish chauffeur. Emil Maurice was also his friend and personal chauffeur. When it got known to many, Heinrich Himmler was ready to target Maurice for expulsion. Hitler came to the rescue and made an exception for him and his brothers. He called them “honorary Aryans”.",
    "In a pre-cursor to modern stances and laws in this area, the Nazi party were the first people to ban smoking. Nazi doctors were the first to establish a link between smoking and lung cancer which meant that a fierce anti-smoking campaign began under Hitler. The Nazi leadership strongly condemned smoking and advised the general population to give it up.",
    "During the Second World War, German doctors came up with a methamphetamine based experimental drug to increase soldier’s performance. This was very successful in trials when tested and made the troops super tough. It was found that they could march 55 miles without any tiredness which is pretty amazing. The plan was to roll it out to all soldiers serving in the war but the German’s lost before it could be put into place."]

ANALYTICS_JSON = "posts_analytics.json"


def get_posts_analytics():
    if not os.path.isfile(ANALYTICS_JSON):
        posts_analytics = []

    # If we have run the code before, load the list of posts we have replied to
    else:
        # Read the file into a list and remove any empty values
        with open(ANALYTICS_JSON, "r") as f:
            posts_analytics = loads(f.read())
    return posts_analytics

def initiate_nlp() -> Pipeline:
    stanza.download('en')
    nlp_pipe = stanza.Pipeline('en', processors="tokenize,pos")
    return nlp_pipe

def fetch_reddit_posts(selected_subreddit: str, limit: int) -> list:
    subreddit = reddit.subreddit(selected_subreddit)
    return subreddit.hot(limit=limit)

def process_post(post, nlp_pipe: Pipeline):
    doc = nlp_pipe(post.title)
    keywords = get_keywords_from_post(doc.sentences)
    print(keywords)
    print(doc.entities)
    return post.id, post.title, keywords

def filter_analytics(posts, posts_analytics):
    post_ids = [post_id for post_id, _, _ in posts_analytics]
    filtered_posts = []
    for post in posts:
        if post.id in post_ids:
            continue
        filtered_posts.append(post)
    return filtered_posts

def get_keywords_from_post(sentences: list):
    keywords = []
    for sentence in sentences:
        for word in sentence.words:
            if word.upos not in ['NOUN', 'VERB', 'NUM', 'PROPN']:
                continue
            keywords.append(word.text)
    return keywords


def filter_posts(posts, posts_replied_to):
    filtered_posts = []
    for post in posts:
        if post.id in posts_replied_to:
            continue
        if not re.search("(nazi|hitler|hilter|german)", post.title, re.IGNORECASE):
            continue
        filtered_posts.append(post)
    return filtered_posts

def reply_to_post(post):
    # Reply to the post
    randomnumber = randint(0, len(LOCATIONS))
    post.reply(f"Did you know that: {LOCATIONS[randomnumber]}")
    print(f"Bot replying to: {post.title} https://www.reddit.com/r/fakehistoryporn/comments/{post.id}")

def store_line(f, line):
    f.write(line + "\n")

if __name__ == '__main__':
    # log into reddit
    reddit = log_into_reddit()
    # check posts replied to
    posts_replied_to = get_posts_replied_to()
    # initiate nlp
    nlp_pipe = initiate_nlp()
    # create posts_analytics
    posts_analytics = get_posts_analytics()
    # fetch reddit posts
    posts = fetch_reddit_posts("fakehistoryporn", 10)
    analytics_filtered = filter_analytics(posts, posts_analytics)
    # read submission titles
    for post in analytics_filtered:
        nlp_data = process_post(post, nlp_pipe)
        posts_analytics.append(nlp_data)
    # store nlp doc in posts_analytics
    with open(ANALYTICS_JSON, "w") as f:
        f.write(dumps(posts_analytics))
    # filter for keywords
    filtered_posts = filter_posts(posts, posts_replied_to)
    # respond to filtered posts
    with open("posts_replied_to.txt", "a") as f:
        for post in filtered_posts:
            reply_to_post(post)
            # store post_id in posts_replied_to
            store_line(f, post.id)