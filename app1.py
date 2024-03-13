import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Google Generative AI with the API key
genai.configure(api_key=api_key)

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="Histopathological Analysis", page_icon="🔬")

# Display the app header
st.title("Histopathological Diagnosis with LLM")
st.caption("🔬 A Streamlit app powered by Google Gemini for clinical analysis.")

# Input section for clinical observations
st.subheader("Clinical Observations Input")
clinical_observations = st.text_area("Enter the clinical observations here:", height=150,
                                     placeholder="Describe the visual and clinical characteristics noted during the examination...")

# Generation configuration and safety settings
generation_config = {
    "temperature": 0.1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 32000,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Button to generate the histopathological diagnosis
submit_button = st.button("Generate Diagnosis")

# Handling the diagnosis generation
if submit_button and clinical_observations:
    detailed_analysis_prompt = f"""
Given the clinical observations listed below, provide a detailed microscopic description that precisely matches one of the melanoma types detailed in the following six shot inferences. It is crucial that the response directly correlates specific clinical inputs with microscopic findings, leading to an exact histopathological diagnosis focusing specifically on melanoma.

Clinical Observations: {clinical_observations}

To assist in your analysis, compare these observations to the melanoma types detailed in the six shot inferences provided. Your response should strictly follow the structure provided in these examples, with a microscopic description highlighting cellular architecture, pigmentation patterns, and any specific markers or cell types noted. The conclusion should be a histopathological diagnosis that aligns strictly with one of the known melanoma types described below.

First shot inference:
Input: Asymmetry in shape and color, horizontal growth within the epidermis before deeper invasion, Pagetoid spread of melanocytes into the epidermis, varied pigmentation.
Output: The examination reveals asymmetry, indicative of irregular melanocytic proliferation. Evidence of horizontal growth characteristic of in situ melanoma is noted, with cancerous cells infiltrating the epidermis and varied pigmentation suggesting diverse melanin patterns.

Second shot inference:
Input: Large, flat patch with irregular borders, primarily epidermal confinement, increased melanin production, single dominant color.
Output: Findings suggest a lentigo maligna melanoma, with a large, irregularly bordered patch, primarily epidermal involvement, increased melanin resulting in darker pigmentation, and a single dominant color.

Third shot inference:
Input: Asymmetry, vertical growth pattern, possible pigmented or amelanotic areas, increased cellularity.
Output: There's marked asymmetry and a vertical growth pattern with deep dermal invasion. The lesion can be pigmented or amelanotic, with densely packed cells, indicative of nodular melanoma.

Fourth shot inference:
Input: Irregular pigmentation with brown, black, or blue-gray hues, longitudinal streaks along the nail unit, Pagetoid spread of melanocytes.
Output: The lesion shows irregular pigmentation and longitudinal streaks in the nail unit, with a pagetoid spread of melanocytes, suggesting acral lentiginous melanoma.

Fifth shot inference:
Input: Spindle-shaped malignant melanocytes, dense collagen fibers, minimal pigmentation.
Output: There is a proliferation of spindle-shaped melanocytes with dense collagen, indicating a desmoplastic melanoma with variable melanin production.

Sixth shot inference:
Input: Absence of melanin, Melan-A and HMB-45 positive, spindle-shaped melanocytes at the dermo-epidermal junction, spread into the dermis.
Output: The lesion lacks melanin but shows melanocytic differentiation markers. Spindle-shaped melanocytes are asymmetrically distributed, with dermal invasion, consistent with amelanotic melanoma.

Your analysis should meticulously adhere to these examples, directly linking the clinical observations to a specific type of melanoma, providing a concise microscopic description, and a definitive diagnosis based on the observed patterns. The output format must consistently reflect the detail and structure observed in the shot inference examples.
"""

    # Create the model with specific configurations
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

    with st.spinner("Generating histopathological diagnosis..."):
        response = model.generate_content(detailed_analysis_prompt)
        # Displaying the generated diagnosis
        st.subheader("Histopathological Diagnosis")
        st.write(response.text)

