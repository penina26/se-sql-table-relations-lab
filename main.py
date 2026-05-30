import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")

df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM Employees
WHERE officeCode IN (
    SELECT officeCode
    FROM Offices
    WHERE city = 'Boston'
)
""", conn)

df_zero_emp = pd.read_sql("""
SELECT o.officeCode, COUNT(e.employeeNumber) AS num_employees
FROM Offices o
LEFT JOIN Employees e ON o.officeCode = e.officeCode
GROUP BY o.officeCode
HAVING COUNT(e.employeeNumber) = 0
""", conn)

df_employee = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM Employees e
JOIN Offices o ON e.officeCode = o.officeCode
WHERE o.state IS NOT NULL AND o.city IS NOT NULL
ORDER BY e.firstName, e.lastName
""", conn)

df_contacts = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM Customers c
LEFT JOIN Orders o USING(customerNumber)
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
""", conn)

df_payment = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, p.paymentDate, CAST(p.amount AS FLOAT) AS amount
FROM Customers c
JOIN Payments p USING(customerNumber)
ORDER BY amount DESC
""", conn)

df_credit = pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName,
       COUNT(DISTINCT c.customerNumber) AS num_customers
FROM Employees e
JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
WHERE c.creditLimit > 90000
GROUP BY e.employeeNumber, e.firstName, e.lastName
ORDER BY num_customers DESC
""", conn)

df_product_sold = pd.read_sql("""
SELECT p.productName,
       COUNT(od.orderNumber) AS numorders,
       SUM(od.quantityOrdered) AS totalunits
FROM Products p
JOIN OrderDetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC
""", conn)

df_total_customers = pd.read_sql("""
SELECT p.productName,
       p.productCode,
       COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM Products p
JOIN OrderDetails od ON p.productCode = od.productCode
JOIN Orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
""", conn)

df_customers = pd.read_sql("""
SELECT o.officeCode,
       o.city,
       COUNT(c.customerNumber) AS n_customers
FROM Offices o
JOIN Employees e ON o.officeCode = e.officeCode
JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY n_customers DESC
""", conn)

df_under_20 = pd.read_sql("""
WITH low_customer_products AS (
    SELECT p.productCode
    FROM Products p
    JOIN OrderDetails od ON p.productCode = od.productCode
    JOIN Orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)
SELECT DISTINCT e.employeeNumber,
       e.firstName,
       e.lastName,
       ofc.city,
       ofc.officeCode
FROM Employees e
JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN Orders o ON c.customerNumber = o.customerNumber
JOIN OrderDetails od ON o.orderNumber = od.orderNumber
JOIN low_customer_products lcp ON od.productCode = lcp.productCode
JOIN Offices ofc ON e.officeCode = ofc.officeCode
ORDER BY e.employeeNumber
""", conn)

conn.close()