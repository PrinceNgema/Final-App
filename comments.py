import pandas as pd
import streamlit as st
import sqlite3 
from datetime import date

conn = sqlite3.connect('comment.db',check_same_thread=False)
c = conn.cursor()

# Functions
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')
create_table()

def add_data(author,title,article,postdate):
	c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
	conn.commit()

def view_all_notes():
	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	return data

def view_all_titles():
	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	return data


def get_blog_by_title(title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data
def get_blog_by_author(author):
	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data

def delete_data(title):
	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()
# Layout Templates

html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">Home of Comments </h1>
</div>
"""
title_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>Author:{}</h6>
<br/>
<br/> 
<p style="text-align:justify">{}</p>
</div>
"""
article_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6 style="color:white;text-align:center;"> Author:{}</h6> 
<h6 style="color:white;text-align:center;"> Post Date: {}</h6> 
</div>
"""
full_message_temp ="""
<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""

news_message_temp= """ 
<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p><a href = {} style="color:#000000;text-decoration: none;"target="_blank"> {}</a></p>
</div>
"""
def add_comments():
        st.subheader("Add Comments")
        create_table()
        blog_author = st.text_input("Enter Author Name",max_chars=50)
        blog_title = st.text_input("Enter Comment Title")
        blog_article = st.text_area("Write Comment Here",height=200)
        blog_post_date = date.today()
        if st.button("Add"):
            add_data(blog_author,blog_title,blog_article,blog_post_date)
            st.success("Comments:{} saved".format(blog_title))
def comment():
    #st.markdown(html_temp.format('blue','white'),unsafe_allow_html=True)
    st.header('Comments Highlights')
    menu = ["Comments Highlights","Add Comments","View Comments","Search Comments","Manage Comments"]
    choose = st.sidebar.selectbox("Menu",menu)

    if choose == "Comments Highlights":
        result = view_all_notes()
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_article = str(i[2])[0:30]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_title,b_author,b_article,b_post_date),unsafe_allow_html=True)

    elif choose == "View Comments":
        st.subheader("View Comments")
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("View Comments",all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            #st.text("Reading Time:{}".format(readingTime(b_article)))
            st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)

    elif choose == "Add Comments":
        add_comments()
        
    elif choose == "Search Comments":
        st.subheader("Search Comments")
        search_term = st.text_input('Enter Search Term')
        search_choice = st.radio("Field to Search By",("title","author"))
        
        if st.button("Search"):

            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "author":
                article_result = get_blog_by_author(search_term)


            for i in article_result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                #st.text("Reading Time:{}".format(readingTime(b_article)))
                st.markdown(head_message_temp.format(b_title,b_author,b_post_date),unsafe_allow_html=True)
                st.markdown(full_message_temp.format(b_article),unsafe_allow_html=True)

    elif choose == "Manage Comments":
        st.subheader("Manage Comments")

        result = view_all_notes()
        clean_db = pd.DataFrame(result,columns=["Author","Title","Articles","Post Date"])
        st.dataframe(clean_db)

        unique_titles = [i[0] for i in view_all_titles()]
        delete_blog_by_title = st.selectbox("Unique Title",unique_titles)
        new_df = clean_db
        if st.button("Delete"):
            delete_data(delete_blog_by_title)
            st.warning("Deleted: '{}'".format(delete_blog_by_title))


        if st.checkbox("Metrics"):
            
            new_df['Length'] = new_df['Articles'].str.len()
            st.dataframe(new_df)


            st.subheader("Author Stats")
            new_df["Author"].value_counts().plot(kind='bar')
            st.pyplot()

            st.subheader("Author Stats")
            new_df['Author'].value_counts().plot.pie(autopct="%1.1f%%")
            st.pyplot()

        if st.checkbox("BarH Plot"):
            st.subheader("Length of Articles")
            new_df = clean_db
            new_df['Length'] = new_df['Articles'].str.len()
            barh_plot = new_df.plot.barh(x='Author',y='Length',figsize=(20,10))
            st.pyplot()
