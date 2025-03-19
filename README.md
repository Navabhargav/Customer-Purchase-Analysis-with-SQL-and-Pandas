# 🛒 Customer Purchase Analysis with SQL and Pandas  

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/) 
[![Pandas](https://img.shields.io/badge/Pandas-Dataframe-orange)](https://pandas.pydata.org/)  
[![SQL](https://img.shields.io/badge/SQL-Query-green)](https://www.mysql.com/)

---

## 📌 **Project Overview**
This project focuses on analyzing customer purchases using **SQL and Python (Pandas)**.  
It involves:
✔ Cleaning and formatting SQL queries for better readability.  
✔ Translating the SQL query logic into **Python using Pandas**.  
✔ Filtering high-value purchases while ensuring product pricing is applied within a valid time frame.  
✔ Identifying **frequent buyers** (customers with **10 or more** purchases).  

---

## 📊 **Dataset Description**
### **1. customer_purchases.csv**
| **Column Name** | **Description** |
|---------------|----------------|
| `customer_id` | Unique ID for each customer |
| `product_id`  | ID of the purchased product |
| `quantity`    | Number of items purchased |
| `purchase_date` | Date when the purchase was made |
| `country`     | Country of the customer |

### **2. product_price.csv**
| **Column Name** | **Description** |
|---------------|----------------|
| `product_id`  | ID of the product |
| `price`       | Price of the product |
| `valid_from`  | Start date for the product price validity |
| `valid_to`    | End date for the product price validity (NULL if still valid) |

---

## ⚙️ **Steps Implemented**
### **1. SQL Query Reformatted**
- Improved query structure for readability.
- Ensured **customer filtering (≥10 purchases)** is applied correctly.
- Fixed **trailing commas and missing `GROUP BY` fields**.

### **2. SQL Query to Python Conversion (Using Pandas)**
- Read **CSV files into Pandas DataFrames**.
- Performed **LEFT JOIN** on `customer_purchases` and `product_price`.
- Applied **conditional filtering** to exclude purchases below a threshold.
- Implemented **grouping and aggregation** to calculate total purchase value.

---

## 📝 **SQL Query**
```sql
SELECT 
    cp.product_id, 
    SUM(
        CASE 
            WHEN cp.quantity * pp.price < 50 THEN 0 
            ELSE cp.quantity * pp.price 
        END
    ) AS total, 
    cp.country
FROM customer_purchases cp
LEFT JOIN product_price pp 
    ON cp.product_id = pp.product_id
WHERE 
    cp.purchase_date >= pp.valid_from 
    AND (cp.purchase_date <= pp.valid_to OR pp.valid_to IS NULL)
    AND cp.customer_id IN (
        SELECT customer_id 
        FROM customer_purchases 
        GROUP BY customer_id 
        HAVING COUNT(*) >= 10
    )
GROUP BY cp.product_id, cp.country 
ORDER BY total DESC;
