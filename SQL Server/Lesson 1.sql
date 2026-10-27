
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
-- commnets-
select * from Employees;

--TOP CLAUSE
select top 3 *  from Employees;

--1 top 3  salary highest salary
select top 3  salary from Employees 
order by salary desc;


--2 top 3 lowest salary
select top 3 salary from Employees
order by Salary asc;

--top with with percentage
select top (3) percent * from Employees;
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

--IN
select * from Employees
where Department in('HR', 'Finance');

select * from Employees
where Salary in (25000, 50000);

---Not in
select * from Employees 
where EmployeeId not in (2, 5);


-- Insert records
select * from Employees;

Insert into dbo.Employees(EmployeeId, FirstName, LastName,Department, Salary, HireDate)
values(6, 'Aradhya', 'Mehra', 'IT', 80000.00, '2022-12-15'),
(7, 'Vihann', 'Sharma', 'Marketing',78000.00,'2026-1-28');

-- want to add full name and id
INSERT INTO dbo.Employees (EmployeeId, FirstName, LastName)
values(8, 'Rohit', 'Mehra');

--- inserting all recodrs in th table
Insert into dbo.Employees
values(9, 'Mahesh', 'Naran','Finance', 73000.00, '2025-1-24');


select * from Employees

--Null Values
insert into dbo.Employees
values(10, 'Jay', '', 'HR',73000,'2022-05-09');

--1 find those reocrds where department is null
select * from Employees
where Department is null;

--2 find those reocdrs where department is not null
select * from Employees
where Department is not null;

-- upadte statement
--1 create a temp table for update
select * into #1 from dbo.Employees;

select * from #1;


--1 update those recodrs where department is null
update #1
set Department = 'Hr'
where Department is null;

--2 update salary and hire date  where  emp id is 7
update #1
set salary =85000 ,Hiredate ='2025-12-28'
where EmployeeId =8;


-- delete vs drop vs truncate
select * from Employees;


-- create a temp table for deletion
select * into #temp1 from dbo.Employees;

--delete records where id =2
delete from #temp1
where EmployeeId =2;

select * from #temp1;

--delete mulitple rows
delete from #temp1
where Department = 'HR';

--delete all records
delete from #temp1;

-- TRUNCATE COMMAND
select * into #temp2 from Employees;

select * from #temp2;

TRUNCATE TABLE #temp2;

--drop commnad
select * from #temp1;

drop table #temp1;




