import streamlit as st
import langhain_helper
st.title("Restaurant name generator")

cuisine=st.sidebar.selectbox("PICK A CUISINE", ("INDIAN", "ITALIAN", "MEXICAN","RUSSIAN"))

if cuisine:
    response=langhain_helper.generate_restaurant_name_and_items(cuisine)
    st.header(response['restaurant_name'].strip())
    menu_items=response['menu_items'].strip().split(",")
    st.write("**MENU ITEMS**")

    for item in menu_items:
        st.write("-",item)

