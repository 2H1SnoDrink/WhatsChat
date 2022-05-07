import os,sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

DEFAULT_GROUP = u'undefined'
DEFAULT_HEAD = u'icons/qq.png'
DEFAULT_USER = u'new user'
DEFAULT_NOTE = u'There is nothing to say...'



class LabelHead(QLabel):
   
    def __init__(self,addr = DEFAULT_HEAD):
        super(LabelHead,self).__init__()
        self.setScaledContents(True)
        self.setReadOnly(True)
        self.setPicture(addr)

    def setReadOnly(self,b):
        self._readOnly = bool(b)

    def setPicture(self,addr):
        
        self._picAddr = str(addr)
        img = QPixmap(addr)
        self.setPixmap(img)
        return True

    def getPicture(self):
        return self._picAddr

    def mousePressEvent(self,e):
        
        if self._readOnly:
            e.ignore() 
        else:
            dialog = QFileDialog(self,u'请选择头像文件...')
            dialog.setDirectory(os.getcwd() + '/icons') 
            dialog.setNameFilter(u"图片文件(*.png *.jpg *.bmp *.ico);;")
            if dialog.exec_():
                selectFileName = str(dialog.selectedFiles()[0])
                self.setPicture(selectFileName)
            else:
                pass
            e.accept() 


class LineEdit(QLineEdit):
    
    def __init__(self,sz = None):
        super(LineEdit,self).__init__(str(sz))
        self.setReadOnly(True)

    def setReadOnly(self,b):
        
        if b:
            self._readOnly = True
            self.setStyleSheet("border-width:0;border-style:outset;background-color:rgba(0,0,0,0)")
        else:
            self._readOnly = False
            self.setStyleSheet("color:#000000")
        super(LineEdit,self).setReadOnly(self._readOnly)

    def contextMenuEvent(self,e):
        
        if self._readOnly:
            e.ignore() 
        else:
            super(LineEdit,self).contextMenuEvent(e)

    def mousePressEvent(self,e):
        
        if self._readOnly:
            e.ignore() 
        else:
            super(LineEdit,self).mousePressEvent(e)

    def mouseDoubleClickEvent(self,e):
        
        if self._readOnly:
            self.setSelection(0,self.maxLength())
            e.ignore() 
        else:
            super(LineEdit,self).mouseDoubleClickEvent(e)

    def mouseMoveEvent(self,e):
        
        if self._readOnly:
            e.ignore() 
        else:
            super(LineEdit,self).mouseMoveEvent(e)


class UserItem(QWidget):
    
    def __init__(self, listWidgetItem, usrId, **args):
        super(UserItem,self).__init__()

        self._listWidgetItem = listWidgetItem
        self._id = usrId

        self._headWidget = LabelHead()
        self._headWidget.setFixedSize(40, 40)
        self.setHead(args.get('head',DEFAULT_HEAD))
        
        self._nameWidget = LineEdit()
        self._nameWidget.setFont(QFont("Microsoft YaHei",10,QFont.Bold))
        self.setName(args.get('name',DEFAULT_USER))

        self._noteWidget = LineEdit()
        self.setNote(args.get('note',DEFAULT_NOTE))

        vbox = QVBoxLayout()
        vbox.addWidget(self._nameWidget)
        vbox.addWidget(self._noteWidget)
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self._headWidget)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

    def getListItem(self):
        return self._listWidgetItem

    def setName(self,name):
        self._name = str(name)
        self._nameWidget.setText('%s (%d)' %(self._name,self._id))
        self._nameWidget.setReadOnly(True)
    def getNameInput(self):
        return self._nameWidget.text()
    def getName(self):
        return self._name

    def setNote(self,note):
        self._note = str(note)
        self._noteWidget.setText(self._note)
        self._noteWidget.setReadOnly(True)
    def getNoteInput(self):
        return self._noteWidget.text()
    def getNote(self):
        return self._note

    def setHead(self,head):
        self._head = str(head)
        self._headWidget.setPicture(self._head)
        self._headWidget.setReadOnly(True)
    def getHead(self):
        return self._headWidget.getPicture()
    def getHeadInput(self):
        return self._headWidget.getPicture()
    
    def editInfo(self):
        self._nameWidget.setReadOnly(False)
        self._noteWidget.setReadOnly(False)
        self._headWidget.setReadOnly(False)
        self._nameWidget.setText(self._name)
        self._nameWidget.setFocus()

    def lockInfo(self):
        self._nameWidget.setReadOnly(True)
        self._noteWidget.setReadOnly(True)
        self._headWidget.setReadOnly(True)


    
    def keyPressEvent(self,e):
        
        if e.key() == Qt.Key_Return:
            self._listWidgetItem.confirmInput()

    def contextMenuEvent(self,e): 
        
        editUser = QAction(QIcon('../icons/edit.png'), u'修改', self)
        editUser.triggered.connect(self.editInfo)

        delUser = QAction(QIcon('../icons/delete.png'), u'删除', self)
        delUser.triggered.connect(self._listWidgetItem.delSelfFromList)

        menu = QMenu()
        menu.addAction(editUser)
        menu.addAction(delUser)
        menu.exec_(QCursor.pos())

        e.accept() 


    def mouseMoveEvent(self, e):
        
        if e.buttons() != Qt.LeftButton:
            return e.ignore()
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)
        e.accept()


class UserListItem(QListWidgetItem):
    
    def __init__(self, parent, usrId, name = DEFAULT_USER, 
            head = DEFAULT_HEAD, note = DEFAULT_NOTE, 
            group = DEFAULT_GROUP):
        super(UserListItem,self).__init__(name,None,QListWidgetItem.UserType)
        
        self._id = usrId
        self._group = str(group) 
        self._parent = parent
        self._widget = UserItem(self,usrId,name = name, head = head, note = note)
        self._widget.lockInfo()

        
        self.setSizeHint(self._widget.sizeHint())

    def getWidget(self):
        return self._widget
    def getId(self):
        return self._id

    def getId(self):
        return self._id

    def setGroup(self,group):
        self._group = str(group)
        self.setText(self._group + '_' + self.getNameInput())
        
    def getGroup(self):
        return self._group

    def setName(self,name):
        self._widget.setName(name)
        self.setText(self._group + '_' + name)
    def getNameInput(self):
        return self._widget.getNameInput()
    def getName(self):
        return self._widget.getName()

    def setNote(self,note):
        self._widget.setNote(note)
    def getNoteInput(self):
        return self._widget.getNoteInput()
    def getNote(self):
        return self._widget.getNote()

    def setHead(self,head):
        self._widget.setHead(head)
    def getHeadInput(self):
        return self._widget.getHeadInput()
    def getHead(self):
        return self._widget.getHead()

    def confirmInput(self):
        self.setName(self.getNameInput())
        self.setNote(self.getNoteInput())
        self.setHead(self.getHeadInput())
        self._widget.lockInfo()

    def giveUpInput(self):
        self.setName(self.getName())
        self.setNote(self.getNote())
        self.setHead(self.getHead())
        self._widget.lockInfo()

    def delSelfFromList(self):
        self._parent.removeUserItem(self)

    


class GroupItem(QWidget,QObject):
    """自定义的组信息控件"""
    expended = pyqtSignal(bool) 
    def __init__(self, listWidgetItem, name = DEFAULT_GROUP):
        super(GroupItem, self).__init__()
        self.setAcceptDrops(True)

        self._listWidgetItem = listWidgetItem
        
        self._expendWidget = QPushButton()
        self._expendWidget.clicked.connect(self.toggleGroup)
        self._expendWidget.setFixedSize(10,10)
        self._isOpen = False
        self.toggleGroup() 

        self._nameWidget = LineEdit()
        self._nameWidget.setFont(QFont("Times",10,QFont.Normal))
        self.setName(name)

        hbox = QHBoxLayout()
        hbox.addWidget(self._expendWidget)
        hbox.addWidget(self._nameWidget)
        hbox.addStretch()

        self.setLayout(hbox)
        

    def setName(self,name):
        self._name = str(name)
        self._nameWidget.setText('%s (%d)'%(name, len(self._listWidgetItem.usrList)))
        self._nameWidget.setReadOnly(True)
    def getNameInput(self):
        return self._nameWidget.text()
    def getName(self):
        return self._name

    def toggleGroup(self):
        self._isOpen = not self._isOpen
        if self._isOpen:
            self._expendWidget.setStyleSheet("border-image: url(icons/arrow_d.png);")
        else:
            self._expendWidget.setStyleSheet("border-image: url(icons/arrow_r.png);")
        self._expendWidget.update()
        self.expended.emit(not self._isOpen)

    def editInfo(self):
        self._nameWidget.setReadOnly(False)
        self._nameWidget.setText(self._name)
        self._nameWidget.setFocus()

    def lockInfo(self):
        self._nameWidget.setReadOnly(True)

    
    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Return:
            self._listWidgetItem.confirmInput()

    def contextMenuEvent(self,e): 
        adusr = QAction(QIcon('../icons/user.png'), u'添加用户', self)
        adusr.triggered.connect(self._listWidgetItem.addNewUser)
        
        editGroup = QAction(QIcon('../icons/edit.png'), u'修改', self)
        editGroup.triggered.connect(self.editInfo)

        delGroup = QAction(QIcon('../icons/delete.png'), u'删除', self)
        delGroup.triggered.connect(self._listWidgetItem.delSelfFromList)

        menu = QMenu()
        menu.addAction(adusr)
        menu.addAction(editGroup)
        menu.addAction(delGroup)
        menu.exec_(QCursor.pos())

        e.accept() 

    def dragEnterEvent(self, e):
        
        self._listWidgetItem.setSelected()
        e.accept()

    def dropEvent(self, e):
        src = e.source() 
        srcUit = src.getListItem()
        self._listWidgetItem.moveUserIn(srcUit)
        e.accept()


class GroupListItem(QListWidgetItem):
    
    
    def __init__(self, parent, name = DEFAULT_GROUP):
        super(GroupListItem,self).__init__(name,None,QListWidgetItem.UserType)

        self.usrList = []
        self._parent = parent
        self._widget = GroupItem(self,name = name)
        self._widget.lockInfo()

        
        self.setSizeHint(self._widget.sizeHint())


    def getWidget(self):
        return self._widget

    def setName(self,name):
        self._widget.setName(name)
        self.setText(self.getName()) 
    def getNameInput(self):
        return self._widget.getNameInput()
    def getName(self):
        return self._widget.getName()


    def confirmInput(self):
        self._parent.groupDict.pop(self.getName())
        self.setName(self._widget.getNameInput())
        self._parent.groupDict[self.getName()] = self
        self._widget.lockInfo()

    def giveUpInput(self):
        self.setName(self.getName())
        self._widget.lockInfo()

    def delSelfFromList(self):
        self._parent.removeGroupItem(self)

    @pyqtSlot()
    def addNewUser(self):
        (ok,uit,git) = self._parent.addUser(group = self.getName())
        self._parent.setCurrentItem(uit)
        
        uit.getWidget().editInfo()

    def addUser(self,uit):
        self.usrList.append(uit)
        self._widget.expended.connect(uit.setHidden)
        self.setName(self.getName())

    def delUser(self, uit):
        self.usrList.pop(self.usrList.index(uit))
        self.setName(self.getName())

    def moveUserIn(self,uit):
        self._parent.moveUser(uit,self.getName())
    def setSelected(self):
        self._parent.setItemSelected(self,True)

    





class UserList(QListWidget):
    
    groupDict = {}
    def __init__(self,parent = None):
        super(UserList, self).__init__(parent)
        self.currentItemChanged.connect(self.chooseItemChanged)
        self.setAcceptDrops(True)

    def addGroup(self, name = DEFAULT_GROUP): 
        
        name = str(name)
        groupNames = self.groupDict.keys()
        
        if name not in groupNames:
            git = GroupListItem(self,name)
            index = self.count() + 1
            self.insertItem(index,git)
            self.groupDict[name] = git 
            return (True, git) 
        else:
            git = self.groupDict[name]
            return (False, git)

    _currentId = 1 
    def addUser(self, name = DEFAULT_USER, head = DEFAULT_HEAD,note = DEFAULT_NOTE,group = DEFAULT_GROUP,uId = None):
        
        (isExist, git) = self.addGroup(group)
        index = self.indexFromItem(git).row()

        if uId:
            uId = int(uId)
            uit = UserListItem(self,uId,name,head,note,group)
        else:
            uit = UserListItem(self,self._currentId,name,head,note,group)
            self._currentId += 1 

        self.insertItem(index+1,uit)
        git.addUser(uit)
        
        return (True,uit,git)

    def removeUserItem(self,uit):
        
        git = self.groupDict[uit.getGroup()]
        git.delUser(uit)
        self.takeItem(self,uit)
        del uit

    def removeGroupItem(self,git):
        
        gName = git.getName()
        if gName == DEFAULT_GROUP:
            
            return False
        for uit in git.usrList:
            self.addUser(name = uit.getName(),head = uit.getHead(),
                note = uit.getNote(),uId = uit.getId())
            self.takeItem(self,uit)
            
            del uit

        self.takeItem(self,git)
        self.groupDict.pop(git.getName())
        del git

    def moveUser(self, uit, group = DEFAULT_GROUP):
        
        self.addUser(name = uit.getName(),head = uit.getHead(),
            note = uit.getNote(),uId = uit.getId(),group = group)
        self.removeUserItem(uit)

    @pyqtSlot(QListWidgetItem,QListWidgetItem)
    def chooseItemChanged(self,curit,preit):
        if preit:
            preit.giveUpInput() 
    _gIndex = 1 
    @pyqtSlot(bool)
    def slotAddGroup(self,b):
        group = u'%s_%d'%(DEFAULT_GROUP,self._gIndex)
        self._gIndex += 1
        (ok,git) = self.addGroup(group)
        self.setCurrentItem(git)
        
        git.getWidget().editInfo()
    @pyqtSlot(bool)
    def slotAddUser(self,b):
        (ok,uit,git) = self.addUser()
        self.setCurrentItem(uit)
        
        uit.getWidget().editInfo()

    
    def insertItem(self,index,it):
        super(UserList, self).insertItem(index, it)
        if isinstance(it,GroupListItem) or isinstance(it,UserListItem):
            self.setItemWidget(it,it.getWidget())

    def takeItem(self,index,it):
        
        if isinstance(it,int):
            return super(UserList, self).takeItem(index)
        else: 
            index = self.indexFromItem(it).row()
            return super(UserList, self).takeItem(index)

    def contextMenuEvent(self,e): 
        
        adgrp = QAction(QIcon('../icons/group.png'), u'增加组', self)
        adgrp.triggered.connect(self.slotAddGroup)

        adusr = QAction(QIcon('../icons/user.png'), u'增加用户', self)
        adusr.triggered.connect(self.slotAddUser)

        menu = QMenu()
        menu.addAction(adgrp)
        menu.addAction(adusr)
        menu.exec_(QCursor.pos())

        e.accept() 

    def dragEnterEvent(self, e):
        
        e.accept()
    def dragMoveEvent(self,e): 
        
        e.accept()
    def dropEvent(self, e):
        
        e.accept()


if __name__=='__main__':
    app = QApplication(sys.argv)
    ul=UserList()
    ul.setMinimumSize(200,500)

    ul.addUser('hello')
    ul.addUser('world')
    ul.addGroup('group')
    ul.addUser('Default',group = 'group')
    ul.addGroup(u'中文')
    ul.addUser(u'默认',group = u'中文')

    ul.show()
    sys.exit(app.exec_())
