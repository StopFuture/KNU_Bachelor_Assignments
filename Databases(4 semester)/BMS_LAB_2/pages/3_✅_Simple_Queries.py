import streamlit as st
import mysql.connector
import pandas as pd
st.header("Simple Queries ✅")
conn = mysql.connector.connect(host="localhost",
                               user="root",
                               password="*****",
                               db="BMS")
cursor = conn.cursor()


st.code("1. Знайти всі філіали банків, що знаходяться в ... :", language="sql")
with st.form("query1"):
    query1 = '''
    SELECT Filials.*
    FROM Filials
    JOIN Banks ON Filials.bank_code = Banks.identification_code
    WHERE Banks.country = X;
    '''
    st.code(query1, language="sql")
    X = st.text_input("Country X:")

    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f" SELECT Filials.* FROM Filials JOIN Banks ON Filials.bank_code = Banks.identification_code WHERE Banks.country = '{X}';")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)

st.code("2. Знайти банківські рахунки типу ... в філіалі ... :", language="sql")
with st.form("query2"):
    query1 = '''
    SELECT 
        a.IBAN, a.type, a.balance, b.name AS bank_name, f.address AS filial_address
    FROM 
        Accounts a
    JOIN 
        Banks b ON a.bank_code = b.identification_code
    JOIN 
        Filials f ON a.bank_code = f.bank_code
    WHERE 
        a.type = X AND f.filial_code = Y;
    '''

    st.code(query1, language="sql")
    X = st.selectbox("Type Х:", [1,2,3])
    Y = st.number_input("FilialCode Y:", step = 1)

    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''SELECT a.IBAN, a.type, a.balance, b.name AS bank_name, f.address AS filial_address
    FROM Accounts a
    JOIN Banks b ON a.bank_code = b.identification_code
    JOIN Filials f ON a.bank_code = f.bank_code
    WHERE a.type = {X} AND f.filial_code = {Y};''')
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)

st.code("3. Знайти інформацію про послуги, доступні в певному філіалі банку ... :", language="sql")
with st.form("query3"):
    query1 = '''
    SELECT 
        s.type, s.involved, s.price, f.filial_code, f.address AS filial_address
    FROM 
        Services s
    JOIN 
        Filials f ON s.filial_code = f.filial_code
    WHERE 
        f.bank_code = Х;
    '''
    st.code(query1, language="sql")
    X = st.number_input("Bank_code X:", min_value=1001, step=1)

    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
        SELECT 
            s.type, s.involved, s.price, f.filial_code, f.address AS filial_address
        FROM 
            Services s
        JOIN 
            Filials f ON s.filial_code = f.filial_code
        WHERE 
            f.bank_code = {X};''')
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)

st.code("4. Знайти середнє значення балансу рахунків певного типу ... в усіх філіалах певного банку ... :", language="sql")
with st.form("query4"):
    query1 = '''
    SELECT 
        f.filial_code, f.address AS filial_address, AVG(a.balance) AS average_balance
    FROM 
        Filials f
    JOIN 
        Accounts a ON f.bank_code = a.bank_code
    WHERE 
        a.type = Х AND f.bank_code = Y
    GROUP BY 
        f.filial_code;

    '''
    st.code(query1, language="sql")
    X = st.selectbox("Type Х:", [1, 2, 3])
    Y = st.number_input("Bank_code Y:", min_value=1001, step=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
        
    SELECT 
        f.filial_code, f.address AS filial_address, AVG(a.balance) AS average_balance
    FROM 
        Filials f
    JOIN 
        Accounts a ON f.bank_code = a.bank_code
    WHERE 
        a.type = {X} AND f.bank_code = {Y}
    GROUP BY 
        f.filial_code;
''')
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)

st.code("5. Знайти філіали банків, які мають певний тип послуги ... :", language="sql")
with st.form("query5"):
    query1 = '''
    SELECT 
        Filials.*
    FROM 
        Filials
    JOIN 
        Banks ON Filials.bank_code = Banks.identification_code
    JOIN 
        Services ON Filials.filial_code = Services.filial_code
    WHERE 
        Services.type = X;
    '''
    st.code(query1, language="sql")
    query2 = '''Select type from services;'''
    cursor.execute(query2)
    data = pd.DataFrame(cursor.fetchall())
    X = st.selectbox("Type Х:", data)

    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
        SELECT 
            Filials.*
        FROM 
            Filials
        JOIN 
            Banks ON Filials.bank_code = Banks.identification_code
        JOIN 
            Services ON Filials.filial_code = Services.filial_code
        WHERE 
            Services.type = '{X}';
        ''')
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)
