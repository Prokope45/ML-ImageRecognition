# Tkinter
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile

# Other
from PIL import Image, ImageTk

# Keras/Tensorflow
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model


root = Tk()
root.geometry("450x600")
root.title('Machine Learning CNN')
# root.resizable(False, False)


filename = ''


def openFile():
    global filename
    f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)


def urlCallback(url):
    webbrowser.open_new_tab(url)


def load_image(file):
    # load the image
    img = load_img(file, target_size=(224, 224))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 3 channels
    img = img.reshape(1, 224, 224, 3)
    # center pixel data
    img = img.astype('float32')
    img = img - [123.68, 116.779, 103.939]
    return img


def run_example(file):
    if file != '':
        # load the image,
        img = load_image(file)
        # load model,
        model = load_model('final_model.h5')
        # predict the class
        predict = model.predict(img)[0][0]
        answer = str(round(predict, 5))
        if predict > 0.9:
            return f'This is a dog.\n Estimation of {answer}'
        elif predict < 0.001:
            return f'This is a cat.\n Estimation of {answer}'
        else:
            return f'I don\'t recognize this.\n Estimation of {answer}'
    else:
        return 'Upload image to test program.'


labelFont = ('arial', 18, 'bold')
subLabelFont = ('arial', 15)
paragraphFont = ('arial', 12)

desc = "This Program uses a trained CNN model to predict images\n" \
       "of dogs and cats. Submitting images not consisting\n" \
       "of either a dog or cat will not be accurately described.\n"

label = Label(root, text='Cats & Dogs\nImage classification', width=30, font=labelFont)
label.grid(row=1, column=1, pady=5)

label = Label(root, text=desc, width=50, font=paragraphFont)
label.grid(row=2, column=1)

source_link = Label(root, text="GitHub Repository", fg="blue", cursor="hand2")
source_link.grid(row=2, column=1, sticky=S)
source_link.bind("<Button-1>", lambda e: urlCallback("https://github.com/JaredP45/ML-ImageRecognition"))

upload = Button(root, text='Upload File', width=15, command=openFile)
upload.grid(row=3, column=1, pady=10)

while True:
    if filename != '':
        get_image = Image.open(filename)
        resize_image = get_image.resize((224, 224))
        render = ImageTk.PhotoImage(resize_image)
        image_label = Label(root, image=render)
        image_label.image = render
        image_label.grid(row=4, column=1, sticky=N)
    else:
        image_label = Label(root, width=30)
        image_label.grid(row=4, column=1, pady=127)

    prediction_result = Label(root, text=run_example(filename), width=30, font=subLabelFont)
    prediction_result.grid(row=5, column=1, pady=15)
    prediction_result.update()

root.mainloop()

