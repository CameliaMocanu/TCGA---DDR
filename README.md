# TCGA-DDR: A Web Tool for Genomic and Survival Analysis

**TCGA-DDR** is a web tool that allows users to define from 1 to 10 DNA-damage deficient TCGA groups and compute:

1. Population statistics across cancer types based on user-defined deficiency groups
2. Survival analysis
3. DDR footprints

## Tutorial for Using the TCGA-DDR Web Tool

### 1. Create a Group

#### A. Choose How Many Deficiency Groups to Compare
You can compare from 1 to 10 deficiency groups.

In this tutorial, we will choose 2 groups: **MMR** (Mismatch Repair Deficient) and **P53** (TP53 Deficient).

#### B. Choose Which Genes Define Each Deficiency Group
A deficiency group is determined by the loss of one or multiple genes of interest. If more than one gene is chosen within a group, users can decide whether:

- The group is defined by the concomitant loss of genes (i.e., the group needs to be deficient in **ALL of the genes**).
- Any of the chosen genes is sufficient to define the deficiency (i.e., the group is deficient if **ANY of the genes** are found to be lost).

In this tutorial, the MMR and P53 groups are defined as follows:

- **MMR Group**: loss in either MLH1, MSH2, PMS2
- **P53 Group**: loss in TP53

#### C. Choose Which Cancer Types to be Analyzed

<details>
  <summary>Click to Expand/Collapse the List of Cancer Types</summary>

| **Abbreviation** | **Cancer Type Full Name**                                             |
|------------------|------------------------------------------------------------------------|
| LAML             | Acute Myeloid Leukemia                                                |
| ACC              | Adrenocortical carcinoma                                              |
| BLCA             | Bladder Urothelial Carcinoma                                          |
| LGG              | Brain Lower Grade Glioma                                              |
| BRCA             | Breast invasive carcinoma                                             |
| CESC             | Cervical squamous cell carcinoma and endocervical adenocarcinoma      |
| CHOL             | Cholangiocarcinoma                                                    |
| LCML             | Chronic Myelogenous Leukemia                                          |
| COAD             | Colon adenocarcinoma                                                  |
| CNTL             | Controls                                                              |
| ESCA             | Esophageal carcinoma                                                  |
| FPPP             | FFPE Pilot Phase II                                                   |
| GBM              | Glioblastoma multiforme                                               |
| HNSC             | Head and Neck squamous cell carcinoma                                 |
| KICH             | Kidney Chromophobe                                                    |
| KIRC             | Kidney renal clear cell carcinoma                                     |
| KIRP             | Kidney renal papillary cell carcinoma                                 |
| LIHC             | Liver hepatocellular carcinoma                                        |
| LUAD             | Lung adenocarcinoma                                                   |
| LUSC             | Lung squamous cell carcinoma                                          |
| DLBC             | Lymphoid Neoplasm Diffuse Large B-cell Lymphoma                       |
| MESO             | Mesothelioma                                                          |
| MISC             | Miscellaneous                                                         |
| OV               | Ovarian serous cystadenocarcinoma                                     |
| PAAD             | Pancreatic adenocarcinoma                                             |
| PCPG             | Pheochromocytoma and Paraganglioma                                    |
| PRAD             | Prostate adenocarcinoma                                               |
| READ             | Rectum adenocarcinoma                                                 |
| SARC             | Sarcoma                                                               |
| SKCM             | Skin Cutaneous Melanoma                                               |
| STAD             | Stomach adenocarcinoma                                                |
| TGCT             | Testicular Germ Cell Tumors                                           |
| THYM             | Thymoma                                                               |
| THCA             | Thyroid carcinoma                                                     |
| UCS              | Uterine Carcinosarcoma                                                |
| UCEC             | Uterine Corpus Endometrial Carcinoma                                  |
| UVM              | Uveal Melanoma                                                        |

</details>

Once the deficiency groups have been created, the tool computes all possible TCGA cohorts. In our case, these would be:

- **dMMR-dP53**: Deficient in MMR, deficient in TP53
- **dMMR-pP53**: Deficient in MMR, proficient in TP53
- **pMMR-dP53**: Proficient in MMR, deficient in TP53
- **pMMR-pP53**: Proficient in MMR, proficient in TP53

> Where **d** indicates 'deficient' and **p** indicates 'proficient'.

The tool indicates the sample number across all cancer types selected, as well as showing interactive pi-echarts of the cancer type distribution. 

![Deficiency groups](https://github.com/user-attachments/assets/0a1130b7-fdcb-47e2-b0a2-894b3fa47186)


### 2. Survival Analysis
Original data-set: [Liu et al. 2018](https://doi.org/10.1016/j.cell.2018.02.052)

The endpoints available for survival analysis are: Overall survival (OS), Disease-specific survival (DDS), Disease-free interval (DFI) and Progression-free interval (PFI). A brief explanation for each endpoint is provided, as well as suggestion for which endpoint to be used based on Liue et al 2018. 
In this tutorial, we are interested in BRCA, OV and UCEC cancers. All endpoints are recommended for OV and UCEC, but OS and DSS have a cautionary note for BRCA samples. For this tutorial, we will plot the DFI, but users can decide on other endspoints that suit their analysis.

The tool plots a Kaplan-Meier probability curve and provides Log-Rank Test Results.

![Survival analysis](https://github.com/user-attachments/assets/614636ab-c76f-48fc-922b-84d777587e44)
![long rank test results](https://github.com/user-attachments/assets/b7f293b6-7a85-4577-a094-ed038e74f4f4)


### 2. DDR footprint
Original data-set: [Knijnenburg et al. 2018](https://doi.org/10.1016/j.celrep.2018.03.076)


This page offers insights into the genomic landscape of the deficiency groups of interest. The users have the option to either display one plot for each feature or all plots simultaneously. Furthermore, there is an added functionality to split the analysis according to cancer types. In case of analysis of multiple groups or cancer types, a scroll bar below the plot is avaiable for improved readability. Furthermore, if the 'Split by cancer type' is ticked, the interactive bar chart allows users to select or deselect cancer types from the legend on the right hand side. 

[DDR footprints.webm](https://github.com/user-attachments/assets/c7ba8969-7074-4769-9b21-c5a909d1609f)


Please visit original paper for further information: [Knijnenburg et al. 2018](https://doi.org/10.1016/j.celrep.2018.03.076)

## FAQ

**Q: How are DDR gene losses defined?**

The DDR gene loss has been obtained from [Knijnenburg et al. 2018](https://doi.org/10.1016/j.celrep.2018.03.076). Please refer to the article for in-depth detail of how the gene losses have been determined.

In short, a gene has been marked as lost if any of the following conditions are met:

1. Deep copy-number genomic deletion
2. Somatic truncating and missense mutations
3. Coupled analysis of methylation and mRNA expression data

