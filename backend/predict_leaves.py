import numpy as np
from keras.models import load_model
from keras.preprocessing import image

model=load_model("leaves_disease_classification_model.h5")
labels=['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

def get_prediction(path):
    img=image.load_img(path,target_size=(224,224))
    img=image.img_to_array(img)
    x=np.expand_dims(img,axis=0)
    probabilities=model.predict(x)
    temp=process_probabilities(probabilities)    
    return labels[model.predict_classes(x)[0]],temp

def process_probabilities(prbs):
    prob_category_list=[]
    probabilities=prbs
    print("Probabilities")
    print(np.argmax(probabilities[0]))
    for i in range(len(probabilities[0])):
        prob_category_list.append((labels[i],probabilities[0][i]))
    prob_category_list.sort(key=lambda x:x[1],reverse=True)
    temp=[]
    for i in prob_category_list[:5]:
        temp.append((i[0],"{:.7f}".format(i[1]*100)))
    return temp
