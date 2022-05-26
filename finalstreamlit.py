import streamlit as st
import pandas as pd
#from gsheetsdb import connect
import plotly.express as px
#gsheet_url = "https://docs.google.com/spreadsheets/d/1djM1EzJ9O6NK75XBk4dNc1GyA0kfwbm5rAi6IRjkDYo/edit#gid=2046088875"
#conn = connect()
#rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
#df_gsheet = pd.DataFrame(rows)

df = pd.read_csv('transformed_data.csv')
df.sort_values("state", inplace = True)

st.title("Consumer Complaint Data")
complaints, State = st.columns((4,1))

states_drop = State.selectbox("State",pd.unique(df["state"]))
df = df[df["state"] == states_drop]




tc = len(df)
filter1 = df[df["company_response"]=="Closed with explanation"]
closed_comp = len(filter1)
filter2 = df[df["timely"]=="Yes"]
timely_comp = len(filter2)
filter3 = df[df["company_response"]=="In progress"]
prog_comp = len(filter3)
states = df['state'].unique()
complaints_prod = df.groupby(['product']).size().reset_index(name='count').sort_values(by='count', ascending=True)
print(complaints_prod)
complaints_month = df.groupby(['date_received']).size().reset_index(name='count').sort_values(by='date_received', ascending=True)
print(complaints_month)
complaints_status = df.groupby(['submitted_via']).size().reset_index(name='count').sort_values(by='count', ascending=True)
print(complaints_status)
complaints_issue = df.groupby(['issue', 'sub_issue']).size().reset_index(name='count').sort_values(by='count', ascending=True)
print(complaints_issue)

tc_kpi,closed_comp_kpi,timely_comp_kpi,prog_comp_kpi, state = st.columns(5)
tc_kpi.metric(label="Total Complaints",value=tc, delta=-0.5)
closed_comp_kpi.metric(label = "Closed Status Complaints",value=closed_comp, delta=-0.5)
timely_comp_kpi.metric(label="Timely Responded Complaints",value=timely_comp, delta=-0.5)
prog_comp_kpi.metric(label="Progress Status Complaints",value=prog_comp, delta=-0.5)

complaints_month_fig, complaints_prod_fig = st.columns(2)
complaints_issue_fig, complaints_status_fig = st.columns(2)

with complaints_month_fig:
    st.subheader("Complaints by Month")
    fig = px.line(complaints_month , x='date_received', y='count')
    st.write(fig)
with complaints_prod_fig:
    st.subheader("Complaints by Product")
    fig = px.bar(complaints_prod, x='product', y='count')
    st.write(fig)
with complaints_issue_fig:
    st.subheader("Complaints by Issue and Sub-Issue")
    fig = px.treemap(complaints_issue, path=['issue', 'sub_issue'], values='count')
    st.write(fig)
with complaints_status_fig:
    st.subheader("Complaints by Submitted via")
    fig = px.pie(complaints_status, values='count', names='submitted_via')
    st.write(fig)
    

