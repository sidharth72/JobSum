import streamlit as st

def retrieve_prompt(search_term):
    prompt = f"""
            Your task is to meticulously review the provided job descriptions and extract distinct, essential keywords pertaining to the {search_term} role. Please categorize the extracted keywords into the following JSON format:

            General Keywords (List[words]):
            Skills (List[words]):
            Qualification (List[words]):
            Soft Skills (List[words]):
            Additional (List[words]):
            Other (List[words]):
            Technologies (List[words]):
            Experience (List[words]):
            Responsibilities (List[words]):
            Industry (List[words]):
            Company Culture (List[words]):

            To ensure optimal results, adhere to the following guidelines:

            1. Populate each category with a list of relevant terms, not sentences.
            2. Ensure that the extracted keywords are highly specific and accurately reflect the core aspects of the {search_term} role, including required skills, qualifications, soft skills, technologies, experience, responsibilities, industry, and company culture.
            3. Each list item should be a concise, role-related word or term.
            4. Populate all categories with at least one relevant keyword; do not leave any category empty.
            5. Avoid including redundant or overly general terms that do not provide meaningful insights into the {search_term} role.
            6. Do not include any additional suggestions, comments, or explanations in the output.

        """
    
    return prompt