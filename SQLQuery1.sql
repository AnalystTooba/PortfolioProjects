Select *
from [Portfolio Projects]..CovidDeaths$
order by 3, 4

--Select *
--from [Portfolio Projects]..CovidVaccinations$
--order by 3, 4

--Select data that we are going to be using

Select location, date, total_cases, new_cases, total_deaths, population
from [Portfolio Projects]..CovidDeaths$
order by 1,2

-- looking at total cases vs total deaths of United States
-- shows the liklyhood of dying if you attract covid in your country
Select location, date, total_cases,  total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from [Portfolio Projects]..CovidDeaths$
where location like '%states%'
order by 1,2

-- looking at the total cases versus the population
-- what percentage of population got infected with COVID
Select Location, date, Population, total_cases,  (total_cases/population)*100 as PercentPopulationInfected
from [Portfolio Projects]..CovidDeaths$
--Where location like '%states%'
order by 1,2

-- Countries with Highest Infection Rate compared to Population
Select location,   population, max (total_cases) as HighestInfectionCount ,max((total_cases/ population))*100 as MaxPercentofInfectedPopulation
from [Portfolio Projects]..CovidDeaths$
--where location like '%states%'
Group by location, population
order by 4 desc

-- -- Countries with Highest Death Count
Select Location, MAX(cast(Total_deaths as int)) as TotalDeathCount
from [Portfolio Projects]..CovidDeaths$
--Where location like '%states%'
where continent is not null
Group by Location
order by TotalDeathCount desc


-- BREAKING THINGS DOWN BY CONTINENT
Select continent, MAX(cast(Total_deaths as int)) as TotalDeathCount
from [Portfolio Projects]..CovidDeaths$
--Where location like '%states%'
where continent is not null
Group by continent
order by TotalDeathCount desc

-- GLOBAL NUMBERS

Select sum(cast(NEW_cases as int)) AS TOTALCASES, sum(cast(NEW_deaths as int)) AS TOTALDEATHS,
sum(cast(NEW_deaths as int))/sum(NEW_cases)*100 as DeathPercentage
From [Portfolio Projects]..CovidDeaths$
--Where location like '%states%'
where continent is not null 
--Group By date
order by 1,2


-- Total populayion vs vaccinated Population
--	Going to Use CTE
With POPvsVAC (continent, location, date, population, new_vaccinations, RollingVaccinationCount)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum (convert(int, vac.new_vaccinations)) over (Partition by dea.location order by dea.location, dea.date) as RollingVaccinationCount
from [Portfolio Projects]..CovidDeaths$ dea
join [Portfolio Projects]..CovidVaccinations$ vac
on dea.location= vac.location
and dea.date= vac.date
where dea.continent is not null )

Select *, ( RollingVaccinationCount/Population)*100 as PopulationagainstCVaccinated
From PopvsVac


--TEMP TABLE
Drop table if exists #PercentPopulationVaccinated
Create table #PercentPopulationVaccinated
( continent nvarchar(255),
location nvarchar(255), 
date datetime,
population numeric, 
new_vaccinations numeric,
RollingVaccinationCount numeric )

Insert into #PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum (convert(int, vac.new_vaccinations)) over (Partition by dea.location order by dea.location, dea.date) as RollingVaccinationCount
from [Portfolio Projects]..CovidDeaths$ dea
join [Portfolio Projects]..CovidVaccinations$ vac
on dea.location= vac.location
and dea.date= vac.date
where dea.continent is not null

Select *, ( RollingVaccinationCount/Population)*100 as PopulationagainstCVaccinated
From #PercentPopulationVaccinated

--Creating View
Create View PopulationVaccinated 
as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum (convert(int, vac.new_vaccinations)) over (Partition by dea.location order by dea.location, dea.date) as RollingVaccinationCount
from [Portfolio Projects]..CovidDeaths$ dea
join [Portfolio Projects]..CovidVaccinations$ vac
on dea.location= vac.location
and dea.date= vac.date
where dea.continent is not null
