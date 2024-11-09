from datetime import date
import streamlit as st
import pandas as pd
import plotly.express as px

# YouTube: A Cozy follow-along introduction to Streamlit
#
# Url: https://www.youtube.com/watch?v=SVArhvcjnuE



##########################################
#### DATA FUNCTIONS
##########################################

@st.cache_data
def load_data(path: str="./data/FinancialConsumerComplaints.csv"):
    df = pd.read_csv(path,
                     parse_dates=["Date Sumbited", "Date Received"])

    df["Date Received"] = pd.to_datetime(df["Date Received"]).dt.date


    df = df.rename(columns={
        "Date Sumbited": "Date Submitted"
    })
    df["Date Submitted"] = pd.to_datetime(df["Date Submitted"]).dt.date


    df['Complaint ID'] = df['Complaint ID'].astype(str)

    return df

df = load_data()

all_products = df.Product.unique()

def number_of_complaints(df):
    return df.shape[0]

def number_of_disputes(df):
    return df[df['Consumer disputed?'] == 'Yes'].shape[0]

@st.cache_data
def transform_data(df, selected_products, selected_date):
    if selected_products:
        df = df[df['Product'].isin(selected_products)]

    if selected_date:
        df = df[df['Date Submitted'] == selected_date]

    return df

def count_complaints_by_product(df):
    return df.groupby(["Date Submitted", "Product"]).size().reset_index(name='Count')

def count_complaints_by_subproducts(df):
    return df.groupby(["Sub-product"]).agg(Count=("Sub-product", "count")).reset_index()

##########################################
#### UI Functions
##########################################

##########################################
#### UI
##########################################
st.title(":phone: Failing Product Complaints")


with st.expander("**Configuration**"):
    left_filter_col, right_filter_col = st.columns(2, gap="medium")

    with left_filter_col:
        selected_products = st.multiselect("Select Product",
                                           all_products)

    with right_filter_col:
        selected_date = st.date_input("Select a Date",
                                      None,
                                      min_value=df["Date Submitted"].min(),
                                      max_value=df["Date Submitted"].max()
                                      )


selected_products = selected_products if selected_products is not None else ""
# st.title(selected_products)

filtered_df = transform_data(df, selected_products, selected_date)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric("Number of complaints",
                  number_of_complaints(filtered_df),
                  delta=f"{1} % since last week")
with col2:
    with st.container(border=True):
        st.metric("Number of disputes",
                  number_of_disputes(filtered_df),
                  delta=f"{-11} % since last week")

with col3:
    with st.container(border=True):
        st.metric("Dispute Rate %",
                  f"{((number_of_disputes(filtered_df) / number_of_complaints(filtered_df))*100):.2f}",
                  delta=f"{3} % since last week")

row_charts = st.columns((2,1))

fig_compliants_by_product = px.line(
    count_complaints_by_product(filtered_df),
    x="Date Submitted",
    y="Count",
    color="Product",
)
fig_compliants_by_subproduct = px.bar(
    count_complaints_by_subproducts(filtered_df),
    x="Count",
    y="Sub-product",
    orientation="h",
)

with row_charts[0]:
    st.plotly_chart(fig_compliants_by_product)

with row_charts[1]:
    st.plotly_chart(fig_compliants_by_subproduct)



st.dataframe(filtered_df, hide_index=True)

