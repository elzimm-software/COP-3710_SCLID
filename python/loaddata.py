import pandas as pd
import random as rng
import mariadb as mdb

import secret

emp_data = pd.read_csv("data/generated/employee.csv")
csh_data = emp_data.loc[emp_data["is_cashier"], ["employee_num"]]
stk_data = emp_data.loc[emp_data["is_stocker"], ["employee_num"]]
mng_data = emp_data.loc[emp_data["is_manager"], ["employee_num"]]
slry_data = emp_data[["employee_num", "salary"]]
emp_data.drop(columns = ["is_cashier", "is_manager", "is_stocker", "salary"], inplace=True)

splr_data = pd.read_csv("data/generated/supplier.csv")
splr_data["phone_number"] = splr_data["supplier_id"].apply(lambda x: f"{rng.randrange(0, 1000)}{rng.randrange(0, 1000)}{rng.randrange(0, 1000)}")

prod_data = pd.read_csv("data/generated/product.csv")
prod_data["location"] = prod_data["upc"].apply(lambda x: "")

prodsup_data =pd.read_csv("data/generated/product_supplied.csv")

sale_data = pd.read_csv("data/generated/sale.csv")

def make_tuple(df):
    return list(df.itertuples(index=False, name=None))

employee = make_tuple(emp_data)
stocker = make_tuple(stk_data)
cashier = make_tuple(csh_data)
manager = make_tuple(mng_data)
salary = make_tuple(slry_data)
supplier = make_tuple(splr_data)
product = make_tuple(prod_data)
product_supplied = make_tuple(prodsup_data)
sale_data["cashier"] = sale_data["cashier"].apply(lambda x: rng.choice(cashier)[0])
product_sold = []
for i in range(1, sale_data.shape[0]):
    n_items = rng.randrange(1, 10)
    tot_price = 0.00
    added_prod=[0]
    for j in range(0, n_items):
        prod=(0,0,0)
        while prod[0] in added_prod:
            prod = rng.choice(product)
        added_prod.append(prod[0])
        product_sold.append((prod[0], i, prod[3]))
        tot_price += prod[3]
    sale_data.loc[sale_data["receipt_num"] == i, "total_sale"] = tot_price
sale = make_tuple(sale_data)

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "admin",
    "password": secret.admin_pass,
    "database": "sclid",
}

conn = mdb.connect(**db_config)
cursor = conn.cursor()

def do_insert(table, width, vals):
    sql = f"INSERT INTO {table} VALUES ({'?,' * (width - 1)}?)"
    try:
        cursor.executemany(sql, vals)
        conn.commit()
    except mdb.Error as e:
        print(f"Error: {e}")
        conn.rollback()

do_insert("employee", 3, employee)
do_insert("stocker", 1, stocker)
do_insert("cashier", 1, cashier)
do_insert("manager", 1, manager)
do_insert("salary", 2, salary)
do_insert("supplier", 3, supplier)
do_insert("product", 8, product)
do_insert("productsupplied", 5, product_supplied)
do_insert("sale", 4, sale)
do_insert("productsold", 3, product_sold)

conn.close()