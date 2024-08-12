# TCGA-DDR: A Web Tool for Genomic and Survival Analysis in the TCGA Cohort

**TCGA-DDR** is a web tool that allows users to define from 1 to 10 DNA-damage deficient TCGA groups and compute:

1. Population statistics across cancer types
2. Survival statistics
3. Genomic landscape

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

- **MMR Group**: [List the genes here]
- **P53 Group**: [List the genes here]

#### C. Choose Which Cancer Types to be Analyzed

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

Once the deficiency groups have been created, the tool computes all possible TCGA cohorts. In our case, these would be:

- **dMMR-dP53**: Deficient in MMR, deficient in TP53
- **dMMR-pP53**: Deficient in MMR, proficient in TP53
- **pMMR-dP53**: Proficient in MMR, deficient in TP53
- **pMMR-pP53**: Proficient in MMR, proficient in TP53

> Where **d** indicates 'deficient' and **p** indicates 'proficient'.

Population statistics for these groups are shown as interactive pie-charts.

### 2. Survival Analysis

_TBC_

## FAQ

**Q: How are DDR gene losses defined?**

The DDR gene loss has been obtained from [reference the article here]. Please refer to the article for in-depth detail of how the gene losses have been determined.

In short, a gene has been marked as lost if any of the following conditions are met:

1. Deep copy-number genomic deletion
2. Somatic truncating and missense mutations
3. Coupled analysis of methylation and mRNA expression data
