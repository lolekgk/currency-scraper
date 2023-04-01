# Currency Scraper

## Table of contents

-   [About the project](#about-the-project)
-   [Tech Stack](#tech-stack)
-   [Dependency management](#dependency-management)
-   [Dependencies](#dependencies)
-   [Future Plans](#future-plans)
-   [Setup](#setup)

## About the project

Currency Scraper is a Python-based backend API that scrapes currency rates from the Poland National Bank website and saves the data in MongoDB. The API is built using FastAPI and BeautifulSoup4 and is ready to be implemented with a matching frontend.

<p align="right">(<a href="#top">back to top</a>)</p>

## Tech stack

-   FastAPI
-   MongoDB
-   Docker and Docker Compose
<p align="right">(<a href="#top">back to top</a>)</p>

## Dependency management

-   poetry
<p align="right">(<a href="#top">back to top</a>)</p>

## Dependencies

-   Python ^3.10
-   FastAPI ^0.85.1
-   beautifulsoup4 ^4.11.1
-   black ^22.10.0
-   uvicorn ^0.18.3
-   requests ^2.28.1
-   lxml ^4.9.1
-   pymongo ^4.3.2
-   python-dotenv ^0.21.0
-   pytest ^7.2.0
-   pytest-cov ^4.0.0
-   pysnooper ^1.1.1

<p align="right">(<a href="#top">back to top</a>)</p>

## Future plans

-   Add celery
-   Scrap data from more tables
-   Add more data filtering options
<p align="right">(<a href="#top">back to top</a>)</p>

## Setup

To run the project you need `Docker` and `Docker Compose` on your machine.

Open your terminal and type in required commands:

```
$ git clone git@github.com:lolekgk/currency-scraper.git
$ cd currency-scraper
```

Fill in provided `.env.sample` file with the required values and save as `.env`.

```
$ docker-compose build
$ docker-compose up
$ docker exec -it currency_scraper bash
```

Visit [0.0.0.0:80/redoc/](http://0.0.0.0/redoc) in the browser to see all available endpoints and their details.

<p align="right">(<a href="#top">back to top</a>)</p>
