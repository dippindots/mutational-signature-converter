#!/bin/bash

PROJECT_PATH=""
PYTHON_PATH=""
DATA_PATH=""
FASTA_FILE_PATH=""
R_LIBRARY=""
CONVERTER_PATH=""

# initialize conda
# reference: https://github.com/conda/conda/issues/7980#issuecomment-492784093
eval "$(conda shell.bash hook)"

# active environment
conda activate mutational_signature

# get spectrum file
${PYTHON_PATH}python ${PROJECT_PATH}make_spectrum.py ${DATA_PATH}data_mutations_extended.tmp.txt ${PROJECT_PATH}msk_impact.tmp ${FASTA_FILE_PATH}hg19.fa

# get output file
Rscript ${PROJECT_PATH}signature.significance.R -i ${PROJECT_PATH}msk_impact.spectrum.txt --signature_file ${PROJECT_PATH}Stratton_signatures30.txt -o ${PROJECT_PATH}msk_impact.out -m ${PROJECT_PATH}signature.significance.stan -l ${R_LIBRARY}

# get tabular file
Rscript ${PROJECT_PATH}summ_to_tab.R ${PROJECT_PATH}msk_impact.spectrum.txt ${PROJECT_PATH}msk_impact.out ${PROJECT_PATH}msk_impact_tab.out

# convert file
${PYTHON_PATH}python ${CONVERTER_PATH}converter.py ${PROJECT_PATH}msk_impact_tab.out ${PROJECT_PATH}msk_impact_data.txt

echo data file generated at: ${PROJECT_PATH}msk_impact_data.txt
