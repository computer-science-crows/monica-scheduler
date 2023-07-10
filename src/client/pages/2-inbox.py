import streamlit as st

st.set_page_config(page_title = "Monica")

st.markdown("# Inbox")


data=st.data_editor({'Title':[1,2,3], 'Date':[34,21,34], 'Place':['ndfnd','fdjd','fmd'], "Time":['1-2','3-4','5-6']},num_rows='fixed',width=2000)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Accept')
right_column.button('Reject')