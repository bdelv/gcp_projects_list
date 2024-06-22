# Function
When it's cleaning time!
Lists all GCP projects in a CSV format

Format: organisation | Project name | ProjectId | LifecycleState | createTime | Owners

# Install

```
virtualenv -p /usr/bin/python3 ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

# Execution

```
python gcpprojects.py
```
Note: You need to be authenticated using
```
gcloud auth application-default login
```

# Leave the virtual environment
```
deactivate
```
