import emoji
def common_emojis(df):
    words=[]
    emojis=[]
    for texts in df["message"]:
        for word in texts.split(" "):
            words.append(word.lower())

    for x in words:
        for y in x:
            if emoji.is_emoji(y):
                emojis.append(y)

    return emojis