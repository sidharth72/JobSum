import streamlit as st
from generate_df import generate_dataframe
from download_csv import get_table_download_link
from response_generator import chat_with_gemini
from response_generator import generate_description_string, set_initial_message
from visualization import count_occurrences, remove_outliers, generate_visualizations
import matplotlib.pyplot as plt

# st.set_page_config(
#     page_title = 'JobSum'
# )

def extraction_tab():
    st.title("Fetch Job Details.")
    st.write('<div style="opacity: 0.7;">Extract data from various sites by providing necessary details.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.session_state.df = None

    site_name = st.selectbox("Select Site Name", ["Indeed", "Linkedin", "Zip_recruiter", "Glassdoor"])
    location = st.text_input("Location", key="location_input", placeholder='Enter Location to search for')
    search_term = st.text_input("Search Term", key="search_term_input", placeholder='Enter Job Role, Eg: Data Scientist')
    results_wanted = st.number_input("Results Wanted", min_value=1, max_value=500, step=1)
    if site_name == "Indeed":
        country = st.text_input("Country", key="country_input", placeholder='Enter Country')
    else:
        country = st.text_input("Country", key="country_input", placeholder='Enter Country', disabled=True)

    if site_name == 'Linkedin':
        st.warning("Selecting LinkedIn might not provide job descriptions, which could limit the model's ability to generate responses accurately.")
    
    # Check if 'desc_string' is not in session_state, initialize it
    if 'desc_string' not in st.session_state:
        st.session_state.desc_string = ""

    # Button 1: Extract Data
    if st.button("Extract Data"):
        with st.spinner("Extracting information ... Please Wait"):      
            df = generate_dataframe(site_name, search_term, location, results_wanted, country)
            st.session_state.df = df
            try:
                st.session_state.desc_string = generate_description_string(df, 30)
            except:
                st.error("Model Got few information!")

            #st.error("Cannot able to parse the content! Please try other keywords.")

        # with st.spinner("Updating data frame..."):
        #     st.dataframe(df)
        
        with st.spinner("Model Understanding Context ... Please Wait"):
            set_initial_message()

        with st.spinner("Generating download link ..."):
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)

    st.dataframe(st.session_state.df)
    if 'df' in st.session_state:
        st.write("***The Chat Model is all set. Headover to the chat tab to start chatting***")



def api_key_interface():
    st.title("API Key Interface")
    api_key = st.text_input("Enter your API Key:")
    if st.button("Submit API Key"):
        # Process the API key (you can add your logic here)
        st.success("API Key submitted successfully!")


if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{'role':'assistant', 'content':'How may I help you?'}]


def chat_tab():
    st.title("Converse with Model.")

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    if prompt := st.chat_input():
        st.session_state.messages.append({'role':'user', 'content':prompt})
        with st.chat_message('user'):
            st.write(prompt)

    if st.session_state.messages[-1]['role'] != 'assistant':
        with st.chat_message("assistant"):
            with st.spinner("Thinking ... "):
                response = chat_with_gemini(prompt)
                st.write(response)

        message = {'role':'assistant', 'content':response}
        st.session_state.messages.append(message)




def visualization_tab():
    st.title("Data Summary & Insights")
        
    # Button to generate visualizations
    if st.button("Visual Insights", key="generate_button", help="Click to generate visualizations"):
        with st.spinner("Generating Visualizations..."):
            if 'fig' not in st.session_state:
                fig = generate_visualizations()
                st.plotly_chart(fig)
            else:
                st.plotly_chart(st.session_state.fig)


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Tab Example")

    # Create tabs
    tabs = ["Data Extraction", "Model Conversation", "Data Summary & Insights", "Other Tab"]
    current_tab = st.sidebar.selectbox("Select Tab", tabs)
    if current_tab == "Data Extraction":
        extraction_tab()
    elif current_tab == "Model Conversation":
        chat_tab()
    elif current_tab == "Data Summary & Insights":
        visualization_tab()
    elif current_tab == "Other Tab":
        st.title("Content for Other Tab")
        # Add content for other tabs as needed
