import streamlit as st

st.set_page_config(page_title = "Monica")

st.markdown("# Workspaces")


def change():
    st.text('change')
    
data=st.data_editor({'Title':[1,2,3], 'Date':[34,21,34], 'Place':['ndfnd','fdjd','fmd'], "Time":['1-2','3-4','5-6']},num_rows='dynamic',width=2000,on_change=change())