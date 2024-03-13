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
st.set_page_config(
    page_title="Histopathological Analysis",
    page_icon="🔬"
)

# Display the app header
st.title("Histopathological Diagnosis with LLM")
st.caption("🔬 A Streamlit app powered by Google Gemini for clinical analysis.")

# Input section for clinical observations
st.subheader("Clinical Observations Input")
clinical_observations = st.text_area(
    "Enter the clinical observations here:",
    height=150,
    placeholder="Describe the visual and clinical characteristics noted during the examination..."
)

# Button to generate the histopathological diagnosis
submit_button = st.button("Generate Diagnosis")

# Handling the diagnosis generation
if submit_button and clinical_observations:
    # Including your detailed analysis prompt with user-provided clinical observations
    detailed_analysis_prompt = f"""Given the clinical observations listed below, provide a detailed microscopic description that leads to a precise histopathological diagnosis. Use the following six shot inferences as a guide to understanding how specific clinical inputs translate into microscopic findings and diagnoses.

Clinical Observations: {clinical_observations}

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

Instructions:
Clinical Observations: Provide the visual and clinical characteristics noted during the examination.
Microscopic Description: Translate these observations into microscopic histopathological findings, detailing the cellular architecture, pigmentation patterns, and any specific markers or cell types noted.
Diagnosis: Conclude with a histopathological diagnosis, considering the microscopic description and how it aligns with known melanoma types.
"""

    # Configuring the model's prompt and settings
    model = genai.GenerativeModel("gemini-pro")
    with st.spinner("Generating histopathological diagnosis..."):
        response = model.generate_content(detailed_analysis_prompt)
        # Displaying the generated diagnosis
        st.subheader("Histopathological Diagnosis")
        st.write(response.text)