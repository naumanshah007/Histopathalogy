
    
import openai
import streamlit as st
from streamlit_chat import message

# Setting page title and header
st.set_page_config(page_title="Histopathological Analysis AI System", page_icon=":microscope:")
st.markdown("<h1 style='text-align: center;'>Histopathological Analysis AI System</h1>", unsafe_allow_html=True)

# Set org ID and API key (Replace with your actual credentials)
openai.organization = "org-XgYioQ92YzmR7LR5kLET6v4b"
openai.api_key = "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"

# Initialise session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]

# Sidebar for model selection
st.sidebar.title("Settings")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5-turbo", "gpt-4"), index=1)

# Function to generate responses from OpenAI's chat model
def generate_response(clinical_observations):
    prompt = f"""Given the clinical observations listed below, provide a detailed microscopic description that leads to a precise histopathological diagnosis. Use the following six shot inferences as a guide to understanding how specific clinical inputs translate into microscopic findings and diagnoses.

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

Here are the Clinical Observations: {clinical_observations}

Instructions:
Clinical Observations: Provide the visual and clinical characteristics noted during the examination.
Microscopic Description: Translate these observations into microscopic histopathological findings, detailing the cellular architecture, pigmentation patterns, and any specific markers or cell types noted.
Diagnosis: Conclude with a histopathological diagnosis, considering the microscopic description and how it aligns with known melanoma types.
"""

    messages = [{"role": "system", "content": prompt}]
    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=messages
    )

    return completion.choices[0].message.content

# Main interface for entering clinical observations
user_input = st.text_area("Enter the clinical observations here:", key='input', height=150)
submit_button = st.button(label='Generate Analysis', key='submit')

# Generate and display response upon submission
if submit_button and user_input:
    response = generate_response(user_input)
    message(user_input, is_user=True)
    message(response)