import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainFunc(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.db = sqlite3.connect('coffee.sqlite')
        self.sql = self.db.cursor()

        self.result.hide()

        self.pushButton.clicked.connect(self.func_search)

    def func_search(self):
        try:
            coffee_data = self.search_db()
            self.result.setText('УСПЕШНО')
            self.result.setStyleSheet("background: #64BE74;\n"
                                      "border-radius: 10px;\n"
                                      "color: white;\n"
                                      "padding: 2px 5px;\n"
                                      "font-weight: 600;")
            self.result.show()
        except ValueError as f:
            coffee_data = ['', '', '', '', '', '', '']
            self.result.setText(str(f).upper())
            self.result.setStyleSheet("background: #F65C5A;\n"
                                      "border-radius: 10px;\n"
                                      "color: white;\n"
                                      "padding: 2px 5px;\n"
                                      "font-weight: 600;")
            self.result.show()
        except TypeError:
            coffee_data = ['', '', '', '', '', '', '']
            self.result.hide()

        self.textBrowser.setText(coffee_data[0])
        self.textBrowser_2.setText(coffee_data[1])
        self.textBrowser_3.setText(coffee_data[2])
        self.textBrowser_4.setText(coffee_data[3])
        self.textBrowser_5.setText(coffee_data[4])
        self.textBrowser_6.setText(coffee_data[5])
        self.textBrowser_7.setText(coffee_data[6])

    def search_db(self):
        coffee_ID = self.lineEdit.text()

        if not coffee_ID:
            raise TypeError()

        if not coffee_ID.isdigit():
            raise ValueError('ID должен быть целым числом')

        coffee = self.sql.execute(f"""SELECT * FROM coffees WHERE ID = {int(coffee_ID)}""").fetchone()

        if coffee is None:
            raise ValueError('Такого кофе нет')

        name = self.sql.execute(f"""SELECT title FROM coffees_name WHERE ID = {coffee[1]}""").fetchone()[0]
        roast = self.sql.execute(f"""SELECT title FROM coffees_roast WHERE ID = {coffee[2]}""").fetchone()[0]
        types = coffee[3]
        description = self.sql.execute(f"""SELECT title FROM coffees_description 
        WHERE ID = {coffee[4]}""").fetchone()[0]
        price = coffee[5]
        volume = coffee[6]

        return [str(coffee_ID), name, roast, types, description, str(price), str(volume)]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFunc()
    ex.show()
    sys.exit(app.exec_())