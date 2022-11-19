import pandas as pd  
import plotly.express as px  
import streamlit as st  
import warnings

warnings.filterwarnings("ignore")


st.set_page_config(page_title="Sales Dashboard", page_icon=":chart:", layout="wide")
placeholder = st.empty()
placeholder.info("To make Your Difficult sales data Easy to Visualize     CONTACT: salesdashboard21900@gmail.com")


# ---- READ EXCEL ----
file = st.file_uploader(label="CSV or XLSL File", type=['csv','xlsx'])
@st.cache

def get_data_from_excel():
    df = pd.read_excel(
        io = file,
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# SIDEBAR 
st.sidebar.header("APPLY FILTERS:")
st.markdown("""---""")
city = st.sidebar.multiselect(
    "PICK A CITY:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "PICK A CUSTOMER_CATEGORY:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "PICK A GENDER:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

quantity = st.sidebar.multiselect(
    "PURCHASED QUANTITY:",
    options=df["Quantity"].unique(),
    default=df["Quantity"].unique()
)

rating = st.sidebar.multiselect(
    "RATINGS:",
    options=df["Rating"].unique(),
    default=df["Rating"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender &  Quantity == @quantity & Rating == @rating"
)

# ---- MAINPAGE ----
st.title(":chart: Sales Analysis Dashboard ")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"IND {total_sales:,}")
with middle_column:
    st.subheader("Average Star Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Customer:")
    st.subheader(f"IND {average_sale_by_transaction}")

st.markdown("""---""")



# SALES BY PRODUCT LINE 
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>SALES BY PRODUCTS</b>",
    color_discrete_sequence=["#b80012"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)

# SALES BY HOUR 
sales_by_hourly = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hourly,
    x=sales_by_hourly.index,
    y="Total",
    title="<b>SALES BY TIME</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hourly),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown("""---""")

# SALES BY QUANTITY
sales_by_cogs= (
    df_selection.groupby(by=["Quantity"]).sum()[["Total"]].sort_values(by="Total")
)
fig_cogs_sales = px.bar(
    sales_by_cogs,
    x=sales_by_cogs.index,
    y="Total",
    orientation="h",
    title="<b>SALES BY QUANTITY</b>",
    color_discrete_sequence=["#26a541"] * len(sales_by_cogs),
    template="plotly_white",
)
fig_cogs_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)

# HIGH RATED PRODUCTS
sales_by_units = df_selection.groupby(by=["Product line"]).sum()[["Rating"]]
fig_units_sales = px.bar(
    sales_by_units,
    x=sales_by_units.index,
    y="Rating",
    title="<b>HIGH RATED PRODUCTS</b>",
    color_discrete_sequence=["#ff4343"] * len(sales_by_units),
    template="plotly_white",
)
fig_units_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=True)),
)

left_bottom_column,right_bottom_column=st.columns(2)
left_bottom_column.plotly_chart(fig_cogs_sales, use_container_width=True)
right_bottom_column.plotly_chart(fig_units_sales, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
