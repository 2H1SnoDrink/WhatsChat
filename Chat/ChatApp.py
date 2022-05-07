import os,sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UserManage.User import UserList
from UserManage.GroupList import GroupList
from ChatUI import ChatUI

DEFAULT_HEAD = 'icons/qq.png'


class TextEdit(QTextEdit,QObject):

    entered = pyqtSignal()
    def __init__(self, parent = None):
        super(TextEdit, self).__init__(parent)
    
    def keyPressEvent(self,e):
        
        if (e.key() == Qt.Key_Return) and (e.modifiers() == Qt.ControlModifier):
            self.entered.emit()
            self.clear()
        super(TextEdit,self).keyPressEvent(e)


class MsgInput(QWidget,QObject):

    textEntered = pyqtSignal(str)
    imgEntered = pyqtSignal(str)

    btnSize = 35
    teditHeight = 200
    
    def __init__(self,parent = None):
        super(MsgInput, self).__init__(parent)
        self.setContentsMargins(3,3,3,3)

        self.textEdit = TextEdit()
        self.textEdit.setMaximumHeight(self.teditHeight)
        self.setMaximumHeight(self.teditHeight+self.btnSize)
        self.textEdit.setFont(QFont("Times",20,QFont.Normal))
        self.textEdit.entered.connect(self.sendText)

        sendImg = QPushButton()
        sendImg.setStyleSheet("QPushButton{border-image:url(icons/img.png);}"
             "QPushButton:hover{border: 2px groove blue;}"
             "QPushButton:pressed{border-style: inset;}")
        sendImg.setFixedSize(self.btnSize,self.btnSize)
        sendImg.clicked.connect(self.sendImage)

        sendTxt = QPushButton(u'发送')
        sendTxt.setFont(QFont("Microsoft YaHei",15,QFont.Bold))
        sendTxt.setFixedHeight(self.btnSize)
        sendTxt.clicked.connect(self.sendText)

        hl = ChatUI()
        hl.addWidget(sendImg)
        hl.addWidget(sendTxt)
        

        vl = QVBoxLayout()
        vl.addLayout(hl)
        vl.addWidget(self.textEdit)
        
        self.setLayout(vl)

    def sendImage(self):
        dialog = QFileDialog(self,u'请选择图像文件...')
        dialog.setDirectory(os.getcwd() + '/ref') 
        dialog.setNameFilter(u"图片文件(*.png *.jpg *.bmp *.ico);;")
        if dialog.exec_():
            selectFileName = str(dialog.selectedFiles()[0])
            self.imgEntered.emit(selectFileName)
        else:
            pass
    def sendText(self):
        txt = self.textEdit.toPlainText()
        if len(txt)>0:
            self.textEntered.emit(txt)


class ChatApp(QSplitter):
    
    curUser = {'id':None,'name':None,'head':DEFAULT_HEAD}
    selfHead = DEFAULT_HEAD
    def __init__(self):
        super(ChatApp, self).__init__(Qt.Horizontal)

        self.setWindowTitle('WhatsChat')
        self.setWindowIcon(QIcon('../icons/chat.png'))
        self.setMinimumSize(500,500) 

        self.ursList = UserList()
        self.ursList.setMaximumWidth(250)
        self.ursList.setMinimumWidth(180)
        self.ursList.itemDoubleClicked.connect(self.setChatUser)
        self.msgList = GroupList()
        self.msgList.setDisabled(True) 
        self.msgInput = MsgInput()
        self.msgInput.textEntered.connect(self.sendTextMsg)
        self.msgInput.imgEntered.connect(self.sengImgMsg)
        
        self.ursList.setParent(self)
        rSpliter = QSplitter(Qt.Vertical, self)
        self.msgList.setParent(rSpliter)
        self.msgInput.setParent(rSpliter)

        self.setDemoUser() 

    def setDemoMsg(self):
        self.msgList.clear()
        self.msgList.addTextMsg("Hello",True,self.curUser['head'])
        self.msgList.addTextMsg("World!",False,self.selfHead)
        self.msgList.addTextMsg(u"昨夜小楼又东风，春心泛秋意上心头，恰似故人远来载乡愁，今夜月稀掩朦胧，低声叹呢喃望星空，恰似回首终究一场梦，轻轻叹哀怨...",True,self.curUser['head'])
        self.msgList.addTextMsg(u"With a gentle look on her face, she paused and said,她脸上带着温柔的表情，稍稍停顿了一下，便开始讲话",False,self.selfHead)
        self.msgList.addImageMsg('ref/bq.gif',True,self.curUser['head'])
        self.msgList.addImageMsg('ref/mt.gif',False,self.selfHead)
    def setDemoUser(self):
        self.ursList.clear()
        self.ursList.addUser('hello')
        self.ursList.addUser('world')
        self.ursList.addGroup('group')
        self.ursList.addUser('HeLiang',group = 'group')
        self.ursList.addGroup(u'中文')
        self.ursList.addUser(u'何亮',group = u'中文',head = 'icons/hd_1.png')

    @pyqtSlot(str)
    def sendTextMsg(self,txt):
        txt = str(txt)
        self.msgList.addTextMsg(txt,False)
    @pyqtSlot(str)
    def sengImgMsg(self,img):
        img = str(img)
        self.msgList.addImageMsg(img,False)
    @pyqtSlot(QListWidgetItem)
    def setChatUser(self,item):
        (self.curUser['id'],self.curUser['name'],self.curUser['head']) = (item.getId(),item.getName(),item.getHead())
        self.msgList.setDisabled(False)
        self.setWindowTitle('WhatsChat: chating with %s...'% self.curUser['name'])
        self.setDemoMsg()


if __name__=='__main__':
    app = QApplication(sys.argv)
    pchat = ChatApp()
    pchat.show()
    sys.exit(app.exec_())
