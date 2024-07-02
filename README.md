# MIMIC Clinical Decision Making

This repository contains the code to create the MIMIC Clinical Decision Making (MIMIC-CDM) Dataset.

## Environment

To setup the environment, create a new virtual environment of your choosing with python=3.10 and then run:

```
pip install --no-deps -r requirements.txt
```


## Option 1: Generate the dataset from MIMIC-IV-Ext-CDM directly

The most straightforward way of using the data is by downloading it from https://physionet.org/content/mimic-iv-ext-cdm/ and then converting it to the necessary format. To convert it, first set the `base_new` variable at the top of [ConvertPhysionet.py](ConvertPhysionet.py) to the folder containing the downloaded MIMIC-IV-Ext-CDM dataset. Then run:

```python ConvertPhysionet.py```

## Option 2: Generate the dataset from scratch from MIMIC-IV v2.2 

The more laborious and time-intensive way of creating the dataset is from the raw MIMIC-IV v2.2 download. First set the following two path variables in [CreateDataset.py](CreateDataset.py):

1. `base_mimic` should be set to the parent folder of your MIMIC-IV download. This folder should contain the hosp and note folders.
2. `base_new` should be set to a folder where the generated files will be saved.

Then run:
   
```python CreateDataset.py```
