from importlib.resources import path
import pyodbc
import pandas as pd
from datetime import datetime
from pathlib import Path

conn = pyodbc.connect('Driver={SQL Server};'
            'Server=DESKTOP-MATEUS;'
            'Database=AdventureWorks2019;'
            'Trusted_Connection=yes;')

date = datetime.today().strftime('%d')
conv=int(date)*100
topn=str(conv)

df = pd.read_sql_query(f"""SELECT TOP ({topn})
    [Sales].[SalesOrderHeader].[CustomerID], CONCAT([Person].[Person].[FirstName],' ', [Person].[Person].[LastName]) AS CustomerName, 
    [Person].[Address].[City], [Person].[StateProvince].[Name] AS 'State', [Person].[CountryRegion].[Name] 'Country',
    [Sales].[SalesOrderHeader].[OrderDate],
    [Sales].[SalesOrderDetail].[SalesOrderID],
    [Person].[Address].[PostalCode],
    [Production].[Product].[Name] AS 'ProductName',
    [Purchasing].[ShipMethod].[Name] AS 'ShipMethod',
    [Purchasing].[PurchaseOrderHeader].[Status], 
    [Purchasing].[PurchaseOrderHeader].[ShipDate],
    [Sales].[SalesOrderDetail].[UnitPriceDiscount] AS 'Discount',
    [Sales].[SalesOrderHeader].[SubTotal] AS 'Sales'
    FROM [Person].[Person]
    INNER JOIN [Sales].[SalesPerson] ON [Sales].[SalesPerson].[BusinessEntityID] = [Person].[Person].[BusinessEntityID]
    INNER JOIN [Sales].[SalesOrderHeader] ON [Sales].[SalesPerson].[TerritoryID] = [Sales].[SalesOrderHeader].[TerritoryID]
    INNER JOIN [Purchasing].[ShipMethod] ON [Sales].[SalesOrderHeader].[ShipMethodID] = [Sales].[SalesOrderHeader].[ShipMethodID]
    INNER JOIN [Purchasing].[PurchaseOrderHeader] ON  [Purchasing].[ShipMethod].ShipMethodID = [Purchasing].[PurchaseOrderHeader].[ShipMethodID]
    INNER JOIN [Sales].[SalesOrderDetail] ON [Sales].[SalesOrderHeader].[SalesOrderID] = [Sales].[SalesOrderDetail].[SalesOrderID]
    INNER JOIN [Production].[Product] ON [Sales].[SalesOrderDetail].[ProductID] = [Production].[Product].[ProductID]
    INNER JOIN [Person].[StateProvince] ON [Sales].[SalesPerson].[TerritoryID] = [Person].[StateProvince].[TerritoryID]
    INNER JOIN [Person].[CountryRegion] ON [Person].[StateProvince].[CountryRegionCode] = [Person].[CountryRegion].[CountryRegionCode]
    INNER JOIN [Person].[Address] ON [Person].[StateProvince].[StateProvinceID] = [Person].[Address].[StateProvinceID];""", conn)

#armazenando os dados da query dentro de um dataframe
data = pd.DataFrame(df, columns=["CustomerID", "CustomerName", "State", "Country", "SalesOrderID", "PostalCode", "ProductName", "ShipMethod", "Discount", "Sales"])

filename='Sales'
date = datetime.today().strftime('%Y-%m-%d')
filepath = Path(f"..\datasource\{filename}_{date}.csv")
data.to_csv(filepath)