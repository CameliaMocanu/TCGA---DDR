import streamlit as st
import pandas as pd
import json
import itertools
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt
import textwrap


def survival_simplified_page():
    st.title("Survival analysis")
    
    @st.cache
    def load_data(file_path):
        return pd.read_excel(file_path)
    
    # Load the survival data
    survival_data = load_data('Survival_simple.xlsx')


    # Load group results from session state or file
    if 'group_results' in st.session_state:
        group_results = st.session_state.group_results
    else:
        with open('group_results.json', 'r') as f:
            group_results = json.load(f)
            st.session_state.group_results = group_results  # Save to session state

    # User selection for endpoint
    st.subheader('Survival Endpoint to Plot')
    endpoint_choice = st.radio('Select one option:', ['OS', 'DSS', 'DFI', 'PFI'])

    # Explanation for each endpoint
    if endpoint_choice == 'OS':
        st.markdown("**OS** (Overall Survival) is the period from the date of diagnosis until the date of death from any cause, including non-cancer-related deaths.")
        endpoint = 'OS'
        time_column = 'OS.time'
    elif endpoint_choice == 'DSS':
        st.markdown("**DSS** (Disease-Specific Survival) is calculated as the period between the date of initial diagnosis until the date of death specifically from the disease.")
        endpoint = 'DSS'
        time_column = 'DSS.time'
    elif endpoint_choice == 'DFI':
        st.markdown("**DFI** (Disease-Free Interval) is the period from the date of diagnosis until the first new tumor progression event after the patient has been declared disease-free post-treatment.")
        endpoint = 'DFI'
        time_column = 'DFI.time'
    else:
        st.markdown("**PFI** (Progression-Free Interval) is the period from the date of diagnosis until the first occurrence of a new tumor event, which includes disease progression, locoregional recurrence, distant metastasis, new primary tumor, or death with a tumor.")
        endpoint = 'PFI'
        time_column = 'PFI.time'
    # Explanation table data
    explanation_data = {
        "Cancer type": ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC", "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PCPG", "PRAD", "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM"],
        "OS": ["✓", "✓", "✓*", "✓", "✓", "✓", "×", "✓", "✓", "✓", "✓*", "✓", "✓", "✓", "✓*", "✓", "✓", "✓", "✓", "✓", "✓", "×", "✓*", "✓*", "✓", "✓", "✓", "×", "✓*", "×", "✓", "✓", "✓"],
        "PFI": ["✓", "✓", "✓", "✓", "✓", "✓", "✓*", "✓", "✓", "✓", "✓*", "✓", "✓", "x", "✓", "✓", "✓", "✓", "✓", "✓", "✓", "×", "✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓", "✓"],
        "DFI": ["✓*", "✓", "✓", "✓", "✓*", "✓", "×", "✓", "×", "✓", "×", "✓*", "✓", "×", "✓", "✓", "✓", "✓", "×", "✓", "✓", "×", "✓", "×", "✓", "×", "✓", "×", "✓", "×", "✓", "✓*", "×"],
        "DSS": ["✓", "✓", "✓*", "✓", "✓*", "✓", "×", "✓", "✓", "✓", "✓*", "✓", "✓", "×", "✓*", "✓*", "✓", "✓", "✓", "✓", "✓", "×", "×", "✓*", "✓", "✓", "×", "×", "×", "×", "✓", "✓", "✓"],
        "Caution": [
            "Number of events is small",
            " ",
            "Need a longer follow-up for OS and DSS",
            " ",
            "Sample size is too small for OS, DSS, DFI, and PFI",
            " ",
            "Sample size and number of events are too small, need a longer follow-up",
            " ",
            "Number of disease-free cases is small", 
            " ",
            "Number of events is too small, need a longer follow-up", 
            "Number of events is small", 
            " ",
            "Only has OS data", 
            "Need a longer follow-up for OS and DSS", 
            "Need a longer follow-up for DSS", 
            " ", 
            " ", 
            "Sample size for DFI is small", 
            " ", 
            " ", 
            "Need a longer follow-up for OS, DSS, DFI, and PFI; number of events is small", 
            "Need a longer follow-up for OS and DSS", 
            "Need a longer follow-up for OS, DSS, and DFI; number of events for DFI is too small", 
            " ",
            "No information to derive DFI", 
            " ",
            "Number of events is too small for OS and DSS; need a longer follow-up",
            "Number of events is too small for OS and DSS; need a longer follow-up", 
            "Number of events is too small for OS and DSS; need a longer follow-up; no information to derive DFI", 
            " ",
            "Sample size is small", 
            "No information to derive DFI"
        ]
    }
    explanation_df = pd.DataFrame(explanation_data)
    explanation_df['Caution'] = explanation_df['Caution'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=40)))

    # Toggleable table
    if st.checkbox('Show suggestions'):
        st.subheader('Suggested endpoint per cancer type')
        st.table(explanation_df)

    # Group selection
    selected_groups = st.multiselect('Select Groups', list(group_results.keys()))

    # Option to toggle legend visibility
    show_legend = st.checkbox('Show Legend', value=True)

    if selected_groups:
        # Filter for the required groups
        filtered_survival_data = pd.concat([survival_data[survival_data['TCGA Sample'].isin(group_results[group])] for group in selected_groups])
        filtered_survival_data = filtered_survival_data.dropna(subset=[time_column, endpoint])

        # Create a dictionary to hold the filtered dataframes
        grouped_data = {group: filtered_survival_data[filtered_survival_data['TCGA Sample'].isin(group_results[group])] for group in selected_groups}

        # Perform log-rank tests
        def perform_logrank_test(grouped_data, groups):
            results = {}
            for group1, group2 in itertools.combinations(groups, 2):
                data1 = grouped_data[group1]
                data2 = grouped_data[group2]

                if not data1.empty and not data2.empty:
                    result = logrank_test(
                        data1[time_column], data2[time_column],
                        event_observed_A=data1[endpoint], event_observed_B=data2[endpoint]
                    )
                    results[(group1, group2)] = result
            return results

        # Plotting functions
        def plot_km_curves(grouped_data, groups, logrank_results, show_legend):
            plt.figure(figsize=(10, 9), dpi=600)
        
            for group in groups:
                data = grouped_data[group]
                if not data.empty:
                    kmf = KaplanMeierFitter()
                    kmf.fit(durations=data[time_column], event_observed=data[endpoint], label=group)
                    kmf.plot_survival_function(ci_show=True)
        
            plt.xlabel('Days', fontsize=20)
            plt.ylabel('Probability', fontsize=20)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            
            if show_legend:
                plt.legend(loc='upper right', fontsize=14)
            else:
                plt.gca().legend().remove()  # Remove legend if the checkbox is unchecked
            
            st.pyplot(plt)
        
            # Display p-values and sample sizes in a table
            p_values = []
            for (group1, group2), result in logrank_results.items():
                n1 = len(grouped_data[group1])
                n2 = len(grouped_data[group2])
                p_values.append([group1, group2, f'{result.p_value:.4f}', f'{n1}', f'{n2}'])
        
            st.subheader('Log-Rank Test Results')
            st.write(pd.DataFrame(p_values, columns=['Group 1', 'Group 2', 'p-value', 'n1', 'n2']))


        logrank_results = perform_logrank_test(grouped_data, selected_groups)
        plot_km_curves(grouped_data, selected_groups, logrank_results, show_legend)

if __name__ == "__main__":
    survival_simplified_page()
