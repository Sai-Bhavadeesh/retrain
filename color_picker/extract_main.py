import numpy as np
import pandas as pd
import streamlit as st 
import os

from PIL import Image

import extract_color_code
import new_product_data
import extract_color_code_gcp
from pathlib import Path
import base64

PAGES = {
    "Color Code Extraction":extract_color_code_gcp,
    "Add New Product": new_product_data
}


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


col1, col2, col3 = st.columns([1,4,1])
with col1:
    st.write("")
with col2:
    st.image(os.getcwd()+"/wawa-logo.png")
with col3:
    st.write("")
st.sidebar.write("**Powered By**")
st.sidebar.image(os.getcwd()+"/Techolution-logo.png")

st.sidebar.title('Choose an option')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.box_detect()
