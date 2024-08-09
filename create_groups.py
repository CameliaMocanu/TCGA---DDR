import streamlit as st
import pandas as pd
import itertools
import json

def create_groups_page():
    st.title("Create Groups")

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

    data = load_data('DDR factors gene loss.xlsx')  # Update this with the correct path

    # Get available genes and cancer types
    genes = data.columns[2:]
    cancer_types = list(data['Cancer type'].unique())
    cancer_types_with_all_none = ["Select All", "Select None"] + cancer_types

    st.sidebar.header('User Input')
    num_groups = st.sidebar.number_input('Number of Deficiencies', min_value=2, max_value=10, step=1, value=2)

    # Initialize group selection
    deficiencies = []
    for i in range(num_groups):
        deficiency = {}
        st.sidebar.subheader(f'Deficiency {i+1}')
        deficiency['name'] = st.sidebar.text_input(f'Deficiency {i+1} Name', f'Deficiency {i+1}')
        deficiency['genes'] = st.sidebar.multiselect(f'Select Genes for {deficiency["name"]}', genes)
        deficiency['mutation_type'] = st.sidebar.radio(
            f'Mutation type for {deficiency["name"]}',
            ('Any of the selected genes', 'All of the selected genes')
        )
        deficiencies.append(deficiency)

    # Sidebar for cancer type selection
    selected_cancer_types = st.sidebar.multiselect('Select Cancer Types', cancer_types_with_all_none, default=cancer_types_with_all_none)

    if "Select All" in selected_cancer_types:
        selected_cancer_types = cancer_types
    elif "Select None" in selected_cancer_types:
        selected_cancer_types = []

    filtered_data = data[data['Cancer type'].isin(selected_cancer_types)]

    # Drop rows with NaN values in the selected genes for each deficiency
    for deficiency in deficiencies:
        selected_genes = deficiency['genes']
        if selected_genes:
            filtered_data = filtered_data.dropna(subset=selected_genes)

    # Display the data
    st.header('TCGA Data Analysis')
    st.write(f'The data for Cancer Types: {", ".join(selected_cancer_types)}')
    st.write(filtered_data.head())

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

    # Display the results
    st.header('Analysis Results')
    for group_name, samples in group_results.items():
        st.subheader(group_name)
        st.write(f'Samples: {len(samples)}')
        st.write(list(samples))

    # Save the group results to a file
    with open('group_results.json', 'w') as f:
        json.dump({k: list(v) for k, v in group_results.items()}, f)
