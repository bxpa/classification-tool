import streamlit as st
import xattr

from classification.classification import classify_file_content

st.header("File classification")
st.write(
    """A tool designed to classify files by labeling them as public, sensitive, or confidential. In line with CIS Control 3.7, organisations must implement and maintain data classification schemes. This involves developing a standardised system to categorise information based on its sensitivity and criticality."""
)

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    file_name = uploaded_file.name
    attribute = "sensitivity"
    file = "/".join(("input", file_name))
    classification = classify_file_content(file)
    xattr.setxattr(f=file, attr=attribute,
                   value=classification.encode("utf-8"))
    value = xattr.getxattr(file, attribute).decode("utf-8")
    st.write(value)
    st.download_button(label=file_name, file_name=file_name,
                       data=uploaded_file)
