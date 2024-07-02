from os.path import join
import json
import pandas as pd
import ast
import pickle

from utils.nlp import extract_primary_diagnosis
from dataset.utils import write_hadm_to_file

base_new = ""

# Process lab test mapping
lab_test_mapping_df = pd.read_csv(join(base_new, "lab_test_mapping.csv"))
lab_test_mapping_df["corresponding_ids"] = lab_test_mapping_df[
    "corresponding_ids"
].apply(ast.literal_eval)
lab_test_mapping_df["corresponding_ids"] = lab_test_mapping_df[
    "corresponding_ids"
].apply(lambda x: [int(i) for i in x])
pickle.dump(lab_test_mapping_df, open(join(base_new, "lab_test_mapping.pkl"), "wb"))


def update_hadm(base_new, filename, hadm_info, key, hadm_name, _list=False):
    df = pd.read_csv(join(base_new, filename))
    for _, row in df.iterrows():
        _id = row["hadm_id"]
        if _list:
            if hadm_name not in hadm_info[_id]:
                hadm_info[_id][hadm_name] = []
            hadm_info[_id][hadm_name].append(row[key])
        # For single value fields
        else:
            hadm_info[_id][hadm_name] = row[key]
    return hadm_info


hadm_info = {}

# Create entries for all hadm_ids
hpi_df = pd.read_csv(join(base_new, "history_of_present_illness.csv"))
hadm_ids = hpi_df["hadm_id"].to_list()
for _id in hadm_ids:
    hadm_info[_id] = {}

hadm_info = update_hadm(
    base_new, "history_of_present_illness.csv", hadm_info, "hpi", "Patient History"
)

hadm_info = update_hadm(
    base_new, "physical_examination.csv", hadm_info, "pe", "Physical Examination"
)

lab_events_df = pd.read_csv(join(base_new, "laboratory_tests.csv"))
for _, row in lab_events_df.iterrows():
    _id = row["hadm_id"]
    if "Laboratory Tests" not in hadm_info[_id]:
        hadm_info[_id]["Laboratory Tests"] = {}
        hadm_info[_id]["Reference Range Lower"] = {}
        hadm_info[_id]["Reference Range Upper"] = {}
    hadm_info[_id]["Laboratory Tests"][row["itemid"]] = row["valuestr"]
    hadm_info[_id]["Reference Range Lower"][row["itemid"]] = row["ref_range_lower"]
    hadm_info[_id]["Reference Range Upper"][row["itemid"]] = row["ref_range_upper"]

microbiology_df = pd.read_csv(join(base_new, "microbiology.csv"))
for _, row in microbiology_df.iterrows():
    _id = row["hadm_id"]
    if "Microbiology" not in hadm_info[_id]:
        hadm_info[_id]["Microbiology"] = {}
        hadm_info[_id]["Microbiology Spec"] = {}
    hadm_info[_id]["Microbiology"][row["test_itemid"]] = row["valuestr"]
    hadm_info[_id]["Microbiology Spec"][row["test_itemid"]] = row["spec_itemid"]

radiology_df = pd.read_csv(join(base_new, "radiology_reports.csv"))
for _, row in radiology_df.iterrows():
    _id = row["hadm_id"]
    if "Radiology" not in hadm_info[_id]:
        hadm_info[_id]["Radiology"] = []
    hadm_info[_id]["Radiology"].append(
        {
            "Note ID": row["note_id"],
            "Modality": row["modality"],
            "Region": row["region"],
            "Exam Name": row["exam_name"],
            "Report": row["text"],
        }
    )

hadm_info = update_hadm(
    base_new,
    "discharge_diagnosis.csv",
    hadm_info,
    "discharge_diagnosis",
    "Discharge Diagnosis",
)

hadm_info = update_hadm(
    base_new,
    "icd_diagnosis.csv",
    hadm_info,
    "icd_diagnosis",
    "ICD Diagnosis",
    _list=True,
)

hadm_info = update_hadm(
    base_new,
    "discharge_procedures.csv",
    hadm_info,
    "discharge_procedure",
    "Procedures Discharge",
    _list=True,
)

icd_procedures_df = pd.read_csv(join(base_new, "icd_procedures.csv"))
for _, row in icd_procedures_df.iterrows():
    _id = row["hadm_id"]
    if "Procedures ICD9" not in hadm_info[_id]:
        hadm_info[_id]["Procedures ICD9"] = []
        hadm_info[_id]["Procedures ICD9 Title"] = []
        hadm_info[_id]["Procedures ICD10"] = []
        hadm_info[_id]["Procedures ICD10 Title"] = []
    if row["icd_version"] == 9:
        hadm_info[_id]["Procedures ICD9"].append(row["icd_code"])
        hadm_info[_id]["Procedures ICD9 Title"].append(row["icd_title"])
    else:
        hadm_info[_id]["Procedures ICD10"].append(row["icd_code"])
        hadm_info[_id]["Procedures ICD10 Title"].append(row["icd_title"])


# Parse patient case files
with open(join(base_new, "pathology_ids.json")) as f:
    patho_ids = json.load(f)

app_hadm_info_firstdiag = {}
cholec_hadm_info_firstdiag = {}
pancr_hadm_info_firstdiag = {}
divert_hadm_info_firstdiag = {}

for _id in patho_ids["appendicitis"]:
    app_hadm_info_firstdiag[_id] = hadm_info[_id]

for _id in patho_ids["cholecystitis"]:
    cholec_hadm_info_firstdiag[_id] = hadm_info[_id]

for _id in patho_ids["diverticulitis"]:
    divert_hadm_info_firstdiag[_id] = hadm_info[_id]

for _id in patho_ids["pancreatitis"]:
    pancr_hadm_info_firstdiag[_id] = hadm_info[_id]

write_hadm_to_file(
    app_hadm_info_firstdiag, "appendicitis_hadm_info_first_diag", base_new
)
write_hadm_to_file(
    cholec_hadm_info_firstdiag, "cholecystitis_hadm_info_first_diag", base_new
)
write_hadm_to_file(
    pancr_hadm_info_firstdiag, "pancreatitis_hadm_info_first_diag", base_new
)
write_hadm_to_file(
    divert_hadm_info_firstdiag, "diverticulitis_hadm_info_first_diag", base_new
)
