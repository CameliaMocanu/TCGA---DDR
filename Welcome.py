import streamlit as st

st.title("TCGA-DDR: A Web Tool for Genomic and Survival Analysis")

st.markdown("""
**TCGA-DDR** is a web tool that allows users to define from 1 to 10 DNA-damage deficient TCGA groups and compute:

1. Population statistics across cancer types based on user-defined deficiency groups
2. Survival analysis
3. DDR footprints
""")

st.header("Tutorial for Using the TCGA-DDR Web Tool")

st.subheader("1. Create a Group")

st.markdown("""
**A. Choose How Many Deficiency Groups to Compare**  
You can compare from 1 to 10 deficiency groups. In this tutorial, we will choose 2 groups: **MMR** (Mismatch Repair Deficient) and **P53** (TP53 Deficient).
""")

st.markdown("""
**B. Choose Which Genes Define Each Deficiency Group**  
A deficiency group is determined by the loss of one or multiple genes of interest. If more than one gene is chosen within a group, users can decide whether:

- The group is defined by the concomitant loss of genes (i.e., the group needs to be deficient in **ALL of the genes**).
- Any of the chosen genes is sufficient to define the deficiency (i.e., the group is deficient if **ANY of the genes** are found to be lost).

In this tutorial, the MMR and P53 groups are defined as follows:

- **MMR Group**: loss in either MLH1, MSH2, PMS2
- **P53 Group**: loss in TP53
""")

st.markdown("""
Once the deficiency groups have been created, the tool computes all possible TCGA cohorts. In our case, these would be:

- **dMMR-dP53**: Deficient in MMR, deficient in TP53
- **dMMR-pP53**: Deficient in MMR, proficient in TP53
- **pMMR-dP53**: Proficient in MMR, deficient in TP53
- **pMMR-pP53**: Proficient in MMR, proficient in TP53

> Where **d** indicates 'deficient' and **p** indicates 'proficient'.
""")

st.image("https://github.com/user-attachments/assets/0a1130b7-fdcb-47e2-b0a2-894b3fa47186")

st.subheader("2. Survival Analysis")

st.markdown("""
Original data-set: [Liu et al. 2018](https://doi.org/10.1016/j.cell.2018.02.052)

The endpoints available for survival analysis are: Overall survival (OS), Disease-specific survival (DDS), Disease-free interval (DFI) and Progression-free interval (PFI). A brief explanation for each endpoint is provided, as well as suggestion for which endpoint to be used based on [Liu et al. 2018](https://doi.org/10.1016/j.cell.2018.02.052). 
In this tutorial, we are interested in BRCA, OV and UCEC cancers. All endpoints are recommended for OV and UCEC, but OS and DSS have a cautionary note for BRCA samples. For this tutorial, we will plot the DFI, but users can decide on other endpoints that suit their analysis.
The tool plots a Kaplan-Meier probability curve and provides Log-Rank Test Results.
""")

st.image("https://github.com/user-attachments/assets/614636ab-c76f-48fc-922b-84d777587e44")
st.image("https://github.com/user-attachments/assets/b7f293b6-7a85-4577-a094-ed038e74f4f4")

st.subheader("3. DDR Footprint")

st.markdown("""
Original data-set: [Knijnenburg et al. 2018](https://doi.org/10.1016/j.celrep.2018.03.076)

This page offers insights into the genomic landscape of the deficiency groups of interest. Users can either display one plot for each feature or all plots simultaneously.

Furthermore, there is an added functionality to split the analysis according to cancer types. The 'Split by cancer type' option enables the interactive bar chart to allow users to select or deselect cancer types from the legend on the right-hand side.
""")

st.video("https://github.com/user-attachments/assets/c7ba8969-7074-4769-9b21-c5a909d1609f")

st.markdown("""
Please visit the original paper for further information: [Knijnenburg et al. 2018](https://doi.org/10.1016/j.celrep.2018.03.076)
""")

st.header("FAQ")

st.markdown("""
**Q: How are DDR gene losses defined?**

The DDR gene loss data is derived from [Knijnenburg et al. 2018](https://doi.org/10.1016/j.celrep.2018.03.076). Please refer to the article for in-depth details.

In short, a gene is marked as lost if any of the following conditions are met:

1. Deep copy-number genomic deletion
2. Somatic truncating and missense mutations
3. Coupled analysis of methylation and mRNA expression data
""")
