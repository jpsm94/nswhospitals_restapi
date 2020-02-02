# nswhospitals_restapi
A Flask-RESTPlus application for searching for hospitals in NSW

# Source Dataset
https://data.nsw.gov.au/data/dataset/nsw-hospitals

# Setup
```
git clone https://github.com/jpsm94/nswhospitals_restapi.git
cd nswhospitals_restapi
```

# Data Preparation
- SQLite database, NSW_HOSPITALS.sqlite is included in the repo
- see the Jupyter Notebook, nswhospitals_dataprep.ipynb for details on how the database was set up

# Running the application
## Install required Python libraries
```
pip install -r requirements.txt 
```

## Run application
```
python app.py
```
