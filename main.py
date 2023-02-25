import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import textwrap

from io import BytesIO
from PIL import Image,ImageQt,ImageDraw,ImageFont
#

class ImageWindow(QWidget):
    def __init__(self,imagelink,toptext,bottomtext):
        super().__init__()
        print(imagelink)
        self.setWindowTitle("Image")


        #!!!WE DONT TALK ABOUT THIS!!!
        #!!!WE DONT TALK ABOUT THIS!!!
        #!!!WE DONT TALK ABOUT THIS!!!
        req = requests.get(imagelink)
        imgbytes = req.content
        imgbytesconvert = BytesIO(imgbytes)
        img = Image.open(imgbytesconvert)


        #save space
        ##add text
        draw = ImageDraw.Draw(img)
        print(img.size[1])
        font = ImageFont.truetype(font="./impact/impact.ttf", size=int(img.size[0]/10))
        fontWidth, fontHeight = font.getsize("A")
        charsPerLine = img.size[1] // fontWidth
        toplines = textwrap.wrap(toptext, width=charsPerLine)
        bottomlines = textwrap.wrap(bottomtext, width=charsPerLine)

        y = 10 
        for line in toplines:
            lineWidth, lineHeight = font.getsize(line)
            x = (img.size[1] - lineWidth)/2
            draw.text((x,y), line, fill='white', font=font, stroke_width=4, stroke_fill='black')
            y += lineHeight
        
        y = img.size[0] - fontHeight * len(bottomlines) - 15
        for line in bottomlines:
            lineWidth, lineHeight = font.getsize(line)
            x = (img.size[1] - lineWidth)/2
            draw.text((x,y), line, fill='white', font=font, stroke_width=4, stroke_fill='black')
            y += lineHeight
        #save space


        qtimg = ImageQt.toqpixmap(img)
        #!!!WE DONT TALK ABOUT THIS!!!
        #!!!WE DONT TALK ABOUT THIS!!!
        #!!!WE DONT TALK ABOUT THIS!!!
        

        #label and size
        self.imageLabel = QLabel(self)
        self.image = QPixmap(qtimg)
        self.imageLabel.setPixmap(self.image)
        self.resize(img.size[1],img.size[0])
        

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.resize(300,200)
        
        self.lyt_main = QHBoxLayout()
        self.lyt_form = QFormLayout()

        self.btn1 = QPushButton("Generuj obrazek")
        self.lineedit1 = QLineEdit("34485603")
        self.lineedit1.setPlaceholderText("Enter player id")
        self.lineedit2 = QLineEdit("Teskt górny")
        self.lineedit2.setPlaceholderText("Top text")
        self.lineedit3 = QLineEdit("Tekst dolny")
        self.lineedit3.setPlaceholderText("Bottom text")
        self.lbl1 = QLabel("Generuj obrazek")
        self.funnyimage = None

        #tu jest api  o tu
        #               |
        #               |
        #               v
        #https://thumbnails.roblox.com/docs/index.html
        urltemplate = "https://thumbnails.roblox.com/v1/users/avatar-headshot?"
        def generujObrazek():
            urlother = f"userIds={self.lineedit1.text()}&size=420x420&format=Png&isCircular=false"
            fullurl = (urltemplate+urlother)
            res = requests.get(url=fullurl)
            res.raise_for_status()
            dane = res.json()
            if len(dane['data'][0]) < 2:
                return False 
            self.funnyimage = ImageWindow(dane['data'][0]['imageUrl'],self.lineedit2.text(),self.lineedit3.text())
            self.funnyimage.show()

        self.btn1.clicked.connect(generujObrazek)
        
        self.lyt_form.addWidget(self.lineedit1)
        self.lyt_form.addWidget(self.lineedit2)
        self.lyt_form.addWidget(self.lineedit3)
        self.lyt_form.addWidget(self.btn1)
        self.lyt_main.addLayout(self.lyt_form)

        self.setLayout(self.lyt_main)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = Main()
    okno.show()
    sys.exit(app.exec_())


    