# 🧩 **Welcome to JobSum!**

#### What is it?

**JobSum** is a job summarization and interactive app built using Streamlit, designed to make your job search process easier and more efficient. It utilizes data fetched from popular websites like Indeed, LinkedIn, Glassdoor, ZipRecruiter, and more, and provides a personalized and comprehensive job summary for each search query. Let's dive into how this tool works and the features it offers.

#### How it Works?

The JobSum tool leverages an advanced LLM model (Gemini-Google) to analyze and understand hundreds of job descriptions in a matter of seconds. The AI can extract essential information such as required skills, experience levels, interview insights, and can even give tutorials and guides to refer to for the job. This process saves you valuable time that would otherwise be spent manually reading through numerous job postings.

#### Features

* **Job Summarization:** JobSum generates a concise summary of each job description, highlighting key details to help you understand the job requirements at a glance.
* **Skill Matching:** It identifies the most relevant skills needed for a particular job, making it easier for you to tailor your resume and cover letter accordingly.
* **Interview Insights:** Based on the job descriptions, you can ask the AI to provide interview questions and tips based on the job description.
* **Chat Functionality:** You can interact with the AI to ask questions about specific job preferences or seek advice on career-related topics.
* **Visualizations:** JobSum provides graphical representations of the data generated, offering a visual understanding of important factors to consider when applying for a job. You can explore different terms, positions within the same job category, and other valuable insights through these visualizations.

### Welcome Contributions!

Welcome contributions from the community to improve JobSum. Whether it's adding new features, fixing bugs, or enhancing documentation, every contribution matters!

### Running Local Setup

To run JobSum locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/sidharth72/JobSum
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your API key:
    ```bash
    python config.py
    ```
   Enter Your API KEY when prompted. Your API key will be saved to secrets.toml.

4. Run the application using Streamlit:
    ```bash
    streamlit run app.py
    ```
