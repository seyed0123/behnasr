
import logging
import tensorflow as tf
import glob,sys
from tensorflow.keras.layers import *
from tensorflow.keras.utils import load_img,img_to_array
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class_names=['اسناد بانکی 1',
 'اسناد بانکی 2',
 'اسناد بانکی 3',
 'اسناد بانکی 4',
 'شناسنامه قدیم صفحه 1',
 'شناسنامه قدیم صفحه 2',
 'شناسنامه جدید صفحه 1',
 'شناسنامه جدید صفحه 2',
 'شناسنامه جدید صفحه 3',
 'شناسنامه جدید صفحه 4',
 'قبض برق',
 'قبض گاز',
 'کارت ملی قدیم',
 'کارت ملی جدید',
 'کارت پایان خدمت قدیم',
 'کارت پایان خدمت جدید',
 'روزنامه',
 'قبض آب',
 'مجله',
 'مقاله',
 'گذرنامه']


# In[3]:


model=tf.keras.applications.VGG16(False,input_shape=(112,112,3),weights=None)
model.trainable=False


x=Flatten()(model.output)
x=Dense(64,activation='relu')(x)
x=BatchNormalization()(x)
x=Dropout(.25)(x)

x=Dense(64,activation='relu')(x)
x=BatchNormalization()(x)
x=Dropout(.25)(x)


x=Dense(21,'softmax')(x)

model=tf.keras.Model(inputs=model.input,outputs=x)
# model.summary()


# In[4]:


#loss_=SparseCategoricalCrossentropy(from_logits=False)
#model.compile('adam',loss=loss_,metrics=['acc'])
model.load_weights("classify_model.h5")


# In[12]:
def classify(image_path):

    img_test=img_to_array(load_img(image_path,target_size=(112,112))).reshape((1,112,112,3))/255.0
    a=model.predict(img_test).argmax()
    return class_names[a]