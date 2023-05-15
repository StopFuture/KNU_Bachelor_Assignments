import streamlit as st
import mysql.connector
import pandas as pd
st.header("Сomplex Queries 🔥")
conn = mysql.connector.connect(host="localhost",
                               user="root",
                               password="****",
                               db="BMS")
cursor = conn.cursor()

st.code("1. Знайти філіали банків у яких такий самий набір послуг, як у філіала ... :", language="sql")
with st.form("query1"):
    query1 = '''
    SELECT 
        DISTINCT f2.filial_code, f2.address
    FROM 
        Filials f1
    JOIN 
        Services s1 ON f1.filial_code = s1.filial_code
    JOIN 
        Filials f2 ON s1.filial_code = f2.filial_code
    WHERE f1.filial_code = X
        AND NOT EXISTS (
        SELECT 
            s3.type
        FROM 
            Services s3
        JOIN 
            Filials f3 ON s3.filial_code = f3.filial_code
        WHERE 
            f3.filial_code <> f1.filial_code
          AND s3.type NOT IN (
            SELECT 
                s4.type
            FROM 
                Services s4
            WHERE 
                s4.filial_code = f1.filial_code
          )
          AND f3.filial_code = f2.filial_code
  );

    '''
    st.code(query1, language="sql")
    X = st.number_input("FilialCode X:", step=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
        SELECT 
            DISTINCT f2.filial_code, f2.address
FROM Filials f1
JOIN Services s1 ON f1.filial_code = s1.filial_code
JOIN Filials f2 ON s1.filial_code = f2.filial_code
WHERE f1.filial_code = {X}
  AND NOT EXISTS (
    SELECT s3.type
    FROM Services s3
    JOIN Filials f3 ON s3.filial_code = f3.filial_code
    WHERE f3.filial_code <> f1.filial_code
      AND s3.type NOT IN (
        SELECT s4.type
        FROM Services s4
        WHERE s4.filial_code = f1.filial_code
      )
      AND f3.filial_code = f2.filial_code
  );

''')
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)

st.code("2. Знайти клієнтів, в яких є акаунти таких самих типів, як і у клієнта з Id ... :", language="sql")
with st.form("query2"):
    query1 = '''
    SELECT 
    Customers.*
FROM 
    Customers
WHERE NOT EXISTS
      (SELECT 
            DISTINCT A.type 
       FROM 
            Customers C
       INNER JOIN OwnershipAccountCustomer OAC on C.id = OAC.customer_id
       INNER JOIN Accounts A on A.IBAN = OAC.IBAN
       WHERE 
            C.id = Х
       EXCEPT
       SELECT DISTINCT A1.type
       FROM Accounts A1
       INNER JOIN OwnershipAccountCustomer OAC1 on A1.IBAN = OAC1.IBAN 
       WHERE OAC1.customer_id = Customers.id
);
    '''
    st.code(query1, language="sql")
    X = st.number_input("Id X:", min_value=1, step=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
        SELECT Customers.*
FROM Customers
WHERE NOT EXISTS
      (SELECT DISTINCT A.type 
       FROM Customers C
       INNER JOIN OwnershipAccountCustomer OAC on C.id = OAC.customer_id
       INNER JOIN Accounts A on A.IBAN = OAC.IBAN
       WHERE C.id = {X}
       EXCEPT
       SELECT DISTINCT A1.type
       FROM Accounts A1
       INNER JOIN OwnershipAccountCustomer OAC1 on A1.IBAN = OAC1.IBAN 
       WHERE OAC1.customer_id = Customers.id
);
''')
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)

st.code("3. Знайти банки, що надають усі послуги, які доступні в банку з певним\n"
        " ідентифікаційним кодом X ... :", language="sql")
with st.form("query3"):
    query1 = '''
    SELECT 
        b.name
    FROM 
        Banks b
    WHERE NOT EXISTS (
        SELECT 
            f1.filial_code
        FROM 
            Filials f1
        WHERE 
            f1.bank_code = X
        AND NOT EXISTS (
            SELECT 
                s1.type
            FROM 
                Services s1
            WHERE 
                s1.filial_code = f1.filial_code
            AND NOT EXISTS (
                SELECT 
                    f2.filial_code
                FROM 
                    Filials f2
                INNER JOIN Services s2 ON f2.filial_code = s2.filial_code
                WHERE 
                    f2.bank_code <> X
                AND 
                    s2.type = s1.type
            )
        )
);
    '''
    st.code(query1, language="sql")
    X = st.number_input("Bank_code X:", step=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
        SELECT b.name
FROM Banks b
WHERE NOT EXISTS (
    SELECT f1.filial_code
    FROM Filials f1
    WHERE f1.bank_code = {X}
    AND NOT EXISTS (
        SELECT s1.type
        FROM Services s1
        WHERE s1.filial_code = f1.filial_code
        AND NOT EXISTS (
            SELECT f2.filial_code
            FROM Filials f2
            INNER JOIN Services s2 ON f2.filial_code = s2.filial_code
            WHERE f2.bank_code <> {X}
            AND s2.type = s1.type
        )
    )
);
''')
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)
