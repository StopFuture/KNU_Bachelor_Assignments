import streamlit as st
from Long.LongNumber import LongNumber
from Cipolla import cipolla
st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("Cipolla Algorithm")
st.sidebar.success("Select a page above.")

try:
    st.header("Calculation:")
    st.image("images/cipolla_6.png")
    inp2 = st.text_input("Input  (numbers separated by space): ", value=None)

    button2 = st.button("Calculate:")
    if inp2 is not None:
        inp2 = [LongNumber(c) for c in inp2.split(" ")]
        str_inp2 = inp2
        result2 = cipolla(*inp2)
        # st.markdown(result2)
        if button2:
            st.header(f"Input: {str_inp2}")
            st.header(f"Result: {result2}")


except Exception as x:
    st.markdown(f"⚠️   **{x}**")
