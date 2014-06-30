# ucbgrades

Code for scraping grade distributions from UC Berkeley's
[ScheduleBuilder](https://schedulebuilder.berkeley.edu/) and
analyzing it.

## Requirements

The project requires Python 2.6 or 2.7 (untested with other versions),
as well as several Python packages, including BeautifulSoup, Requests,
SQLAlchemy, and PyExecJS (which will require a JavaScript runtime).

## Usage

`python run.py` will run the scrapers, populate a SQLite3 database
`grades.db`, and output department course averages to `dept_avgs.csv`.
`plots/plots.R` will generate some histograms and a density overlay
plot once the path to the CSV file is changed inside the script.
