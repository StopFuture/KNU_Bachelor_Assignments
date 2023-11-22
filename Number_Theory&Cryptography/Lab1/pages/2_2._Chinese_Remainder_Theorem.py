import streamlit as st
import re
from Long.LongNumber import LongNumber
st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("愛           Chinese Remainder Theorem ")
st.sidebar.success("Select a page above.")


def extended_gcd(a, b):
    if a == LongNumber(0):
        return (b, LongNumber(0), LongNumber(1))
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)


def chinese_remainder_theorem(equations):
    x = LongNumber("0")
    prod = LongNumber("1")
    # Calculate product of all n_i
    for _, ni in equations:
        prod = prod * ni

    # Apply CRT formula
    for ai, ni in equations:
        p = prod // ni
        gcd, mi, _ = extended_gcd(p, ni)
        if gcd != LongNumber(1):
            raise Exception("Moduli are not coprime")
        x = x + ai * mi * p

    return x % prod


try:
    st.header("CRT:")
    st.image("images/crt.png")
    inp3 = st.text_input("Write a pairs: (remainder_1, mod_1), (remainder_2 mod_2)", value=None)
    str_inp3 = inp3

    pattern = r"\((\d+), (\d+)\)"

    matches = re.findall(pattern, str_inp3)
    equations = [(LongNumber(a), LongNumber(b)) for a, b in matches]
    st.write(equations)

    button3 = st.button("Calculate X:")
    if inp3 is not None:
        result3 = chinese_remainder_theorem(equations)
        if button3:
            st.header(f"Input: {equations}")
            st.header(f"Result: {result3}")

except Exception as x:

    st.markdown(f"⚠️   **{x}**")

