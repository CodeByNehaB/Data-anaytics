-- 1. Test select all the data
Select * from PortfolioProjects..CovidDeaths
where continent is not null
order by 3,4

--- 2 Select data that we are going to use

Select country, date, total_cases, new_cases , total_deaths, population
from PortfolioProjects..CovidDeaths
where continent is not null
order by 1, 2


--3 Looking at Total Cases vs Total Deaths
--shows likelihood of dying you contract coid in your conutry


Select country, date, total_cases, total_deaths,(TRY_CONVERT(float,total_deaths)/NULLIF(TRY_CONVERT(float, total_cases),0)) *100 as DeathPercentage
from PortfolioProjects..CovidDeaths
Where country like '%states%'
and continent is not null
order by 1, 2


-- 4 Looking at total cases vs population

select country, date, total_cases, population ,(total_cases/ population) *100 as percentpopulationinfected
from PortfolioProjects..CovidDeaths
--Where country like '%states%'
where continent is not null
order by 1, 2


-- 5 Looking at countries with highest infection rate compared to population
Select country , population, max(total_cases) as HighestInfectioncount, Max((total_cases /population)) *100 as PercentPopulationInfected
From PortfolioProjects..CovidDeaths
Where continent is not null
Group by country, population
order by PercentPopulationInfected desc


--6 showing countries with highest Death count per polution
Select country, MAX(total_deaths) as TotalDeathCount
From PortfolioProjects..CovidDeaths
where continent is not null
Group by Country
order by TotalDeathCount desc


---7 LET'S BREAJ THINGS DOWN BY CONTINENT
---showing continents with the highest death per population
select continent, max(cast(total_deaths as bigint)) as TotalDeathcount
from PortfolioProjects..CovidDeaths
Where continent is not null
Group by continent
order by TotalDeathCount desc


select country , Max(cast(total_deaths as Bigint)) as TotalDeathCount
from PortfolioProjects..CovidDeaths
where continent is not null
group by country
order by TotalDeathCount desc





select country , sum(cast(total_deaths as Bigint)) as TotalDeathCount
from PortfolioProjects..CovidDeaths
where continent is not null
group by country
order by TotalDeathCount desc


--Global Numbers
select  date,sum(new_cases) as TotoalGlobalcases, sum(cast(new_deaths as int)) as totalGlobalDeaths, (sum(cast(new_deaths as float))/NULLIF(sum(new_cases),0))*100 as DeathPercentage
from PortfolioProjects..CovidDeaths
where continent is not null
group by  date
order by 1, 2

select sum(new_cases) as TotoalGlobalcases, sum(cast(new_deaths as int)) as totalGlobalDeaths, (sum(cast(new_deaths as float))/NULLIF(sum(new_cases),0))*100 as DeathPercentage
from PortfolioProjects..CovidDeaths
where continent is not null
---group by  date
order by 1, 2

select * from PortfolioProjects.dbo.CovidVaccinations

