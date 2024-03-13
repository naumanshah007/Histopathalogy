import streamlit as st
import anthropic

# Set up the Anthropic API key
anthropic.api_key = "YOUR_API_KEY"

def get_detailed_analysis(clinical_observations):
    detailed_analysis_prompt = f""" Given the clinical observations listed below, provide a detailed microscopic description that precisely matches one of the melanoma types detailed in the following six shot inferences. It is crucial that the response directly correlates specific clinical inputs with microscopic findings, leading to an exact histopathological diagnosis focusing specifically on melanoma. First shot inference: Input: Asymmetry in shape and color, horizontal growth within the epidermis before deeper invasion, Pagetoid spread of melanocytes into the epidermis, varied pigmentation. Output: The examination reveals asymmetry, indicative of irregular melanocytic proliferation. Evidence of horizontal growth characteristic of in situ melanoma is noted, with cancerous cells infiltrating the epidermis and varied pigmentation suggesting diverse melanin patterns. Second shot inference: Input: Large, flat patch with irregular borders, primarily epidermal confinement, increased melanin production, single dominant color. Output: Findings suggest a lentigo maligna melanoma, with a large, irregularly bordered patch, primarily epidermal involvement, increased melanin resulting in darker pigmentation, and a single dominant color. Third shot inference: Input: Asymmetry, vertical growth pattern, possible pigmented or amelanotic areas, increased cellularity. Output: There's marked asymmetry and a vertical growth pattern with deep dermal invasion. The lesion can be pigmented or amelanotic, with densely packed cells, indicative of nodular melanoma. Fourth shot inference: Input: Irregular pigmentation with brown, black, or blue-gray hues, longitudinal streaks along the nail unit, Pagetoid spread of melanocytes. Output: The lesion shows irregular pigmentation and longitudinal streaks in the nail unit, with a pagetoid spread of melanocytes, suggesting acral lentiginous melanoma. Fifth shot inference: Input: Spindle-shaped malignant melanocytes, dense collagen fibers, minimal pigmentation. Output: There is a proliferation of spindle-shaped melanocytes with dense collagen, indicating a desmoplastic melanoma with variable melanin production. Sixth shot inference: Input: Absence of melanin, Melan-A and HMB-45 positive, spindle-shaped melanocytes at the dermo-epidermal junction, spread into the dermis. Output: The lesion lacks melanin but shows melanocytic differentiation markers. Spindle-shaped melanocytes are asymmetrically distributed, with dermal invasion, consistent with amelanotic melanoma. Clinical Observations: {clinical_observations} To assist in your analysis, compare these observations to the melanoma types detailed in the six shot inferences provided. Your response should strictly follow the structure provided in these examples, with a microscopic description highlighting cellular architecture, pigmentation patterns, and any specific markers or cell types noted. The conclusion should be a histopathological diagnosis that aligns strictly with one of the known melanoma types described below. ... """
    return detailed_analysis_prompt.format(clinical_observations=clinical_observations)

def get_claude_response(prompt):
    response = anthropic.completions(prompt=prompt, model="claude-3-opus-20240229")
    return response.result["completionResult"]

def main():
    st.title("Detailed Melanoma Analysis")
    clinical_observations = st.text_area("Enter clinical observations")
    if clinical_observations:
        detailed_analysis_prompt = get_detailed_analysis(clinical_observations)
        with st.spinner("Generating detailed analysis..."):
            detailed_analysis = get_claude_response(detailed_analysis_prompt)
        st.markdown(detailed_analysis)

if __name__ == "__main__":
    main()