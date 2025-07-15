# Modules
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPlainTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import Qt
from collapsible_box import QCollapsibleBox
from search_cdx import getStartAndEndCursors
import json
import csv
from cdx_reader import CDXFileReader, CDXURLReader
import webbrowser
# webbrowser.open('http://stackoverflow.com')

# Class
class Home(QWidget):
    # Constructor
    def __init__(self):
        super().__init__()
        self.cdx_path = ""
        self.initUI()
        self.settings()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.searchCdx()

    # App Object and Design
    def initUI(self):
        
        master = QVBoxLayout()
        master.addLayout(self.makeMenu())

        self.info_text = QLabel()
        master.addWidget(self.info_text)

        self.search_results_text = QPlainTextEdit()
        self.search_results_text.setReadOnly(True)
        self.search_results_text.setWordWrapMode(0)
        self.search_results_text.setLineWrapMode(0)
        self.search_results_text.setFont(QFont('Consolas', 10))

        master.addWidget(self.search_results_text)

        self.search_results_table = QTableWidget()
        self.search_results_table.setFont(QFont('Consolas', 10))
        self.search_results_table.setColumnCount(11)
        self.search_results_table.setHorizontalHeaderLabels(["surt", "timestamp", "url", "mime", "status", "digest", "length", "offset", "filename", "collection", "linkToArchive"])
        self.search_results_table.hide()

        master.addWidget(self.search_results_table)

        self.setLayout(master)

    def makeMenu(self):
        menu = QVBoxLayout()
        
        menu_row1 = QHBoxLayout()

        where_cdx_label = QLabel("Get file from:")
        where_cdx_label.setMaximumWidth(150)
        self.where_cdx_input = QComboBox()
        self.where_cdx_input.addItem('Local file')
        self.where_cdx_input.addItem('Internet')
        self.where_cdx_input.setMaximumWidth(150)
        self.where_cdx_input.activated.connect(self.onWhereCdxChange)

        self.open_cdx = QPushButton("Open CDX")
        self.open_cdx.setMaximumWidth(100)
        self.open_cdx.clicked.connect(self.openFileDialog)

        self.cdx_path_label = QLabel()
        self.updateCdxPathLabel()
        
        self.cdx_url_label = QLabel("CDX Url:")
        self.cdx_url_input = QLineEdit()
        
        self.cdx_url_label.hide()
        self.cdx_url_input.hide()

        menu_row1.addWidget(where_cdx_label)
        menu_row1.addWidget(self.where_cdx_input)
        menu_row1.addWidget(self.open_cdx)
        menu_row1.addWidget(self.cdx_path_label)
        menu_row1.addWidget(self.cdx_url_label)
        menu_row1.addWidget(self.cdx_url_input)

        menu.addLayout(menu_row1)

        menu_row2 = QHBoxLayout()
        url_label = QLabel("Url:")
        self.url_input = QLineEdit()

        match_type_label = QLabel("Match type:")
        self.match_type_input = QComboBox()
        self.match_type_input.addItem('exact')
        self.match_type_input.addItem('prefix')
        self.match_type_input.addItem('domain')

        menu_row2.addWidget(url_label)        
        menu_row2.addWidget(self.url_input)
        menu_row2.addWidget(match_type_label) 
        menu_row2.addWidget(self.match_type_input)       

        menu.addLayout(menu_row2)

        menu_row3 = QHBoxLayout()
        from_label = QLabel("From:")
        self.from_input = QLineEdit()

        menu_row3.addWidget(from_label)        
        menu_row3.addWidget(self.from_input)

        to_label = QLabel("To:")
        self.to_input = QLineEdit()

        menu_row3.addWidget(to_label)        
        menu_row3.addWidget(self.to_input)

        menu.addLayout(menu_row3)

        menu_row5 = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.setMaximumWidth(100)
        search_button.clicked.connect(self.searchCdx)
        menu_row5.addWidget(search_button)

        menu_row5.addWidget(QLabel("Search type:"))
        self.search_type_input = QComboBox()
        self.search_type_input.addItem("First 100 results")
        self.search_type_input.addItem("All results")
        menu_row5.addWidget(self.search_type_input)

        menu_row5.addWidget(QLabel("Number of Results: "))
        self.num_results_label = QLabel("")
        menu_row5.addWidget(self.num_results_label)

        menu_row5.addStretch()

        menu_row5.addWidget(QLabel("Output type:"))
        self.output_type_input = QComboBox()
        self.output_type_input.addItem("Text")
        self.output_type_input.addItem("Table")
        self.output_type_input.activated.connect(self.changeOutputType)
        menu_row5.addWidget(self.output_type_input)

        export_to_csv = QPushButton("Export to CSV")
        export_to_csv.setMaximumWidth(200)
        export_to_csv.clicked.connect(self.exportToCSV)
        menu_row5.addWidget(export_to_csv)
        
        menu.addLayout(menu_row5)

        return menu

    def exportToCSV(self):
        if(len(self.search_results_text.toPlainText()) == 0):
            self.info_text.setText("Nothing to export")
            return
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Export to CSV")
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.selectFile("cdx_search.csv")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            csv_path = selected_files[0]

            with open(csv_path,"w",newline='') as f:
                f.write("surt;timestamp;url;mime;status;digest;length;offset;filename;collection\r\n")
                for line in self.search_results_text.toPlainText().split("\n"):
                    if(len(line) > 0):
                        csv_line = ";".join(list(map(lambda cell: '"' + '""'.join(cell.split('"')) + '"',self.cdxLineToArray(line)))) + "\r\n"
                        f.write(csv_line)

    def changeOutputType(self):
        if(self.output_type_input.currentText() == "Table"):
            self.search_results_text.hide()
            self.search_results_table.show()

        else:
            self.search_results_text.show()
            self.search_results_table.hide()

    def openFileDialog(self):
      file_dialog = QFileDialog(self)
      file_dialog.setWindowTitle("Open File")
      file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
      file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

      if file_dialog.exec():
         selected_files = file_dialog.selectedFiles()
         self.cdx_path = selected_files[0]
         self.updateCdxPathLabel()

    def onWhereCdxChange(self, value):
        if(value == 0):
            self.open_cdx.show()
            self.cdx_path_label.show()
            self.cdx_url_label.hide()
            self.cdx_url_input.hide()
        else:
            self.open_cdx.hide()
            self.cdx_path_label.hide()
            self.cdx_url_label.show()
            self.cdx_url_input.show()

    def updateCdxPathLabel(self):
        if not self.checkValidCdxPath():
            self.cdx_path_label.setText("None selected")
        else:
            self.cdx_path_label.setText(self.cdx_path)

    def checkValidCdxPath(self):
        where = self.where_cdx_input.currentText()
        if where == 'Local file':
            if not self.cdx_path or not isinstance(self.cdx_path, str):
                return False
            else:
                return True
        else: 
            if not self.cdx_url_input.text():
                return False
            else:
                return True

    def searchCdx(self):
        if not self.checkValidCdxPath() or not self.url_input.text():
            self.info_text.setText("Please input a CDX file and a URL")
        else:
            self.info_text.setText("Searching...")
            QtWidgets.qApp.processEvents()
            where = self.where_cdx_input.currentText()

            if where == 'Local file':
                f = CDXFileReader(self.cdx_path)
            else:
                f = CDXURLReader(self.cdx_url_input.text())

            surt = self.urlToSurt(self.url_input.text())
            mode = self.match_type_input.currentText()
            start,end = getStartAndEndCursors(f,surt,mode)

            f.seek(start)
            text = ""
            num_results = 0
            search_type = self.search_type_input.currentText()
            num_tries = 0

            self.search_results_table.clearContents()
            while f.tell() < end and (num_results < 100 or search_type != "First 100 results"):
                line = f.readLine()
                num_tries += 1
                if len(line) > 0 and self.checkFilters(line):
                    text = text + line
                    self.search_results_table.insertRow(num_results)
                    self.cdxLineToTableRow(line,num_results)
                    num_results += 1
                if (num_tries % 1000 == 0):
                    self.info_text.setText("Searching... \n"+str(num_results)+" found so far...")
                    QtWidgets.qApp.processEvents()

            self.search_results_text.setPlainText(text)
            if(search_type == "All results" or num_results < 100):
                self.num_results_label.setText(str(num_results))
            else:
                estimated_num_results = (end-start) * num_results // (f.tell() - start)
                self.num_results_label.setText(str(estimated_num_results) + " (estimated)")

            self.info_text.setText("")
            self.search_results_table.setRowCount(num_results)
            
            f.close()
    
    def cdxLineToArray(self,line):
        s = line.split(" ",2)
        surt = s[0]
        timestamp = s[1]
        metadata = json.loads(s[2])
        array = []
        keys = ["url", "mime", "status", "digest", "length", "offset", "filename", "collection"]

        array.append(surt)
        array.append(timestamp)

        for key in keys:
            try:
                array.append(metadata[key])
            except:
                array.append('')
        return array

    def cdxLineToTableRow(self,line:str,row:int):
        arr = self.cdxLineToArray(line)
        for col in range(10):
            self.search_results_table.setItem(row,col, QTableWidgetItem(arr[col]))
        
        timestamp = arr[1]
        url = arr[2]

        def openLink(self):
            webbrowser.open('http://arquivo.pt/wayback/{0}/{1}'.format(timestamp,url))

        linkToArchive_button = QPushButton(self.search_results_table)
        linkToArchive_button.setText('->')
        linkToArchive_button.clicked.connect(openLink)
        self.search_results_table.setCellWidget(row, 10, linkToArchive_button)

    def urlToSurt(self,url:str):
        # From Pywb docs:
        #   SURT-formatted, canonicalized URL:
        #     - Does not differentiate between HTTP and HTTPS
        #     - Is not case-sensitive
        #     - Treats www. and www*. subdomains the same as no subdomain at all
        if(url.startswith("http://")):
            url = url[7:]
        elif url.startswith("https://"):
            url = url[8:]
        if(url.startswith("www.")):
            url = url[4:]
        elif(url.startswith("www") and len(url.split('.',1)[0]) == 4):
            url = url[5:]
        split_url = url.split("/",1)

        surt_end = ""
        if(len(split_url) == 2):
            surt_end = split_url[1]
            
        surt_start = ",".join(reversed(split_url[0].split("."))) + ')'
        return (surt_start + '/' + surt_end).lower()
    
    def checkFilters(self,line:str):
        s = line.split(" ",2)
        surt = s[0]
        timestamp = s[1]
        json = s[2]

        # From
        if len(self.from_input.text()) > 0:
            from_s = self.from_input.text()
            try:
                if(len(from_s) < len(timestamp)):
                    from_i = int(from_s)
                    ts_i = int(timestamp[0:len(from_s)])
                else:
                    from_i = int(from_s[0:len(timestamp)])
                    ts_i = int(timestamp)
                if (ts_i < from_i):
                    return False
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("\"from\" field invalid: '"+from_s+"' is not a valid timestamp")
                msg.setWindowTitle("Bad filter")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                self.from_input.setText("")
        # To
        if len(self.to_input.text()) > 0:
            to_s = self.to_input.text()
            try:
                if(len(to_s) < len(timestamp)):
                    to_i = int(to_s)
                    ts_i = int(timestamp[0:len(to_s)])
                else:
                    to_i = int(to_s[0:len(timestamp)])
                    ts_i = int(timestamp)
                if (ts_i > to_i):
                    return False
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("\"to\" field invalid: '"+to_s+"' is not a valid timestamp")
                msg.setWindowTitle("Bad filter")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                self.to_input.setText("")
        return True
            
    # App Settings
    def settings(self):
        self.setWindowTitle("CDX Explorer - Arquivo.pt")
        self.setWindowIcon(QIcon('icon.ico'))

# Main Run
if __name__ in "__main__": 
    app = QApplication([])
    app.setStyle('Windows')
    main = Home()
    main.show()
    app.exec()
