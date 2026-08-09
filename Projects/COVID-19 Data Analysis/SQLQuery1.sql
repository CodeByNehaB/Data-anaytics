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
order by PercentPopulationInfected desc;


--6 showing countries with highest Death count per polution
Select country, MAX(total_deaths) as TotalDeathCount
From PortfolioProjects..CovidDeaths
where continent is not null
Group by Country
order by TotalDeathCount desc;


---7 LET'S BREAking THINGS DOWN BY CONTINENT
---showing continents with the highest death per population
select continent, max(cast(total_deaths as bigint)) as TotalDeathcount
from PortfolioProjects..CovidDeaths
Where continent is not null
Group by continent
order by TotalDeathCount desc


---select country , Max(cast(total_deaths as Bigint)) as TotalDeathCount
--from PortfolioProjects..CovidDeaths
--where continent is not null
--group by country
--order by TotalDeathCount desc





--select country , sum(cast(total_deaths as Bigint)) as TotalDeathCount
--from PortfolioProjects..CovidDeaths
---where continent is not null
---group by country
---order by TotalDeathCount desc


--Global Numbers
select  date,
sum(new_cases) as TotoalGlobalcases, 
sum(cast(new_deaths as int)) as totalGlobalDeaths, 
(sum(cast(new_deaths as float))/NULLIF(sum(new_cases),0))*100 as DeathPercentage
from PortfolioProjects..CovidDeaths
where continent is not null
group by  date
order by 1, 2

select sum(new_cases) as TotoalGlobalcases, 
sum(cast(new_deaths as int)) as totalGlobalDeaths, 
(sum(cast(new_deaths as float))/NULLIF(sum(new_cases),0))*100 as DeathPercentage
from PortfolioProjects..CovidDeaths
where continent is not null
---group by  date
--order by 1, 2


select * from PortfolioProjects.dbo.CovidVaccinations

-- 10. Test Base Vaccination Join

select * from PortfolioProjects..CovidDeaths as dea
join PortfolioProjects..CovidVaccinations as vac
  on dea.country = vac.country
  and dea.date = vac.date;

--Looking for the total populations vs vaccinations(Window Function)

select dea.continent, dea.country, dea.date, dea.population, vac.new_vaccinations,
    sum(convert(bigint, vac.new_vaccinations )) Over (partition by dea.country order by dea.country, dea.date)
as RollingPeopleVaccinated
from PortfolioProjects..CovidDeaths as dea
join PortfolioProjects..CovidVaccinations as vac
   on dea.country = vac.country
   and dea.date = vac.date
where dea.continent is not null
order by  2, 3;


 ---Advanced Extraction via CTE (Added terminating semicolon before CTE)
with PopVsVac (continent, country, date, population, new_vaccinations, RollingPeopleVaccinated)
as
(
select dea.continent, dea.country, dea.date, dea.population, vac.new_vaccinations,
  sum(convert(bigint, vac.new_vaccinations )) Over (partition by dea.country order by dea.country, dea.date)
--as RollingPeopleVaccinated
from PortfolioProjects..CovidDeaths as dea
join PortfolioProjects..CovidVaccinations as vac
  on dea.country = vac.country
  and dea.date = vac.date
where dea.continent is not null
--order by  2, 3
)
select * ,(RollingPeopleVaccinated/NULLIF(Population,0))*100 as PercentVaccinated
from PopVsVac;


--Temp Table

---Advanced Extraction via Temp Table (Added DROP statement for re-run safety)
DROP Table if exists #PercentPopulationVaccinated;
create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Country nvarchar(255),
Date dateTime,
Population numeric,
New_Vaccinations numeric,
RollingPeopleVaccinated numeric
);


Insert into #PercentPopulationVaccinated
select dea.continent, dea.country, dea.date, dea.population, vac.new_vaccinations,
  sum(convert(bigint, vac.new_vaccinations )) Over (partition by dea.country order by dea.country, dea.date)
--as RollingPeopleVaccinated
from PortfolioProjects..CovidDeaths as dea
join PortfolioProjects..CovidVaccinations as vac
  on dea.country = vac.country
  and dea.date = vac.date
where dea.continent is not null;
--order by  2, 3

select *, (RollingPeopleVaccinated / NULLIF(Population, 0)) * 100 as PercentVaccinated
from #PercentPopulationVaccinated;
GO


-----Creating view to store data for later visualization


--Creating view to store data for visualization (Isolated using GO batches)
DROP VIEW IF EXISTS PercentPopulationVaccinated;
GO

Create View PercentPopulationVaccinated as
select dea.continent, dea.country, dea.date, dea.population, vac.new_vaccinations,
    sum(convert(bigint, vac.new_vaccinations )) Over (partition by dea.country order by dea.country, dea.date) as RollingPeopleVaccinated
from PortfolioProjects..CovidDeaths as dea
join PortfolioProjects.dbo.CovidVaccinations as vac
    on dea.country = vac.country
    and dea.date = vac.date
where dea.continent is not null;
GO


select * from PercentPopulationVaccinated;



