import streamlit as st
from generate_df import generate_dataframe
from download_csv import get_table_download_link

headers = {
    'authorization': st.secrets['auth_token']
}


def extraction_tab():
    st.title("Data Extraction")
    site_name = st.selectbox("Select Site Name", ["Indeed", "Linkedin", "Zip_recruiter", "Glassdoor"])
    location = st.text_input("Location", key="location_input", placeholder='Enter Location to search for')
    search_term = st.text_input("Search Term", key="search_term_input", placeholder='Enter Job Role, Eg: Data Scientist')
    results_wanted = st.number_input("Results Wanted", min_value=1, step=1)
    if site_name == "Indeed":
        country = st.text_input("Country", key="country_input", placeholder='Enter Country')
    else:
        country = st.text_input("Country", key="country_input", placeholder='Enter Country', disabled=True)
    if st.button("Extract Data"):
        df = generate_dataframe(site_name, search_term, location, results_wanted, country)
        st.dataframe(df)
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)


def api_key_interface():
    st.title("API Key Interface")
    api_key = st.text_input("Enter your API Key:")
    if st.button("Submit API Key"):
        # Process the API key (you can add your logic here)
        st.success("API Key submitted successfully!")


def chat_tab():
    st.title("Chat Interface")

    if st.session_state.api_key is None:
        api_key_interface()
    else:

        if 'messages' not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

        if prompt := st.chat_input("What is up?"):
            st.chat_message('user').markdown(prompt)
            st.session_state.messages.append({'role':'user', 'content':prompt})
            response = f"Echo: {prompt}"

            with st.chat_message('Assistant'):
                st.markdown(response)

            st.session_state.messages.append({'role':'assistant', 'content':response})

def visualization_tab():
    st.title("Data Visualization")
    chart_data = {'x': [1, 2, 3, 4, 5], 'y': [10, 20, 30, 40, 50]}
    st.line_chart(chart_data)

if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Tab Example")

    # Create tabs
    tabs = ["Extraction", "Chat", "Visualization", "Other Tab"]
    current_tab = st.sidebar.selectbox("Select Tab", tabs)
    if current_tab == "Extraction":
        extraction_tab()
    elif current_tab == "Chat":
        chat_tab()
    elif current_tab == "Visualization":
        visualization_tab()
    elif current_tab == "Other Tab":
        st.title("Content for Other Tab")
        # Add content for other tabs as needed
