# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = """
SELECT firstName, LastName, jobTitle
FROM Employees"""

# STEP 2
# Replace None with your code
df_zero_emp = """
SELECT o.officeCode, COUNT(e.employeeNumber) AS num_employees
FROM Offices o LEFT JOIN Employees e ON o.officeCode = e.officeCode
GROUP BY o.officeCode
HAVING num_employees = 0"""

# STEP 3
# Replace None with your code
df_employee = """
SELECT e.firstName, e.lastName, o.city,o.state
FROM Employees e JOIN Offices o ON e.officeCode = o.officeCode
WHERE o.state IS NOT NULL OR o.city IS NOT NULL
ORDER BY firstName, lastName"""

# STEP 4
# Replace None with your code
df_contacts = """
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM Customers c
LEFT JOIN orders o USING(customerNumber)
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
"""

# Replace None with your code
df_payment = """
SELECT c.contactFirstName, c.contactLastName, paymentDate, CAST(amount AS FLOAT) AS amount
FROM Customers c
JOIN payments p USING(customerNumber)
ORDER BY amount DESC
"""

# STEP 6
# Replace None with your code
df_credit = """
SELET e.employeeNumber, e.firstName,e.lastName, COUNT(DISTINCT c.customerNumber) AS num_customers
FROM Employees e
JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
WHERE c.creditLimit > 90000
GROUP BY e.employeeNumber, e.firstName, e.lastName
ORDER BY num_customers DESC
"""

# STEP 7
# Replace None with your code
df_product_sold = """
SELECT p.productName,
       COUNT(od.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od
    ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC
"""

# STEP 8
# Replace None with your code
df_total_customers = """
SELECT p.productName,
       p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od
    ON p.productCode = od.productCode
JOIN orders o
    ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
"""

# STEP 9
# Replace None with your code

df_customers = """
SELECT o.officeCode,
       o.city,
       COUNT(c.customerNumber) AS n_customers
FROM offices o
JOIN employees e
    ON o.officeCode = e.officeCode
JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
"""

# STEP 10
# Replace None with your code
df_under_20 = """
WITH low_customer_products AS (
    SELECT p.productCode
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)
SELECT DISTINCT e.employeeNumber,
       e.firstName,
       e.lastName,
       ofc.city,
       ofc.officeCode
FROM employees e
JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o
    ON c.customerNumber = o.customerNumber
JOIN orderdetails od
    ON o.orderNumber = od.orderNumber
JOIN low_customer_products lcp
    ON od.productCode = lcp.productCode
JOIN offices ofc
    ON e.officeCode = ofc.officeCode
ORDER BY e.employeeNumber
"""

conn.close()