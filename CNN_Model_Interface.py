# Tkinter
import tkinter as tk
from tkinter import ttk
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

# Other
from PIL import Image, ImageTk

# Keras/Tensorflow
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

filePath = ''


class ImageUpload(tk.Tk):
    def __init__(self):
        super().__init__()
        options = {'padx': 5, 'pady': 5}
        self.geometry("450x600")
        self.title('Machine Learning CNN')
        self.resizable(False, False)

        # Font Styles
        self.labelFont = ('arial', 18, 'bold')
        self.subLabelFont = ('arial', 15)
        self.paragraphFont = ('arial', 12)

        # File Path
        global filePath

        # Description
        self.desc = "This Program uses a trained CNN model to predict images\n" \
                    "of dogs and cats. Submitting images not consisting\n" \
                    "of either a dog or cat will not be accurately described.\n"

        # Repository URL
        self.repoURL = "https://github.com/JaredP45/ML-ImageRecognition"

        self.label = Label(self, text='Cats & Dogs\nImage classification', width=30, font=self.labelFont)
        self.label.grid(row=1, column=1, pady=5)

        self.label = Label(self, text=self.desc, width=50, font=self.paragraphFont)
        self.label.grid(row=2, column=1)

        self.source_link = Label(self, text='GitHub Repository', fg="blue", cursor="hand2")
        self.source_link.grid(row=2, column=1, sticky=S)
        self.source_link.bind("<Button-1>", lambda e: self.url_callback())

        self.upload = Button(self, text='Upload Image', width=15, command=self.open_file)
        self.upload.grid(row=3, column=1, pady=10)

        self.display_and_return_result()

    def display_and_return_result(self):
        global filePath
        if filePath != '':
            get_image = Image.open(filePath)
            resize_image = get_image.resize((224, 224))
            render = ImageTk.PhotoImage(resize_image)
            image_label = Label(self, image=render)
            image_label.image = render
            image_label.grid(row=4, column=1, sticky=N)
            image_label.update()
        else:
            image_label = Label(self, width=30)
            image_label.grid(row=4, column=1, pady=127)

        prediction_result = Label(self, text=self.run_analysis(), width=30, font=self.subLabelFont)
        prediction_result.grid(row=5, column=1, pady=15)

    @staticmethod
    def load_image(path):
        # load the image
        img = load_img(path, target_size=(224, 224))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 3 channels
        img = img.reshape(1, 224, 224, 3)
        # center pixel data
        img = img.astype('float32')
        img = img - [123.68, 116.779, 103.939]
        return img

    def run_analysis(self):
        global filePath
        if filePath != '':
            # load the image,
            img = self.load_image(filePath)
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

    @staticmethod
    def open_file():
        global filePath
        f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]
        filePath = askopenfilename(filetypes=f_types)
        return filePath

    def url_callback(self):
        webbrowser.open_new_tab(self.repoURL)


if __name__ == '__main__':
    app = ImageUpload()
    app.mainloop()
