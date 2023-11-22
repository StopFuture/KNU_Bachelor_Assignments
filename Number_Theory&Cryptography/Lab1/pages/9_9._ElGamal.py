import streamlit as st
from ElGamal import ElGamal
from Point import Point

st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("ElGamal Crypto System")
st.sidebar.success("Select a page above.")

P = Point(
    int('A1455B33_4DF099DF_30FC28A1_69A467E9_E47075A9_0F7E650E_B6B7A45C', 16),
    int('7E089FED_7FBA3442_82CAFBD6_F7E319F7_C0B0BD59_E2CA4BDB_556D61A5', 16)
)

try:
    st.header("Calculation:")
    st.write("Used: https://www.secg.org/SEC2-Ver-1.0.pdf")
    st.image("images/gamal_9.png")

    button2 = st.button("Calculate")
    if button2:
        st.write("Point: ", P)
        message = P * 1233
        st.write(message)
        # Bob generates a key pair
        secret_key, public_key = ElGamal.generate_key()
        st.write("Secret Key:", secret_key)
        st.write("Public Key:", public_key)
        # Encrypt secret message
        encoded_text = ElGamal.encrypt(public_key, message)
        st.write("Encoded Text:", encoded_text)
        # Decrypt message
        received_message = ElGamal.decrypt(secret_key, encoded_text)
        st.write("Received Text:", received_message)
        # st.write(f"{received_message=}")
        # Check if correct
        st.write(message == received_message)


except Exception as x:
    st.markdown(f"⚠️   **{x}**")
