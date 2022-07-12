import  os
import matplotlib.pyplot as plt

def show_image():
    img_path =r"D:\Working\Python\Smilesproject\app\static\uploads"+"\\"+os.listdir(r"../static/uploads")[-1]
    img = plt.imread(img_path)
    fig = plt.figure('show picture')
    # ax = fig.add_subplot(111)
    plt.imshow(img)
    plt.show()

