--- LIKE
-- create table
Create Table Employees_US(
 employeeId int primary Key,
 firstname varchar(50),
 lastname varchar(50),
 Department varchar(50)
);

--insert data in it
INSERT INTO Employees_US(employeeId,firstname,lastname,Department)
values
(1, 'Alice','Smith','Finance'),
(2, 'Bob', 'Johnson','Engineering'),
(3, 'Charlie', 'willams','Marketing'),
(4, 'Diana', 'Brows','Finance'),
(5, 'Edward', 'Jones','Engineering'),
(6, 'Fiona', 'JGarcia','Marketing'),
(7, 'Gorge', 'Millar','Finance'),
(8, 'Hannah', 'Wilson','Engineering');

-- retiev all data
select * from Employees_US;

--find Employees whose last name starts with 'S'
select * from Employees_US 
where lastname like 's%';

--find employee whose department contains 'Eng';
Select * from Employees_US
where department like '%Eng%';

--find employee whose name end with a 
select * from Employees_US
where firstname like '%a';

--find employee whose lastname is exactly 5 character long
select * from Employees_US
where lastname like '_____';

--find emplooye whose first nmae start with 'c' or 'D'
select * from Employees_US
where firstname like '[CD]%';

--find employee whose last name contains son
select * from Employees_US
where lastname like '%son%';

--find employees whose first name contain the letter 'i' as the second charater
select * from Employees_US
where firstname like '_i%';

--find employyes whose first name start with vowel
select * from Employees_US
where firstname like '[ariou]%';

--find employyes whose firtname does not start with a consant
select * from Employees_US
where firstname like '[^aeiou]%';



--create table Products
CREATE TABLE Products(
ProductId int Primary key,
ProductName Varchar(50),
Category varchar(20),
Price Decimal(10,2),
stockQuality INT,
Supplier Varchar(50),
Rating Decimal(3, 1)
);

--insert data into products table
INSERT INTO Products(ProductId,ProductName, Category,Price,stockQuality,Supplier,Rating)
values
(1,'Wireless Mouse', 'Electronics',25.99, 150, 'Tech Supplier',4.5),
(2,'office chairs', 'Furniture',120.00,85, 'comfort co',4.7),
(3,'Water bottle', 'Accessories',15.00, 250, 'Aquagear',4.3),
(4,'Laptop Backpack', 'Accessories',45.99, 200, 'GearUp',4.6),
(5,'Gaming Laptop', 'Electronics',999.99, 45, 'Tech Supplier',4.8),
(6,'Desk Lamp', 'Furniture',30.00,120, 'Light house',4.2),
(7,'Bluetooth Speaker', 'Electronics',59.99, 95, 'Soundwave',4.4),
(8,'Standing Desk', 'Furniture',250.00,50, 'comfort co',4.9),
(9,'Fitness Tracker', 'Electronics',129.99, 180, 'FitTech',4.7),
(10,'Coffee Mug', 'Accessories',9.99, 300, 'MugMasters',4.1);

--retrive all data
select * from Products;

--CASE STATEMENT
--Example 1 - Add a columns categories each prodcut into categories hgih meduim low
SELECT *,
case
  when Price >500 then 'High'
  when Price <=500  and price >=200 then 'Medium'
  else 'Low'
end as [High/Medium/Low]
from Products;

--Exaple 2: provide priority to each catrogire and sort the data according to their priority
select *
from Products order by
case 
   when Category in ('Eletronics') then 1
   when Category in('Furniture') then 2
   else 3
end ;


--Example 3:we need to group the data based on column category % price into different categories i.e affordable & premium
select *,
case
   when Category ='Electronics' then
        case when Price >=300 then 'Preminum Electronics'
        else 'Affordable Electronics'
        end
   when Category='Furniture' then
       case when price >= 250 then 'Premium Furniture'
       else 'Affordable Furniture'
       end
else
        case when price >=25 then 'Primium Accessories'
        else 'Affordable Accessories'
        end
end as [Group]
from Products;


