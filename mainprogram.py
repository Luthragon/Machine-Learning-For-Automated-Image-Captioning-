import tkinter as tk
from _xxsubinterpreters import destroy
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy as np

#load the trained model to classify sign
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from pickle import dump, load
from tensorflow.keras.preprocessing.image import load_img, img_to_array
'''
base_model = InceptionV3(weights = 'inception_v3_weights_tf_dim_ordering_tf_kernels.h5')
vgg_model = Model(base_model.input, base_model.layers[-2].output)
'''
base_model = ResNet50(weights = 'resnet50_weights_tf_dim_ordering_tf_kernels.h5')
resnet_model = Model(base_model.input, base_model.layers[-2].output)

def preprocess_img(img_path):
    #inception v3 excepts img in 299*299
    img = load_img(img_path, target_size = (224, 224))
    x = img_to_array(img)
    # Add one more dimension
    x = np.expand_dims(x, axis = 0)
    x = preprocess_input(x)
    return x

def encode(image):
    image = preprocess_img(image)
    vec = resnet_model.predict(image)
    vec = np.reshape(vec, (vec.shape[1]))
    return vec

def greedy_search(pic):
    start = 'startseq'
    for i in range(max_length):
        seq = [wordtoix[word] for word in start.split() if word in wordtoix]
        seq = pad_sequences([seq], maxlen = max_length)
        yhat = model.predict([pic, seq])
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        start += ' ' + word

        if word == 'endseq':
            break

    final = start.split()
    final = final[25:-1]
    final = ' '.join(final)

    return final




pickle_in = open("wordtoix.pkl", "rb")
wordtoix = load(pickle_in)
pickle_in = open("ixtoword.pkl", "rb")
ixtoword = load(pickle_in)
max_length = 37
model = load_model('model.h5')




#initialise GUI
top=tk.Tk()
top.geometry('1300x720')
top.resizable(0,0)
top.title('Caption Generator')
top.configure(background='#fffbde')
label=Label(top, font=('arial',15))
label3=Label(top, font=('arial',10))
sign_image = Label(top)
def classify(file_path):
    global label_packed
    enc = encode(file_path)
    image = enc.reshape(1, 2048)

    pred = greedy_search(image)
    print(pred)
    label.configure(foreground='#000', text=pred)
    label3.configure(text='Accuracy around 80%')
    label.pack(side=BOTTOM,expand=True)
    label3.place(relx=0.3,rely= 0.3)

def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        label3.configure(text='')
        show_classify_button(file_path)
    except:
        pass

def show_classify_button(file_path):
    classify_b=Button(top,text="Proses",command=lambda: classify(file_path), padx=10,pady=10)
    classify_b.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
    classify_b.place(relx=0.82,rely=0.5)


exit = Button(top,text='Exit Aplikasi',command=exit)
exit.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
exit.pack(side=RIGHT, padx=50, pady=50)


upload=Button(top,text="Pilih Gambar",command=upload_image,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload.pack(side=RIGHT,padx=70)
sign_image.pack(side=BOTTOM,expand=True)


#label2.pack(side = BOTTOM, expand = True)
heading = Label(top, text="Pembuat Caption",pady=20, font=('arial',22,'bold'))

heading.pack(side=TOP)
top.mainloop()

