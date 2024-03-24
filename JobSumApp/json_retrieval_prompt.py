import streamlit as st

def retrieve_prompt(search_term):
    prompt = f"""
        Extract as much as distinct, important skill and requirement keywords related to {search_term} from this job descriptions. Here is how the format needed:

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

            Instructions while filling:

            1. Fill those and give it as a JSON file, values must be a list.
            2. Don't Give any other suggestion or comments.
            3. Ensure that the terms provided are highly relevant to the job role and reflect the skills, qualifications, soft skills, technologies, experience, responsibilities, industry, and company culture associated with {search_term}.
            4. Each item inside the list must be a word of term related to the role (as required).
            5. Fill all the fields; it's mandatory.

        """
    
    return prompt