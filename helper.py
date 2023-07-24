import pandas as pd
df=pd.read_csv('Amazon_Cleaned_Data_Set.csv')
# return values in millions
def yearly_stats(year):
    total_revenue,total_cost,total_profit,profit_margin=None,None,None,None

    if year!='All':
        new_df=df[df['Order Year']==year]
        total_revenue=round(new_df['Total Revenue'].sum()/10**6)
        total_cost=round(new_df['Total Cost'].sum()/10**6)  
        total_profit=round(new_df['Total Profit'].sum()/10**6)   
        try:
            profit_margin=round(total_profit/total_revenue*100,2)
        except Exception as e:
            profit_margin=0

    else:
        total_revenue=round(df['Total Revenue'].sum()/10**6)
        total_cost=round(df['Total Cost'].sum()/10**6)  
        total_profit=round(df['Total Profit'].sum()/10**6)    
        profit_margin=round(total_profit/total_revenue*100,2)
    
    return total_revenue,total_cost,total_profit,profit_margin


def yearly_region_sales(year):
    d=dict()
    if year=="All":
        temp_df=df.groupby('Region').sum().reset_index()
    else:
        temp_df=df[df['Order Year']==year].groupby('Region').sum().reset_index()
    temp_df['Total Revenue']=round(temp_df['Total Revenue']/10**6,2)
    temp_df['Total Profit']=round(temp_df['Total Profit']/10**6,2)
    d['Region']=list(temp_df['Region'])
    d['Units Sold']=list(temp_df['Units Sold'])
    d['Total Revenue']=list(temp_df['Total Revenue'])
    d['Total Profit']=list(temp_df['Total Profit'])
    return d


# retrun offline and oline channels value
def Yearly_Sales_Channels(year):
    if year=='All':
        temp=df['Sales Channel'].value_counts()
        return temp[0], temp[1]
    if year!='All':
        temp=df[df['Order Year']==year]['Sales Channel'].value_counts()
        return temp[0],temp[1]
    
def Yearly_item_type_analysis(year):
    if year=='All':
        data=df['Item Type'].value_counts().reset_index()
    if year!='All':
        data=df[df['Order Year']==year]['Item Type'].value_counts().reset_index()
    
    return data