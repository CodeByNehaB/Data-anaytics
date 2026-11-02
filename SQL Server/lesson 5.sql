-- create table 
CREATE TABLE Customers(
   customer_id INT PRIMARY KEY,
   Customer_name varchar(50),
   email varchar(100)
);

--insert data into customer table
INSERT INTO Customers(customer_id, Customer_name, email)
VALUES
(1, 'Alice Smith', 'alice@example.com'),
(2, 'Bob Johnson','bob@example.com'),
(3, 'Chalrie Brown', 'charli@gmail.com');




CREATE TABLE Orders(
   order_id INT PRIMARY KEY,
   customer_id int,
   order_date DATE,
   amount DECIMAL (10,2)
   FOREIGN KEY(customer_id) references customers(customer_id)
);

INSERT INTO Orders(order_id,customer_id,order_date, amount)values
(101,1,'2024-07-15',250.00),
(102,1,'2024-08-05',300.00),
(103,2,'2024-08-10',150.00),
(104,2,'2024-06-25',100.00);


SELECT * from Customers;
select * from Orders;

--SUBQUERY
select * from Customers
where customer_id in(select distinct customer_id 
from Orders where order_date between '2024-08-01' and '2024-08-31')


--fetch the data from employee table where salary > avrage salary
select * from Employees where Salary >(
select avg(salary) from Employees);


--CONSTRAINTS
--constiton that can be applied on cloumn of a table & these constion are to be folwed table

--Not NUll constraint
-- CASE 1: We will have to create a new table
create table test_not_null(
 EId int not null,
 age tinyint,
 firstName varchar(256));

 select * from test_not_null;
 select * from INFORMATION_SCHEMA.COLUMNS
 where TABLE_NAME like 'test_not_null';

 insert into test_not_null values(1,23,'Mayank');

 --here data will not insert becuase eid is not null
  insert into test_not_null values(null,23,'Mayank');

 insert into test_not_null values(2,NULL,'Shyam');
  

--CASE 2: IF the table already exists
--WE want firstNmae column nullable

ALTER TABLE test_not_null
alter column firstName varchar(256) not null

--data will not insert because firstname is not null must insert value
insert into test_not_null values (21, 34, null);



--UNIQUE CONSTRAINTS
--it ensure that column consists of unique values

--CASE 1: when the table already exits
alter table test_Unique
add unique (LastName)




--CASE 2: We need to create the table
Create table test_Unique(
S_Id int unique,
age TinyInt not null,
FirstName varchar(256) not null unique,
LastName varchar(256)
);

select * from test_Unique;

INSERT INTO test_Unique values
(1,23,'Shalin', 'Verma');

--data will not insert it is duplicate sid
INSERT INTO test_Unique values
(1,24,'Mohan', 'Verma');

INSERT INTO test_Unique values
(NULL,24,'Mohan', 'Verma');


--CHECK CONSTRAINTS
create table test_Check(
Id int unique,
firstName varchar(30) not null,
age int check(age >10)
);

select * from test_Check;

insert into test_Check values(1, 'Navin','20');
--not inserted because consiton is more than 10
insert into test_Check values(2, 'Raj','9');

update test_Check set Id = 11 where Id =1;

--case 2 if table is already created
alter table test_check
add check(Id >5);

insert into test_Check values(3, 'Mohan',34);

insert into test_Check values(30, 'Mohan',34);


--DEFAULT CONSTAINTS
--This contraints to proivde fdefault value to columns

--Case 1: The Table doest not exits
create table test_default(
 Id int  not null,
 FirstName varchar(30) default 'Stranger',
 lastName varchar(30),
 age tinyint
);

select * from test_default;

insert into test_default values(1, 'Nititn','Jian', 23);

insert into test_default (Id, lastName, age) values(1,'Jian', 23);

