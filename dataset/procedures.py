import re


def extract_procedure_from_discharge_summary(discharge_summary):
    # Extracts everything after the "Major Surgical or Invasive Procedure:" line until the next empty line
    # Returns a list of procedures
    procedure_substrings = [
        "Major Surgical or Invasive Procedure:",
        "PROCEDURES:",
        "PROCEDURE:",
        "Major Surgical ___ Invasive Procedure:",
        "___ Surgical or Invasive Procedure:",
        "INVASIVE PROCEDURE ON THIS ADMISSION:",
        "Major ___ or Invasive Procedure:",
        "MAJOR SURGICAL AND INVASIVE PROCEDURES PERFORMED THIS DURING\nADMISSION:",
    ]
    for substring in procedure_substrings:
        pattern = rf"{re.escape(substring)}.*?\n\s*\n"
        match = re.search(pattern, discharge_summary, re.DOTALL)
        if match:
            procedures_string = match.group(0)

            # Remove section title
            procedures_string = procedures_string.replace(substring, "")

            # Replace newline with space to make one sentence
            procedures_string = procedures_string.replace("\n", " ")

            # Split on delimiters
            procedures = re.split(r"\: |, |\. | - ", procedures_string)

            # Clean
            procedures = [proc.strip() for proc in procedures if proc.strip() != ""]
            return procedures
    return []


def extract_procedures(hadm_info, procedures_df_icd9, procedures_df_icd10):
    for _id in hadm_info:
        discharge_procedures = extract_procedure_from_discharge_summary(
            hadm_info[_id]["Discharge"]
        )
        if len(discharge_procedures) == 0:
            print("No procedures found for {}".format(_id))
        hadm_info[_id]["Procedures Discharge"] = discharge_procedures

        procedures_icd9 = procedures_df_icd9[procedures_df_icd9["hadm_id"] == _id][
            "icd_code"
        ].values
        hadm_info[_id]["Procedures ICD9"] = procedures_icd9.tolist()
        hadm_info[_id]["Procedures ICD9"] = [int(p) for p in procedures_icd9]

        procedures_str = procedures_df_icd9[procedures_df_icd9["hadm_id"] == _id][
            "long_title"
        ].values
        hadm_info[_id]["Procedures ICD9 Title"] = procedures_str.tolist()

        procedures_icd10 = procedures_df_icd10[procedures_df_icd10["hadm_id"] == _id][
            "icd_code"
        ].values
        hadm_info[_id]["Procedures ICD10"] = procedures_icd10.tolist()
        hadm_info[_id]["Procedures ICD10"] = [str(p) for p in procedures_icd10]

        procedures_str = procedures_df_icd10[procedures_df_icd10["hadm_id"] == _id][
            "long_title"
        ].values
        hadm_info[_id]["Procedures ICD10 Title"] = procedures_str.tolist()
    return hadm_info
