import streamlit as st
from Long.LongNumber import LongNumber
from LegendreJacobi import legendre_symbol, jacobi_symbol
st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("Calculation of Legendre and Jacobi symbols ")
st.sidebar.success("Select a page above.")

try:
    st.header("Calculation of Legendre symbols:")
    st.image("images/legendre.png")
    inp2 = st.text_input("Input (numbers separated by space): ", value=None)

    button2 = st.button("Calculate Legendre:")
    if inp2 is not None:
        str_inp2 = inp2
        inp2 = inp2.split(" ")
        result2 = legendre_symbol(*inp2)
        if button2:
            st.header(f"Input: {str_inp2}")
            st.header(f"Result: {result2}")

except Exception as x:
    st.markdown(f"⚠️   **{x}**")

try:
    st.header("Calculation of Jacobi symbols:")
    st.image("images/jacobi.png")
    inp3 = st.text_input("Input(numbers separated by space): ", value=None)

    button3 = st.button("Calculate Jacobi:")
    if inp3 is not None:
        str_inp3 = inp3
        inp3 = inp3.split(" ")
        result3 = jacobi_symbol(*inp3)
        if button3:
            st.header(f"Input: {str_inp3}")
            st.header(f"Result: {result3}")

except Exception as x:
    st.markdown(f"⚠️   **{x}**")

