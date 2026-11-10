CREATE DATABASE [SQL Question];

use [SQL Question];

--Create table Employee
CREATE TABLE Employees(
    EmployeeId INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Department VARCHAR(50),
    Salary DECIMAL(10, 2)
);

INSERT INTO Employees(EmployeeId,FirstName,LastName, Department,Salary)
VALUES
(101, 'Rahul', 'Sharma', 'IT', 45000),
(102, 'Priya', 'Verma', 'HR', 35000),
(103, 'Amit', 'Kumar', 'Finance', 50000),
(104, 'Sneha', 'Patel', 'Marketing', 40000),
(105, 'Rohit', 'Singh', 'IT', 55000),
(106, 'Anjali', 'Gupta', 'HR', 38000),
(107, 'Vikas', 'Yadav', 'Sales', 42000),
(108, 'Neha', 'Joshi', 'Finance', 48000),
(109, 'Arjun', 'Mehta', 'IT', 60000),
(110, 'Pooja', 'Mishra', 'Sales', 36000),
(111, 'Karan', 'Das', 'Marketing', 43000),
(112, 'Simran', 'Kaur', 'HR', 39000),
(113, 'Mohit', 'Jain', 'Finance', 52000),
(114, 'Riya', 'Shah', 'IT', 58000),
(115, 'Deepak', 'Roy', 'Sales', 41000),
(116, 'Kavita', 'Rao', 'Marketing', 47000),
(117, 'Suresh', 'Nair', 'IT', 62000),
(118, 'Meena', 'Thakur', 'HR', 37000),
(119, 'Varun', 'Soni', 'Finance', 49000),
(120, 'Aarti', 'Desai', 'Sales', 44000);

SELECT * FROM Employees;


--1) HOw do you select all columns from the Employee table
SELECT * FROM Employees;

--2 HOw do you select only the firstname and lastname column from the employee table
SELECT FirstName, LastName from Employees;

--3 HOw do you find all employee who work in 'IT' department
SELECT * from Employees where Department ='IT';

--4 how do you select employee with a salary greater than 60000
SELECT * FROM Employees WHERE Salary >60000;

--5 how do you sort the result by last name in ascending order

SELECT * FROM Employees ORDER BY LastName asc;

--6 how do you select distinct department from the employees table
select distinct Department from Employees;

--7 how do you count the number of employee in each deaprtment

select Department, count(*) from Employees group by Department;

--8 how do you find the maximum salary in the employee table
select Max(Salary) from Employees;

--9 how do you find the avaerae salary of employee in the 'Finnace' department
SELECT AVG(Salary) AS Finance_avg from Employees where Department ='Finance';

--10 how do you select employee whoese last nsam esatart with 'M'
SELECT * FROM Employees where LastName like 'M%';

--11 how do you select employee who work in 'IT' Department and have salary is greater than 50000;
SELECT * FROM Employees where Department ='IT' and Salary > 50000;

--12) how do you select employee who work in 'HR' Department and have salary is less than 55000;
SELECT * FROM Employees where Department = 'HR' or Salary < 60000;

--13) how do you select employee who do not work in the 'Finance' department
SELECT * FROM Employees WHERE Department not in('Finance');

--14) HOW do you find employee whose salary is between 50,000 and 60,000 and work in the 'fiNANCE DEPARTMENT
SELECT * FROM Employees where salary between 50000 and 60000  and Department ='Finance';

--15) HOW  do you find employee who work in IT department and do not have salary is grtaer than 50000;
SELECT * FROM Employees where Department ='IT' and salary <= 50000;

--16) how do you find employee who work in the 'HR' or 'fINANCE' Department and have a salary greater than 45000;
SELECT * FROM Employees WHERE Department in( 'HR','Finance') and Salary > 45000;

--17) how do you select employee whose last name start with 'D' and do not work in HR department
select * from Employees where LastName like 'D%' and Department not in('HR');

--18) how do you find employee who do not work in the 'IT' department and have a salary greater than 70,000;
select * from Employees where Department not in('IT') and Salary >70000;

--19) how do you select employee who work in the 'IT' department and either have a salary is grater then 65000 or have firstname 'Neha'
select * from Employees where Department not in('IT') and salary > 65000 or FirstName ='Neha';

--20) how do you find employee who do not work in 'HR' or 'IT' department
select * from Employees where Department not in('IT', 'HR') ;



--create the customer table
CREATE TABLE Customers(
 CustomerID int primary key,
 CustomerName VARCHAR(50),
 City VARCHAR(50)

);

--insert data into customer table
INSERT INTO Customers VALUES
(1,'Rahul Sharma','Delhi'),
(2,'Priya Verma','Mumbai'),
(3,'Amit Kumar','Bhopal'),
(4,'Sneha Patel','Indore'),
(5,'Rohit Singh','Pune'),
(6,'Anjali Gupta','Delhi'),
(7,'Vikas Yadav','Jaipur'),
(8,'Neha Joshi','Mumbai'),
(9,'Karan Mehta','Indore'),
(10,'Pooja Mishra','Bhopal'),
(11,'Simran Kaur','Chandigarh'),
(12,'Mohit Jain','Jaipur');

select * from Customers;

--create order tabel
CREATE TABLE Orders(
 OrderId INT PRIMARY KEY,
 CustomerID INT,
 OrderDate DATE,
 ProductID INT,
 FOREIGN KEY(CustomerId) REFERENCES Customers(CustomerID)
);

INSERT INTO Orders
(OrderId, CustomerID, OrderDate, ProductID)
VALUES
(101, 1, '2026-01-05', 501),
(102, 2, '2026-01-07', 502),
(103, 3, '2026-01-10', 503),
(104, 4, '2026-01-12', 504),
(105, 5, '2026-01-15', 505),
(106, 1, '2026-01-18', 506),
(107, 2, '2026-01-20', 507),
(108, 6, '2026-01-22', 508),
(109, 7, '2026-01-25', 509),
(110, 3, '2026-01-28', 510),
(111, 8, '2026-02-01', 501),
(112, 9, '2026-02-03', 502),
(113, 1, '2026-02-05', 503),
(114, 10, '2026-02-08', 504),
(115, 5, '2026-02-10', 505),
(116, 11, '2026-02-12', 506),
(117, 12, '2026-02-15', 507),
(118, 6, '2026-02-18', 508),
(119, 3, '2026-02-20', 509),
(120, 9, '2026-02-22', 510);

select * from Orders;

--CREATE TABEL PRODUCT
CREATE TABLE Products(
  ProductID INT PRIMARY KEY,
  ProductName VARCHAR(50),
  Price DECIMAL(10,2)

);

INSERT INTO Products
(ProductID, ProductName, Price)
VALUES
(501, 'Laptop', 55000),
(502, 'Smartphone', 25000),
(503, 'Headphones', 2000),
(504, 'Keyboard', 1500),
(505, 'Mouse', 800),
(506, 'Monitor', 15000),
(507, 'Printer', 12000),
(508, 'Tablet', 22000),
(509, 'Smart Watch', 5000),
(510, 'Speaker', 4500),
(511, 'Power Bank', 1200),
(512, 'USB Drive', 600),
(513, 'Hard Disk', 4500),
(514, 'Webcam', 3000),
(515, 'Microphone', 3500),
(516, 'Router', 2800),
(517, 'SSD', 6500),
(518, 'Projector', 30000),
(519, 'Gaming Chair', 18000),
(520, 'Bluetooth Earbuds', 3500); 

select * from Products;


--1)Write a query to find the name of customer who placed order
SELECT CustomerName from Customers C
inner join Orders O
on O.CustomerID =C.CustomerID;


--2) find the list of customer who have not placed any orders.
Select * from Customers c
left join Orders o 
on o.CustomerID = c.CustomerID
where o.OrderId is null;


--3)list all order along with the product name and price
 SELECT  ProductName , price
 from Orders o
 join Products p
 on o.ProductID = p.ProductID;

 --find the name of customer nad their order ,including customer who have not place any order
select distinct customerName, OrderID FROM Customers c left join Orders o 
on o.CustomerID = c.CustomerID ;

--5) find the total number of order placed by each customer
select customerName , count(orderId) 
from Customers c
inner join Orders o
 on o.CustomerID = c.CustomerID
 group by CustomerName;


 --6) Indentify pair of customer who live in the same country
 select c1.CustomerName, c2.CustomerName from Customers c1
 join Customers c2 
 on c1.City = c2.City
 and c1.CustomerID <> c2.CustomerID;

 --7) find the customr who has spent the most on thier orders
 select CustomerName, SUM(Price) as [Amount Spent] from Customers c 
 inner join Orders o
 on c.CustomerID = o.CustomerID
 inner join Products p
 on p.productId = o.ProductID
 group by CustomerName;

 --8) find customer who have ordered more than one tuye pof products
 SELECT CustomerName, count(ProductID) FROM Customers c
 join Orders o 
 on c.CustomerID = o.CustomerID
 group by CustomerName
 having count(ProductID) > 1;

 --9) list of all procut and thier corresponding order, using a right join , including product that hvae never been ordered.
 select OrderId, p.ProductID, p.ProductName from Orders o
 right join Products p
 on o.ProductID = p.ProductID;

 --10) retrive all order placed by customer from the mumbai.
 select * from Customers c
 inner join Orders o
 on c.CustomerID = o.CustomerID
 where city in ('Mumbai');

 

 --11) find the name of cutomer who have orderd a product priced abouve $500,
 select * from Customers c
 inner join Orders o
 on c.CustomerID = o.CustomerID
 inner join Products p
 on p.ProductID = o.ProductID
 where Price >50000;

 --12) find customer who have ordered the same product more than once.
 select CustomerName, ProductID, count(orderId) as counts from Customers c
 inner join Orders o
 on c.CustomerID = o.CustomerID
 group by CustomerName, ProductID
 having count(orderId) >1;
