import streamlit as st
import xattr

from classification.classification import classify_file_content


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    file_name = uploaded_file.name
    attribute = 'sensitivity'
    file = "/".join(('input', file_name))
    classification = classify_file_content(file)
    xattr.setxattr(f=file, attr=attribute,
                   value=classification.encode('utf-8'))
    value = xattr.getxattr(file, attribute).decode('utf-8')
    st.write(value)
    st.download_button(label=file_name, file_name=file_name,
                       data=uploaded_file)
