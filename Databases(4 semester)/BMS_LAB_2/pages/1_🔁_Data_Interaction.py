import mysql.connector
import pandas as pd
import streamlit as st


st.header("Insert Data 📩")

st.subheader("Database Schema:")
st.image("BMS_DIAGRAM_MYSQL.jpg")


conn = mysql.connector.connect(host="localhost",
                               user="root",
                               password="*****",
                               db="BMS")
cursor = conn.cursor()


cursor.execute("Show Tables;")
data = cursor.fetchall()
df = pd.DataFrame(data)

st.subheader("Interaction:")
table = st.selectbox("Select Table for Insertion Data:", df[0])
st.subheader(table + " Insertion")


def get_current_bank_codes():
    cursor.execute("SELECT identification_code FROM Banks;")
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    current_codes = list(df[0])
    return current_codes


if table == "Banks":
    with st.form(table + " Insertion"):
        current_codes = get_current_bank_codes()

        bank_name = st.text_input("Name:")
        country = st.text_input("Country:")
        identification_code = st.number_input("Identification Code:", min_value=max(current_codes) + 1, step=1)

        submitted = st.form_submit_button("Submit")
        if submitted:
            value = f"('{bank_name}', '{country}', {identification_code})"
            cursor.execute("INSERT INTO Banks (name, country, identification_code) VALUES" + value +";")
            conn.commit()
            st.write("Record " + value + " added.")

    st.subheader(table + " Updating")
    with st.form(table + " Updating"):
        current_codes = get_current_bank_codes()

        bank_name = st.text_input("Name:")
        country = st.text_input("Country:")
        identification_code = st.number_input("Identification Code:", min_value=min(current_codes),
                                              max_value=max(current_codes), step=1)

        submitted = st.form_submit_button("Update")
        if submitted:
            cursor.execute(f"UPDATE Banks SET name = '{bank_name}', country = '{country}' WHERE identification_code = {identification_code};")
            conn.commit()
            st.write("Record updated.")

    st.subheader(table + " Deletion")
    with st.form(table + " Deletion"):
        current_codes = get_current_bank_codes()
        identification_code = st.number_input("Identification Code:", min_value=min(current_codes), max_value=max(current_codes), step=1)

        submitted = st.form_submit_button("Delete")
        if submitted:
            cursor.execute("DELETE FROM Banks WHERE identification_code =" + str(identification_code) +" ;")
            conn.commit()
            st.write("Record deleted.")

    show_banks = st.checkbox("Show Banks Table:")
    if show_banks:
        cursor.execute("SELECT * FROM BANKS;")
        data = cursor.fetchall()
        st.table(data)
elif table == "Accounts":
    with st.form(table + " Insertion"):
        current_codes = get_current_bank_codes()
        IBAN = st.number_input("IBAN", step=1)
        type = st.slider("Type", min_value=1, max_value=3)
        balance = st.number_input("Balance")
        opening_date = st.date_input("Opening Date")
        bank_code = st.number_input("Bank Code", min_value=min(current_codes), max_value=max(current_codes), step=1)

        submitted = st.form_submit_button("Submit")
        if submitted:
            value = f"('{IBAN}', '{type}', {balance}, '{opening_date}', {bank_code})"
            cursor.execute("INSERT INTO Accounts (IBAN, type, balance, opening_date, bank_code) VALUES" + value +";")
            conn.commit()
            st.write("Record " + value + " added.")

    st.subheader(table + " Updating")
    with st.form(table + " Updating"):
        current_codes = get_current_bank_codes()
        IBAN = st.number_input("IBAN", step=1)
        type = st.slider("Type", min_value=1, max_value=3)
        balance = st.number_input("Balance")
        opening_date = st.date_input("Opening Date")
        bank_code = st.number_input("Bank Code", min_value=min(current_codes), max_value=max(current_codes),
                                    step=1)

        submitted = st.form_submit_button("Update")
        if submitted:
            cursor.execute(f"UPDATE Accounts SET type = {type}, balance = {balance}, opening_date = '{opening_date}', bank_code = {bank_code} WHERE IBAN = {IBAN};")
            conn.commit()
            st.write("Record updated.")

    st.subheader(table + " Deletion")
    with st.form(table + " Deletion"):
        current_codes = get_current_bank_codes()
        identification_code = st.number_input("IBAN", step=1)

        submitted = st.form_submit_button("Delete")
        if submitted:
            cursor.execute(f"DELETE FROM {table} WHERE IBAN =" + str(IBAN) +" ;")
            conn.commit()
            st.write("Record deleted.")

    show_banks = st.checkbox(f"Show {table} Table:")
    if show_banks:
        cursor.execute(f"SELECT * FROM {table};")
        data = cursor.fetchall()
        st.table(data)
elif table == "Customers":
    pass
elif table == "Filials":
    pass
elif table == "Services":
    pass
elif table == "AvailabilityServiceAccount":
    pass
else:
    pass

