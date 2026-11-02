Create DATABASE EcommerceCustomerAnalytics;

--CHECK ROW COUNTS AFTER IMPORT

SELECT COUNT(*) AS Rows_2009_2010 From dbo.[Year 2009-2010];
SELECT COUNT(*) AS Rows_2010_2011 From dbo.[Year 2010-2011];

DROP TABLE IF EXISTS dbo.RetailCombined;

--CONVERT BOTH YEARS AND CONVERT TYPE SAFELY (Means combine both csv file in one table with union all to keep duplicate also an in one table that name is Retailcombined)
SELECT 
   Invoice, StockCode, Description, 
   TRY_CONVERT(int,Quantity) AS Quantity,
   COALESCE(
        TRY_CONVERT(datetime2, InvoiceDate, 120),
        TRY_CONVERT(datetime2, InvoiceDate, 105)
   ) as InvoiceDate,
   TRY_CONVERT(decimal(10,2), Price) as Price,
   customer_ID, Country, '2009-2010' AS SourceSheet
   INTO dbo.RetailCombined
   from dbo.[year 2009-2010]

UNION ALL

SELECT 
   Invoice, StockCode, Description, 
   TRY_CONVERT(int,Quantity) AS Quantity,
   COALESCE(
        TRY_CONVERT(datetime2, InvoiceDate, 120),
        TRY_CONVERT(datetime2, InvoiceDate, 105)
   ) as InvoiceDate,
   TRY_CONVERT(decimal(10,2), Price) as Price,
   customer_ID, Country, '2010-2011' AS SourceSheet
   from dbo.[year 2010-2011];

select count(*) as TotalRows from dbo.RetailCombined;

--CONFIRM THE CONVERSION WORKED CLEANLY
--( Means checck how may rows come and also count any null or fialse value
SELECT COUNT(*) AS Total_Rows from dbo.RetailCombined;
Select count(*) As Failed_Dates From dbo.RetailCombined where InvoiceDate is Null;
SELECT COUNT(*) AS Failed_Priices from dbo.RetailCombined where Price IS NULL;
SELECT COUNT(*) As Failed_Quantity from dbo.RetailCombined where Quantity is null;

--(date range per sheet)
SELECT SourceSheet, Min(InvoiceDate) As FirstDate,Max(InvoiceDate) AS LastDate,
count(*) AS Row_count from dbo.RetailCombined
group by SourceSheet;

--DATA EXPLORATION
-- CHECK 1- MISSING CUSTOMER ID
SELECT COUNT(*) AS Missing_CustomerId 
FROM DBO.RetailCombined where Customer_ID IS NULL;

--check 2- NEGETIVE OR ZERO QUANTITY
SELECT COUNT(*) AS Negetive_Qty
from dbo.RetailCombined where Quantity <= 0;


--CHECK 3 - MISSING DESCRIPTION
SELECT COUNT(*) AS Missing_Description
from dbo.RetailCombined where Description IS NULL;


--CHECK 4 - EXACT DUPLICTAE ROWS
SELECT Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer_ID, Country,
count(*) as ExactDupeCount
from dbo.RetailCombined
Group by Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer_ID, Country
having count(*) > 1;


DROP TABLE RetailCleaned;

--DUPLICATE AND PRODUCE THE FINAL CLEANED TABLE(use winndow function)
WITH Deduped AS(
   Select *,
   Row_Number() OVER(
       PARTITION BY Invoice, stockCode, Description, Quantity, InvoiceDate, Price, Customer_ID, Country
       ORDER BY (SELECT NULL)
   ) as RowNum
   From dbo.RetailCombined
) 
SELECT Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer_ID, Country, SourceSheet
INTO dbo.RetailCleaned
from Deduped
where RowNum = 1;

select * from dbo.RetailCleaned;