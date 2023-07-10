import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Monica")

st.markdown("# Profile")


#x = st.slider('x')  # 👈 this is a widget
#st.write(x, 'squared is', x * x)

username = st.text_input("Username", value="Some long comment to edit")

full_name = st.text_input("Full Name", value="Some long comment to edit")

password = st.text_input("Password", value="Some long comment to edit")

left_column, right_column = st.columns(2)

left_column.button('Edit')

#def cleaning_function():
#    pass
#
#input_data = st.text_area("input")
#parsed_data = cleaning_function() # Some function you've made to clean the input data
#
#allow_editing = st.radio("Edit parsed data", [True, False])
#
#if allow_editing:
#    output = st.text_area("parsed data", value=parsed_data)
#else:
#    st.text(parsed_data)



#st.text_input("Your name", key="name")
#
## You can access the value at any point with:
#st.session_state.name
#
#df = pd.DataFrame({
#    'first column': [1, 2, 3, 4],
#    'second column': [10, 20, 30, 40]
#    })
#
# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])

# 'You selected: ', option


# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )


# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")