-- create sales database
create database [sales database];

--use sales database
use [sales database];


-- creating a table with more columns , including a varchar columns
CREATE TABLE Sales(
  ProductId Int,
  saleDate Date,
  Quantity int,
  TotalAmount Decimal(10, 2),
  CustomerId int,
  StoreId int,
  SalespersonId int,
  PaymentMethod Varchar(50) 


);

---inserting data into the sales table
INSERT INTO Sales(ProductId,saleDate,Quantity,TotalAmount,CustomerId,StoreId,SalespersonId,PaymentMethod)
values
(1, '2023-08-01',10,200.00,101,1,201,'Credit card'),
(2, '2023-08-02',5,150.00,102,1,202,'Cash'),
(1, '2023-08-03',8,160.00,103,2,203,'Credit card'),
(2, '2023-08-01',7,210.00,104,2,204,'Cash'),
(3, '2023-08-03',6,122.00,105,1,201,NULL),
(1, '2023-08-01',12,300.00,106,3,205,'Credit card'),
(2, '2023-08-04',5,100.00,107,3,206,'Debit card'),
(2, '2023-08-05',9,270.00,108,1,202,NULL),
(3, '2023-08-05',17,375.00,108,1,207,'Cash'),
(1, '2023-08-06',7,140.00,110,2,203,'Credit card');


-- check the all records
select * from Sales;


--GROUP BY WITH AGGERGATE FUNCTION
--1 find the maximum amount in sales
select max(TotalAmount) as MaximumAmount  from Sales;

--2 find the maximum sale date from the table
SELECT Max(SaleDate) as Maximumdate from Sales;

--find the highest paymant method from table
SELECT Max(PaymentMethod) as Method from Sales;

--find out maximum quanttiy sold for each product id
select productId,  max(Quantity)  as highest_quantity from Sales
group by ProductId;

--find out maximum total amount for all distinct dates in sales date column
select saleDate , max(TotalAmount) as Maximum_TotalAmount 
from sales
group by saleDate;


--find minimum quantity from table
SELECT MIN(Quantity) as Min_Quanttiy from Sales;

--find out minimum amout from date column
SELECT MIN(SaleDate) as Min_date from sales;

--find out minimum method amount
SELECT MIN(PaymentMethod) as min_method from sales;

--find out minimum totalAmount sold for each product id
Select ProductId, min(TotalAmount) as MIn_TotalAmount from sales
group by ProductId;

--find out the sum of quantity in sales table
SELECT SUM(Quantity) as total_Quantity from sales;
SELECT SUM(Quantity) as total_Quantity, sum(totalAmount ) as TotalAmount from sales; 

--find out the avearge amount of quanity
SELECT AVG(Quantity) as Avg_Quantity from sales;
SELECT AVG(Quantity) as Avg_Quantity , avg(TotalAmount) as Avg_TotalAmount from sales;

--find  out the sum of total amount , average of taila amount for each prodcut id
SELECT productId ,Sum(Quantity) as total_Quantity, 
sum(TotalAmount) as TotalAmount ,
avg(TotalAmount) AS Avg_TotalAmount from sales
group by ProductId;

--find the sum of quantity and amount , avg of quantity and amount for each productid ans storeid
SELECT ProductId, StoreId,
sum(Quantity) as[sum of Qunatity],
avg(Quantity) as[Avg of Qunatity],
sum(TotalAmount) as [Sum of total],
avg(TotalAmount) as [Avg of total]
from sales
group by productId, storeId;

--find count of all reocds
select count(*)  as [number of rows]from sales;

--count of how many payment method availbe in sales
select count(PaymentMethod) as PaymantMethod from sales;

select count(distinct productId) as [Distinct product] from sales;

select count(distinct PaymentMethod) as [Distinct PaymentMethod] from sales;

select paymentMethod , count(paymentMethod) from sales
group by paymentMethod;

select * from sales;

--total sales value for each payment method
select paymentMethod, sum(TotalAmount) from sales
group by paymentMethod;

select productId, PaymentMethod, SUM(TotalAmount) as [Sum of Sales]
from sales
group by ProductId, PaymentMethod;



--HAVING CLAUSE
select * from sales;

select productid,
sum(TotalAmount) as[sum of sales],
avg(TotalAmount) as[ Avergae of sales],
sum(Quantity) as [total Quantity],
avg(Quantity) as[ aVERAGE Quantity]
from sales
group by ProductId
having sum(TotalAmount) < 750;


select productid,
sum(TotalAmount) as[sum of sales],
avg(TotalAmount) as[ Avergae of sales],
sum(Quantity) as [total Quantity],
avg(Quantity) as[ aVERAGE Quantity]
from sales
group by ProductId
having sum(TotalAmount) < 700 and sum(Quantity) = 21;

---WHERE VS HAVING CLAUSE
select * from sales;

select * from sales
where TotalAmount >=162;

select productiD, sum(totalAmount) as[sum of sales] from sales
group by productid
having sum(totalAmount) <700;


select productid, sum(totalamount) as [ sum of sale] from sales
where TotalAmount >=161
group by ProductId
having sum(totalamount) >=250
order by ProductId desc;

