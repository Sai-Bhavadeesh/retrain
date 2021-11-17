import streamlit as st
import pandas as pd

def header1(url): 
    st.markdown(f'<p style="color:#66cdaa;font-size:25px;border-radius:2%;"><center><strong>{url}</strong></center></p>', unsafe_allow_html=True)
    
def box_detect():
    
    st.title("Adding New Product Details")
            
    cl = st.text_input('Color of the Box:', "Hunter Green")
    dn = st.text_input("Dashboard Name:", "Double Bacon Croissant")
    bn = st.text_input("Sizzli Box Name:", "DOUBLE MEAT SIZZLI BACON 6.9OZ - 7.1OZ")
    
    if st.button("Save to big query"):
        list1 = []
        list2 = []
        list3 = []
        list1.append(cl)
        list2.append(dn)
        list3.append(bn)
        
        df = pd.DataFrame(
        {
            "Color":list1,
            "Dashboard":list2,
            "Box":list3
        }
    )
        
        df.to_gbq("wawa.color-product-dataset","wawa-smart-store", if_exists="append")
        header1("The new product is saved to Big Query")
    

if __name__ == "__main__":
    box_detect()