import streamlit as st
import time
import csv
import pandas_gbq
import SessionState
import pandas as pd
from streamlit import caching
import webcolors
from math import floor
from collections import Counter
from zipfile import ZipFile
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from sklearn.cluster import KMeans
from detecto import core, utils, visualize
from detecto.utils import reverse_normalize, normalize_transform, _is_iterable
import torchvision, torch
from torchvision import transforms
from PIL import Image
from google.cloud import storage, bigquery
print(os.getcwd())

clientbq = storage.Client.from_service_account_json(json_credentials_path='wawa-smart-store-82072f7ce73f.json')
bucketx = clientbq.get_bucket('wawa-zipped-assets')

gcs = storage.Client()
storage_client = clientbq 

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

def store_selector():
    bucket = storage_client.get_bucket('wawa-zipped-assets')
    iterator = bucket.list_blobs(delimiter="/")
    response = iterator._get_next_page_response()
    return response['prefixes']

def warmer_selector(prefix):
    bucket = storage_client.get_bucket('wawa-zipped-assets')
    iterator = bucket.list_blobs(delimiter="/",prefix = prefix)
    response = iterator._get_next_page_response()
    data = [x.split("/")[-2] for x in response['prefixes'] if "cooler" not in x]
    return data
 
def file_selector(prefix):
    bucket = storage_client.get_bucket('wawa-zipped-assets')
    iterator = bucket.list_blobs(delimiter="/",prefix = prefix)
    response = iterator._get_next_page_response()
    data=[]
    for i in response['items']:
        z='gs://'+'wawa-zipped-assets'+'/'+i['name']
        data.append(z)
    data=data[1:]
    data = [x.split("/")[-1] for x in data]
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
    
    choosen_color = st.selectbox("Choose the Color",color_names)

    if st.button("Save Color"):
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
    store_list = store_selector()
    store_list = store_list[::-1]
    store_list.append("-")
    store_list = store_list[::-1]
    store_choosen = st.selectbox("Choose the Store ID",store_list)
    if store_choosen != "-":
        ls = warmer_selector(store_choosen)
        ls = ls[::-1]
        ls.append("-")
        ls = ls[::-1]
        warmer_choosen = st.selectbox("Choose the Warmer",ls)
        
        if warmer_choosen != "-":
            warmer_path = store_choosen + warmer_choosen + "/"
            warmer_images = file_selector(warmer_path)
            
            sql = """
            SELECT *
            FROM `wawa.zipfile-extractcode-checklist`
            ;
            """

            zipfile_details = pandas_gbq.read_gbq(sql,project_id="wawa-smart-store")
            new_data = zipfile_details[zipfile_details["Store_Name"] == store_choosen]
            coded_files = list(new_data["ZipFile_Name"])
            
            new_warmer_images = [x for x in warmer_images if x not in coded_files]
            
            new_warmer_images.append("-")
            new_warmer_images = new_warmer_images[::-1]
            zip_file = st.selectbox("Choose the file to Collect Images",new_warmer_images)
            

            if zip_file != "-":
                blob = bucketx.blob(f'{store_choosen}{warmer_choosen}/{zip_file}')
                st.info(os.listdir(f'{os.getcwd()}/zip_files'))
                blob.download_to_filename(f'{os.getcwd()}/zip_files/{zip_file}')
                st.info(os.listdir(f'{os.getcwd()}/zip_files'))
                with ZipFile("zip_files/{}".format(zip_file), 'r') as zipObj:
                    zipObj.extractall('images')
                
                os.remove("zip_files/{}".format(zip_file))
                
                image_files = os.listdir("images")
                image_files = [x for x in image_files if "png" in x]
                image_files.append("-")
                image_files = image_files[::-1]
                choose_image = st.selectbox("Choose An Image: ",image_files)
                
                          
                if choose_image != "-":
                    
                    image = Image.open("images/{}".format(choose_image))
                    st.image(image)
            
                    if "bottom" in choose_image:
                        query = "SELECT url FROM `wawa.ai-models` where type='bottomRight' ORDER BY time desc limit 1;"
                        client = bigquery.Client()
                        query_job = client.query(query)
                        model_path = ""
                        for item in query_job:
                            model_path = item[0]
                        
                        storage_client = storage.Client()
                        bucket = storage_client.bucket('wawa-data-models')
                        blob = bucket.blob(model_path.split('gs://wawa-data-models/')[-1])
                        blob.download_to_filename(os.getcwd()+'/models/'+'bottom_high_resolution_model.pth')
                        model = loadmodel("bottom_high_resolution_model.pth")
                        
                    else:
                        query = "SELECT url FROM `wawa.ai-models` where type='topLeft' ORDER BY time desc limit 1;"
                        client = bigquery.Client()
                        query_job = client.query(query)
                        model_path = ""
                        for item in query_job:
                            model_path = item[0]
                        
                        storage_client = storage.Client()
                        bucket = storage_client.bucket('wawa-data-models')
                        blob = bucket.blob(model_path.split('gs://wawa-data-models/')[-1])
                        blob.download_to_filename(os.getcwd()+'/models/'+'top_high_resolution_model.pth')
                        model = loadmodel("top_high_resolution_model.pth")
                        
                    predictions = model.predict(image)
                    labels, boxes, scores = predictions

                    def condition(x): 
                        return x > 0.8
                    output = [idx for idx, element in enumerate(scores) if condition(element)]            
                    labels=[labels[i] for i in output]
                    boxes=boxes[output,:]
                    scores=scores[output]
                    
                    if len(labels) != 0:
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        show_labeled_image(image, boxes, scores, labels)
                    else:
                        header2("No boxes Detected")
                    
                    st.write("")
                    st.write("")
                    
                    if st.button("Save File"):

                        list1 = []
                        list2 = []
                        list1.append(store_choosen)
                        list2.append(zip_file)

                        df = pd.DataFrame(
                        {
                            "Store_Name":list1,
                            "ZipFile_Name":list2
                        }
                    )

                        df.to_gbq("wawa.zipfile-extractcode-checklist","wawa-smart-store", if_exists="append")
                        
            st.button("refresh")
                

if __name__ == "__main__":
    box_detect()