import streamlit as st
import pandas as pd
import json
from streamlit_echarts import st_echarts

def ddr_footprints_page():
    def load_group_results(file_path):
        with open(file_path, 'r') as f:
            group_results = json.load(f)
        return group_results

    @st.cache
    def load_data():
        return pd.read_excel("DDR footprint.xlsx", sheet_name=None)

    data_dict = load_data()

    data = data_dict["Sheet1"].copy()  
    descriptions = data_dict["Sheet2"].copy() 
    data.columns = data.columns.str.replace('_', ' ')
    descriptions['DDR Score'] = descriptions['DDR Score'].str.replace('_', ' ')
    
    group_results = load_group_results('group_results.json')

    cancer_types = list(data['Cancer type'].unique())
    color_palette = [
        "#FF6F61", "#FFA177", "#FFD670", "#FF9B85", "#FFADAD",  
        "#B565A7", "#8A2BE2", "#A34DA3", "#DDA0DD", "#F9A602",  
        "#FF8C42", "#FF6700", "#D93B30", "#B22222", "#A52A2A",  
        "#007FFF", "#4F86F7", "#007BA7", "#ADD8E6", "#72A0C1",  
        "#228B22", "#66CDAA", "#ADFF2F", "#BDFCC9", "#7FFF00",  
        "#F5B041", "#F4D03F", "#F39C12", "#F7DC6F", "#FAD02E",  
        "#FF1493", "#FF69B4", "#FF7F50", "#FF4500"
    ]
    color_map = {cancer_types[i]: color_palette[i % len(color_palette)] for i in range(len(cancer_types))}

    selected_groups = st.multiselect("Select Deficiency Groups for Analysis", list(group_results.keys()))
    features = data.columns[3:].tolist()
    selected_features = st.multiselect("Select Features to Plot (Select 'Display All' for all features)", ['Display All'] + features)
    split_by_cancer_type = st.checkbox("Split by Cancer Type", value=False)

    if 'Display All' in selected_features:
        selected_features = features

    def wrap_labels(labels):
        wrapped_labels = []
        for label in labels:
            wrapped_label = []
            start = 0
            for i in range(1, len(label)):
                if label[i] in ['d', 'p']:
                    wrapped_label.append(label[start:i])
                    start = i
            wrapped_label.append(label[start:])
            wrapped_labels.append('\n'.join(wrapped_label))
        return wrapped_labels

    max_chart_width = 700  # This is a safer width to ensure it's within Streamlit's limits
    
    bar_width = max(15, 20 - len(selected_groups) * 0.5)

    if selected_groups and isinstance(selected_features, list) and selected_features:
        for selected_feature in selected_features:
            group_means = []
            cancer_type_means = {}
            valid_groups = []  # Track valid groups
            
            for group in selected_groups:
                group_samples = group_results[group]
                group_filtered_data = data[data['TCGA Sample'].isin(group_samples)]
                group_filtered_data = group_filtered_data.dropna(subset=[selected_feature])
                
                if not group_filtered_data.empty:  # Only consider groups with valid data
                    mean_value = round(group_filtered_data[selected_feature].mean(), 1)
                    group_means.append(mean_value)
                    valid_groups.append(group)  # Add to valid groups
                    
                    if split_by_cancer_type:
                        cancer_type_means[group] = group_filtered_data.groupby('Cancer type')[selected_feature].mean().round(1).dropna()

            wrapped_group_labels = wrap_labels(valid_groups)

            # Display the brief description for the selected feature before rendering the plot
            description = descriptions.loc[descriptions['DDR Score'] == selected_feature, 'Brief Description'].values
            # Custom function to capitalize only the first letter if the entire string is in lowercase
            def smart_capitalize(text):
                if text.islower():
                    return text.capitalize()
                return text
            
            # Apply the smart capitalization to the selected feature
            capitalized_feature = smart_capitalize(selected_feature)
            
            if description:
                st.markdown(f"<h3 style='text-align: center;'>{capitalized_feature}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-style: italic;'>{description[0]}</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal divider line

            if split_by_cancer_type and valid_groups:
                categories = sorted(set([ct for means in cancer_type_means.values() for ct in means.index]))
                series = []
                for idx, cat in enumerate(categories):
                    bar_color = color_map.get(cat, '#FFFFFF')
                    series.append({
                        "name": cat,
                        "type": 'bar',
                        "data": [cancer_type_means[group].get(cat) for group in valid_groups if cat in cancer_type_means[group].index],
                        "itemStyle": {
                            "color": bar_color
                        },
                        "label": {
                            "show": True,
                            "position": 'top',
                            "formatter": "{c}",
                            "fontSize": 12,  
                            "fontWeight": 'bold',
                            "color": bar_color, 
                            "backgroundColor": "rgba(110, 122, 131, 0.3)",  
                            "padding": [3, 5],  
                            "borderRadius": 3, 
                            "distance": 10
                        }

                    })
                
                options = {
                    "tooltip": {
                        "trigger": 'axis',
                        "axisPointer": {"type": 'shadow'}
                    },
                    "legend": {
                        "data": categories,
                        "orient": 'vertical',
                        "right": '5%',
                        "top": 'middle',
                        "type": 'scroll',
                        "textStyle": {"color": "#FFFFFF", "fontSize": 12}
                    },
                    "grid": {
                        "left": '6%',
                        "right": '20%',
                        "bottom": '10%',
                        "containLabel": True
                    },
                    "xAxis": {
                        "type": 'category',
                        "data": wrapped_group_labels,
                        "axisLabel": {
                            "color": "#FFFFFF",
                            "fontSize": 12
                        }
                    },
                    "yAxis": {
                        "type": 'value',
                        "name": f"Mean of {selected_feature}",
                        "nameLocation": 'middle',
                        "nameGap": 50,
                        "nameTextStyle": {
                            "fontSize": 14,
                            "fontWeight": 'bold',
                            "color": "#FFFFFF"
                        },
                        "axisLabel": {"color": "#FFFFFF"}
                    },
                    "dataZoom": [
                        {
                            "type": "slider",
                            "xAxisIndex": 0,
                            "start": 0,
                            "end": 100,  
                            "handleSize": "150%",  
                            "height": 25,  
                            "bottom": '2%',
                            "backgroundColor": "rgba(0, 0, 0, 0)",  
                            "dataBackground": {
                                "lineStyle": {
                                    "color": {
                                        "type": 'linear',
                                        "x": 0,
                                        "y": 0,
                                        "x2": 1,
                                        "y2": 0,
                                        "colorStops": [
                                            {"offset": 0, "color": "#E07B5F"},  # Coral Pink (light)
                                            {"offset": 1, "color": "#C1533E"}   # Dark Coral (dark)
                                        ]
                                    },
                                    "width": 2
                                },
                                "areaStyle": {"color": "rgba(0, 0, 0, 0)"}
                            },
                            "handleStyle": {
                                "color": "#E07B5F",  # Coral Pink
                                "borderColor": "#C1533E",  # Dark Coral
                                "borderWidth": 2,
                                "borderRadius": "50%"
                            },
                            "textStyle": {
                                "color": "#C1533E",  # Dark Coral
                                "fontSize": 9
                            },
                            "fillerColor": "rgba(224, 123, 95, 0.2)", 
                            "borderColor": "#C1533E"  # Dark Coral
                        }
                    ],
                    "series": series
                }
            elif valid_groups:
                options = {
                    "tooltip": {"trigger": 'axis', "axisPointer": {"type": 'shadow'}},
                    "legend": {
                        "data": valid_groups,
                        "orient": 'vertical',
                        "right": '5%',
                        "top": 'middle',
                        "type": 'scroll',
                        "textStyle": {"color": "#FFFFFF", "fontSize": 12}
                    },
                    "grid": {
                        "left": '7%',
                        "right": '5%',
                        "bottom": '10%',
                        "containLabel": True
                    },
                    "xAxis": {
                        "type": 'category',
                        "data": wrapped_group_labels,
                        "axisLabel": {
                            "color": "#FFFFFF",
                            "fontSize": 12
                        },
                        "axisTick": {
                            "alignWithLabel": True
                        },
                        "axisLine": {
                            "onZero": False
                        }
                    },
                    "yAxis": {
                        "type": 'value',
                        "name": f"Mean of {selected_feature}",
                        "nameLocation": 'middle',
                        "nameGap": 50,
                        "nameTextStyle": {
                            "fontSize": 14,
                            "fontWeight": 'bold',
                            "color": "#FFFFFF"
                        },
                        "axisLabel": {"color": "#FFFFFF"}
                    },
                    "dataZoom": [
                        {
                            "type": "slider",
                            "xAxisIndex": 0,
                            "start": 0,
                            "end": 100,  
                            "handleSize": "150%",  
                            "height": 25,  
                            "bottom": '2%',
                            "backgroundColor": "rgba(0, 0, 0, 0)",  
                            "dataBackground": {
                                "lineStyle": {
                                    "color": {
                                        "type": 'linear',
                                        "x": 0,
                                        "y": 0,
                                        "x2": 1,
                                        "y2": 0,
                                        "colorStops": [
                                            {"offset": 0, "color": "#E07B5F"},  # Coral Pink (light)
                                            {"offset": 1, "color": "#C1533E"}   # Dark Coral (dark)
                                        ]
                                    },
                                    "width": 2
                                },
                                "areaStyle": {"color": "rgba(0, 0, 0, 0)"}
                            },
                            "handleStyle": {
                                "color": "#E07B5F",  # Coral Pink
                                "borderColor": "#C1533E",  # Dark Coral
                                "borderWidth": 2,
                                "borderRadius": "50%"
                            },
                            "textStyle": {
                                "color": "#C1533E",  # Dark Coral
                                "fontSize": 9
                            },
                            "fillerColor": "rgba(224, 123, 95, 0.2)",  # Coral Pink with transparency
                            "borderColor": "#C1533E"  # Dark Coral
                        }
                    ],
            
                    "series": [{
                        "name": "Mean Value",
                        "type": 'bar',
                        "data": group_means,
                        "itemStyle": {
                            "color": {
                                "type": 'linear',
                                "x": 0,
                                "y": 0,
                                "x2": 0,
                                "y2": 1,  # Vertical gradient (top to bottom)
                                "colorStops": [
                                    {"offset": 0, "color": '#E07B5F'},  # Coral Pink
                                    {"offset": 1, "color": '#C1533E'}   # Dark Coral
                                ]
                            }
                        },
                        "barWidth": bar_width,
                        "label": {
                            "show": True,
                            "position": 'top',
                            "formatter": "{c}",
                            "fontSize": 15,
                            "fontWeight": 'bold',
                            "color": '#E07B5F',
                            "backgroundColor": "rgba(110, 122, 131, 0.5)", 
                            "padding": [3, 5],  
                            "borderRadius": 3,  
                            "distance": 10
                        }
                    }]
                }
            st_echarts(options=options, height="600px", width=f"{max_chart_width}px")

if __name__ == "__main__":
    ddr_footprints_page()
