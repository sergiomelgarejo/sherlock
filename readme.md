### Sherlock 🕵🏻🔎

A library that will help you *detect* junk data the way the legendary detective Sherlock Holmes would do.
Sherlock support many source data types such as .csv, .xlsx, .json, relational databases, etc.


#### Set up:

1. ``pyhton3 pip install -r requirements.txt``

2. If you are dealing with a relational database, you need to create a config.json file with all the parameters needed to create the sqlalchemy connection.
[SQLAlchemy](https://www.sqlalchemy.org/).


#### Data cleaning methods:

Sherlock offers 4 methods for detecting corrupted and junk data.

- `buscar_duplicados:` Find duplicated rows.

- `buscar_nulos:` Find null values in a specific column or a set of columns.

- `buscar_no_numericos:` Find non-numeric values in a column restricted to only numeric values.

- `buscar_patron_regex:` Find values that does not match a given Regex pattern.
