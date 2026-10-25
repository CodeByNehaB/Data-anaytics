
-- Create a database 

CREATE Database employee_details;

-- use this database

Use employee_details;

-- create a table inside the database

CREATE Table Employees(
  EmployeeId INT PRIMARY KEY,
  FirstName varchar(50),
  LastName varchar(50),
  Department varchar(50),
  Salary decimal(10, 2),
  HireDate Date
);


--- Insert the data inside the employye table

INSERT INTO Employees(EmployeeId,FirstName,LastName,Department,Salary,HireDate)
Values
(1,'John','Doe','IT',50000.00,'2020-01-15'),
(2,'Alice','Johnson','HR',60000.00,'2019-02-23'),
(3,'Reyansh','Khurana','Finance',75000.00,'2021-09-30'),
(4,'Meera','Sharma','IT',55000.00,'2018-09-10'),
(5, 'Arora','Ctrast','HR',70000.00,'2022-02-20');


--- SELECT STATEMENT
---1. select all employee from table

SELECT * FROM Employees;

--2 select fristname from the table

SELECT FirstName from Employees;

--3 select firstname and salary from the table
SELECT FirstName , Salary from Employees;


--4 select first and last name from the table
SELECT FirstName, LastName from Employees;

--5 select id and fullname from table
SELECT EmployeeId, concat(firstname,' ',lastname)[Full Name] from Employees;


--TEMPORARY TABLE
-- Crate a tempory table from orginal
SELECT * into #temp
from dbo.Employees;

select * from #temp;

---Where clause
--1 find all details where id is 2
SELECT * FROM Employees
where EmployeeId =2;

--2 find all details from employee tbale where  salary is grater than or qeual 75000.00
SELECT * FROM Employees
where Salary >= 75000.00;

--3 find all record from table where salary is grater than 70000
SELECT * FROM Employees
WHere Salary >70000.00;



--order by clause
--1 sort the salary by asc
SELECT * FROM  Employees
order by salary asc;


--2 sort the salary asc and firstname desc order
SELECT * FROM Employees
order by Salary asc , FirstName DESC;

--3 find the records from table where lastame is jondson

select * from employees
where lastname = 'Johnson' and EmployeeId =2;

--4 find all recodrs whose work in hr or finance department
Select * from Employees
where Department = 'HR' or Department ='Finance';

--5 find the employee who work in hr or finance and their salary is more than 60000;
SELECT * from Employees
where Salary >60000 and Department='Hr' or Department='Finance';

--SQL OPERATORS
--and + or
select * from Employees
where not firstName ='John' and not salary=60000;

--not + or
select * from Employees
where not LastName='millar' or not Department='HR';

--between
select * from Employees
where Salary between 75000 and 80000;


select * from Employees
where salary not between 65000 and 75000;

