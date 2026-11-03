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
INSERT INTO CUSTOMERS
(CUSTOMERID, CUSTOMERNAME, CITY)
VALUES
(201, 'Rahul Sharma', 'Delhi'),
(202, 'Priya Verma', 'Mumbai'),
(203, 'Amit Kumar', 'Bhopal'),
(204, 'Sneha Patel', 'Indore'),
(205, 'Rohit Singh', 'Jaipur'),
(206, 'Anjali Gupta', 'Pune'),
(207, 'Vikas Yadav', 'Jabalpur'),
(208, 'Neha Joshi', 'Nagpur'),
(209, 'Arjun Mehta', 'Surat'),
(210, 'Pooja Mishra', 'Lucknow'),
(211, 'Karan Das', 'Kolkata'),
(212, 'Simran Kaur', 'Chandigarh'),
(213, 'Mohit Jain', 'Gwalior'),
(214, 'Riya Shah', 'Ahmedabad'),
(215, 'Deepak Roy', 'Ranchi'),
(216, 'Kavita Rao', 'Hyderabad'),
(217, 'Suresh Nair', 'Kochi'),
(218, 'Meena Thakur', 'Rewa'),
(219, 'Varun Soni', 'Ujjain'),
(220, 'Aarti Desai', 'Vadodara');

select * from Customers;

--create order tabel
CREATE TABLE Orders(
 OrderId INT PRIMARY KEY,
 CustomerID INT,
 OrderDate DATE,
 ProductID INT,
 FOREIGN KEY(CustomerId) REFERENCES Customers(CustomerID)
);


INSERT INTO ORDERS
(ORDERID, CUSTOMERID, ORDERDATE, PRODUCTID)
VALUES
(301, 201, '2026-01-05', 501),
(302, 202, '2026-01-07', 502),
(303, 203, '2026-01-10', 503),
(304, 204, '2026-01-12', 504),
(305, 205, '2026-01-15', 505),
(306, 206, '2026-01-18', 506),
(307, 207, '2026-01-20', 507),
(308, 208, '2026-01-22', 508),
(309, 209, '2026-01-25', 509),
(310, 210, '2026-01-28', 510),
(311, 211, '2026-02-01', 501),
(312, 212, '2026-02-03', 502),
(313, 213, '2026-02-05', 503),
(314, 214, '2026-02-08', 504),
(315, 215, '2026-02-10', 505),
(316, 216, '2026-02-12', 506),
(317, 217, '2026-02-15', 507),
(318, 218, '2026-02-18', 508),
(319, 219, '2026-02-20', 509),
(320, 220, '2026-02-22', 510);

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
(503, 'Headphones', 1500),
(504, 'Keyboard', 1200),
(505, 'Mouse', 600),
(506, 'Monitor', 12000),
(507, 'Printer', 8500),
(508, 'Tablet', 18000),
(509, 'Smart Watch', 5000),
(510, 'Speaker', 2500),
(511, 'Power Bank', 1200),
(512, 'USB Drive', 500),
(513, 'Hard Disk', 4500),
(514, 'Webcam', 2200),
(515, 'Microphone', 3500),
(516, 'Router', 2800),
(517, 'SSD', 6000),
(518, 'Projector', 22000),
(519, 'Gaming Chair', 15000),
(520, 'Bluetooth Earbuds', 3000);

select * from Products;


