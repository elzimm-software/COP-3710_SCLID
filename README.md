# Sclid - Supply Chain Logistics & Inventory Database

Sclid is a supply chain database integrating suppliers, inventory, shipments, and delays.  Includes bottleneck detection queries, trigger-based inventory alerts, and indexed joins.

## Useage

Clone the repo: `git clone https://github.com/elzimm-software/COP-3710_SCLID`

Enter the cloned directory: `cd COP-3710_SCLID`

Initialize a MariaDB instance with a sclid database and user.

Activate the python .venv: `source ./python/.venv/activate`

Install dependencies: `pip install -r python/requirements.txt`

Run preprocessor: `python ./python/preprocessor.py`

Enter MariaDB instance connection info into `loaddata.py` and `app.py`.

Run data load: `python ./python/loaddata.py`

Run application: `python ./python/app.py`

## Scope

It encompases a desktop GUI for inventory management and product order generation, a mobile app for location and price management on the salesfloor, and a point of sale system to tracking outgoing product and KPI generation.  All systems interface with an in-store database to ensure data is synced between all instances.  Order forms can be generated as CSV files for manual ordering or cXML PunchOut for automated ordering.  Products can define minimum quanitiy alerts or leverage algorithmic, smart product ordering which uses historic sales trends to ensure replishment arrives before the product is completely depleted.

## Users

Sclid aims to be a fully qualified inventory management system for single location retail businesses.  In its various forms, it may be used by management, warehouse, and sales personel.

## Datasets

**Products:** https://www.kaggle.com/datasets/salahuddinahmedshuvo/grocery-inventory-and-sales-dataset

**Employees:** https://www.kaggle.com/datasets/abdallahwagih/company-employees

**Sales:** https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset

## DBMS

Sclid uses MariaDB for its serverside portability and stability.
