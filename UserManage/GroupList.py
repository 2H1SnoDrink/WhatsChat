import os,sys
import importlib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *

DEFAULT_HEAD = 'icons/qq.png'
DEFAULT_MSG = 'Hello is there anyone?'
DEFAULT_IMG = 'icons/img.png'

def checkContainChinese(s):
    for ch in s.decode('utf-8',errors = 'ignore'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def splitStringByLen(text,Len):
    importlib.reload(sys) 
   
    text = text.replace('\n','.')
    (myText, nLen) = ('',0)

    return myText

class BubbleText(QLabel):
   
    border = 5
    trigon = 20
    lineLen = 40 

    minH = 2 * trigon + 2 * border
    minW = 2 * trigon + 2 * border

    def __init__(self,listItem,listView,text = DEFAULT_MSG,lr = True):
        self.listItem = listItem
        self.listView = listView
        self.text = text
    
        myText = splitStringByLen(text, self.lineLen) 

        super(BubbleText, self).__init__(myText)

        self.setMinimumWidth(self.minW)
        self.setFont(QFont("Times",20,QFont.Normal))
        self.setState(False)

        self.lr = lr
        if self.lr:
    
            self.setContentsMargins(self.trigon*sqrt(3)/2 + 3,self.border + 3,self.border + 3,self.border + 3)
        else:
            self.setContentsMargins(self.border + 3,self.border + 3,self.trigon*sqrt(3)/2 + 3,self.border + 3)

    def paintEvent(self, e):
        size =  self.size()
        qp = QPainter()
        qp.begin(self)
        if self.lr:
            self.leftBubble(qp,size.width(),size.height())
        else:
            self.rightBubble(qp,size.width(),size.height())
        qp.end()
        super(BubbleText, self).paintEvent(e)

    def leftBubble(self,qp, w, h):
        qp.setPen(self.colorLeftE)
        qp.setBrush(self.colorLeftM)
        middle = h/2
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        pL = QPolygonF()
        pL.append(QPointF(0,middle)) 
        pL.append(QPointF(shiftx, middle + shifty)) 
        pL.append(QPointF(shiftx, h - self.border))
        pL.append(QPointF(w - self.border, h - self.border)) 
        pL.append(QPointF(w - self.border, self.border))
        pL.append(QPointF(shiftx, self.border)) 
        pL.append(QPointF(shiftx, middle - shifty))
        qp.drawPolygon(pL)

    def rightBubble(self, qp, w, h):
        qp.setPen(self.colorRightE)
        qp.setBrush(self.colorRightM)
        middle = h/2
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        pL = QPolygonF()
        pL.append(QPointF(w,middle)) 
        pL.append(QPointF(w - shiftx, middle + shifty)) 
        pL.append(QPointF(w - shiftx, h - self.border)) 
        pL.append(QPointF(self.border, h - self.border)) 
        pL.append(QPointF(self.border, self.border)) 
        pL.append(QPointF(w - shiftx, self.border)) 
        pL.append(QPointF(w - shiftx, middle - shifty)) 
        qp.drawPolygon(pL)

    def setState(self,mouse):
        
        if mouse:
            self.colorLeftM = QColor("#eaeaea")
            self.colorLeftE = QColor("#D6D6D6")
            self.colorRightM = QColor("#8FD648")
            self.colorRightE = QColor("#85AF65")
        else:
            self.colorLeftM = QColor("#fafafa")
            self.colorLeftE = QColor("#D6D6D6")
            self.colorRightM = QColor("#9FE658")
            self.colorRightE = QColor("#85AF65")
        self.update() 

    def enterEvent(self,e):
        
        self.setState(True)
    def leaveEvent(self,e):
        
        self.setState(False)
    
    def contextMenuEvent(self,e): 
        
        editUser = QAction(QIcon('../icons/copy.png'), u'复制', self)
        editUser.triggered.connect(self.copyText)

        delUser = QAction(QIcon('../icons/delete.png'), u'删除', self)
        delUser.triggered.connect(self.delTextItem)

        menu = QMenu()
        menu.addAction(editUser)
        menu.addAction(delUser)
        menu.exec_(QCursor.pos())

        e.accept() 

    def copyText(self,b):
        
        cb = QApplication.clipboard()
        cb.setText(self.text)
    def delTextItem(self,b):
        
        self.listView.takeItem(self.listView.indexFromItem(self.listItem).row())

class LabelHead(QLabel):
    
    def __init__(self,addr = DEFAULT_HEAD):
        super(LabelHead,self).__init__()
        self.setScaledContents(True)
        self.setReadOnly(True)
        self.setPicture(addr)

    def setReadOnly(self,b):
        self._readOnly = bool(b)

    def setPicture(self,addr):
        
        
        img = QPixmap(addr)
        self.setPixmap(img)
        return True

    def getPicture(self):
        return self._picAddr


class TextItem(QWidget):
    
    def __init__(self, listItem, listView, text = DEFAULT_MSG, lr=True, head = DEFAULT_HEAD):
        super(TextItem,self).__init__()
        hbox = QHBoxLayout()
        text = BubbleText(listItem,listView,text,lr)
        head = LabelHead(head)
        head.setFixedSize(50,50)

        if lr is not True:
            hbox.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding,QSizePolicy.Preferred))
            hbox.addWidget(text)
            hbox.addWidget(head)
        else:
            hbox.addWidget(head)
            hbox.addWidget(text)
            hbox.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding,QSizePolicy.Preferred))
            
        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)
        self.setContentsMargins(0,0,0,0)


class BubbleImage(QLabel):

    border = 5
    trigon = 20
    lineLen = 40

    minH = 2 * trigon + 2 * border
    minW = 2 * trigon + 2 * border

    def __init__(self,listItem,listView,img = DEFAULT_IMG,lr = True,maxWidth = 500):
        self.listItem = listItem
        self.listView = listView
        self.img = img
        super(BubbleImage, self).__init__()

        self.setMinimumWidth(self.minW)

        self.setState(False)

        self.lr = lr
        if self.lr:
            self.setContentsMargins(self.trigon*sqrt(3)/2 + 3,self.border + 3,self.border + 3,self.border + 3)
        else:
            self.setContentsMargins(self.border + 3,self.border + 3,self.trigon*sqrt(3)/2 + 3,self.border + 3)

        self.setScaledContents(True)
        if not os.path.exists(img):
            img = DEFAULT_IMG

        pic = QPixmap(img)
        self.wid = pic.size().width() if pic.size().width()<maxWidth else maxWidth
        nPic = pic.scaledToWidth(self.wid)
        self.setPixmap(nPic)

        if img.endswith('gif'):
            self.movie = QMovie(self)
            self.movie.setFileName(img)
            self.movie.setCacheMode(QMovie.CacheNone)
            self.movie.frameChanged.connect(self.animate)
            self.movie.start()

    @pyqtSlot(int)
    def animate(self,index):
        pic = self.movie.currentPixmap()
        nPic = pic.scaledToWidth(self.wid)
        self.setPixmap(nPic)

    def paintEvent(self, e):
        size =  self.size()
        qp = QPainter()
        qp.begin(self)
        if self.lr:
            self.leftBubble(qp,size.width(),size.height())
        else:
            self.rightBubble(qp,size.width(),size.height())
        qp.end()
        super(BubbleImage, self).paintEvent(e)

    def leftBubble(self,qp, w, h):
        qp.setPen(self.colorLeftE)
        qp.setBrush(self.colorLeftM)
        middle = h/2
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        pL = QPolygonF()
        pL.append(QPointF(0,middle))
        pL.append(QPointF(shiftx, middle + shifty))
        pL.append(QPointF(shiftx, h - self.border))
        pL.append(QPointF(w - self.border, h - self.border))
        pL.append(QPointF(w - self.border, self.border))
        pL.append(QPointF(shiftx, self.border))
        pL.append(QPointF(shiftx, middle - shifty))
        qp.drawPolygon(pL)

    def rightBubble(self, qp, w, h):
        qp.setPen(self.colorRightE)
        qp.setBrush(self.colorRightM)
        middle = h/2
        shifty = self.trigon/2
        shiftx = self.trigon*sqrt(3)/2
        pL = QPolygonF()
        pL.append(QPointF(w,middle))
        pL.append(QPointF(w - shiftx, middle + shifty))
        pL.append(QPointF(w - shiftx, h - self.border))
        pL.append(QPointF(self.border, h - self.border))
        pL.append(QPointF(self.border, self.border))
        pL.append(QPointF(w - shiftx, self.border))
        pL.append(QPointF(w - shiftx, middle - shifty))
        qp.drawPolygon(pL)

    def setState(self,mouse):

        if mouse:
            self.colorLeftM = QColor("#eaeaea")
            self.colorLeftE = QColor("#D6D6D6")
            self.colorRightM = QColor("#8FD648")
            self.colorRightE = QColor("#85AF65")
        else:
            self.colorLeftM = QColor("#fafafa")
            self.colorLeftE = QColor("#D6D6D6")
            self.colorRightM = QColor("#9FE658")
            self.colorRightE = QColor("#85AF65")
        self.update()

    def enterEvent(self,e):

        self.setState(True)
    def leaveEvent(self,e):

        self.setState(False)

    def contextMenuEvent(self,e):

        editUser = QAction(QIcon('../icons/copy.png'), u'复制', self)
        editUser.triggered.connect(self.copyImage)

        delUser = QAction(QIcon('../icons/delete.png'), u'删除', self)
        delUser.triggered.connect(self.delTextItem)

        menu = QMenu()
        menu.addAction(editUser)
        menu.addAction(delUser)
        menu.exec_(QCursor.pos())

        e.accept()

    def copyImage(self,b):

        cb = QApplication.clipboard()
        cb.setImage(QImage(self.img))
    def delTextItem(self,b):

        self.listView.takeItem(self.listView.indexFromItem(self.listItem).row())

    def mouseDoubleClickEvent(self,e):
        from PIL import Image
        im = Image.open(self.img)
        im.show()


class ImageItem(QWidget):

    def __init__(self, listItem, listView, img = DEFAULT_MSG, lr=True, head = DEFAULT_HEAD):
        super(ImageItem,self).__init__()
        hbox = QHBoxLayout()
        img = BubbleImage(listItem,listView,img,lr)
        head = LabelHead(head)
        head.setFixedSize(50,50)

        if lr is not True:
            hbox.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding,QSizePolicy.Preferred))
            hbox.addWidget(img)
            hbox.addWidget(head)
        else:
            hbox.addWidget(head)
            hbox.addWidget(img)
            hbox.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding,QSizePolicy.Preferred))

        hbox.setContentsMargins(0,0,0,0)
        self.setLayout(hbox)
        self.setContentsMargins(0,0,0,0)




class GroupList(QListWidget):

    def __init__(self):
        super(GroupList, self).__init__()
        
        self.setStyleSheet(
            "QListWidget::item{border:0px solid gray;background-color:transparent;padding:0px;color:transparent}"  
            "QListView::item:!enabled{background-color:transparent;color:transparent;border:0px solid gray;padding:0px 0px 0px 0px;}"  
            "QListWidget::item:hover{background-color:transparent;color:transparent;border:0px solid gray;padding:0px 0px 0px 0px;}"  
            "QListWidget::item:selected{background-color:transparent;color:transparent;border:0px solid gray;padding:0px 0px 0px 0px;}")

    def addTextMsg(self,sz = DEFAULT_MSG, lr = True, head = DEFAULT_HEAD):
        it = QListWidgetItem(self)
        wid = self.size().width()
        item = TextItem(it,self,sz,lr,head) 
        
        it.setSizeHint(item.sizeHint())
        it.setFlags(Qt.ItemIsEnabled)
        self.addItem(it)
        self.setItemWidget(it,item)
        self.setCurrentItem(it)
        
    def addImageMsg(self,img = DEFAULT_IMG, lr = True, head = DEFAULT_HEAD):
        it = QListWidgetItem(self)
        wid = self.size().width()
        item = ImageItem(it,self,img,lr,head) 
        
        it.setSizeHint(item.sizeHint())
        it.setFlags(Qt.ItemIsEnabled)
        self.addItem(it)
        self.setItemWidget(it,item)
        self.setCurrentItem(it)




if __name__=='__main__':
    app = QApplication(sys.argv)
    ml=GroupList()
    ml.setMinimumSize(500,500)
    ml.addTextMsg("Hello",True)
    ml.addTextMsg("World!",False)
    ml.addTextMsg(u"昨夜小楼又东风，春心泛秋意上心头，恰似故人远来载乡愁，今夜月稀掩朦胧，低声叹呢喃望星空，恰似回首终究一场梦，轻轻叹哀怨...",True)
    ml.addTextMsg(u"With a gentle look on her face, she paused and said,她脸上带着温柔的表情，稍稍停顿了一下，便开始讲话",False)
    ml.addImageMsg('ref/bq.gif',True)
    ml.addImageMsg('ref/mt.gif',False)
    ml.show()

    sys.exit(app.exec_())
