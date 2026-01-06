import pandas as pd
import re
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji_detect
def create_dataframe(text):
    text_new = []
    text = text.split("\n")
    text.pop(0)
    pattern_filter = r"\d{1,2}\/\d{1,2}\/\d{1,2}\,\ \d{1,2}\:\d{1,2}"
    for lines in text:
        prev = lines
        match = re.search(pattern_filter, lines)
        if match:
            text_new.append(prev)
        else:
            text_new[-1] = text_new[-1] + " " + prev

    date_time = []
    # Normalise the unicode space
    text_final = []
    for lines in text_new:
        lines2 = lines.replace("\u202f", " ")
        text_final.append(lines2)

    pattern_all = re.compile(
        r"(\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}\s*(?:am|pm|AM|PM)) - (.*?): (.*)"
    )

    date_time = []
    user = []
    message = []

    for line in text_final:
        match = pattern_all.match(line)
        if match:
            date_time.append(match.group(1))
            user.append(match.group(2))
            message.append(match.group(3))
    # Creating a dataframe
    df = pd.DataFrame({
        "date_time": date_time[:len(message)],
        "user": user[:len(message)],
        "message": message})
    df["date_time"] = pd.to_datetime(df["date_time"])
    df["year"] = df["date_time"].dt.year
    df["month"] = df["date_time"].dt.month
    df["day"] = df["date_time"].dt.day
    df["time"] = df["date_time"].dt.time
    df["hour"] = df["date_time"].dt.hour
    df["minutes"] = df["date_time"].dt.minute
    df["day_name"] = df["date_time"].dt.day_name()
    return df

def call_count(df):
    # for call_counts in df["message"]
    call_counts = df["user"][df["message"] == ''].value_counts()
    df_calls = call_counts.reset_index()
    return df_calls

def call_count_user(df,choice):
    # for call_counts in df["message"]
    call_counts = df[(df["user"]==choice)&(df["message"] == '')]["user"].tolist()
    return len(call_counts)

def text_counts(df,df_calls):
    # Number of texts per user
    texts_user = df["user"].value_counts()
    df_texts = texts_user.reset_index()
    df_texts["count"] = df_texts["count"] - df_calls["count"]
    return df_texts




def media_counts(df):
    # Number of media sent
    media_count=df["user"][df["message"] == "<Media omitted>"].value_counts()
    df_media_count=media_count.reset_index()
    return df_media_count

def media_counts_user(df,choice):
    return len(df[(df["user"] == choice) & (df["message"] == "<Media omitted>")]["user"].tolist())



def num_words(df):
    words=[]
    #Iterating through every message one by one and splitting on basis of spacebar
    for messages in df["message"]:
        # Modifying the original list in place by adding an element at the end
        words.extend(messages.split(" "))

    return len(words)

def links_count(df):
    #Special library to detect urls is used
    extract = URLExtract()
    links = []
    for messages in df["message"]:
        #Modifying the original list in place by adding an element at the end
        links.extend(extract.find_urls(messages))
    return len(links)

def num_links_user(df,choice):
    extract2= URLExtract()
    links=[]
    for messages in df[df["user"]==choice]["message"]:
        links.extend(extract2.find_urls(messages))
    return len(links)

def message_counts(df):
    df_message_month = df.groupby("month")["date_time"].count().reset_index()
    return df_message_month

def user_messages_month(df,choice):
    df_user_month = df.groupby(["user", "month"])["date_time"].count().reset_index()
    df_user_unique = df_user_month[df_user_month["user"] == choice].reset_index()
    return df_user_unique

def message_day_trends(df):
    df_message_day = df["day_name"].value_counts().reset_index()
    return df_message_day

def month_talkative(df):
    df_month_talk = df["month"].value_counts().reset_index()["month"].tolist()[0]
    if df_month_talk == 1:
        df_month_talk = "January"
    if df_month_talk == 2:
        df_month_talk = "February"
    if df_month_talk == 3:
        df_month_talk = "March"
    if df_month_talk == 4:
        df_month_talk = "April"
    if df_month_talk == 5:
        df_month_talk = "May"
    if df_month_talk == 6:
        df_month_talk = "June"
    if df_month_talk == 7:
        df_month_talk = "July"
    if df_month_talk == 8:
        df_month_talk = "August"
    if df_month_talk == 9:
        df_month_talk = "September"
    if df_month_talk == 10:
        df_month_talk = "October"
    if df_month_talk == 11:
        df_month_talk = "November"
    if df_month_talk == 12:
        df_month_talk = "December"

    return df_month_talk

def hour_talkative(df):
    df_hour_talk = df["hour"].value_counts().reset_index()["hour"].tolist()[0]
    return df_hour_talk





def word_image(df):
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")


    #Removes media messages
    df = df[df["message"] != "<Media omitted>"]


    #Removes hinglish stopwords
    words = []
    for message in df["message"]:
        for word in message.split(" "):
            words.append(word.lower())
    df_wc = wc.generate(" ".join(words))
    return df_wc





