import streamlit as st
import time
import csv
import pandas_gbq
import SessionState
import pandas as pd
import webcolors
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from collections import Counter
from math import floor
import cv2
import os
import numpy as np
from sklearn.cluster import KMeans
from detecto import core, utils, visualize
from detecto.utils import reverse_normalize, normalize_transform, _is_iterable
from torchvision import transforms
import torchvision, torch
from PIL import Image
from google.cloud import storage
gcs = storage.Client()

def header1(url): 
    st.markdown(f'<p style="color:#66cdaa;font-size:25px;border-radius:2%;"><strong>{url}</strong></p>', unsafe_allow_html=True)

def header2(url): 
    st.markdown(f'<p style="color:#1261A0;font-size:40px;border-radius:2%;"><center><strong>{url}</strong></center></p>', unsafe_allow_html=True)
    
def header3(url): 
    st.markdown(f'<p style="color:#d6b798;font-size:25px;border-radius:2%;"><strong>{url}</strong></p>', unsafe_allow_html=True)
    
def loadmodel(model_name):
    label=['sizzli_box']
    model = core.Model.load(os.getcwd() + '/models/{name}'.format(name=model_name.split('/')[-1]),label)
    return model

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def model_selector():
    storage_client = storage.Client()
    bucket_name='sizzli_warmer_data'
    bucket = storage_client.get_bucket(bucket_name)
    prefix='models/'
    iterator = bucket.list_blobs(delimiter='/', prefix=prefix)
    response = iterator._get_next_page_response()
    data=[]
    for i in response['items']:
        z='gs://'+bucket_name+'/'+i['name']
        data.append(z)
    data=data[1:]
    return data

def new_closer_color(image):
    #new_hex_colors = {}
    
    sql = """
    SELECT *
    FROM `wawa.box-color-dataset`
    ;
    """
    data_frame = pandas_gbq.read_gbq(sql,project_id="wawa-smart-store")
    
    color_code = data_frame["Color_code"]
    color_name = data_frame["Color_name"]
    
    zipbObj = zip(color_code, color_name)
    new_hex_colors = dict(zipbObj)
    
    hexnames = new_hex_colors
    names = []
    positions = []
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    dst = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    modified_image = cv2.resize(dst, (600, 400), interpolation = cv2.INTER_AREA)
    
    input_image = image.reshape(image.shape[0]*image.shape[1], 3)
    clf = KMeans(n_clusters = 1)
    labels = clf.fit_predict(input_image)
    counts = Counter(labels)

    center_colors = clf.cluster_centers_
    
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    
    for i in hexnames:
        names.append(hexnames[i])
        positions.append(webcolors.hex_to_rgb(i))
        
    spacedb = KDTree(positions)

    x = rgb_colors
    
    x[0] = [int(i) for i in x[0]]
    dist, index = spacedb.query(x[0])
    
    #print('The color %r is closest to %s.'%(x[0], names[index]))
    return names[index]

def find_color_code(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    dst = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    modified_image = cv2.resize(dst, (600, 400), interpolation = cv2.INTER_AREA)
    input_image = image.reshape(image.shape[0]*image.shape[1], 3)

    clf = KMeans(n_clusters = 1)
    labels = clf.fit_predict(input_image)
    counts = Counter(labels)

    center_colors = clf.cluster_centers_

    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    
    
    plt.figure(figsize = (6, 6))
    fig, ax = plt.subplots()
    ax.pie(counts.values(), colors = hex_colors)
    st.pyplot(fig)
    return hex_colors[0]

def show_labeled_image(image, boxes, scores, labels=None):

    color = []

    if boxes.ndim == 1:
        boxes = boxes.view(1, 4)
        
    x = []
    
    for i in range(boxes.shape[0]):
        x.append(float(boxes[i][0])) 
        
    x.sort()
    
    session_state = SessionState.get(page_number = 0)
    last_page = boxes.shape[0] - 1
    
    if st.button("Next"):

            if session_state.page_number + 1 > last_page:
                session_state.page_number = 0
            else:
                session_state.page_number += 1
                
    val = session_state.page_number
    
    header2("Box {}".format(val+1))
    
    box = boxes[val]
    y = float(box[0].item())
    
    bbox = (floor(box[0]),floor(box[1]),floor(box[2]),floor(box[3]))
    crop_img = image.crop(bbox)
    new_crop_img = np.array(crop_img) 
    new_crop_img = new_crop_img[:, :, ::-1].copy() 

    col1, col2 = st.columns([1,1])
    
    with col1:
        st.image(crop_img)
        new_color = new_closer_color(new_crop_img)
        
    with col2:
        hex_code = find_color_code(new_crop_img)
    
    header1("Detected Color : {}".format(new_color))
    header3("Hex code of detected color: {}".format(hex_code))
    
    st.warning("If the detected color is wrong, Please choose the correct color and save it!")
    sql = """
    SELECT *
    FROM `wawa.color-product-dataset`
    ;
    """
    data_frame = pandas_gbq.read_gbq(sql,project_id="wawa-smart-store")
    
    color_names = data_frame["Color"]
    
    choosen_color = st.selectbox("Choose the color:",color_names)

    if st.button("Save"):
        #create a data frame and add it to the big query
        list1 = []
        list2 = []
        list1.append(hex_code)
        list2.append(choosen_color)
        
        df = pd.DataFrame(
        {
            "Color_code":list1,
            "Color_name":list2
        }
    )
        
        df.to_gbq("wawa.box-color-dataset","wawa-smart-store", if_exists="append")
        
        newly_detected_color = new_closer_color(new_crop_img)
        header1("The detected color after saving is {}".format(newly_detected_color))
        
    
def box_detect():
    
    st.title("Color detection of sizzli box")
    
    uploaded_file = st.file_uploader("Upload Image Files",type=['jpg','png','jpeg'])
        
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image)
        
        model_path=model_selector()
        model_path = model_path[::-1]
        model_path.append("-")
        model_path = model_path[::-1]
        model_name = st.selectbox('Select the model', model_path)

        if model_name != "-":
            model = loadmodel(model_name)
            
            predictions = model.predict(image)
            labels, boxes, scores = predictions

            def condition(x): 
                return x > 0.8
            output = [idx for idx, element in enumerate(scores) if condition(element)]            
            labels=[labels[i] for i in output]
            boxes=boxes[output,:]
            scores=scores[output]
            
            st.set_option('deprecation.showPyplotGlobalUse', False)
            show_labeled_image(image, boxes, scores, labels)

if __name__ == "__main__":
    box_detect()