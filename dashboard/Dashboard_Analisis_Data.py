import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_monthly_user_df(df):
    data_monthly = df.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
    }).reset_index()
    return data_monthly

## Group by time
def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )
    return byhour_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday").agg(
        {
            "casual" : "mean",
            "registered" : "mean",
            "cnt": "mean"
        }
    )
    return byweekday_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )

    return byholiday_df

def create_bymonth_df(df):
    bymonth_df = df.groupby(by="mnth").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )
    return bymonth_df

## Group by weather

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )
    return byweathersit_df


def create_bywindspeed_df(df):
    bywindspeed_df = df.groupby(by="windspeed_cat").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )

    return bywindspeed_df

def create_bytemp_df(df):
    bytemp_df = df.groupby(by="temp_cat").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )

    return bytemp_df

def create_byatemp_df(df):
    byatemp_df = df.groupby(by="atemp_cat").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )

    return byatemp_df

def create_byhum_df(df):
    byhum_df = df.groupby(by="hum_cat").agg(
    {
        "casual" : "mean",
        "registered" : "mean",
        "cnt": "mean"
    }
    )

    return byhum_df


# Load cleaned data

dir_path = "https://raw.githubusercontent.com/Mehmed13/bike-sharing-rental/refs/heads/main/dashboard/"
day_df = pd.read_csv(dir_path + "final_day.csv")
hour_df = pd.read_csv(dir_path+"final_hour.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Period',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

filtered_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe

monthly_df = create_monthly_user_df(filtered_day_df)

byhour_df = create_byhour_df(filtered_hour_df)
byweekday_df =create_byweekday_df(filtered_day_df)
byholiday_df =create_byholiday_df(filtered_day_df)
bymonth_df = create_bymonth_df(filtered_day_df)

byweathersit_df = create_byweathersit_df(filtered_hour_df)
bywindspeed_df = create_bywindspeed_df(filtered_hour_df)
bytemp_df = create_bytemp_df(filtered_hour_df)
byatemp_df = create_byatemp_df(filtered_hour_df)
byhum_df = create_byhum_df(filtered_hour_df)


# plot number of daily or monthly users (2011-2012)
st.title('Bike-Sharing Rental Dashboard :bike:')

time_horizon = "Daily"
time_horizon = st.selectbox(
    label= "Time Horizon",
    options=('Daily', 'Monthly')
)
st.header(time_horizon + " User")

## Numeric Information on Top
col1, col2, col3 = st.columns(3)

total_casual_user = filtered_day_df["casual"].sum()
total_registered_user = filtered_day_df["registered"].sum()
total_user = total_casual_user + total_registered_user

with col1:
    st.metric("Casual User", value='{:,}'.format(total_casual_user))
with col2:
    st.metric("Registered User", value='{:,}'.format(total_registered_user))
with col3:
    st.metric("Total", value='{:,}'.format(total_user))

## Line graph and pie chart

### Pie chart
with st.sidebar:
    st.subheader("Bike-Sharing Rental's User")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.pie(
        x=[total_casual_user, total_registered_user],
        labels=["casual", "registered"],
        autopct='%1.1f%%',
        colors=["#FAA0A0", "#A7C7E7"]
    )
    st.pyplot(fig)    

### Line graph

line_df = filtered_day_df if time_horizon=="Daily" else monthly_df

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    line_df["dteday"],
    line_df["cnt"], 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.header("Analysis Number of User")

# Highest and Lowest by Time

tab1, tab2 = st.tabs(["By Time", "By Weather"])

with tab1:

    st.subheader("Highest and Lowest Number of User by Hour")
    with st.expander("See the graphics", expanded=True):
        # Highest
        fig, ax = plt.subplots(figsize=(16, 8))
        colors = ["#D3D3D3" for i in range (17)] + ["#5ce65c"] + ["#D3D3D3" for i in range (6)] 
        sns.barplot(x="hr", y="cnt", data=byhour_df, palette=colors)
        ax.set_title("Highest Average Number of User by Hour", loc="center")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)


        # Lowest
        fig, ax = plt.subplots(figsize=(16, 8))
        colors = ["#D3D3D3" for i in range (4)] + ["#d20a2e"] + ["#D3D3D3" for i in range (19)]
        sns.barplot(x="hr", y="cnt", data=byhour_df, palette=colors)
        ax.set_title("Lowest Average Number of User by Hour", loc="center")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

    st.subheader("Highest and Lowest Number of User by Weekday")
    with st.expander("See the graphics", expanded=True):
        # Highest
        fig, ax = plt.subplots(figsize=(16, 8))
        colors = ["#D3D3D3" for i in range (5)] + ["#5ce65c"] + ["#D3D3D3" for i in range (6)]
        sns.barplot(x="weekday", y="cnt", data=byweekday_df, palette=colors)
        ax.set_title("Highest Average Number of User by Weekday", loc="center")
        ax.set_xlabel("Weekday")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)


        # Lowest
        fig, ax = plt.subplots(figsize=(16, 8))
        colors = ["#d20a2e"] + ["#D3D3D3" for i in range (6)] 
        sns.barplot(x="weekday", y="cnt", data=byweekday_df, palette=colors)
        ax.set_title("Lowest Average Number of User by Weekday", loc="center")
        ax.set_xlabel("Weekday")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

    st.subheader("Highest and Lowest Number of User by Month")
    with st.expander("See the graphics", expanded=True):
        # Highest
        fig, ax = plt.subplots(figsize=(16, 8))
        colors = ["#D3D3D3" for i in range (5)] + ["#5ce65c"] + ["#D3D3D3" for i in range (1)]
        sns.barplot(x="mnth", y="cnt", data=bymonth_df, palette=colors)
        ax.set_title("Highest Average Number of User by Month", loc="center")
        ax.set_xlabel("Month")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)


        # Lowest
        fig, ax = plt.subplots(figsize=(16, 8))
        colors = ["#d20a2e"] + ["#D3D3D3" for i in range (11)] 
        sns.barplot(x="mnth", y="cnt", data=bymonth_df, palette=colors)
        ax.set_title("Lowest Average Number of User by Month", loc="center")
        ax.set_xlabel("Month")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

with tab2:
    st.subheader("Average Number of User by Weathersit")
    with st.expander("See the graphics", expanded=True):
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(x="weathersit", y="cnt", data=byweathersit_df, palette=sns.color_palette("crest"))
        ax.set_xlabel("Weathersit")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

    st.subheader("Average Number of User by Windspeed")
    with st.expander("See the graphics", expanded=True):
        fig, ax = plt.subplots(figsize=(16, 8))
        colors = ["#4CB4BE", "#4CB4BE", "#1E4D4B", "#1E4D4B", "#4CB4BE", "#4CB4BE",  "#4CB4BE"]
        sns.barplot(x="windspeed_cat", y="cnt", data=bywindspeed_df, palette=colors)
        ax.set_xlabel("Windspeed")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

    st.subheader("Average Number of User by Temperature")
    with st.expander("See the graphics", expanded=True):
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(x="temp_cat", y="cnt", data=bytemp_df, palette=sns.color_palette("rocket_r"))
        ax.set_xlabel("Temperature")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

    st.subheader("Average Number of User by Feeling Temperature")
    with st.expander("See the graphics", expanded=True):
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(x="atemp_cat", y="cnt", data=byatemp_df, palette=sns.color_palette("rocket_r"))
        ax.set_xlabel("Feeling Temperature")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

    st.subheader("Average Number of User by Humidity")
    with st.expander("See the graphics", expanded=True):
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(x="hum_cat", y="cnt", data=byhum_df, palette=sns.color_palette("crest"))
        ax.set_xlabel("Humidity")
        ax.set_ylabel("Average Number of User")
        st.pyplot(fig)

st.caption('Copyright © Fadhil 2024')