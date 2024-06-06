# MIMIC Clinical Decision Making

This repository contains the code to create the MIMIC Clinical Decision Making (MIMIC-CDM) Dataset

```python CreateDataset.py``` creates the dataset from raw MIMIC-IV v2.2 download. Before executing, three paths must be set at the top of the file. base_mimic should be set to the parent folder of your MIMIC-IV download. This folder should contain the hosp and note folders. base_new should be set to a folder where the generated files will be saved. 


```python ConvertPhysionet.py``` creates the pickle files need for the MIMIC Clinical Decision Making task from the MIMIC-CDM downloaded directly from PhysioNet. base_new should be set to the path containing the raw MIMIC-CDM dataset files downloaded from PhysioNet. The MIMIC-CDM dataset can be downloaded from https://physionet.org/content/mimic-iv-ext-cdm/1.0/

## Environment

To setup the environment, create a new virtual environment of your choosing and then run 

```
pip install --no-deps -r requirements.txt
```
