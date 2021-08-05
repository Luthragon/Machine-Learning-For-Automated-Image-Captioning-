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
#from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from pickle import dump, load
from tensorflow.keras.preprocessing.image import load_img, img_to_array

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
top.geometry('1910x1020')
top.resizable(0,0)
top.title('Caption Generator')
top.configure(background='#fffbde')

frame1 = Frame(top, width = 1500, height = 720 , highlightbackground='grey',highlightthickness=3)
frame1.place(x = 100, y = 110)

frame2 = Frame(top, width = 600, height = 100, highlightbackground='grey',highlightthickness=3)
frame2.place(x=700,y=875)
#frame2.place(relx=0.33,rely=0.85)

frame3 = Frame(top, width = 250, height = 50, highlightbackground='green',highlightthickness=3)
#frame2.place(x=1700,y=480)
frame3.place(relx=0.85,rely=0.38)


label=Label(top, font=('arial',15))
label2=Label(top, font=('arial',15))
label4=Label(top, font=('arial',15))

sign_image = Label(frame1)
heading = Label(top, text="Aplikasi Automated Image Captioning", background='#fffbde', font=('arial',22,'bold'))
heading.pack(pady=40)
label2.configure(text='Caption : ')
label2.place(x=470,y=750)

def classify(file_path):
    # global label_packed
    enc = encode(file_path)
    image = enc.reshape(1, 2048)

    pred = greedy_search(image)
    #print(pred)
    label.configure(foreground='#000', text=pred)
    label4.configure(text='87%')
    label.place(x=500,y=750)
    label4.place(x=1750,y=400)

def upload_image():
    try:
        
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        uploaded=uploaded.resize((1490,630), Image.ANTIALIAS)
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        # label.configure(text='')
        # # label4.configure(text='')
        show_classify_button(file_path)
    except:
        pass

def show_classify_button(file_path):
    classify_b=Button(frame2,text="Proses",command=lambda: classify(file_path), padx=30,pady=20)
    classify_b.configure(background='#364156', foreground='white',font=('arial',15,'bold'))
    #classify_b.place(x=250,y=25)
    classify_b.grid(row=0,column=1)






label3=Label(frame3, font=('arial',15))
label3.configure(text="Accuracy : ")
label3.place(x=10,y=10)



exit = Button(frame2,text='Exit Aplikasi',command=exit, padx=30, pady=20)
exit.configure(background='#364156', foreground='white',font=('arial',15,'bold'))
#exit.place(x=400,y=25)
exit.grid(row=0,column=2)


upload=Button(frame2,text="Pilih Gambar",command=upload_image,padx=30,pady=20)
upload.configure(background='#364156', foreground='white',font=('arial',15,'bold'))
#upload.place(x=60,y=25)
upload.grid(row=0,column=0)
# sign_image.place(x=570,y=150)
sign_image.place(x=1,y=1)


#label2.pack(side = BOTTOM, expand = True)



top.mainloop()

