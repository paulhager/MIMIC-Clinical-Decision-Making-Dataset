from os.path import join
import pickle

from dataset.dataset import load_data, extract_info, extract_hadm_ids
from dataset.utils import load_hadm_from_file
from utils.nlp import extract_primary_diagnosis
from dataset.labs import generate_lab_test_mapping

base_mimic = ""
base_new = ""
MIMIC_hosp_base = join(base_mimic, "hosp")


(
    admissions_df,
    transfers_df,
    diag_icd,
    procedures_df,
    discharge_df,
    radiology_report_df,
    radiology_report_details_df,
    lab_events_df,
    microbiology_df,
) = load_data(base_mimic)

# Appendicitis
app_hadm_ids = extract_hadm_ids("acute appendicitis", diag_icd, discharge_df)

app_hadm_info, app_hadm_info_clean = extract_info(
    app_hadm_ids,
    "appendicitis",
    ["acute appendicitis", "appendicitis", "appendectomy"],
    discharge_df,
    admissions_df,
    transfers_df,
    lab_events_df,
    microbiology_df,
    radiology_report_df,
    radiology_report_details_df,
    diag_icd,
    procedures_df,
)

# Cholecystitis
cholec_hadm_ids = extract_hadm_ids("acute cholecystitis", diag_icd, discharge_df)

cholec_hadm_info, cholec_hadm_info_clean = extract_info(
    cholec_hadm_ids,
    "cholecystitis",
    ["acute cholecystitis", "cholecystitis", "cholecystostomy"],
    discharge_df,
    admissions_df,
    transfers_df,
    lab_events_df,
    microbiology_df,
    radiology_report_df,
    radiology_report_details_df,
    diag_icd,
    procedures_df,
)

# Pancreatitis
pancr_hadm_ids = extract_hadm_ids("acute pancreatitis", diag_icd, discharge_df)

pancr_hadm_info, pancr_hadm_info_clean = extract_info(
    pancr_hadm_ids,
    "pancreatitis",
    ["acute pancreatitis", "pancreatitis", "pancreatectomy"],
    discharge_df,
    admissions_df,
    transfers_df,
    lab_events_df,
    microbiology_df,
    radiology_report_df,
    radiology_report_details_df,
    diag_icd,
    procedures_df,
)

# Diverticulitis
divert_hadm_ids = extract_hadm_ids(
    "diverticulitis", diag_icd, discharge_df, diag_counts=30, cc=10
)

divert_hadm_info, divert_hadm_info_clean = extract_info(
    divert_hadm_ids,
    "diverticulitis",
    ["acute diverticulitis", "diverticulitis"],
    discharge_df,
    admissions_df,
    transfers_df,
    lab_events_df,
    microbiology_df,
    radiology_report_df,
    radiology_report_details_df,
    diag_icd,
    procedures_df,
)


# Create Dr Evaluation cases
all_pathos = ["appendicitis", "cholecystitis", "pancreatitis", "diverticulitis"]

dr_eval = {}

# randomly sampled 20 cases from each patho
dr_eval["appendicitis"] = [
    20414022,
    20921058,
    21528320,
    22360162,
    23101737,
    23459798,
    23472780,
    23553042,
    24613821,
    25579760,
    25731420,
    26064146,
    27022057,
    27260340,
    28174867,
    28466255,
    29080331,
    29468247,
    29646721,
    29815898,
]
dr_eval["cholecystitis"] = [
    20491815,
    22023307,
    22386848,
    22825632,
    23322902,
    24642301,
    24646115,
    25643992,
    26014747,
    26146550,
    26286187,
    26354137,
    26679345,
    26983655,
    27286714,
    28342261,
    28862495,
    29573603,
    29580001,
    29723478,
]
dr_eval["pancreatitis"] = [
    20275938,
    20464014,
    20804346,
    21238215,
    21285450,
    21849575,
    22778345,
    23507935,
    23869693,
    24338433,
    24571788,
    24706695,
    25693057,
    25706907,
    25779570,
    26086670,
    26351914,
    27875265,
    29037588,
    29413431,
]
dr_eval["diverticulitis"] = [
    20348908,
    20754081,
    21177686,
    21233315,
    21793374,
    21906103,
    22631597,
    24009412,
    24188879,
    25568418,
    25682814,
    26581302,
    27371462,
    27794752,
    27989275,
    28678157,
    28967154,
    29137933,
    29270681,
    29781321,
]
dr_eval["gastritis"] = [23541137, 25942424, 27148050, 29661958, 29405818]
dr_eval["urinary_tract_infection"] = [23228674, 21812195, 28441616, 26600738, 27795432]
dr_eval["esophageal_reflux"] = [27209421, 22004397, 27318752, 27297450, 29649502]
dr_eval["hernia"] = [28020857, 24364147, 21309128, 26512162, 26027327]

# Manual corrections after case review. These _ids have multiple diagnoses of our abdominal pathologies and are thus too inspecific
multi_diag_ids = [26769588, 24309551, 20525915, 23074436]

id_difficulty = {}
for patho, hadm_info in zip(
    ["appendicitis", "cholecystitis", "pancreatitis", "diverticulitis"],
    [
        app_hadm_info_clean,
        cholec_hadm_info_clean,
        pancr_hadm_info_clean,
        divert_hadm_info_clean,
    ],
):
    first_diag_ids = []
    for p in hadm_info:
        if p in multi_diag_ids:
            continue
        dd = hadm_info[p]["Discharge Diagnosis"]
        dd = dd.lower()
        first_diag = extract_primary_diagnosis(dd)
        if first_diag and patho in first_diag.lower():
            first_diag_ids.append(p)

    id_difficulty[patho] = {"first_diag": first_diag_ids, "dr_eval": dr_eval[patho]}
    print(
        f"There are {len(first_diag_ids)} {patho} cases with first diagnosis out of {len(hadm_info)} total cases"
    )
    print()

id_difficulty["gastritis"] = {}
id_difficulty["gastritis"]["dr_eval"] = dr_eval["gastritis"]

id_difficulty["urinary_tract_infection"] = {}
id_difficulty["urinary_tract_infection"]["dr_eval"] = dr_eval["urinary_tract_infection"]

id_difficulty["esophageal_reflux"] = {}
id_difficulty["esophageal_reflux"]["dr_eval"] = dr_eval["esophageal_reflux"]

id_difficulty["hernia"] = {}
id_difficulty["hernia"]["dr_eval"] = dr_eval["hernia"]

pickle.dump(id_difficulty, open(join(base_new, "id_difficulty.pkl"), "wb"))

id_difficulty = pickle.load(open(join(base_new, "id_difficulty.pkl"), "rb"))
for patho, hadm_info in zip(
    ["appendicitis", "cholecystitis", "pancreatitis", "diverticulitis"],
    [app_hadm_info, cholec_hadm_info, pancr_hadm_info, divert_hadm_info],
):
    hadm_info_firstdiag = {}
    for _id in id_difficulty[patho]["first_diag"]:
        hadm_info_firstdiag[_id] = hadm_info[_id]
    pickle.dump(
        hadm_info_firstdiag,
        open(join(base_new, f"{patho}_hadm_info_first_diag.pkl"), "wb"),
    )


# Generate lab test mapping files
generate_lab_test_mapping(MIMIC_hosp_base)

lab_test_mapping_df = pickle.load(
    open(join(MIMIC_hosp_base, "lab_test_mapping.pkl"), "rb")
)
lab_test_mapping_df.to_csv(join(base_new, "lab_test_mapping.csv"), index=False)
