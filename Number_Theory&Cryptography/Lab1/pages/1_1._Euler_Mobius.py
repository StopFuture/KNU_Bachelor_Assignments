import streamlit as st
from EulerMobius import mobius_mu_function, euler_phi_function
from Long.LongNumber import LongNumber

st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("📈           Euler and Mobius Functions     +      GCD N numbers ")
st.sidebar.success("Select a page above.")


try:
    st.header("Mobius function: \n")
    st.image("images/mob_function.jpg")
    inp1 = st.number_input("Input1: ", value=None, step=1)
    button1 = st.button("Calculate Mu")
    if inp1 is not None:
        result = mobius_mu_function(inp1)
        if button1:
            st.header(f"Input: {inp1}")
            st.header(f"Result: {result}")

except Exception as x:
    st.markdown(x)
    st.markdown("⚠️   **Enter a number**")

try:
    st.header("Euler function: \n")
    st.image("images/EulerPhi.svg.png")
    inp2 = st.number_input("Input2: ", value=None, step=1)
    button2 = st.button("Calculate Phi")
    if inp2 is not None:

        result2 = euler_phi_function(inp2)
        if button2:
            st.header(f"Input: {inp2}")
            st.header(f"Result: {result2}")


except Exception as x:
    st.markdown(x)
    st.markdown("⚠️   **Enter a number**")

try:
    st.header("GCD N numbers:")
    inp3 = st.text_input("Write a numbers separated by space:", value=None)
    str_inp3 = inp3
    button3 = st.button("Calculate GCD")
    if inp3 is not None:
        result3 = LongNumber.GCD_n(inp3)
        if button3:
            st.header(f"Input: {str_inp3}")
            st.header(f"Result: {result3}")

except Exception as x:
    st.markdown(x)
    st.markdown("⚠️   **Enter a number**")

