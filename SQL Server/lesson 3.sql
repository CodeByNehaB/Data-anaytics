CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    age INT,
    gender VARCHAR(10),
    city VARCHAR(50),
    state VARCHAR(50),
    phone VARCHAR(15),
    email VARCHAR(100),
    registration_date DATE,
    membership VARCHAR(20)
);

INSERT INTO Customers VALUES
(1, 'Amit Sharma', 25, 'Male', 'Bilaspur', 'Chhattisgarh',
 '9876543210', 'amit@gmail.com', '2024-01-15', 'Gold'),

(2, 'Priya Verma', 30, 'Female', 'Raipur', 'Chhattisgarh',
 '9876543211', 'priya@gmail.com', '2024-02-20', 'Silver'),

(3, 'Rahul Patel', 28, 'Male', 'Durg', 'Chhattisgarh',
 '9876543212', 'rahul@gmail.com', '2024-03-10', 'Gold'),

(4, 'Neha Singh', 22, 'Female', 'Bilaspur', 'Chhattisgarh',
 '9876543213', 'neha@gmail.com', '2024-04-05', 'Bronze'),

(5, 'Ravi Gupta', 35, 'Male', 'Korba', 'Chhattisgarh',
 '9876543214', 'ravi@gmail.com', '2024-05-12', 'Silver'),

(6, 'Sneha Jain', 27, 'Female', 'Raipur', 'Chhattisgarh',
 '9876543215', 'sneha@gmail.com', '2024-06-18', 'Gold'),

(7, 'Vikas Yadav', 40, 'Male', 'Jabalpur', 'Madhya Pradesh',
 '9876543216', 'vikas@gmail.com', '2024-07-22', 'Bronze'),

(8, 'Pooja Mishra', 32, 'Female', 'Nagpur', 'Maharashtra',
 '9876543217', 'pooja@gmail.com', '2024-08-14', 'Silver'),

(9, 'Karan Mehta', 29, 'Male', 'Raipur', 'Chhattisgarh',
 '9876543218', 'karan@gmail.com', '2024-09-01', 'Gold'),

(10, 'Anjali Das', 24, 'Female', 'Bilaspur', 'Chhattisgarh',
 '9876543219', 'anjali@gmail.com', '2024-10-11', 'Bronze');


 --find all recors from customer table
 select * from Customers;

 CREATE TABLE Stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    manager_name VARCHAR(50),
    category VARCHAR(50),
    opening_date DATE,
    monthly_sales DECIMAL(12,2),
    rating DECIMAL(2,1),
    customer_id INT,
    FOREIGN KEY (customer_id)
        REFERENCES Customers(customer_id)
);

INSERT INTO Stores VALUES
(101, 'City Mart', 'Bilaspur', 'Chhattisgarh',
 'Suresh Kumar', 'Grocery', '2022-01-10', 250000, 4.5, 1),

(102, 'Fresh Store', 'Raipur', 'Chhattisgarh',
 'Manoj Sahu', 'Grocery', '2021-05-15', 180000, 4.2, 2),

(103, 'Mega Mart', 'Durg', 'Chhattisgarh',
 'Ramesh Patel', 'Electronics', '2020-08-20', 420000, 4.7, 3),

(104, 'Smart Shop', 'Bilaspur', 'Chhattisgarh',
 'Anil Verma', 'Clothing', '2023-03-12', 150000, 3.9, 1),

(105, 'Daily Needs', 'Raipur', 'Chhattisgarh',
 'Sunil Jain', 'Grocery', '2022-11-25', 210000, 4.3, 2),

(106, 'Tech World', 'Korba', 'Chhattisgarh',
 'Deepak Gupta', 'Electronics', '2021-09-05', 350000, 4.6, 5),

(107, 'Style Hub', 'Jabalpur', 'Madhya Pradesh',
 'Aakash Yadav', 'Clothing', '2023-06-18', 125000, 3.8, 7),

(108, 'Home Choice', 'Nagpur', 'Maharashtra',
 'Pankaj Desai', 'Furniture', '2019-12-01', 300000, 4.4, 8),

(109, 'Fashion Point', 'Raipur', 'Chhattisgarh',
 'Vivek Sharma', 'Clothing', '2022-04-22', 195000, 4.1, 9),

(110, 'Super Bazaar', 'Bilaspur', 'Chhattisgarh',
 'Rajesh Mishra', 'Grocery', '2020-02-14', 275000, 4.8, 10);

 -- find the records from store table
 select * from Stores;

 --INNER JOIN
 --display customer name ans store name 
 select customer_name, store_name 
 from Customers c
 inner join Stores s
 on c.customer_id = s.customer_id;

 --display customer name and monthy sale of stroe
 select customer_name, monthly_sales
 from Customers c
 inner join Stores s
 on c.customer_id = s.customer_id;

 --display customers whoo store have monthly sale grtaer than 20000;
 select *, monthly_sales
 from Customers c
 inner join Stores s
 on c.customer_id = s.customer_id
 where monthly_sales >= 200000;

 -- display customer name, store name and rating for store rated above 4.3
 select customer_name, store_name, rating
 from Customers c
 inner join Stores s
 on c.customer_id = s.customer_id
 where rating > 4.3;

 --display customer name, storename and montly sale for store  btween 150000 and 300000
 select customer_name, store_name, monthly_sales
 from Customers c
 inner join Stores s
 on c.customer_id = s.customer_id
 where monthly_sales between 150000 and  300000;

 --Find the customer names, store names, categories, and monthly sales for the top five highest-selling matching stores.
 SELECT top 5 customer_name, store_name, category, monthly_sales
FROM Customers c
INNER JOIN Stores s
    ON c.customer_id = s.customer_id
ORDER BY s.monthly_sales DESC;


--LEFT JOIN
--Display all customer names and their store names, including customers who have no matching store.
select customer_name , store_name 
from Customers c
left join Stores s
on c.customer_id = s.customer_id;

--Display all customers and their membership types along with their store names
select customer_name, store_name , membership
from Customers c
left join Stores s
on c.customer_id = s.customer_id;

--Display all customers from Bilaspur and their store names, including customers without a matching store.
select  customer_name,c.city, store_name
from Customers c
left join Stores s
on c.customer_id = s.customer_id
where c.city = 'Bilaspur';

select * from Customers;

--RIGHT JOIN
--display all store name and customer name using right outer join
select store_name, customer_name
from Customers c
right join Stores s
on c.customer_id = s.customer_id;

--disply all sotre montly sale and cutomer name
select customer_name , monthly_sales
from Customers c
right join Stores s
on c.customer_id = s.customer_id;

--Display all stores with their customer names and membership types, sorted by monthly sales in descending order.

select customer_name, membership , monthly_sales
from Customers c
right join Stores s
on c.customer_id = s.customer_id
order by monthly_sales desc;



---Find stores that have no matching customer.
SELECT
    s.store_id,
    s.store_name,
    c.customer_name
FROM Customers c
RIGHT OUTER JOIN Stores s
    ON c.customer_id = s.customer_id
WHERE c.customer_id IS NULL;


--Display all stores and show No Customer instead of NULL when no customer matches.
SELECT
    s.store_id,
    s.store_name,
    ISNULL(c.customer_name, 'No Customer') AS customer_name,
    s.category,
    s.monthly_sales
FROM Customers c
RIGHT OUTER JOIN Stores s
    ON c.customer_id = s.customer_id;


    --FULL OUTER JOIN
    --Write a SQL Server query to display all customers and all stores, including unmatched records, and show No Customer when the customer name is missing.
    select store_id,
    c.customer_id, 
    store_name,
   isnull(customer_name, 'No Customer') as customer_name
   from stores s
   full outer join customers c
   on c.customer_id = s.customer_id;

   --diaplya ll customer name and  stroe name
   select customer_name, store_name
   from Customers c
   full outer join Stores s
   on c.customer_id = s.customer_id;

   --: Find customers without stores AND stores without customers
   select c.customer_id, customer_name, store_id, store_name
   from Customers c
   full outer join Stores s
   on c.customer_id = s.customer_id
   where c.customer_id is null 
   OR
   s.customer_id is null;


   --SELF JOIN
   --find customer living in same city
   select c1.customer_name as customer1,
   c2.customer_name as customer2,
   c1.city
   from Customers c1
   join Customers c2
   on c1.customer_id = c2.customer_id;

   --UNION
   --Combine customer cities and store cities, removing duplicates
   select c.city from Customers c
   union
   select s.city from Stores s;

   --Combine customer names and store names into one column using UNION.
   select customer_name from Customers
   union
   select store_name from Stores;

   --UNION ALL
   --Combine customer cities and store cities, keeping duplicates.
   select c.city from Customers c
   union all
   select s.city from Stores s;


   --Combine customer cities from Bilaspur and Raipur with store cities from Bilaspur and Raipur, retaining duplicates.
   select city from Customers 
   where city IN('Bilaspur','Raipur')
   union all
   select city from stores
   where city in('Bilaspur', 'Raipur');

   --Use UNION to combine customers' city values with stores' city values, then count the number of distinct cities.
  select count(*) as total_city from  (select city from Customers
   union 
   select city from Stores) as cityList;
