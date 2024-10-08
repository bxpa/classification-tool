import streamlit as st
import xattr

from classification.classification import classify_file_content

st.set_page_config(page_title="File classification")
st.markdown("# File classification")
st.write(
    """A tool designed to classify files by labeling them as public, sensitive, or confidential. In line with CIS Control 3.7, organisations must implement and maintain data classification schemes. This involves developing a standardised system to categorise information based on its sensitivity and criticality."""
)

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    file_name = uploaded_file.name
    attribute = "sensitivity"
    file = "/".join(("input", file_name))
    classification = classify_file_content(file)
    if classification not in ['public', 'confidential', 'sensitive']:
        st.error(classification)
        st.stop()
    match classification:
        case 'public':
            st.markdown("Classification: **:green[Public]**")
        case 'confidential':
            st.markdown("Classification: :orange[Sensitive]")
        case 'sensitive':
            st.markdown("Classification: :red[Confidential]")
    st.markdown("#### Options")
    option = st.selectbox('Change classification',
                          ('Public', 'Confidential', 'Sensitive'))
    xattr.setxattr(f=file, attr=attribute,
                   value=classification.encode("utf-8"))
    value = xattr.getxattr(file, attribute).decode("utf-8")
    if st.button('Download file'):
        st.download_button(label=file_name, file_name=file_name,
                           data=uploaded_file)
