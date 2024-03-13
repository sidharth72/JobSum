import streamlit as st
import numpy as np
from response_generator import get_json, preprocess_json_string
import plotly.graph_objs as go

def count_occurrences(data_dict):
    occurrences = {}
    for keys, values in data_dict.items():
        count_dict = {}
        for value in values:
            count_dict[value] = st.session_state.desc_string.lower().count(value.lower())
        occurrences[keys] = count_dict
    print(occurrences)
    return occurrences

def remove_outliers(data_dict, multiplier=2.5):
    cleaned_data = {}
    removed_keys = {}

    for category, counts in data_dict.items():
        if len(counts.values()) == 0:
            continue
        values = list(counts.values())

        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)

        iqr = q3 - q1
        threshold = multiplier * iqr

        cleaned_data[category] = {key: count for key, count in counts.items() if q1 - threshold <= count <= q3 + threshold}
        removed_keys[category] = [key for key, count in counts.items() if count < q1 - threshold or count > q3 + threshold]

    return cleaned_data, removed_keys

def generate_visualizations():
    if 'json_model_response' not in st.session_state:
        json_model_response = get_json()
        st.session_state.json_model_response = json_model_response

    if 'fig' not in st.session_state:
        json_model_response = st.session_state.json_model_response
        json_cleaned = preprocess_json_string(json_model_response)
        occurrence = count_occurrences(json_cleaned)
        cleaned_data, removed_keys = remove_outliers(occurrence)
        
        # Plot each category horizontally with Plotly
        categories = list(cleaned_data.keys())

        # Create a figure with subplots for each category
        fig = go.Figure()
        for i, category in enumerate(categories):
            values = list(cleaned_data[category].values())
            labels = list(cleaned_data[category].keys())

            # Add horizontal bar plot trace
            fig.add_trace(go.Bar(
                y=labels,
                x=values,
                orientation='h',
                name=category
            ))

        # Update layout
        fig.update_layout(
            title="Data Summary & Insights",
            yaxis=dict(title="Values"),
            xaxis=dict(title="Counts")
        )

        st.session_state.fig = fig
    else:
        fig = st.session_state.fig

    return fig