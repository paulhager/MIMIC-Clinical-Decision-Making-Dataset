# MIMIC Clinical Decision Making


For a video overview of the paper, checkout this talk I held for the BZKF: https://www.youtube.com/watch?v=sCDaUC16mHA

## News

**🔥 New Addition: Llama 3.3 has been added to the leaderboard! 🔥**

**🔥 New Addition: Llama 3.1 has been added to the leaderboard! 🔥**

**🔥 New Addition: OpenBio has been added to the leaderboard! 🔥**

**🔥 New Addition: Llama 3 has been added to the leaderboard! 🔥**

## Overview

This repository contains the code to create the MIMIC Clinical Decision Making (MIMIC-CDM) Dataset.

Visit https://huggingface.co/spaces/MIMIC-CDM/leaderboard to check out the current leaderboard. I will update this as new models are released. If you would like a model to be tested and put on the board, please write me an email at paul (dot) hager (at) tum (dot) de.


## Environment

To setup the environment, create a new virtual environment of your choosing with python=3.10 and then run:

```
pip install --no-deps -r requirements.txt
```


## Option 1: Generate the dataset from MIMIC-IV-Ext-CDM directly

The most straightforward way of using the data is by downloading it from https://physionet.org/content/mimic-iv-ext-cdm/ and then converting it to the necessary format. To convert it, first set the `base_new` variable at the top of [ConvertPhysionet.py](ConvertPhysionet.py) to the folder containing the downloaded MIMIC-IV-Ext-CDM dataset. Then run:

```python ConvertPhysionet.py```

## Option 2: Generate the dataset from scratch from MIMIC-IV v2.2 

The more laborious and time-intensive way of creating the dataset is from the raw MIMIC-IV v2.2 download. First download the necessary hospital data from https://physionet.org/content/mimiciv/2.2/ and the necessary text data from https://www.physionet.org/content/mimic-iv-note/2.2/.  Then set the following two path variables in [CreateDataset.py](CreateDataset.py):

1. `base_mimic` should be set to the parent folder of your MIMIC-IV download. This folder should contain the [hosp](https://physionet.org/content/mimiciv/2.2/) and [note](https://www.physionet.org/content/mimic-iv-note/2.2/) folders.
2. `base_new` should be set to a folder where the generated files will be saved.

Then run:
   
```python CreateDataset.py```

# Citation

If you found this code and dataset useful, please cite our paper and dataset with:

Hager, P., Jungmann, F., Holland, R. et al. Evaluation and mitigation of the limitations of large language models in clinical decision-making. Nat Med (2024). https://doi.org/10.1038/s41591-024-03097-1
```
@article{hager_evaluation_2024,
	title = {Evaluation and mitigation of the limitations of large language models in clinical decision-making},
	issn = {1546-170X},
	url = {https://doi.org/10.1038/s41591-024-03097-1},
	doi = {10.1038/s41591-024-03097-1},,
	journaltitle = {Nature Medicine},
	shortjournal = {Nature Medicine},
	author = {Hager, Paul and Jungmann, Friederike and Holland, Robbie and Bhagat, Kunal and Hubrecht, Inga and Knauer, Manuel and Vielhauer, Jakob and Makowski, Marcus and Braren, Rickmer and Kaissis, Georgios and Rueckert, Daniel},
	date = {2024-07-04},
}
```

Hager, P., Jungmann, F., & Rueckert, D. (2024). MIMIC-IV-Ext Clinical Decision Making: A MIMIC-IV Derived Dataset for Evaluation of Large Language Models on the Task of Clinical Decision Making for Abdominal Pathologies (version 1.0). PhysioNet. https://doi.org/10.13026/2pfq-5b68.
```
@misc{hager_mimic-iv-ext_nodate,
	title = {{MIMIC}-{IV}-Ext Clinical Decision Making: A {MIMIC}-{IV} Derived Dataset for Evaluation of Large Language Models on the Task of Clinical Decision Making for Abdominal Pathologies},
	url = {https://physionet.org/content/mimic-iv-ext-cdm/1.0/},
	shorttitle = {{MIMIC}-{IV}-Ext Clinical Decision Making},
	publisher = {{PhysioNet}},
	author = {Hager, Paul and Jungmann, Friederike and Rueckert, Daniel},
	urldate = {2024-07-04},
	doi = {10.13026/2PFQ-5B68},
	note = {Version Number: 1.0
Type: dataset},
}
```
