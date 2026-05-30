# STEP 0

import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
df_boston = pd.read_sql("""
SELECT e.firstName, e.lastName, e.jobTitle
FROM Employees e
JOIN Offices o
    ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
SELECT o.officeCode, COUNT(e.employeeNumber) AS num_employees
FROM Offices o
LEFT JOIN Employees e
    ON o.officeCode = e.officeCode
GROUP BY o.officeCode
HAVING COUNT(e.employeeNumber) = 0
""", conn)

# STEP 3
df_employee = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM Employees e
LEFT JOIN Offices o
    ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
df_contacts = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM Customers c
LEFT JOIN Orders o
    ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
""", conn)

# STEP 5
df_payment = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, p.paymentDate,
       CAST(p.amount AS FLOAT) AS amount
FROM Customers c
JOIN Payments p
    ON c.customerNumber = p.customerNumber
ORDER BY amount DESC
""", conn)

# STEP 6
df_credit = pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName,
       COUNT(c.customerNumber) AS num_customers
FROM Employees e
JOIN Customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_customers DESC
""", conn)

# STEP 7
df_product_sold = pd.read_sql("""
SELECT p.productName,
       COUNT(od.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM Products p
JOIN OrderDetails od
    ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC
""", conn)

# STEP 8
df_total_customers = pd.read_sql("""
SELECT p.productName,
       p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM Products p
JOIN OrderDetails od
    ON p.productCode = od.productCode
JOIN Orders o
    ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
""", conn)

# STEP 9
df_customers = pd.read_sql("""
SELECT o.officeCode, o.city,
       COUNT(c.customerNumber) AS n_customers
FROM Offices o
LEFT JOIN Employees e
    ON o.officeCode = e.officeCode
LEFT JOIN Customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
""", conn)

# STEP 10
df_under_20 = pd.read_sql("""
SELECT DISTINCT e.employeeNumber,
       e.firstName,
       e.lastName,
       ofc.city,
       ofc.officeCode
FROM Employees e
JOIN Customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN Orders o
    ON c.customerNumber = o.customerNumber
JOIN OrderDetails od
    ON o.orderNumber = od.orderNumber
JOIN Offices ofc
    ON e.officeCode = ofc.officeCode
WHERE od.productCode IN (
    SELECT od.productCode
    FROM OrderDetails od
    JOIN Orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY od.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)
ORDER BY e.employeeNumber
""", conn)

conn.close()