import streamlit as st
import pandas as pd
import itertools
import json
from streamlit_echarts import st_echarts

def create_groups_page():
    # Initialize session state for group results
    if 'group_results' not in st.session_state:
        st.session_state.group_results = {}
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False

    # Load the data
    @st.cache
    def load_data(file_path):
        data = pd.read_excel(file_path)
        return data

    data = load_data('DDR factors gene loss.xlsx')

    # Get available genes and cancer types
    genes = data.columns[2:]
    cancer_types = list(data['Cancer type'].unique())
    cancer_types_with_all_none = ["Select All"] + cancer_types

    # Define the color palette and map to cancer types
    color_palette = [
    "#FF6F61", "#FFA177", "#FFD670", "#FF9B85", "#FFADAD",  # Warm pinks, corals, and peaches
    "#6A0572", "#8A2BE2", "#9C51B6", "#DA70D6", "#F9A602",  # Purples and oranges
    "#FF8C42", "#FF6700", "#D93B30", "#B22222", "#A52A2A",  # Bold reds and oranges
    "#007FFF", "#4F86F7", "#007BA7", "#ADD8E6", "#72A0C1",  # Vibrant blues
    "#228B22", "#66CDAA", "#ADFF2F", "#BDFCC9", "#7FFF00",  # Greens and limes
    "#F5B041", "#F4D03F", "#F39C12", "#F7DC6F", "#FAD02E",  # Bright yellows and golds
    "#FF1493", "#FF69B4", "#FF7F50", "#FF4500"              # Pinks and oranges
]
    color_map = {cancer_types[i]: color_palette[i] for i in range(len(cancer_types))}

    st.sidebar.header('User Input')
    num_groups = st.sidebar.number_input(
        'Number of Deficiencies', min_value=1, max_value=10, step=1, value=2, key='num_deficiencies'
    )

    # Initialize group selection
    deficiencies = []
    for i in range(num_groups):
        deficiency = {}
        st.sidebar.subheader(f'Deficiency {i+1}')
        deficiency['name'] = st.sidebar.text_input(f'Deficiency {i+1} Name', f'Deficiency {i+1}', key=f'deficiency_name_{i}')
        deficiency['genes'] = st.sidebar.multiselect(f'Select Genes for {deficiency["name"]}', genes, key=f'deficiency_genes_{i}')
        deficiency['mutation_type'] = st.sidebar.radio(
            f'Mutation type for {deficiency["name"]}',
            ('Any of the selected genes', 'All of the selected genes'), key=f'mutation_type_{i}'
        )
        deficiencies.append(deficiency)

    # Sidebar for cancer type selection
    selected_cancer_types = st.sidebar.multiselect('Select Cancer Types', cancer_types_with_all_none, default=cancer_types_with_all_none, key='selected_cancer_types')

    if "Select All" in selected_cancer_types:
        selected_cancer_types = cancer_types

    filtered_data = data[data['Cancer type'].isin(selected_cancer_types)]

    # Drop rows with NaN values in the selected genes for each deficiency
    for deficiency in deficiencies:
        selected_genes = deficiency['genes']
        if selected_genes:
            filtered_data = filtered_data.dropna(subset=selected_genes)

    # Submit button for user to finalize selections
    if st.sidebar.button("Submit", key='submit_button'):
        # Analyze the data based on user input
        results = {}
        for deficiency in deficiencies:
            deficiency_name = deficiency['name']
            selected_genes = deficiency['genes']
            mutation_type = deficiency['mutation_type']
            if selected_genes:
                if mutation_type == 'Any of the selected genes':
                    results[deficiency_name] = {
                        'deficient': set(filtered_data[filtered_data[selected_genes].any(axis=1)]['TCGA Sample']),
                        'proficient': set(filtered_data[~filtered_data[selected_genes].any(axis=1)]['TCGA Sample'])
                    }
                else:  # All of the selected genes
                    results[deficiency_name] = {
                        'deficient': set(filtered_data[filtered_data[selected_genes].all(axis=1)]['TCGA Sample']),
                        'proficient': set(filtered_data[~filtered_data[selected_genes].all(axis=1)]['TCGA Sample'])
                    }
            else:
                results[deficiency_name] = {'deficient': set(), 'proficient': set()}

        # Generate all possible combinations of deficiencies and proficiencies
        combinations = list(itertools.product(['d', 'p'], repeat=num_groups))

        # Calculate the groups based on these combinations
        group_results = {}
        all_samples = set(filtered_data['TCGA Sample'])

        for comb in combinations:
            group_name_parts = []
            group_samples = all_samples.copy()
            for i, status in enumerate(comb):
                if status == 'd':
                    group_name_parts.append(f'd{deficiencies[i]["name"]}')
                    group_samples &= results[deficiencies[i]['name']]['deficient']
                else:
                    group_name_parts.append(f'p{deficiencies[i]["name"]}')
                    group_samples &= results[deficiencies[i]['name']]['proficient']
            group_name = '-'.join(group_name_parts)
            group_results[group_name] = group_samples

        # Save the group results to session state
        st.session_state.group_results = group_results
        st.session_state.initialized = True

        # Display the results as a table
        st.header('Deficiency Groups Summary')
        summary_table = []

        for group_name, samples in group_results.items():
            summary_table.append({
                'Deficiency Group': group_name,
                'Sample Number': len(samples)
            })

        summary_df = pd.DataFrame(summary_table)
        st.table(summary_df)

        # Display the pie charts in a 2-per-row grid
        st.header('Cancer Type Distribution by Group')
        
        # Determine the number of columns for the grid (2 columns instead of 4)
        cols = st.columns(2)
        
        for idx, row in summary_df.iterrows():
            group_name = row['Deficiency Group']
            group_samples = group_results[group_name]
        
            group_data = filtered_data[filtered_data['TCGA Sample'].isin(group_samples)]
            cancer_type_counts = group_data['Cancer type'].value_counts()
        
            # Define options for ECharts
            options = {
                "backgroundColor": "rgba(51, 51, 51, 0.8)", 
                "title": {
                    "text": group_name,
                    "left": "center",
                    "top": 14,
                    "textStyle": {
                        "color": "#FFFFFF",  
                        "fontSize": 14,
                    }
                },
                "tooltip": {
                    "trigger": "item",
                    "formatter": "{b}: {c} ({d}%)"  
                },
                "series": [
                    {
                        "name": "Cancer Type",
                        "type": "pie",
                        "radius": ["20%", "50%"], 
                        "avoidLabelOverlap": False,
                        "label": {
                            "show": True, 
                            "position": "outside"
                        },
                        "labelLine": {
                            "show": True
                        },
                        "data": [
                            {
                                "value": count,
                                "name": name,
                                "itemStyle": {"color": color_map[name]}
                            }
                            for name, count in cancer_type_counts.items()
                        ]
                    }
                ]
            }

        
            # Display in grid
            with cols[idx % 2]:  # Adjust for 2 columns per row
                st_echarts(options=options, height="400px")
            
            # Toggleable Cancer Type Legend
        with st.expander("Cancer Type Legend"):
            st.header("Cancer Type Legend")

            # Create a DataFrame for the legend
            legend_data = {
                "Abbreviation": cancer_types,
                "Cancer type": [
                    "Adrenocortical carcinoma", "Bladder Urothelial Carcinoma", "Breast invasive carcinoma", 
                    "Cervical squamous cell carcinoma and endocervical adenocarcinoma", "Cholangiocarcinoma", 
                    "Colon adenocarcinoma", "Lymphoid Neoplasm Diffuse Large B-cell Lymphoma", "Esophageal carcinoma", 
                    "Glioblastoma multiforme", "Brain Lower Grade Glioma", "Head and Neck squamous cell carcinoma", 
                    "Kidney Chromophobe", "Kidney renal clear cell carcinoma", "Kidney renal papillary cell carcinoma", 
                    "Acute Myeloid Leukemia", "Liver hepatocellular carcinoma", "Lung adenocarcinoma", 
                    "Lung squamous cell carcinoma", "Mesothelioma", "Ovarian serous cystadenocarcinoma", 
                    "Pancreatic adenocarcinoma", "Pheochromocytoma and Paraganglioma", "Prostate adenocarcinoma", 
                    "Rectum adenocarcinoma", "Sarcoma", "Skin Cutaneous Melanoma", "Stomach adenocarcinoma", 
                    "Thyroid carcinoma", "Thymoma", "Testicular Germ Cell Tumors", "Uterine Corpus Endometrial Carcinoma", 
                    "Uterine Carcinosarcoma", "Uveal Melanoma"
                ],
                "Color": [color_map[ct] for ct in cancer_types]
            }

            legend_df = pd.DataFrame(legend_data)
    
            # Function to format the color cells
            def color_format(color):
                return f"<div style='background-color:{color}; width:20px; height:20px;'></div>"
    
            # Apply the color formatting
            legend_df['Color'] = legend_df['Color'].apply(color_format)
    
            # Convert the DataFrame to an HTML table with colored cells
            table_html = legend_df.to_html(escape=False, index=False)
    
            # Display the table in Streamlit
            st.markdown(table_html, unsafe_allow_html=True)

        # Save the group results to a file
        with open('group_results.json', 'w') as f:
            json.dump({k: list(v) for k, v in group_results.items()}, f)


if __name__ == "__main__":
    create_groups_page()