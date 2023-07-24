import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from helper import yearly_stats
import helper
from cleaning_layout import layout_modifications

# Cleaning Layout
layout_modifications(st)

# Reading dataset
df=pd.read_csv("Amazon_Cleaned_Data_Set.csv")

# year list
year_list=list(df['Order Year'].unique())
year_list.sort(reverse=True)
year_list.insert(0,'All')

# Region 
region_list=list(df['Region'].unique())
region_list.sort()
region_list.insert(0,'All')

# Load the Amazon logo image
logo_image = "amazon-logo.jpg"
st.sidebar.image(logo_image, use_column_width=True,width=50)

st.sidebar.title("Amazon Data Analysis")
btn=st.sidebar.radio("Select an option",options=['OverAll','Yearly','Monthly'])

if btn=='OverAll':
    st.markdown("""<h2 style='text-align: center;'>Amazon Sales Data Overall Analysis</h2>""", unsafe_allow_html=True)

    total_revenue,total_cost,total_profit,profit_margin=helper.yearly_stats(year='All')

    if total_revenue or total_cost or total_profit or profit_margin:
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.metric("Total Revenue (in Millions)", f"{total_revenue}M")
        with col2:
            st.metric("Total Cost (in Millions)", f"{total_cost}M")
        with col3:
            st.metric("Total Profit (in Millions)", f"{total_profit}M")
        with col4:
            st.metric("Profit Margin", f"{profit_margin}%")
    else:
        st.info("No Data")

    temp_df=df.groupby('Order Year').sum().reset_index()

    t1,t2,t3,t4=st.tabs(['Revenue','Profit','Cost','Units SOld'])

    with t1:
        fig = px.line(temp_df, x="Order Year", y="Total Revenue",title="Revenue Over the Years")
        st.plotly_chart(fig)
    with t2:
        fig = px.line(temp_df, x="Order Year", y="Total Profit",title="Profit Over the Years")
        st.plotly_chart(fig)
    with t3:
        fig = px.line(temp_df, x="Order Year", y="Total Cost",title="Cost Over the Years")
        st.plotly_chart(fig)
    with t4:
        fig = px.line(temp_df, x="Order Year", y="Units Sold",title="Units Sold Over the Years")
        st.plotly_chart(fig)


elif btn=='Yearly':
    st.markdown("""<h2 style='text-align: center;'>Amazon Sale's Yearly Analysis</h2>""", unsafe_allow_html=True)


    year=st.sidebar.selectbox(label="Year",options=year_list)

    st.write(" ")
    st.write(" ")
    total_revenue,total_cost,total_profit,profit_margin=yearly_stats(year=year)

    if total_revenue or total_cost or total_profit or profit_margin:
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.metric("Total Revenue (in Millions)", f"{total_revenue}M")
        with col2:
            st.metric("Total Cost (in Millions)", f"{total_cost}M")
        with col3:
            st.metric("Total Profit (in Millions)", f"{total_profit}M")
        with col4:
            st.metric("Profit Margin", f"{profit_margin}%")
    else:
        st.info("No Data")


    region,sales_channel,item_type=st.tabs(['Regions','Sales Channels','Item Type'])
    with region:
        if year=='All':
            x=f"Regional Analysis Over the Years"
        if year!='All':
            x=f"Regional Analysis For - {year}"

        st.markdown(f"""<h3 style='text-align: center;'>{x} </h3>""", unsafe_allow_html=True)

        data = helper.yearly_region_sales(year=year)
        
        fig = px.bar(data, x='Region', y='Units Sold', title='Units Sold',color='Region')
        fig.update_layout(showlegend=False,title=dict(text='RegionWise Units Sold -', font=dict(size=24))) 
        st.plotly_chart(fig)
        st.write(" ")

        fig = px.bar(data, x='Region', y='Total Revenue', title='Total Revenue',color='Region')
        fig.update_layout(showlegend=False,title=dict(text='RegionWise Total Revenue (in millions) -', font=dict(size=24))) 
        fig.update_yaxes(title_text="Total Revenue (in Million)")
        st.plotly_chart(fig)
        st.write(" ")

        fig = px.bar(data, x='Region', y='Total Profit', title='Total Profit',color='Region')
        fig.update_layout(showlegend=False,title=dict(text='RegionWise Total Profit (in Millions) -', font=dict(size=24))) 
        fig.update_yaxes(title_text="Total Profit (in Million)")
        st.plotly_chart(fig)

    with sales_channel:
        st.write(" ")
        if year=='All':
            x=f"Sales Channel's Analysis Over the Years"
        if year!='All':
            x=f"Sales Channel's Analysis For - {year}"

        st.markdown(f"""<h3>{x} </h3>""", unsafe_allow_html=True)
        
        offline, online=helper.Yearly_Sales_Channels(year)

        labels = ["Offline", "Online"]
        values = [offline, online]

        # Create the pie chart trace
        trace = go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=["darkblue", "aliceblue"]),
            textinfo="label+percent",  
            insidetextorientation="radial", 
            hole=0.4
        )
        fig = go.Figure(data=[trace])
        st.plotly_chart(fig)

    with item_type:
        st.write(" ")
        if year=='All':
            x=f"Item Type Analysis Over the Years"
        if year!='All':
            x=f"Item Type Analysis For - {year}"

        st.markdown(f"""<h3>{x} </h3>""", unsafe_allow_html=True)
        st.write(" ")
        data=helper.Yearly_item_type_analysis(year)
        fig = px.bar(data,x='index', y='Item Type', color='index')
        fig.update_layout(showlegend=False,title=dict(text="Number of Item's Type -", font=dict(size=20)),xaxis_title="Item's Type",yaxis_title="Total Count",) 
        st.plotly_chart(fig)
        st.write(" ")


elif btn=='Monthly':
    st.markdown("""<h2 style='text-align: center;'>Amazon Sale's Monthly Analysis </h2>""", unsafe_allow_html=True)

    temp_df=df.groupby('Order Month Name').sum().reset_index()

    t1,t2,t3,t4=st.tabs(['Revenue','Profit','Cost','Units Sold'])

    with t1:
        fig = px.bar(temp_df, x="Order Month Name", y="Total Revenue",title="Monhtly Revenue",color='Order Month Name')
        st.plotly_chart(fig)
    with t2:
        fig = px.bar(temp_df, x="Order Month Name", y="Total Profit",title="Monthly Profit",color='Order Month Name')
        st.plotly_chart(fig)
    with t3:
        fig = px.bar(temp_df, x="Order Month Name", y="Total Cost",title="Monhtly Cost",color='Order Month Name')
        st.plotly_chart(fig)
    with t4:
        fig = px.bar(temp_df, x="Order Month Name", y="Units Sold",title="Monhtly Units Sold",color='Order Month Name')
        st.plotly_chart(fig)

