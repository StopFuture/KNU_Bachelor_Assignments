import random
import streamlit as st
from sympy import isprime, mod_inverse
from math import gcd

st.set_page_config(page_title="@pnqwf the best", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

st.title("Rivest–Shamir–Adleman Crypto System")
st.sidebar.success("Select a page above.")


def generate_keypair(keysize):
    # Generate two random prime numbers
    p = q = 1
    while not isprime(p):
        p = random.randrange(2**(keysize-1), 2**keysize)
    while not isprime(q) or p == q:
        q = random.randrange(2**(keysize-1), 2**keysize)

    n = p * q
    phi = (p-1) * (q-1)

    # Choose e
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Compute d
    d = mod_inverse(e, phi)

    # Public key (e, n) and private key (d, n)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    # Convert plaintext to an integer
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    d, n = private_key
    # Generate the plaintext based on the ciphertext and key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)


try:
    st.header("Calculation:")
    st.image("images/rsa_8.jpg")
    inp2 = st.number_input("KeySize: ", value=None, step=1)
    message = st.text_input("Enter a message to encrypt: ", value=None)
    button2 = st.button("Generate KeyPair:")
    if inp2 is not None:
        public, private = generate_keypair(int(inp2))
        if button2:
            st.write("Public key: ", public)
            st.write("Private key: ", private)

            encrypted_msg = encrypt(public, message)
            st.write("Encrypted message: ", encrypted_msg)

            decrypted_msg = decrypt(private, encrypted_msg)
            st.write("Decrypted message: ", decrypted_msg)

except Exception as x:
    st.markdown(f"⚠️   **{x}**")

