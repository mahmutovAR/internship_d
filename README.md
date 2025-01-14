# API autotests
***


## Requirements
* [Python](https://www.python.org/downloads/) (3.12)
* [Allure](https://allurereport.org/docs/install/) (2.30.0)
* [Docker](https://www.docker.com/get-started/) (24.0.5)
* WordPress training project

The Python packages can be installed by running  
```commandline
python3 -m pip install -r requirements.txt
```
***


# Run tests and generate Allure report
```
./run_pytest_with_allure.sh
```
***


### Files and directories:
- `allure-report/index.html` allure report
- `allure-results/` test results directory  
**Note:** These directories will be created after running tests script

* `data/` module with settings and data (database and api configuration, data classes and generators)
* `tests/` test modules
* `create_env_properties_file.py` info file generating script
* `requirements.txt` required packages
* `run_pytest_with_allure.sh` testing script