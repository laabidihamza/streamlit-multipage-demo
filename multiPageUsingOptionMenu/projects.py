import streamlit as st
import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import plotly.express as px
import chart_studio.plotly as py
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
from collections import Counter


from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

def projects():

    st.write("This is the Projects page content.")
    
    key = os.getenv('SUPABASE_KEY')
    url = os.getenv('SUPABASE_URL')

    supabase = create_client(url, key)

    # Retrieve summaries from the user_search table
    search_table_res = supabase.table("user_search").select("*").execute()
    searches = search_table_res.data
    summaries = [entry["summary"] for entry in searches]
    descriptions = [entry["description"] for entry in searches]
    search_dates = [entry["search_date"] for entry in searches]

    report_table_res = supabase.table("user_report").select("*").execute()
    reports = report_table_res.data
    report_dates = [entry["report_date"] for entry in reports]
    ratings = [entry["rating"] for entry in reports]


    # Combine all summaries into a single string
    all_summaries = " ".join(summaries)
    all_descriptions = " ".join(descriptions)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            sum_wordcloud = WordCloud(width=400, height=200, background_color="white").generate(all_summaries)

            # Create a new Matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 5))  # Define figure size
            ax.imshow(sum_wordcloud, interpolation="bilinear")  # Display the word cloud on the figure
            ax.axis("off")  # Hide axis lines and labels

            # Display the figure in Streamlit
            st.pyplot(fig)
            st.markdown("""
                        ##### This is the summary word cloud
                        """)

        with col2:
            des_wordcloud = WordCloud(width=400, height=200, background_color="white").generate(all_descriptions)

            # Create a new Matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 5))  
            ax.imshow(des_wordcloud, interpolation="bilinear")  
            ax.axis("off")  # Hide axis lines and labels

            # Display the figure in Streamlit
            st.pyplot(fig)
            st.markdown("""
                ##### This is the report word cloud
            """)
            
    # Convert to pandas DataFrames for easier manipulation
    search_dates = pd.DataFrame(searches)
    report_dates = pd.DataFrame(reports)

    # Convert datestamps to datedate objects
    search_dates["search_date"] = pd.to_datetime(search_dates["search_date"])
    report_dates["report_date"] = pd.to_datetime(report_dates["report_date"])

    search_counts = search_dates.groupby(search_dates["search_date"].dt.date).size().reset_index(name="count")
    report_counts = report_dates.groupby(report_dates["report_date"].dt.date).size().reset_index(name="count")
    st.write(report_counts)

    # Create a plot with both search and report counts
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot search counts
    ax.plot(search_counts["search_date"], search_counts["count"], label="Searches", marker='o', linestyle='-')

    # Plot report counts
    ax.plot(report_counts["report_date"], report_counts["count"], label="Reports", marker='o', linestyle='-')

    # Add titles and labels
    ax.set_title("User Searches and Reports Over date")
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)



    fig = go.Figure([go.Scatter(x=report_counts['report_date'], y=report_counts['count'])])
    fig.show()
    st.plotly_chart(fig)

    fig = px.line(report_counts, x="report_date", y="count", title="User Reports Over Time")
    
    fig.show()
    st.plotly_chart(fig)




    # Count the occurrences of each rating
    rating_counts = Counter(ratings)

    # Create a pie chart with Plotly Express
    pie_chart = px.pie(
        data_frame=pd.DataFrame(rating_counts.items(), columns=["stars", "count"]),
        names="stars", 
        values = "count",
        title="Distribution of User Ratings",  
        hole=0.4,  
        labels={1: "1 Star", 2: "2 Stars", 3: "3 Stars", 4: "4 Stars", 5: "5 Stars"}, 
        )
    
    st.plotly_chart(pie_chart)


    # Create a stick plot with Plotly
    fig = go.Figure()

    # Add stick plot for searches
    fig.add_trace(
        go.Scatter(
            x=search_counts["search_date"],
            y=search_counts["count"],
            mode='markers+lines',  # Both markers and lines for sticks
            name='Searches',
            line=dict(width=2, color='blue'),  # Stick appearance
            marker=dict(size=10)  # Marker appearance
        )
    )

    # Add stick plot for reports
    fig.add_trace(
        go.Scatter(
            x=report_counts["report_date"],
            y=report_counts["count"],
            mode='markers+lines',
            name='Reports',
            line=dict(width=2, color='red'),
            marker=dict(size=10)
        )
    )

    # Customize plot layout
    fig.update_layout(
        title="User Activity Over Time (Searches and Reports)",
        xaxis_title="Date",
        yaxis_title="Count",
        showlegend=True,
        legend=dict(x=0.01, y=0.99)  # Legend position
    )

    st.plotly_chart(fig)


    # Create a stick plot
    stick_plot = go.Figure()

    # Add search counts as sticks
    stick_plot.add_trace(
        go.Scatter(
            x=search_counts["search_date"],
            y=search_counts["count"],
            mode="markers+lines",
            name="Searches",
            line=dict(width=0.5),  # Thin lines for sticks
            marker=dict(size=10),  # Larger markers for visual emphasis
        )
    )

    # Add report counts as sticks
    stick_plot.add_trace(
        go.Scatter(
            x=report_counts["report_date"],
            y=report_counts["count"],
            mode="markers+lines",
            name="Reports",
            line=dict(width=0.5),  # Thin lines for sticks
            marker=dict(size=10),  # Larger markers for visual emphasis
        )
    )

    # Add title and axis labels
    stick_plot.update_layout(
        title="User Activity by Date (Searches and Reports)",
        xaxis_title="Date",
        yaxis_title="Action Count",
        showlegend=True,
    )

    # Display the plot in Streamlit
    st.plotly_chart(stick_plot)
