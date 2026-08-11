 /*

Queries used for Tableau Project

*/



----1.Global Metrics Scorecard (Total Cases, Total Deaths, & Overall Death Rate)

Select 
      Sum(new_cases) as total_cases ,
      Sum(cast(new_deaths as bigint)) as total_deaths,
      (Sum(cast(new_deaths as float))/NULLIF(Sum(new_cases),0)) *100 as DeathPercentage
from PortfolioProjects..CovidDeaths
--where location like '%states%'
where continent is not null
--Group by date
order by 1, 2;

-- Just a double check based off the data provided
-- numbers are extremely close so we will keep them - The Second includes "International"  Location

--Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(New_Cases)*100 as DeathPercentage
--From PortfolioProjects..CovidDeaths
---Where country like '%states%'
--where country = 'World'
--Group By date
--order by 1,2


--2  Total Death Count per Continent Bar Chart
-- We take these out as they are not inluded in the above queries and want to stay consistent
-- European Union is part of Europe


--select 
    -- country,Sum(cast(new_deaths as bigint)) as TotalDeathCount
--from PortfolioProjects..CovidDeaths
--where country like '%states%'
--where continent is not null
   --  and country not in('World', 'European Union', 'International','High income', 'Upper middle income', 'Lower middle income', 'Low income')
---Group by country
--order by TotalDeathCount desc;


--select 
     --country,Sum(cast(new_deaths as bigint)) as TotalDeathCount
---from PortfolioProjects..CovidDeaths
--where country like '%states%'
---where continent is  null
    -- and country not in('World', 'European Union', 'International','High income', 'Upper middle income', 'Lower middle income', 'Low income')
---Group by country
---order by TotalDeathCount desc;


SELECT 
    continent, 
    SUM(CAST(new_deaths AS bigint)) AS TotalDeathCount
FROM 
    PortfolioProjects..CovidDeaths
WHERE 
    continent IS NOT NULL
GROUP BY 
    continent
ORDER BY 
    TotalDeathCount DESC;


--3  global Choropleth Map (Infection Rates Compared to Country Population)
select 
   country , 
   Population, 
   Max(total_cases) as HighestInfectionCount, 
   Max((total_cases/NULLIF(population,0)))*100 as PercentPopulationInfected
From PortfolioProjects..CovidDeaths
--where country like '%states%'
where continent is not null
group by Country, population
order by PercentPopulationInfected desc;


--4  Dynamic Time-Series Line Graph (Daily Infection Rates Over Time)

select 
     country , 
     population , 
     date, 
     Max(total_cases) as HighestInfectionCount, 
     Max((total_cases/NULLIF(population,0)))*100 as PercentPopulationInfected
from PortfolioProjects..CovidDeaths
--Where country like '%states%'
where continent is not null
Group by country, Population, date
order by PercentPopulationInfected desc;


--5 Vaccine Rollout Tracking (Total Population vs Total Cumulative Vaccinations)

Select 
     dea.continent, 
     dea.country,
     dea.date,
     dea.population,
     MAX(vac.total_vaccinations) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProjects..CovidDeaths dea
Join PortfolioProjects..CovidVaccinations vac
	On dea.country = vac.country
	and dea.date = vac.date
where dea.continent is not null 
group by dea.continent, dea.country, dea.date, dea.population
order by 1,2,3;


--Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(New_Cases)*100 as DeathPercentage
--From PortfolioProjects..CovidDeaths
--Where location like '%states%'
---where continent is not null 
--Group By date
order by 1,2



















