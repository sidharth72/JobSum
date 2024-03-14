import streamlit as st
import numpy as np
from response_generator import get_json, preprocess_json_string
import plotly.graph_objs as go
from response_generator import generate_description_string

def count_occurrences(data_dict):
    occurrences = {}
    for keys, values in data_dict.items():
        count_dict = {}
        for value in values:
            count_dict[value] = generate_description_string(st.session_state.df, 30, full = True).lower().count(value.lower())
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

def generate_bar_plots():
    if 'json_model_response' not in st.session_state:
        json_model_response = get_json()
        st.session_state.json_model_response = json_model_response

    if 'barplot' not in st.session_state:
        json_model_response = st.session_state.json_model_response
        json_cleaned = preprocess_json_string(json_model_response)
        occurrence = count_occurrences(json_cleaned)
        cleaned_data, removed_keys = remove_outliers(occurrence)
        
        # Plot each category horizontally with Plotly
        categories = list(cleaned_data.keys())

        # Create a figure with subplots for each category
        bar = go.Figure()
        for i, category in enumerate(categories):
            values = list(cleaned_data[category].values())
            labels = list(cleaned_data[category].keys())

            # Add horizontal bar plot trace
            bar.add_trace(go.Bar(
                y=labels,
                x=values,
                orientation='h',
                name=category
            ))

        # Update layout
        bar.update_layout(
            title="Data Summary & Insights",
            yaxis=dict(title="Values"),
            xaxis=dict(title="Counts")
        )

        st.session_state.barplot = bar
    else:
        bar = st.session_state.barplot

    return bar


def generate_pie_plots():
    if 'json_model_response' not in st.session_state:
        json_model_response = get_json()
        st.session_state.json_model_response = json_model_response

    if 'pieplot' not in st.session_state:
        json_model_response = st.session_state.json_model_response
        json_cleaned = preprocess_json_string(json_model_response)
        occurrence = count_occurrences(json_cleaned)
        cleaned_data, removed_keys = remove_outliers(occurrence)
        
        # Plot each category horizontally with Plotly
        categories = list(cleaned_data.keys())

        # Create a figure with subplots for each category
        pie = go.Figure()
        for i, category in enumerate(categories):
            values = list(cleaned_data[category].values())
            labels = list(cleaned_data[category].keys())

            # Add pie chart trace
            pie.add_trace(go.Pie(
                labels=labels,  # Use the same labels as the last category for the pie chart
                values=values,  # Use the same values as the last category for the pie chart
                name="Pie Chart"
            ))

        # Update layout
        pie.update_layout(
            title="Data Summary & Insights",
            yaxis=dict(title="Values"),
            xaxis=dict(title="Counts")
        )

        st.session_state.pieplot = pie
    else:
        pie = st.session_state.pieplot

    return pie
