import streamlit as st
from Long.LongNumber import LongNumber
from RhoPollard import pollard_rho

st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("Pollard's Rho Algorithm")
st.sidebar.success("Select a page above.")

try:
    st.header("Calculation of Rho-Pollard Factorization:")
    st.image("images/4_rho.png")
    inp2 = st.text_input("Input LongNumber: ", value=None)

    button2 = st.button("Calculate Factorization:")
    if inp2 is not None:
        str_inp2 = inp2
        result2 = [i.__str__() for i in pollard_rho(LongNumber(inp2))]

        if button2:
            st.header(f"Input: {str_inp2}")
            st.header(f"Result: {result2}")


except Exception as x:
    st.markdown(f"⚠️   **{x}**")
