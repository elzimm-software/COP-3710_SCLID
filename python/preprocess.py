import pandas as pd
import random as rng

rng.seed()
gi_data = pd.read_csv("data/Grocery_Inventory_and_Sales_Dataset.csv")
emp_data = pd.read_excel("data/Employees.xlsx")
sale_data = pd.read_csv("data/retail_sales_dataset.csv")
employee = pd.DataFrame(columns=["employee_num", "first_name", "last_name", "is_cashier", "is_manager", "is_stocker", "salary"]);
employee["employee_num"] = emp_data["No"]
employee["first_name"] = emp_data["First Name"]
employee["last_name"] = emp_data["Last Name"]
employee["is_cashier"] = emp_data["No"].apply(lambda x: rng.random() > 0.5)
employee["is_manager"] = emp_data["No"].apply(lambda x: rng.random() > 0.5)
employee["is_stocker"] = emp_data["No"].apply(lambda x: rng.random() > 0.5)
employee["salary"] = emp_data["Monthly Salary"]
sale = pd.DataFrame(columns=["receipt_num", "made_at", "cashier", "total_sale"])
sale["receipt_num"] = sale_data["Transaction ID"]
sale["made_at"] = sale_data["Date"]
supplier = pd.DataFrame(columns=["supplier_id", "name", "phone_number"])
supplier["supplier_id"] = gi_data["Supplier_ID"].apply(lambda x: x.replace("-", ""))
supplier["name"] = gi_data["Supplier_Name"]
supplier.drop_duplicates(subset="supplier_id", inplace=True)
supplier.drop_duplicates(subset="name", inplace=True)
product = pd.DataFrame(columns=["upc", "preferred_supplier", "sku", "price", "quantity", "location", "minimum_quantity", "replen_quantity"])
product["upc"]=gi_data["Product_ID"].apply(lambda x: x.replace("-", ""))
product["sku"] = gi_data["Product_Name"].apply(lambda x: x.lower().replace(" ", "-").replace("-(", "_").replace(")", ""))
product["preferred_supplier"] = gi_data["Supplier_ID"].apply(lambda x: x.replace("-", ""))
product["price"] = gi_data["Unit_Price"].apply(lambda x: round(float(x.replace("$", "")) * (rng.random() + 1), 2)) # random markup
product["minimum_quantity"] = gi_data["Reorder_Level"]
product["quantity"] = gi_data["Stock_Quantity"]
product["replen_quantity"] = gi_data["Reorder_Quantity"]
product = product[product["preferred_supplier"].isin(supplier["supplier_id"])]
product_supplied = pd.DataFrame(columns=["upc", "supplier_id", "price_per_unit", "shipping_cost", "lead_time"])
product_supplied["upc"] = product["upc"]
product_supplied["supplier_id"] = product["preferred_supplier"]
product_supplied["price_per_unit"] = gi_data["Unit_Price"].apply(lambda x: x.replace("$", ""))
product_supplied["shipping_cost"] = product_supplied["price_per_unit"].apply(lambda x: round(rng.randrange(0, int(float(x)) // 3 + 1) + rng.randrange(1, 100) / 100.0, 2))
product_supplied["lead_time"] = product_supplied["upc"].apply(lambda x: rng.randrange(1, 30))
product_supplied.to_csv("data/generated/product_supplied.csv", index=False)
supplier.to_csv("data/generated/supplier.csv", index=False)
product.to_csv("data/generated/product.csv", index=False)
sale.to_csv("data/generated/sale.csv", index=False)
employee.to_csv("data/generated/employee.csv", index=False)