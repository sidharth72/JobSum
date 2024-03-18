import streamlit as st
from generate_df import generate_dataframe
from download_csv import get_table_download_link
from response_generator import chat_with_gemini
from response_generator import generate_description_string, set_initial_message
from visualization import generate_bar_plots, generate_pie_plots


def home_tab():
    """ Home Tab"""
    # Title
    st.title("""Welcome to JobSum!""")
    # Description
    st.write("""
### **Introduction**

**JobSum** is a job summarization and chatting app build using streamlit designed to make your job search process easier and more efficient. By utilizing data scraped from popular websites like Indeed, LinkedIn, Glassdoor, ZipRecruiter, and more, this tool provides a personalized and comprehensive job summary for each search query. Let's dive into how this tool works and the features it offers.

### How it Works

The JobSum tool leverages an advanced LLM model (Gemini-Google) to analyze and understand hundreds of job descriptions in a matter of seconds. The AI can extract essential information such as required skills, experience levels, interview insights, and can give tutorials and guides to refer for the job. This process saves you valuable time that would otherwise be spent manually reading through numerous job postings.

### Features

* **Job Summarization:** The AI tool generates a concise summary of each job description, highlighting key details to help you understand the job requirements at a glance.
* **Skill Matching:** It identifies the most relevant skills needed for a particular job, making it easier for you to tailor your resume and cover letter accordingly.
* **Interview Insights:** Based on the job descriptions, you can ask the AI to provide interview questions and tips based on the job description.
* **Chat Functionality:** You can interact with the AI to ask questions about specific job preferences or seek advice on career-related topics.
* **Visualizations:** obSum provides graphical representations of the data generated, offering a visual understanding of important factors to consider when applying for a job. You can explore different terms, positions within the same job category, and other valuable insights through these visualizations.

## Links:
https://github.com/sidharth72/JobSum
             
https://www.linkedin.com/in/sidharth-gn-4ab311208/        
""")


    # Welcome contribution message
    st.write("### Welcome Contributions!")
    st.write("We welcome contributions from the community to improve JobSum. Whether it's adding new features, fixing bugs, or enhancing documentation, every contribution matters!")



def extraction_tab():
    """Data Extraction Tab"""

    st.title("Fetch Job Details.")
    st.write(
        '<div style="opacity: 0.7;">Extract data from various sites by providing necessary details.</div>',
            unsafe_allow_html=True
        )
    st.markdown("<br>", unsafe_allow_html=True)

    if 'df' not in st.session_state:
        st.session_state.df = None

    col1, col2 = st.columns(2)

    with col1:
        site_name = st.selectbox("Select Site Name", ["Indeed", "Linkedin", "Zip_recruiter", "Glassdoor"])
    with col2:
        location = st.text_input("Location", key="location_input", placeholder='Enter Location to search for')
    search_term = st.text_input("Search Term", key="search_term_input", placeholder='Enter Job Role, Eg: Data Scientist')
    col3, col4 = st.columns(2)
    with col3:
        results_wanted = st.number_input("Results Wanted", min_value=1, max_value=500, step=1)
    with col4:
        if site_name == "Indeed":
            country = st.text_input("Country", key="country_input", placeholder='Enter Country')
        else:
            country = st.text_input("Country", key="country_input", placeholder='Enter Country', disabled=True)

    if site_name == 'Linkedin':
        st.warning(
            "Selecting LinkedIn might not provide job descriptions, which could limit the model's ability to generate responses accurately."
            )
    
    # Check if 'desc_string' is not in session_state, initialize it
    if 'desc_string' not in st.session_state:
        st.session_state.desc_string = ""

    # Button 1: Extract Data
    if st.button("Extract Data"):
        
        # Setting plots to None when use extracts new data
        st.session_state.barplot = None
        st.session_state.pieplot = None

        with st.spinner("Extracting information ... Please Wait"):  
            try:
                # Generate the dataframe from details
                df = generate_dataframe(site_name, search_term, location, results_wanted, country)
                st.session_state.df = df  # Add to the session_state

                # Description String combines all the description generated for the model to summarize   
                st.session_state.desc_string = generate_description_string(df, 30, False)
            except Exception as e:
                st.error(f"Sorry, there is a problem: {e}")
        
        # Passing the initial System Message
        with st.spinner("AI Understanding Context ... Please Wait"):
            set_initial_message()

        with st.spinner("Generating download link ..."):
            try:
                st.markdown(get_table_download_link(df), unsafe_allow_html=True)
            except:
                pass

    st.dataframe(st.session_state.df)

if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{'role':'assistant', 'content':'How may I help you?'}]

def chat_tab():
    """Chat Interface"""
    st.title("Converse with AI.")

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    if prompt := st.chat_input("Eg: What are the key insights can you provide from the job descriptions?"):
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
    """Visualization Interface"""
    st.title("Data Summary & Insights.")

    tab1, tab2 = st.tabs(['Bar Plots', 'Pie Charts'])

    with tab1:      
        if st.button("Show Bar Plot", key="generate_barplot", help="Click to generate bar plots"):
            if st.session_state.df is None:
                st.warning("Dataset not available!")
            else:
                with st.spinner("Generating Barplot ... Please wait"):
                    if st.session_state.barplot is None:
                        try:
                            st.session_state.barplot = generate_bar_plots()
                            st.plotly_chart(st.session_state.barplot)
                        except:
                            st.error(f"Sorry, the model not able to generate visuals. Please try extracting again")
                    else:
                        st.plotly_chart(st.session_state.barplot)

    with tab2:
        col1, col2 = st.columns(2)
        col2.markdown("<div style='width: 1px; height: 28px;'></div>", unsafe_allow_html=True)
        with col1:
            threshold_setting =  st.selectbox("Select Threshold", 
                                              [0.2, 0.5, 0.7], 
                                              help="What portion of the data is needed for plotting?"
                                              )
            
        with col2:
            if st.button("Show Pie Chart", key="generate_pieplot", help="Click to generate pie charts"):
                if st.session_state.df is None:
                    st.warning("Dataset not available!")
                else:
                    with st.spinner("Generating Pie Chart ... Please Wait"):
                        previous_threshold = st.session_state.get('previous_threshold', None)
                        if st.session_state.pieplot is None or threshold_setting != previous_threshold: 
                            try:   
                                st.session_state.pieplot = generate_pie_plots(threshold_setting)
                                st.plotly_chart(st.session_state.pieplot)
                                st.session_state.previous_threshold = threshold_setting
                            except:
                                st.error("Sorry, the model not able to generate visuals. Please try extracting again")
                        else:
                            st.plotly_chart(st.session_state.pieplot)
                    

if __name__ == "__main__":
    st.set_page_config(page_title="JobSum - Job Summary & Analysis")

    # Create tabs
    tabs = ["Home", "Data Extraction", "AI Conversation", "Data Summary & Insights", "Help", "About"]
    current_tab = st.sidebar.selectbox("Select Tab", tabs)
    if current_tab == "Home":
        home_tab()
    if current_tab == "Data Extraction":
        extraction_tab()
    elif current_tab == "AI Conversation":
        chat_tab()
    elif current_tab == "Data Summary & Insights":
        visualization_tab()
    elif current_tab == "Help":
        st.title("Content for Other Tab")
    elif current_tab == "About":
        st.title("About")
