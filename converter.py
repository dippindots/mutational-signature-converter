import csv
import pandas as pd
import sys

# read data from  command line
input_file = sys.argv[1]
output_file = sys.argv[2]

# read data from data file
df = pd.read_csv(input_file, sep='\t')

# delete columns (impact_version, Nmut_Mb, signatureInterpretation) 
if 'impact_version' in df:
    del df['impact_version']
if 'Nmut_Mb' in df:
    del df['Nmut_Mb']
if 'signatureInterpretation' in df:
    del df['signatureInterpretation']

# transpose the data
df = df.transpose()

# change first column name to ENTITY_STABLE_ID
df = df.rename({"Tumor_Sample_Barcode": "ENTITY_STABLE_ID"}, axis='index')

# add name, description and statement columns
mutatinoalSignatureDictionary = {
    "1": "Signature 1, the aging signature, is detected in this case.",
    "2": "Signature 2, the APOBEC signature, is detected in this case.  This signature often coccurs with signature 13, the other APOBEC signature",
    "3": "Signature 3, the signature of Homologous Recombination Repair deficiency is detected in this case.  This signature is most commonly associated with BRCA mutations",
    "4": "Signature 4, the smoking signature is detected in this case",
    "5": "Signature 5 is detected in this case.  We are not confident that we are able to detect signature 5 in the IMPACT cohort.  It is a 'flat' signature--when it is detected it is more likely to be an artefact. In the literature it is associated with age",
    "6": "Signature 6, a MMR signature, is detected in this case.  It is usually associated with high mutational burden.  This signature often co-occurs with other MMR signatures (14, 15, 20, 21 26)",
    "7": "Signature 7, the UV light signature, is detected in this case.",
    "8": "Signature 8 is detected in this case. We are not confident that we are able to detect signature 8 in the IMPACT cohort. It is a 'flat' signature--when it is detected it is more likely to be an artefact. In the literature it is associated with HRD defects",
    "9": "Signature 9 is detected in this case.  We are not confident that we are able to detect signature 9 in the IMPACT cohort.  In the literature it is associated with POLH.",
    "10": "Signature 10, the POLE signature, is detected in this case.  It is associated with functions to the exonucleus domain of the POLE gene and enormous mutational burden.  Oftentimes MMR signatures 6, 14,16, 20,21 and 26 co-occur with the POLE signature.",
    "11": "Signature 11, the Temozolomide (TMZ) signature, is detected in this case.",
    "12": "Signature 12 is detected in this case.  We are not confident that we are able to detect signature 9 in the IMPACT cohort.  In the literature it is found in liver cancer.",
    "13": "Signature 13, the APOBEC signature, is detected in this case.  This signature often coccurs with signature 2, the other APOBEC signature.",
    "14": "Signature 14, the signature of simultaneous MMR and POLE dysfunction is detected in this case.  This signature usually occurs in cases with the POLE signature (signature 10) and other MMR signatures (6, 15, 20, 21 26).",
    "15": "Signature 15, a MMR signature, is detected in this case.  It is usually associated with high mutational burden.",
    "16": "Signature 16 is detected in this case. We are not confident that we are able to detect signature 16 in the IMPACT cohort.  In the literature it is associated with Liver cancer and alcohol consumption.",
    "17": "Signature 17 is detected in this case.  The aetiology of this signature is unknown.  It is predominantly found in gastric cancers.",
    "18": "Signature 18 is detected in this case.  This signature is associated with MUTYH dysfunction and neuroblastoma.",
    "19": "Signature 19 is detected in this case. We are not confident that we are able to detect signature 19 in the IMPACT cohort.",
    "20": "Signature 20 is detected in this case. This signature is associated with MMR and usually occurs in cases with the POLE signature (signature 10) and other MMR signatures (6, 14, 15, 21, 26).",
    "21": "Signature 21 is detected in this case. This signature is associated with MMR and usually co-occurs with other MMR signatures (6, 14, 15, 21, 26).",
    "22": "Signature 22 is detected in this case. We are not confident that we are able to detect signature 22 in the IMPACT cohort. In the literature it is associated with exposure to Aristolochic Acid.",
    "23": "Signature 23 is detected in this case. We are not confident that we are able to detect signature 23 in the IMPACT cohort.",
    "24": "Signature 24 is detected in this case. We are not confident that we are able to detect signature 24 in the IMPACT cohort.  In the literature it is associated with aflatoxin exposure.  In our cohort we believe it is detected by accident in cases with the smoking signature (signature 4).",
    "25": "Signature 25 is detected in this case. We are not confident that we are able to detect signature 25 in the IMPACT cohort.",
    "26": "Signature 26 is detected in this case.  This signature is associated with MMR and usually co-occurs with other MMR signatures (6, 14, 15, 20, 21).",
    "27": "Signature 27 is detected in this case. We are not confident that we are able to detect signature 27 in the IMPACT cohort.",
    "28": "Signature 28 is detected in this case. We are not confident that we are able to detect signature 28 in the IMPACT cohort.  It often co-occurs with signature 28.",
    "29": "Signature 29, the mutational signature of chewing tobacco is detected in this case.",
    "30": "Signature 30 is detected in this case. We are not confident that we are able to detect signature 30 in the IMPACT cohort."
}

displayNameDictionary = {
    "mean": "exposure",
    "confidence": "confidence"
}

def rowFuncForNameColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "NAME"
    if row.name == "Nmut":
        return "Number of mutations"
    return "mutational signature " + row.name.split('_')[1] + " " + displayNameDictionary[row.name.split('_')[0]]

def rowFuncForDescriptionColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "DESCRIPTION"
    if row.name == "Nmut":
        return "Number of mutations"
    return displayNameDictionary[row.name.split('_')[0]] + " data for mutational signature " + row.name.split('_')[1]

def rowFuncForUrlColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "URL"
    if row.name == "Nmut":
        return "NA"
    return "https://cancer.sanger.ac.uk/cosmic/signatures_v2"

def rowFuncForConfidenceStatementColumn(row):
    if row.name == "ENTITY_STABLE_ID":
        return "CONFIDENCE_STATEMENT"
    if row.name == "Nmut":
        return "NA"
    return mutatinoalSignatureDictionary[row.name.split('_')[1]]

df['NAME'] = df.apply(rowFuncForNameColumn, axis = 1)
df['DESCRIPTION'] = df.apply(rowFuncForDescriptionColumn, axis = 1)
df['URL'] = df.apply(rowFuncForUrlColumn, axis = 1)
df['CONFIDENCE_STATEMENT'] = df.apply(rowFuncForConfidenceStatementColumn, axis = 1)

# get a list of columns
cols = list(df)

# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('NAME')))
cols.insert(1, cols.pop(cols.index('DESCRIPTION')))
cols.insert(2, cols.pop(cols.index('URL')))
cols.insert(3, cols.pop(cols.index('CONFIDENCE_STATEMENT')))

# reorder
df = df.loc[:, cols]

# write the output file
out = df.to_csv(output_file, sep='\t', header=False)
