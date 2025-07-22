# F1 analysis

## Commands

- type `python3 run.py` to scrape all of the needed information.

## Data Flow

1. Scrapers in `src/scrapers/` fetch race, team, weather, and racetrack data from external sources.
2. Scraped data is saved as JSON files in the `/data` directory.
3. The main analysis script (`src/main.py`) loads these JSON files, processes the data, and performs analysis (e.g., regression).
4. Results (plots, metrics) are displayed or saved as output.

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the main analysis: `python3 -m src.main`
3. Scraped data will be stored in `/data`, and results will be shown in the terminal or as plots.

## TODO

### Testing

- Add a `/tests` directory with unit tests for utilities and models

### Configuration

- Use a configuration file for URLs, paths, and constants
- Pass dependencies (like file paths, API keys) via config or parameters, not hardcoded

### Code Quality & Structure

- Add type hints and docstrings consistently across all modules
- Follow PEP8 for code style and use relative imports within packages

### Error Handling & Logging

- Improve error handling in scrapers and data loaders
- Use Python’s logging module instead of print statements

### Data Handling

- Validate data when loading/parsing JSON

### Documentation

- Document the data flow and usage in the README

## Random stats

sum of thing in degree 2:
r^2 = 1.328
rsme = 27.38

sum of things in degree 3:
r^2 = 1,797
rsme = 26.523
