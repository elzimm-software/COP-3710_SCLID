CREATE TABLE Employee
(
    employee_num INTEGER     NOT NULL,
    first_name   VARCHAR(50) NOT NULL,
    last_name    VARCHAR(50) NOT NULL,
    CONSTRAINT pk_employee PRIMARY KEY (employee_num)
);

CREATE TABLE Stocker
(
    employee_num INTEGER NOT NULL,
    CONSTRAINT pk_stocker PRIMARY KEY (employee_num),
    CONSTRAINT fk_stocker_employee_num FOREIGN KEY (employee_num) REFERENCES Employee (employee_num)
);

CREATE TABLE Cashier
(
    employee_num INTEGER NOT NULL,
    CONSTRAINT pk_cashier PRIMARY KEY (employee_num),
    CONSTRAINT fk_cashier_employee_num FOREIGN KEY (employee_num) REFERENCES Employee (employee_num)
);

CREATE TABLE Manager
(
    employee_num INTEGER NOT NULL,
    CONSTRAINT pk_manager PRIMARY KEY (employee_num),
    CONSTRAINT fk_manager_employee_num FOREIGN KEY (employee_num) REFERENCES Employee (employee_num)
);

CREATE TABLE Salary
(
    employee_num INTEGER        NOT NULL,
    amount       DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_salary PRIMARY KEY (employee_num),
    CONSTRAINT fk_salary_employee_num FOREIGN KEY (employee_num) REFERENCES Employee (employee_num),
    CONSTRAINT ck_salary_amount_gez CHECK ( amount >= 0.00 )
);

CREATE TABLE Hourly
(
    employee_num INTEGER        NOT NULL,
    rate         DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_hourly PRIMARY KEY (employee_num),
    CONSTRAINT fk_hourly_employee_num FOREIGN KEY (employee_num) REFERENCES Employee (employee_num),
    CONSTRAINT ck_salary_rate_gez CHECK ( rate >= 0.00 )
);

CREATE TABLE Shipment
(
    shipment_id   INTEGER  NOT NULL,
    created_at    DATETIME NOT NULL DEFAULT NOW(),
    total_cartons INTEGER  NOT NULL DEFAULT 0,
    CONSTRAINT pk_shipment PRIMARY KEY (shipment_id),
    CONSTRAINT ck_shipment_total_cartons_gez CHECK ( total_cartons >= 0 )
);

CREATE TABLE Supplier
(
    supplier_id  INTEGER     NOT NULL,
    name         VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    CONSTRAINT pk_supplier PRIMARY KEY (supplier_id),
    CONSTRAINT uk_supplier_name UNIQUE (name),
    CONSTRAINT uk_supplier_phone_number UNIQUE (phone_number)
);

CREATE TABLE Product
(
    upc                INTEGER        NOT NULL,
    preferred_supplier INTEGER        NULL,
    sku                VARCHAR(50)    NULL,
    price              DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    quantity           INTEGER        NOT NULL DEFAULT 0.00,
    location           VARCHAR(50)    NULL,
    minimum_quantity   INTEGER        NULL,
    replen_quantity   INTEGER        NULL,
    CONSTRAINT pk_product PRIMARY KEY (upc),
    CONSTRAINT fk_product_preferred_supplier FOREIGN KEY (preferred_supplier) REFERENCES Supplier (supplier_id),
    CONSTRAINT fk_product_minimum_quantity CHECK ( minimum_quantity >= 0 ),
    CONSTRAINT fk_product_replen_quantity CHECK ( replen_quantity >= 0 )
);

CREATE TABLE ProductSupplied
(
    upc            INTEGER        NOT NULL,
    supplier_id    INTEGER        NOT NULL,
    price_per_unit DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    shipping_cost  DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    lead_time      INTEGER        NOT NULL DEFAULT 0,
    CONSTRAINT pk_product_supplied PRIMARY KEY (upc, supplier_id),
    CONSTRAINT fk_product_supplied_upc FOREIGN KEY (upc) REFERENCES Product (upc),
    CONSTRAINT fk_product_supplied_supplier_id FOREIGN KEY (supplier_id) REFERENCES Supplier (supplier_id),
    CONSTRAINT ck_product_supplied_price_per_unit_gez CHECK ( price_per_unit >= 0.00 ),
    CONSTRAINT ck_product_supplied_shipping_cost_gez CHECK ( shipping_cost >= 0.00 ),
    CONSTRAINT ck_product_supplied_lead_time_gez CHECK ( lead_time >= 0 )
);

CREATE TABLE ShipmentReceipt
(
    shipment_id      INTEGER  NOT NULL,
    received_by      INTEGER  NOT NULL,
    received_at      DATETIME NULL     DEFAULT NULL,
    cartons_received INTEGER  NOT NULL DEFAULT 0,
    CONSTRAINT pk_shipment_receipt PRIMARY KEY (shipment_id, received_at),
    CONSTRAINT fk_shipment_receipt_shipment_id FOREIGN KEY (shipment_id) REFERENCES Shipment (shipment_id),
    CONSTRAINT fk_shipment_receipt_received_by FOREIGN KEY (received_by) REFERENCES Stocker (employee_num),
    CONSTRAINT ck_shipment_receipt_cartons_received_gez CHECK ( cartons_received >= 0 )
);

CREATE TABLE ProductShipped
(
    shipment_id INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT pk_product_shipped PRIMARY KEY (shipment_id, product_id, supplier_id),
    CONSTRAINT fk_product_shipped_shipment_id FOREIGN KEY (shipment_id) REFERENCES Shipment (shipment_id),
    CONSTRAINT fk_product_shipped_product_id FOREIGN KEY (product_id) REFERENCES Product (upc),
    CONSTRAINT fk_product_shipped_supplier_id FOREIGN KEY (supplier_id) REFERENCES Supplier (supplier_id),
    CONSTRAINT ck_product_shipped_quantity_gez CHECK ( quantity >= 0 )
);

CREATE TABLE Sale
(
    receipt_num INTEGER        NOT NULL,
    made_at     DATETIME       NOT NULL,
    cashier     INTEGER        NOT NULL,
    total_sale  DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_sale PRIMARY KEY (receipt_num),
    CONSTRAINT fk_sale_cashier FOREIGN KEY (cashier) REFERENCES Cashier (employee_num),
    CONSTRAINT ck_sale_total_sale_gez CHECK ( total_sale >= 0.00 )
);

CREATE TABLE ProductSold
(
    upc         INTEGER        NOT NULL,
    receipt_num INTEGER        NOT NULL,
    sale_price  DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_product_sold PRIMARY KEY (upc, receipt_num),
    CONSTRAINT fk_product_sold_upc FOREIGN KEY (upc) REFERENCES Product (upc),
    CONSTRAINT fk_product_sold_receipt_num FOREIGN KEY (receipt_num) REFERENCES Sale (receipt_num),
    CONSTRAINT ck_product_sold_sale_price_gez CHECK ( sale_price >= 0.00 )
);

CREATE TABLE TransactionDiscount
(
    discount_id     INTEGER        NOT NULL,
    receipt_num     INTEGER        NOT NULL,
    authorizer      INTEGER        NOT NULL,
    discount_amount DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_transaction_discount PRIMARY KEY (discount_id),
    CONSTRAINT fk_transaction_discount_receipt_num FOREIGN KEY (receipt_num) REFERENCES Sale (receipt_num),
    CONSTRAINT fk_transaction_discount_authorizer FOREIGN KEY (authorizer) REFERENCES Manager (employee_num),
    CONSTRAINT ck_transaction_discount_discount_amount_gez CHECK ( discount_amount >= 0.00 )
);

CREATE TABLE LineDiscount
(
    discount_id     INTEGER        NOT NULL,
    upc             INTEGER        NOT NULL,
    receipt_num     INTEGER        NOT NULL,
    authorizer      INTEGER        NOT NULL,
    discount_amount DECIMAL(19, 4) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_line_discount PRIMARY KEY (discount_id),
    CONSTRAINT fk_line_discount_upc_receipt_num FOREIGN KEY (upc, receipt_num) REFERENCES ProductSold (upc, receipt_num),
    CONSTRAINT fk_line_discount_authorizer FOREIGN KEY (authorizer) REFERENCES Manager (employee_num),
    CONSTRAINT ck_line_discount_discount_amount_gez CHECK ( discount_amount >= 0.00 )
);