import streamlit as st
import pandas as pd
import json
import itertools
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt


def survival_simplified_page():
    st.title("Simplified Survival Analysis")
    
    @st.cache
    def load_data(file_path):
        return pd.read_excel(file_path)
    
    # Load the survival data
    survival_data = load_data('/Users/cmocanu/Desktop/OMICS ANALYSIS/TCGA PanCanAtlas resources DDR/Web app/Survival_simple.xlsx')  # Update this with the correct path

    st.header('Survival Data Analysis')

    # Load and display survival data
    st.subheader('Survival Data')
    st.write(survival_data.head())

    # Load group results from session state or file
    if 'group_results' in st.session_state:
        group_results = st.session_state.group_results
    else:
        with open('group_results.json', 'r') as f:
            group_results = json.load(f)
            st.session_state.group_results = group_results  # Save to session state

    # User selection for endpoint
    st.subheader('Select Endpoint to Plot')
    endpoint_choice = st.radio('Select Endpoint', ['OS', 'DSS', 'DFI', 'PFI'])

    # Determine the endpoint and time columns based on user selection
    if endpoint_choice == 'OS':
        endpoint = 'OS'
        time_column = 'OS.time'
    elif endpoint_choice == 'DSS':
        endpoint = 'DSS'
        time_column = 'DSS.time'
    elif endpoint_choice == 'DFI':
        endpoint = 'DFI'
        time_column = 'DFI.time'
    else:
        endpoint = 'PFI'
        time_column = 'PFI.time'

    # Group selection
    selected_groups = st.multiselect('Select Groups', list(group_results.keys()))

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
        def plot_km_curves(grouped_data, groups, logrank_results):
            plt.figure(figsize=(10, 9), dpi=600)

            for group in groups:
                data = grouped_data[group]
                if not data.empty:
                    kmf = KaplanMeierFitter()
                    kmf.fit(durations=data[time_column], event_observed=data[endpoint], label=group)
                    kmf.plot_survival_function(ci_show=True)

            plt.xlabel('Days', fontsize=20)
            plt.ylabel(endpoint, fontsize=20)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            plt.legend(loc='lower right', fontsize=18)
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
        plot_km_curves(grouped_data, selected_groups, logrank_results)

if __name__ == "__main__":
    survival_simplified_page()
