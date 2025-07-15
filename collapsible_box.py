from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,QFrame 

class QCollapsibleBox(QWidget):
    # Constructor
    def __init__(self, collapsible_layout, start_collapsed):
        super().__init__()
        if start_collapsed:
            self.is_collapsed = True
        else:
            self.is_collapsed = False
        self.collapsible_l = collapsible_layout
        self.button_label_collapsed = ">"
        self.button_label_expanded = "v"
        self.label = ""
        self.initUI()
        
    def initUI(self):
        master_layout = QVBoxLayout()
        self.visible_row = QHBoxLayout()
        self.collapsible = QFrame()
        self.collapsible_layout = self.collapsible_l
        self.collapsible.setLayout(self.collapsible_layout)

        self.collapse_button = QPushButton(self.getButtonLabel())
        self.collapse_button.clicked.connect(self.toggleCollapse)
        self.collapse_button.setFixedWidth(30)
        self.visible_label = QLabel(self.label)
        self.visible_row.addWidget(self.collapse_button)
        self.visible_row.addWidget(self.visible_label)

        master_layout.addLayout(self.visible_row)
        master_layout.addWidget(self.collapsible)
        
        self.setLayout(master_layout)
        
        if self.is_collapsed:
            self.collapsible.hide()

    def toggleCollapse(self):
        if(self.is_collapsed):
            self.collapsible.show()
            self.is_collapsed = False
        else:
            self.collapsible.hide()
            self.is_collapsed = True
        self.collapse_button.setText(self.getButtonLabel())

    def getButtonLabel(self):
        if(self.is_collapsed):
            return self.button_label_collapsed
        else:
            return self.button_label_expanded

    def setLabel(self,label):
        self.label = label
        self.visible_label.setText(self.label)

    def getLabel(self):
        return self.label
