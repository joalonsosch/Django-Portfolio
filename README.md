# Portfolio Investment Tracking System

A Django-based system for tracking and analyzing investment portfolios with multiple assets over time.

## Project Description

This system models investment portfolios composed of multiple assets, tracking:
- Asset prices over time ($p_{i,t}$)
- Asset quantities ($c_{i,t}$)
- Asset amounts ($x_{i,t} = p_{i,t} \times c_{i,t}$)
- Portfolio weights ($w_{i,t} = x_{i,t} / V_t$)
- Portfolio total values ($V_t = \sum x_{i,t}$)

## Features

- Django models for assets, portfolios, prices, and weights
- ETL function to load data from Excel files
- REST API endpoints for portfolio weights and values
- Initial quantity calculations based on initial weights and portfolio value
- Visualization views for portfolio analysis (Bonus 1)
- Transaction processing for buy/sell operations (Bonus 2)

## Requirements

- Python 3.8+
- Django
- Django REST Framework
- PostgreSQL/SQLite
- Excel file reader (openpyxl or pandas)
- Visualization library (Plotly, Chart.js, or matplotlib)

## Documentation

Project documentation is available in the `docs/` folder:
- `project-roadmap.md` - Complete development roadmap
- `enunciado.md` - Project requirements and specifications
- `django-styleguide.md` - Django coding styleguide
- `branches-and-commits-styleguide.md` - Git workflow conventions

## Setup Instructions

_To be completed during project development_

## API Endpoints

_To be documented during project development_

## Project Structure

This project follows the Django Styleguide conventions with:
- Business logic in `services.py` and `selectors.py`
- API endpoints in `apis.py`
- Models in `models.py`
- Tests organized by domain (models, services, selectors)

## License

_To be determined_
