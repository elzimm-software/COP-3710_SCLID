import mysql.connector
from mysql.connector import Error


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="student",
        password="studentpass",
        database="sclid"
    )


def print_rows(rows, headers):
    if not rows:
        print("\nNo results found.\n")
        return

    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))

    line = " | ".join(str(headers[i]).ljust(widths[i]) for i in range(len(headers)))
    sep = "-+-".join("-" * widths[i] for i in range(len(headers)))

    print()
    print(line)
    print(sep)
    for row in rows:
        print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row))))
    print()


def feature_1_low_stock(cursor):
    query = """
        SELECT
            upc,
            sku,
            quantity,
            minimum_quantity,
            replen_quantity,
            location
        FROM Product
        WHERE minimum_quantity IS NOT NULL
          AND quantity < minimum_quantity
        ORDER BY quantity ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    print("\nProducts Below Minimum Stock")
    print_rows(rows, ["UPC", "SKU", "Qty", "Min Qty", "Replen Qty", "Location"])


def feature_2_products_with_supplier(cursor):
    query = """
        SELECT
            p.upc,
            p.sku,
            p.price,
            p.quantity,
            p.location,
            s.supplier_id,
            s.name AS supplier_name,
            s.phone_number
        FROM Product p
        LEFT JOIN Supplier s
            ON p.preferred_supplier = s.supplier_id
        ORDER BY p.upc;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    print("\nProducts with Preferred Supplier")
    print_rows(rows, ["UPC", "SKU", "Price", "Qty", "Location", "Supplier ID", "Supplier Name", "Phone"])


def feature_3_products_by_supplier(cursor):
    supplier_id = input("Enter supplier ID: ").strip()
    query = """
        SELECT
            s.supplier_id,
            s.name AS supplier_name,
            p.upc,
            p.sku,
            ps.price_per_unit,
            ps.shipping_cost,
            ps.lead_time
        FROM Supplier s
        JOIN ProductSupplied ps
            ON s.supplier_id = ps.supplier_id
        JOIN Product p
            ON ps.upc = p.upc
        WHERE s.supplier_id = %s
        ORDER BY p.upc;
    """
    cursor.execute(query, (supplier_id,))
    rows = cursor.fetchall()
    print(f"\nProducts Supplied by Supplier {supplier_id}")
    print_rows(rows, ["Supplier ID", "Supplier Name", "UPC", "SKU", "Unit Price", "Shipping Cost", "Lead Time"])


def feature_4_shipment_details(cursor):
    shipment_id = input("Enter shipment ID: ").strip()
    query = """
        SELECT
            sh.shipment_id,
            sh.created_at,
            sh.total_cartons,
            p.upc,
            p.sku,
            s.supplier_id,
            s.name AS supplier_name,
            ps.quantity
        FROM Shipment sh
        JOIN ProductShipped ps
            ON sh.shipment_id = ps.shipment_id
        JOIN Product p
            ON ps.product_id = p.upc
        JOIN Supplier s
            ON ps.supplier_id = s.supplier_id
        WHERE sh.shipment_id = %s
        ORDER BY p.upc;
    """
    cursor.execute(query, (shipment_id,))
    rows = cursor.fetchall()
    print(f"\nShipment Details for Shipment {shipment_id}")
    print_rows(rows, ["Shipment ID", "Created At", "Cartons", "UPC", "SKU", "Supplier ID", "Supplier Name", "Qty Shipped"])


def feature_5_sales_and_discounts(cursor):
    receipt_num = input("Enter receipt number: ").strip()
    query = """
        SELECT
            s.receipt_num,
            s.made_at,
            s.total_sale,
            s.cashier,
            p.upc,
            p.sku,
            ps.sale_price,
            td.discount_amount AS transaction_discount,
            ld.discount_amount AS line_discount
        FROM Sale s
        JOIN ProductSold ps
            ON s.receipt_num = ps.receipt_num
        JOIN Product p
            ON ps.upc = p.upc
        LEFT JOIN TransactionDiscount td
            ON s.receipt_num = td.receipt_num
        LEFT JOIN LineDiscount ld
            ON ps.upc = ld.upc
           AND ps.receipt_num = ld.receipt_num
        WHERE s.receipt_num = %s
        ORDER BY p.upc;
    """
    cursor.execute(query, (receipt_num,))
    rows = cursor.fetchall()
    print(f"\nSale and Discounts for Receipt {receipt_num}")
    print_rows(
        rows,
        ["Receipt #", "Made At", "Total Sale", "Cashier", "UPC", "SKU", "Sale Price", "Txn Discount", "Line Discount"]
    )


def show_menu():
    print("\nSupply Chain Logistics & Inventory Database")
    print("1. View products below minimum stock")
    print("2. View products with preferred supplier")
    print("3. View all products supplied by a supplier")
    print("4. View shipment details by shipment ID")
    print("5. View sales and discounts by receipt number")
    print("0. Exit")


def main():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Connected to database successfully.")

        while True:
            show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                feature_1_low_stock(cursor)
            elif choice == "2":
                feature_2_products_with_supplier(cursor)
            elif choice == "3":
                feature_3_products_by_supplier(cursor)
            elif choice == "4":
                feature_4_shipment_details(cursor)
            elif choice == "5":
                feature_5_sales_and_discounts(cursor)
            elif choice == "0":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.\n")

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()