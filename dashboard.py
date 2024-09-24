import streamlit as st
import plotly.express as px
import pandas as pd 
from PIL import Image
from datetime import datetime


# Function to load data from multiple uploaded files
def load_data(uploaded_files):
    if uploaded_files:
        dfs = []
        for file in uploaded_files:
            df = pd.read_csv(file)
            dfs.append(df)
        df = pd.concat(dfs, ignore_index=True)
        return df, True
    else:
        # Create an empty DataFrame with the necessary columns if no file is uploaded
        df = pd.DataFrame(columns=["order_year","order_month","customer","count"])
        return df, False

#df= pd.DataFrame(columns=["order_year", "order_month", "customer"] )
#uztuzt#

st.set_page_config(page_title="OR KPI", page_icon="mb_icon.png", layout="wide")
# SVG Icon for Mercedes
svg_icon = """<svg fill="#000000" version="1.1" id="svg3544" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 80 80" xml:space="preserve" width="64px" height="64px"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M58.6,4.5C53,1.6,46.7,0,40,0c-6.7,0-13,1.6-18.6,4.5v0C8.7,11.2,0,24.6,0,40c0,15.4,8.7,28.8,21.5,35.5 C27,78.3,33.3,80,40,80c6.7,0,12.9-1.7,18.5-4.6C71.3,68.8,80,55.4,80,40C80,24.6,71.3,11.2,58.6,4.5z M4,40 c0-13.1,7-24.5,17.5-30.9v0C26.6,6,32.5,4.2,39,4l-4.5,32.7L21.5,46.8v0L8.3,57.1C5.6,52,4,46.2,4,40z M58.6,70.8 C53.1,74.1,46.8,76,40,76c-6.8,0-13.2-1.9-18.6-5.2c-4.9-2.9-8.9-6.9-11.9-11.7l11.9-4.9v0L40,46.6l18.6,7.5v0l12,4.9 C67.6,63.9,63.4,67.9,58.6,70.8z M58.6,46.8L58.6,46.8l-12.9-10L41.1,4c6.3,0.2,12.3,2,17.4,5.1v0C69,15.4,76,26.9,76,40 c0,6.2-1.5,12-4.3,17.1L58.6,46.8z"></path> </g></svg>"""

# Display the title with the Mercedes logo
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        {svg_icon}
        <h1 style="margin-left: 10px;">MB Online Retrieval KPIs</h1>
    </div>
    """,
    unsafe_allow_html=True
)



uploaded_file = st.sidebar.file_uploader(":file_folder: upload a report", type=(["csv", "txt","xlsx","xls"]), accept_multiple_files=True)
df,is_loaded = load_data(uploaded_file)
#if uploaded_file is not None:
 #   filename = uploaded_file.name
  #  df = pd.read_csv(filename)
#else:
    
 #   df = pd.read_csv("OR_Sales_KPI.csv")

   
#Create a sidebar to filter the data based on year, month and customer
#create for Order Year   
st.sidebar.header("Choose your filter:")
Year = st.sidebar.multiselect("Pick your Order Year:", df["order_year"].unique())
if not Year:
    df2=df.copy()
else:
    df2 = df[df["order_year"].isin(Year)]

#create for Order Month

Month = st.sidebar.multiselect("Pick your Order Month:", df2["order_month"].unique())
if not Month:
    df3= df2.copy()
else:
    df3 = df2[df2["order_month"].isin(Month)]


#create for customer

Customer = st.sidebar.multiselect("Pick your Customer:", df3["customer"].unique())
if not Customer:
    filtered_by = df3.copy()
else:
    filtered_by = df3[df3["customer"].isin(Customer)]

if is_loaded:
    #Filter the data based on Year, Month and customer
    monthyear_df = filtered_by.groupby(by = ["order_year", "order_month"])["count"].sum().reset_index()

    monthyear_df["year_month"] = monthyear_df["order_year"].astype(str) + "-" + monthyear_df["order_month"].astype(str).str.zfill(2)


    #df1 = df.sort_values(["order_year", "order_month"])


    #df1= df1.groupby(["order_year", "order_month"])["count"].sum().reset_index(name = "Sum")


    col1, col2 = st.columns((2))
    with col1:
        st.subheader("OR Monthly Sales")
        fig = px.bar(monthyear_df, x = "year_month", y = "count", text = "count")
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=monthyear_df['year_month'],
                ticktext=monthyear_df['year_month'],
                tickangle=45
            )
        )
        st.plotly_chart(fig,use_container_width=True, height = 200)
        

    with col2:
        year_df = filtered_by.groupby(by = ["order_year"])["count"].sum().reset_index()
        st.subheader("OR YTD Sales")
        fig2 = px.bar(year_df, x = "order_year", y = "count", text = "count")
        fig2.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=year_df['order_year'],
                ticktext=year_df['order_year'],
                tickangle=45
            )
        )
        st.plotly_chart(fig2,use_container_width=True, height = 200)





