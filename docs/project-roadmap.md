# Portfolio Investment Tracking System - Project Roadmap

This document provides a high-level overview of the step-by-step approach to build the complete Django portfolio investment tracking system, including all core requirements and bonus features.

---

## 0. Create GitHub Repository for Reviewers

- Initialize a new Git repository locally
- Create a GitHub repository to host the project
- Set up remote connection between local repository and GitHub
- Create an initial README.md with project description
- Ensure repository is properly configured for collaboration and code review

---

## 1. Make sure you have everything in your machine that you'll need in order to finish this assignment

### Required Software and Tools
- **Python** (3.8+ recommended) - for Django development
- **Django** - web framework
- **Django REST Framework** - for building REST APIs
- **PostgreSQL/SQLite** - database system (SQLite for development, PostgreSQL preferred for production)
- **Git** - version control system
- **Virtual environment tool** (venv, virtualenv, or poetry) - for dependency management
- **Code editor/IDE** - with Python and Django support
- **Excel file reader library** (openpyxl or pandas) - for reading datos.xlsx
- **Graphing/visualization library** (Plotly, Chart.js, or matplotlib) - for Bonus 1 visualizations
- **django-filter** - for filtering in selectors (as per styleguide)
- **django-environ** - for environment variable management (as per styleguide)
- **Testing framework** (pytest or Django's TestCase) - for writing tests

### Required Files
- `datos.xlsx` - Excel file containing weights and prices data
- All documentation files (Enunciado, Styleguide, Git guide)

---

## 2. Initialize project

- Create a new Django project following the styleguide structure
- Set up project configuration directory (config/django/ with base.py, production.py, test.py)
- Create virtual environment and install dependencies
- Initialize Git repository and create initial commit
- Set up .gitignore file
- Create requirements.txt or similar dependency file
- Configure environment variables using django-environ
- Set up basic project settings in config/django/base.py
- Create main project structure

---

## 3. Set up project structure following Django Styleguide

- Create Django apps as needed (likely a `portfolios` app or similar domain-based app)
- Set up the standard app structure:
  - `models.py` - for data models
  - `services.py` - for business logic (write operations)
  - `selectors.py` - for data fetching logic
  - `apis.py` - for APIView classes
  - `filters.py` - for django-filter FilterSets
  - `urls.py` - for URL routing
  - `admin.py` - for Django admin configuration
  - `tests/` directory with subdirectories for models, services, and selectors
- Create a BaseModel class with created_at and updated_at fields
- Set up URL configuration following the styleguide pattern (domain patterns)
- Configure Django REST Framework settings
- Set up exception handling structure (if custom exception handler needed)

---

## 4. Design and create data models

- **Asset Model**: Represents the 17 investable assets (with name, symbol, etc.)
- **Portfolio Model**: Represents the 2 portfolios (Portfolio 1 and Portfolio 2)
- **Price Model**: Stores historical prices for each asset (asset, date, price)
- **PortfolioWeight Model**: Stores initial weights for assets in portfolios (portfolio, asset, initial_weight)
- **PortfolioHolding Model** (optional): Tracks quantities held over time (portfolio, asset, date, quantity)
- **PortfolioValue Model** (optional): Stores calculated portfolio values over time (portfolio, date, total_value)
- **Transaction Model** (for Bonus 2): Stores buy/sell transactions (portfolio, asset, date, transaction_type, amount)

Consider relationships, constraints, and indexes. All models should inherit from BaseModel. Use database constraints where appropriate for validation.

---

## 5. Create ETL function to load datos.xlsx data

- Create a management command or service function to read the Excel file
- Read the "Weights" sheet to extract initial weights for Portfolio 1 and Portfolio 2
- Read the "Precios" sheet to extract historical prices for all 17 assets
- Parse dates correctly (15/02/22 format)
- Create Asset instances for all 17 assets
- Create Portfolio instances (Portfolio 1 and Portfolio 2)
- Store initial weights in the database
- Store all historical prices in the database
- Handle data validation and error cases
- Test the ETL process to ensure data integrity

This ETL function should be callable via a management command (e.g., `python manage.py load_portfolio_data`).

---

## 6. Calculate initial quantities for both portfolios

- Create a service function to calculate initial quantities
- For each portfolio (V₀ = $1,000,000,000 on 15/02/22):
  - For each asset in the portfolio:
    - Retrieve initial weight (w_{i,0}) from database
    - Retrieve initial price (P_{i,0}) for date 15/02/22
    - Calculate initial quantity: C_{i,0} = (w_{i,0} * V₀) / P_{i,0}
    - Store the initial quantity in the database
- Ensure calculations are performed using Django ORM queries
- Store quantities in a way that supports time-series tracking (consider PortfolioHolding model)

---

## 7. Create selectors for data retrieval

- Create selector functions following styleguide patterns:
  - `portfolio_list` - get all portfolios
  - `portfolio_get` - get specific portfolio
  - `asset_list` - get all assets
  - `price_list` - get prices with date filtering
  - `portfolio_weight_list` - get weights with filtering
  - `portfolio_holding_list` - get holdings with date range filtering
- Implement filtering using django-filter FilterSets in filters.py
- Ensure selectors use keyword-only arguments and type annotations
- Design selectors to efficiently fetch data needed for API endpoints and calculations

---

## 8. Create services for business logic

- Create service functions for write operations:
  - `portfolio_create` - create new portfolio
  - `asset_create` - create new asset
  - `price_create` - create price record
  - `portfolio_holding_update` - update holdings (for Bonus 2)
- All services should:
  - Use `@transaction.atomic` decorator when needed
  - Use keyword-only arguments
  - Have type annotations
  - Call `obj.full_clean()` before saving
- Create calculation services:
  - Service to calculate portfolio value (V_t) at a given date
  - Service to calculate asset weights (w_{i,t}) at a given date
  - Service to calculate asset amounts (x_{i,t}) at a given date

---

## 9. Create REST API endpoints for weights and portfolio values

- Create API classes following styleguide patterns (EntityActionApi naming):
  - `PortfolioWeightsListApi` - returns weights over date range
  - `PortfolioValuesListApi` - returns portfolio values over date range
- Each API should:
  - Have InputSerializer for validating fecha_inicio and fecha_fin parameters
  - Have OutputSerializer for response data
  - Use selectors to fetch data (not direct ORM queries)
  - Use services for calculations
  - Return JSON responses
- Implement date range filtering (fecha_inicio to fecha_fin)
- Use Django ORM through selectors to retrieve prices and calculate:
  - w_{i,t} = (p_{i,t} * c_{i,0}) / V_t (where quantities remain constant)
  - V_t = Σ(x_{i,t}) = Σ(p_{i,t} * c_{i,0})
- Configure URL routing following styleguide pattern (one URL per API, domain patterns)
- Test endpoints with various date ranges

---

## 10. Bonus 1: Create visualization views

- Create a view (TemplateView or similar) that displays graphs
- Integrate with the REST API endpoints created in step 9 (either by calling them internally or using JavaScript to fetch data)
- Implement stacked area chart for weights (w_{i,t}):
  - X-axis: dates (fecha_inicio to fecha_fin)
  - Y-axis: percentage (0-100%)
  - Stacked areas for each asset showing weight evolution
- Implement line chart for portfolio values (V_t):
  - X-axis: dates
  - Y-axis: portfolio value in dollars
  - Separate lines for Portfolio 1 and Portfolio 2
- Add date range selector to the view
- Style the view appropriately with modern UI/UX
- Ensure graphs are interactive and informative

---

## 11. Bonus 2: Implement transaction processing

- Design transaction model and relationships (if not done in step 4)
- Create service function to process transactions:
  - `portfolio_transaction_process` - handles buy/sell operations
- For the specific example (15/05/2022 transaction):
  - Sell $200,000,000 worth of "EEUU" asset from Portfolio 1
  - Buy $200,000,000 worth of "Europa" asset for Portfolio 1
  - Calculate new quantities based on prices at transaction date
  - Update holdings: reduce EEUU quantity, increase Europa quantity
- After transaction date, recalculate:
  - c_{i,t} - quantities change at transaction date and remain constant afterward
  - x_{i,t} = p_{i,t} * c_{i,t} (using updated quantities)
  - w_{i,t} = x_{i,t} / V_t
  - V_t = Σ(x_{i,t})
- Ensure transaction processing maintains data integrity
- Update API endpoints to reflect transaction history
- Update visualization views to show impact of transactions

---

## 12. Write tests

- Create test structure following styleguide:
  - `tests/models/` - test models with validation
  - `tests/services/` - test business logic in services
  - `tests/selectors/` - test data fetching logic
- Test ETL function:
  - Data loading correctness
  - Data validation
- Test calculation services:
  - Initial quantity calculations
  - Portfolio value calculations
  - Weight calculations
- Test API endpoints:
  - Input validation
  - Response format
  - Date range filtering
- Test transaction processing (Bonus 2):
  - Transaction execution
  - Quantity updates
  - Recalculation after transactions
- Use factories (factory_boy) and fakes (faker) for test data
- Ensure good test coverage for critical business logic

---

## 13. Set up Django Admin

- Register all models in admin.py
- Configure admin interfaces for:
  - Assets
  - Portfolios
  - Prices
  - Weights
  - Holdings
  - Transactions (if applicable)
- Add useful list filters and search functionality
- Configure inline editing where appropriate
- Ensure admin is user-friendly for data inspection and management

---

## 14. Code quality and styleguide compliance

- Review all code against Django styleguide requirements:
  - Business logic in services/selectors (not in APIs or models)
  - Proper use of BaseModel
  - Type annotations in services and selectors
  - Keyword-only arguments
  - Proper use of full_clean() in services
  - Filtering logic in selectors using FilterSets
  - API structure (one class per operation, Input/Output serializers)
  - URL patterns (one URL per API, domain patterns)
- Run code quality tools (ruff, if configured)
- Ensure consistency across the codebase
- Review for any styleguide violations

---

## 15. Documentation

- Update README.md with:
  - Project description
  - Setup instructions
  - How to run the ETL process
  - How to access APIs
  - How to use visualization views
  - Environment variables needed
- Document API endpoints (list endpoints, parameters, responses)
- Add docstrings to services and selectors
- Document any complex business logic or calculations

---

## 16. Git workflow and commits

- Follow Git workflow guide throughout development:
  - Create feature branches for each major component (feature/models, feature/etl, feature/api, etc.)
  - Use conventional commit messages (feat, fix, refactor, test, etc.)
  - Keep commits focused and logical
  - Use descriptive branch names (feature/portfolio-models, feature/etl-loading, etc.)
- Before finalizing:
  - Review commit history
  - Ensure commits follow conventions
  - Clean up any unnecessary commits (if needed)
  - Ensure main/master branch has clean, meaningful commits

---

## 17. Final review and cleanup

- Review all requirements checklist:
  - ✅ Django project with proper models
  - ✅ ETL function for datos.xlsx
  - ✅ Initial quantity calculations
  - ✅ REST API endpoints (weights and values)
  - ✅ Bonus 1: Visualization views
  - ✅ Bonus 2: Transaction processing
  - ✅ Styleguide compliance
- Test the complete system end-to-end
- Verify data accuracy and calculations
- Check for any bugs or edge cases
- Clean up any temporary files or debug code
- Ensure project runs smoothly from scratch (fresh install)
- Prepare final commit and ensure repository is ready for review

---

## 18. Prepare for submission

- Ensure all code is committed and pushed to GitHub
- Verify repository is accessible and well-organized
- Double-check that datos.xlsx is either included or documented where to place it
- Create a summary document if needed (or ensure README is comprehensive)
- Verify all dependencies are listed in requirements.txt
- Test that a fresh clone and setup works correctly
- Ensure README includes clear instructions for reviewers

---

## Notes

- This roadmap assumes a logical order, but some steps can be done in parallel or reordered based on preference
- The styleguide should be followed throughout all development steps
- Git workflow conventions should be used from the beginning
- Testing can be done incrementally as features are developed
- The transaction processing (Bonus 2) requires careful consideration of how to handle historical data recalculations

---

*This roadmap serves as a high-level guide. Detailed implementation decisions will be made during development while adhering to the Django Styleguide and Git workflow conventions.*
