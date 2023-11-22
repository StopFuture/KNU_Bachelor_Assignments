import streamlit as st
from Long.LongNumber import LongNumber
from DiscreteLog import bsgs_log, verify

st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("Discrete Logarithm")
st.sidebar.success("Select a page above.")

try:
    st.header("Calculation of Discrete Logarithm(BabyStepGiantStep):")
    st.image("images/5_bsgs.png")
    inp2 = st.text_input("Input g h p (numbers separated by space): ", value=None)

    button2 = st.button("Calculate Log:")
    if inp2 is not None:
        str_inp2 = inp2
        inp2 = inp2.split(" ")
        result2 = bsgs_log(*inp2)

        if button2:
            st.header(f"Input: {str_inp2}")
            st.header(f"Result: {result2}")

            st.write(verify(*inp2, result2))

except Exception as x:
    st.markdown(f"⚠️   **{x}**")
