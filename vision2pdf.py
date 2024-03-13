import openai
import streamlit as st
from streamlit_chat import message
import pandas as pd
from docx import Document
from io import BytesIO

# Setting page title and header
st.set_page_config(page_title="Histopathological Analysis AI System", page_icon=":microscope:")
st.markdown("<h1 style='text-align: center;'>Histopathological Analysis AI System</h1>", unsafe_allow_html=True)

# Set org ID and API key (Replace with your actual credentials)
openai.organization = "org-XgYioQ92YzmR7LR5kLET6v4b"
openai.api_key = "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"

# Ensure session state for DataFrame is correctly initialized
if 'data' not in st.session_state or not isinstance(st.session_state['data'], pd.DataFrame):
    st.session_state['data'] = pd.DataFrame(columns=['Index', 'Input', 'Output'])

# Sidebar for model selection
st.sidebar.title("Settings")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5-turbo", "gpt-4"), index=1)

# Function to generate responses from OpenAI's chat model
def generate_response(clinical_observations):
    prompt = f"""Based on the clinical observations listed below, generate a detailed microscopic description leading to a precise histopathological diagnosis. Follow the structure provided in these examples to ensure the response aligns closely with professional histopathology reports.

Clinical Observations: {clinical_observations}

Using the format below, interpret these observations to provide:
Microscopic Description: A detailed account of the histopathological features observed under the microscope, including cellular architecture, pigmentation patterns, and identification of specific markers or cell types.
Diagnosis: A concise histopathological diagnosis based on the microscopic description, clearly stating the type of melanoma or other skin lesion identified.

Example Inferences:

- Asymmetry, Pagetoid spread, varied pigmentation → In situ melanoma with irregular melanocytic proliferation and horizontal epidermal invasion.
- Large, flat patch, increased melanin → Lentigo maligna melanoma with epidermal confinement and single dominant color.
- Vertical growth pattern, increased cellularity → Nodular melanoma with deep dermal invasion and possible pigmentation variations.
- Irregular pigmentation, longitudinal nail streaks → Acral lentiginous melanoma with Pagetoid melanocyte spread.
- Spindle-shaped melanocytes, dense collagen → Desmoplastic melanoma with minimal pigmentation.
- Absence of melanin, Melan-A and HMB-45 positive → Amelanotic melanoma with dermal invasion and spindle-shaped melanocytes at the junction.

Please adhere to the structure and detail level illustrated in these examples to formulate your response. Make it concise, brief and accurate as much as possible."""

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
    
    # Append the new input and output to the DataFrame in session state
    new_index = len(st.session_state['data']) + 1
    new_row = pd.DataFrame({'Index': [new_index], 'Input': [user_input], 'Output': [response]})
    st.session_state['data'] = pd.concat([st.session_state['data'], new_row], ignore_index=True)

# Display the updated DataFrame as a table
if not st.session_state['data'].empty:
    st.write(st.session_state['data'])

# Function to convert DataFrame to Word document
def df_to_docx(df):
    doc = Document()
    table = doc.add_table(rows=1, cols=3)
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Index'
    hdr_cells[1].text = 'Input'
    hdr_cells[2].text = 'Output'
    
    for index, row in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(row['Index'])
        row_cells[1].text = str(row['Input'])
        row_cells[2].text = str(row['Output'])
    
    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()

# Download buttons for Excel and Word
file_format = st.selectbox("Select Download Format:", ["Excel", "Word"])

if st.button('Download Data') and not st.session_state['data'].empty:
    if file_format == "Excel":
        to_download = BytesIO()
        with pd.ExcelWriter(to_download, engine="openpyxl") as writer:
            st.session_state['data'].to_excel(writer, index=False)
        to_download.seek(0)
        st.download_button(label="Download Excel", data=to_download.getvalue(), file_name="analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif file_format == "Word":
        docx_bytes = df_to_docx(st.session_state['data'])
        st.download_button(label="Download Word", data=docx_bytes, file_name="analysis.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")