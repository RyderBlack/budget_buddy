import mysql.connector
import os
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv(".env")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DATABASE_PASSWORD,
    )
    
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS budget_buddy")
    cursor.execute("USE budget_buddy")

    cursor.execute("CREATE TABLE IF NOT EXISTS category (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, category_type VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS user (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255) NOT NULL, forename VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS bank_account (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, account_balance DECIMAL NOT NULL, id_user INT, account_balance DECIMAL NOT NULL, FOREIGN KEY (id_user) REFERENCES user(id))")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_transaction (
        id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        reference VARCHAR(255) NOT NULL,
        description TEXT,
        amount DECIMAL NOT NULL,
        date DATETIME NOT NULL,
        transaction_type VARCHAR(255) NOT NULL,
        id_user INT,
        id_category INT,
        id_bank_account INT,
        FOREIGN KEY (id_user) REFERENCES user(id),
        FOREIGN KEY (id_category) REFERENCES category(id),
        FOREIGN KEY (id_bank_account) REFERENCES bank_account(id)
    )
    """)

    cursor.execute("SHOW TABLES")
    rows = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    print(tabulate(rows, headers=column_names, tablefmt="psql"))

except mysql.connector.Error as e:
    print("Erreur MySQL :", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals() and db.is_connected():
        db.close()
    print("Connexion MySQL fermée.")
