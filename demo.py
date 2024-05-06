from PyQt6.QtWidgets import QMainWindow,QWidget,QApplication,QHBoxLayout,QTableWidget,QTableWidgetItem,QDockWidget,QFormLayout,QLineEdit,QSpinBox,QPushButton,QToolBar,QMessageBox,QMenu
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QAction, QContextMenuEvent,QIcon
import sys

class Window(QMainWindow):
  def __init__(self):
    super().__init__()
    self.initUI()  
  
  def initUI(self):
    self.setGeometry(0,0,700,500)

    self.people = [
      {"First Name":"John", "Last Name":"Doe", "Age":21},
      {"First Name":"Rob", "Last Name":"Ford", "Age":31},
      {"First Name":"Bob", "Last Name":"Tyson", "Age":41},
    ]

    self.table_widget = QTableWidget()
    self.table_widget.setRowCount(len(self.people))
    self.table_widget.setColumnCount(3)
    self.table_widget.setHorizontalHeaderLabels(self.people[0].keys())

    for person in self.people:
      for column,key in enumerate(person.keys()):
        item = QTableWidgetItem(str(person[key]))
        self.table_widget.setItem(self.people.index(person),column,item)
    
    dock = QDockWidget()
    dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
    self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)


    form = QWidget()
    layout = QFormLayout(form)
    form.setLayout(layout)

    self.first_name = QLineEdit(form)
    self.last_name = QLineEdit(form)
    self.age = QSpinBox(form,minimum=18,maximum=60)

    layout.addRow('First name',self.first_name)
    layout.addRow('Last name',self.last_name)
    layout.addRow('Age',self.age)

    add_button = QPushButton("Add")
    add_button.clicked.connect(self.add)
    layout.addRow(add_button)

    dock.setWidget(form)

    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16,16))
    self.addToolBar(toolbar)

    self.delete_action = QAction(QIcon("icons/delete.png"),"Delete",self)
    self.delete_action.triggered.connect(self.delete)
    toolbar.addAction(self.delete_action)

    self.add_above = QAction("Add row above cell", self)
    self.add_above.triggered.connect(lambda:self.add_row("above"))
    self.add_below = QAction("Add row below cell", self)
    self.add_below.triggered.connect(lambda:self.add_row("below"))

    self.copy_text = QAction("Copy", self)
    self.copy_text.triggered.connect(self.copy)
    self.paste_text = QAction("Paste", self)
    self.paste_text.triggered.connect(self.paste)

    self.setCentralWidget(self.table_widget)
  
  def add(self):
    row = self.table_widget.rowCount()
    self.table_widget.insertRow(row)
    new_person = {"First Name":self.first_name.text(), "Last Name":self.last_name.text(), "Age":self.age.text()}

    for column,key in enumerate(new_person.keys()):
        item = QTableWidgetItem(str(new_person[key]).strip())
        self.table_widget.setItem(row,column,item)

  def delete(self):
    current_row = self.table_widget.currentRow()
    if current_row < 0:
        return QMessageBox.warning(self,"No row selected")
    res = QMessageBox.question(self,"Delete Row","Do you want to delete the row?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if res == QMessageBox.StandardButton.Yes:
      self.table_widget.removeRow(current_row)
    
  def contextMenuEvent(self, event):
    context_menu = QMenu(self)
    context_menu.addAction(self.delete_action)
    context_menu.addAction(self.add_above)
    context_menu.addAction(self.add_below)
    context_menu.addAction(self.copy_text)
    context_menu.addAction(self.paste_text)
    context_menu.exec(event.globalPos())
  
  def add_row(self, position):
    current_row = self.table_widget.currentRow()
    if current_row < 0:
      return
    if position == "above":
      self.table_widget.insertRow(current_row)
    elif position == "below":
      self.table_widget.insertRow(current_row+1)
  
  def copy(self):
    text = self.table_widget.currentItem().text()  
    self.item_text = text

  def paste(self):
    if self.item_text != None:
      current_row = self.table_widget.currentRow()
      current_column = self.table_widget.currentColumn()
      if current_row < 0 | current_column < 0:
        return
      self.table_widget.setItem(current_row,current_column,QTableWidgetItem(self.item_text))


app = QApplication(sys.argv)
app.setStyle("Fusion")
window = Window()
window.show()
app.exec()