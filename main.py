import sys
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5 import QtWidgets
from ui import Ui_MainWindow
import database


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.title = str(self.ui.titleValue.text())
        self.author = str(self.ui.authorValue.text())
        self.releaseDate = str(self.ui.dateValue.text())
        self.releasePlace = str(self.ui.placeValue.text())
        self.pages = str(self.ui.pagesValue.text())
        self.ISBN = str(self.ui.ISBNValue.text())

        self.centerScreen()
        self.ui.tableWidget.itemClicked.connect(self.whenClicked)
        self.ui.quitBtn.clicked.connect(self.closeApplication)
        self.ui.clearBtn.clicked.connect(self.clearData)
        self.ui.addNewBtn.clicked.connect(self.addData)
        self.ui.displayBtn.clicked.connect(self.displayData)
        self.ui.searchBtn.clicked.connect(self.searchData)
        self.ui.deleteBtn.clicked.connect(self.deleteData)
        self.ui.updateBtn.clicked.connect(self.updateData)

    def centerScreen(self):
        """
        shows main window in the center of the screen

        """
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def closeApplication(self):
        """
        close main window

        """
        response = QMessageBox.question(self, "Message Box", "Do you want to quit?",
                                        QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if response == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def clearData(self):
        """
        clear all line inputs

        """
        self.ui.titleValue.clear()
        self.ui.authorValue.clear()
        self.ui.dateValue.clear()
        self.ui.placeValue.clear()
        self.ui.pagesValue.clear()
        self.ui.ISBNValue.clear()

    def addData(self):
        """
        add the text in the entries to the database and table widget

        """
        values = [self.ui.titleValue.text(), self.ui.authorValue.text(), self.ui.dateValue.text(),
                  self.ui.placeValue.text(), self.ui.pagesValue.text(), self.ui.ISBNValue.text()]

        if len(self.ui.titleValue.text()) != 0:
            database.addBookRec(self.ui.titleValue.text(), self.ui.authorValue.text(), self.ui.dateValue.text(),
                                self.ui.placeValue.text(), self.ui.pagesValue.text(), self.ui.ISBNValue.text())
            self.ui.tableWidget.clear()
            self.ui.tableWidget.insertRow(0)

            for column, value in enumerate(values, 1):
                self.ui.tableWidget.setItem(0, column, QtWidgets.QTableWidgetItem(value))

            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["id", "Title", "Author", "Release Date", "Release Place", "Pages", "ISBN"])
        else:
            msg = QMessageBox.information(self, "Message Box", "Fill in the missing values", QMessageBox.Ok)

    def displayData(self):
        """
        display the data from database to table widget

        """
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        for row, rowData in enumerate(database.viewData()):
            self.ui.tableWidget.insertRow(row)
            for column, data in enumerate(rowData):
                self.ui.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["id", "Title", "Author", "Release Date", "Release Place", "Pages", "ISBN"])

    def whenClicked(self):
        """
        display data in line edits when item is clicked

        """
        row = self.ui.tableWidget.currentRow()
        columnCount = self.ui.tableWidget.columnCount()
        lineEdit = [self.ui.titleValue, self.ui.authorValue, self.ui.dateValue,
                    self.ui.placeValue, self.ui.pagesValue, self.ui.ISBNValue]

        for i in range(1, columnCount, 1):
            cell = self.ui.tableWidget.item(row, i).text()
            lineEdit[i - 1].setText(str(cell))

    def deleteData(self):
        """
        delete selected item from database and table widget

        """
        row = self.ui.tableWidget.currentItem().row()
        columnCount = self.ui.tableWidget.columnCount()

        for i in range(0, columnCount, 1):
            header = self.ui.tableWidget.horizontalHeaderItem(i).text()
            if header == "id":
                cell = self.ui.tableWidget.item(row, i).text()
                database.deleteRec(cell)

        self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow())
        self.clearData()

    def searchData(self):
        """
        searches the database and displays the item

        """
        self.ui.tableWidget.clear()

        for row, rowData in enumerate(
                database.searchRec(self.ui.titleValue.text(), self.ui.authorValue.text(), self.ui.dateValue.text(),
                                   self.ui.placeValue.text(), self.ui.pagesValue.text(), self.ui.ISBNValue.text())):
            self.ui.tableWidget.insertRow(row)
            for column, data in enumerate(rowData):
                self.ui.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))

        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["id", "Title", "Author", "Release Date", "Release Place", "Pages", "ISBN"])

    def updateData(self):
        """
        updates and displays selected item

        """
        row = self.ui.tableWidget.currentItem().row()
        columnCount = self.ui.tableWidget.columnCount()
        if len(self.ui.titleValue.text()) != 0:
            for i in range(0, columnCount, 1):
                header = self.ui.tableWidget.horizontalHeaderItem(i).text()
                if header == "id":
                    cell = self.ui.tableWidget.item(row, i).text()
                    database.updateRec(self.ui.titleValue.text(), self.ui.authorValue.text(), self.ui.dateValue.text(),
                               self.ui.placeValue.text(), self.ui.pagesValue.text(), self.ui.ISBNValue.text(), cell)
            self.displayData()

        else:
            msg = QMessageBox.information(self, "Message Box", "Fill in the missing values", QMessageBox.Ok)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())
