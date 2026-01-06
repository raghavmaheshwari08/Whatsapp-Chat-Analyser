import streamlit as st
from matplotlib import pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import preprocessor
import seaborn as sns
from urlextract import URLExtract
import emoji_detect
import pandas as pd
st.sidebar.header("Whatsapp Chat Analyser")
uploaded_file=st.sidebar.file_uploader("Choose a File")
if uploaded_file:
    data_bytes=uploaded_file.getvalue()
    data=data_bytes.decode("utf-8")
    # This creates our dataframe
    dataframe=preprocessor.create_dataframe(data)
    #st.dataframe(dataframe)

    #This creates a list of the unique users present in our chat( could be a group chat too )
    user_list=dataframe["user"].unique().tolist()
    #user_list.remove("group_notification")
    user_list.append("Overall")
    choice=st.sidebar.selectbox("Choose an Option",user_list)

    #The execution part
    if st.sidebar.button("Show analysis"):
        if (choice=="Overall"):
            #This reflects the count of the unique number of users.
            st.header("Number of users")
            st.subheader(len(dataframe["user"].unique().tolist()))

            #Divides the space into three columns
            col1,col2,col3=st.columns(3)
            with col1:
                st.header("Number of words")
                num_words=preprocessor.num_words(dataframe)
                st.subheader(num_words)
            with col2:
                st.header("Total links shared")
                num_links=preprocessor.links_count(dataframe)
                st.subheader(num_links)

            with col3:
                st.header("Most talkative day")
                most_day_talk= preprocessor.message_day_trends(dataframe)
                most_day_talk= most_day_talk["day_name"].tolist()[0]
                st.subheader(most_day_talk)

            #Counting the number of calls made by unique users
            df_calls=preprocessor.call_count(dataframe)
            st.header("Number of calls made")
            st.dataframe(df_calls) #Display the dataframe in the webpage


            st.header("Number of Texts")
            df_texts=preprocessor.text_counts(dataframe,df_calls)
            st.dataframe(df_texts) #Displays the dataframe in the webpage


            df_media=preprocessor.media_counts(dataframe)
            st.header("Media Count")
            st.dataframe(df_media)

            #Displaying a graph of trend of total messages sent with respect to every day
            st.header("Message trends wrt days of the week")
            df_message_day_trend = preprocessor.message_day_trends(dataframe)
            fig = px.bar(df_message_day_trend,x="day_name",y="count")
            st.plotly_chart(fig)

            col10, col11 = st.columns(2)
            with col10:
                st.header("Most talkative month")
                month_talkative= preprocessor.month_talkative(dataframe)
                st.subheader(month_talkative)

            with col11:
                st.header("Most talkative hour(24 hour clock)")
                hour_talkative= preprocessor.hour_talkative(dataframe)
                st.subheader(hour_talkative)

            #Common Words used in the chat
            image_common_words = preprocessor.word_image(dataframe)
            fig, ax = plt.subplots()
            ax.imshow(image_common_words)
            st.pyplot(fig)

            #Common emojis used
            st.header("Common Emojis used")
            list_emojis = emoji_detect.common_emojis(dataframe)
            df_emojis = pd.DataFrame(list_emojis, columns=["emoji"])
            df_emojis = pd.DataFrame(df_emojis.value_counts(),columns = ["count"])
            st.dataframe(df_emojis.head(5))




        else:
            st.title(choice)
            st.subheader("Analysis")
            col4, col5, col6 = st.columns(3)
            with col4:
                st.header("Number of words")
                num_words = preprocessor.num_words(dataframe[dataframe["user"]==choice])
                st.subheader(num_words)
            with col5:
                st.header("Number of media")
                num_media = preprocessor.media_counts_user(dataframe,choice)
                st.subheader(num_media)
            with col6:
                st.header("Number of calls made")
                calls_count=preprocessor.call_count_user(dataframe,choice)
                st.subheader(calls_count)


            #Filtering our dataset with respect to the choice made
            dataframe_choice = dataframe[dataframe["user"]==choice]

            st.header("Most common emojis")
            list_emojis = emoji_detect.common_emojis(dataframe_choice)
            df_emojis = pd.DataFrame(list_emojis, columns=["emoji"])
            df_emojis = pd.DataFrame(df_emojis.value_counts(), columns=["count"])
            st.dataframe(df_emojis.head(5))

            col10, col11 = st.columns(2)
            with col10:
                st.header("Usually texts on")
                most_day_talk = preprocessor.message_day_trends(dataframe_choice)
                most_day_talk = most_day_talk["day_name"].tolist()[0]
                st.subheader(most_day_talk)

            with col11:
                image_wordcloud = preprocessor.word_image(dataframe_choice)
                fig,ax = plt.subplots()
                ax.imshow(image_wordcloud)
                st.pyplot(fig)

            st.header("Monthly Timeline")
            ax, fig = plt.subplots()
            fig = px.line(dataframe_choice.groupby("month")["message"].count())
            st.plotly_chart(fig)








            # col7, col8, col9 = st.columns(3)
            # with col7:
            #     st.header("Number of links shared")
            #     num_links=preprocessor.num_links_user(dataframe,choice)
            #     st.subheader(num_links)





