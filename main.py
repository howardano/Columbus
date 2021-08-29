from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # Используем SQLite, потому что, возмонжо, у проверяющего нет драйверов
        # Если есть возможность использовать PostgreSql - можно использовать. Внизу есть заготовки
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        #        db.setDatabaseName(" ")
        #        db.setHostName(" ")
        #        db.setPort( )
        #        db.setUserName(" ")
        #        db.setPassword(" ")
        if (self.db.open()):
            mes = QtWidgets.QMessageBox()
            mes.setText("Connected")
            mes.show()
            mes.exec_()
        else:
            mes = QtWidgets.QMessageBox()
            mes.setText("Can not connect")
            mes.show()
            mes.exec_()

        myQ = QSqlQuery(self.db)
        myQ.exec("CREATE TABLE products13 (prodid SERIAL PRIMARY KEY, name VARCHAR(20) NOT NULL, price int NOT NULL)")
        myQ.exec("CREATE TABLE sales13 (prodid SERIAL REFERENCES products13(prodid) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL, year int NOT NULL, month int NOT NULL, sum int DEFAULT 0)")
        myQ.exec("CREATE TABLE plans13 (prodid SERIAL REFERENCES products13(prodid) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL, year int NOT NULL, month int NOT NULL, sum int DEFAULT 0)")
        myQ.exec("INSERT INTO products13 VALUES (1, 'Tefal', 1000), (2, 'Bosch', 5000), (3, 'Kaercher', 10000)")
        myQ.exec("INSERT INTO plans13 VALUES (1, 2021, 8, 4000), (2, 2021, 9, 10000), (3, 2021, 8, 10000)")

        self.setWindowTitle("Interface")
        self.setGeometry(300, 250, 1205, 609)
        self.setFixedSize(1205, 609)

        self.table = QtWidgets.QTableView(self)
        self.table.setFixedSize(1205, 300)

        self.button_pr = QtWidgets.QPushButton(self)
        self.button_pr.setGeometry(1, 302, 400, 50)
        self.button_pr.setText("Table Products")
        self.button_pr.clicked.connect(self.show_pr)

        self.button_sl = QtWidgets.QPushButton(self)
        self.button_sl.setGeometry(403, 302, 400, 50)
        self.button_sl.setText("Table Sales")
        self.button_sl.clicked.connect(self.show_sl)

        self.button_pl = QtWidgets.QPushButton(self)
        self.button_pl.setGeometry(805, 302, 400, 50)
        self.button_pl.setText("Table Plans")
        self.button_pl.clicked.connect(self.show_pl)

        self.spin_num_of_prod = QtWidgets.QSpinBox(self)
        self.spin_num_of_prod.setGeometry(1, 355, 600, 50)

        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.setGeometry(605, 355, 600, 50)
        myQ.exec("SELECT name FROM products13")
        while(myQ.next()):
            self.combo_box.addItem(myQ.record().value(0))

        self.button_ins = QtWidgets.QPushButton(self)
        self.button_ins.setGeometry(1, 410, 1200, 50)
        self.button_ins.setText("Sell")
        self.button_ins.clicked.connect(self.ins)

        mdl = QSqlQueryModel()
        myQ.exec("SELECT * FROM products13")
        mdl.setQuery(myQ)
        self.table.setModel(mdl)
        self.table.resizeColumnsToContents();
        self.table.show()

    def show_pr(self):
        myQ = QSqlQuery(self.db)
        myQ.exec("SELECT * FROM products13")
        mdl = QSqlQueryModel()
        mdl.setQuery(myQ)
        self.table.setModel(mdl)
        self.table.resizeColumnsToContents();
        self.table.show()

    def show_sl(self):
        myQ = QSqlQuery(self.db)
        myQ.exec("SELECT * FROM sales13")
        mdl = QSqlQueryModel()
        mdl.setQuery(myQ)
        self.table.setModel(mdl)
        self.table.resizeColumnsToContents();
        self.table.show()

    def show_pl(self):
        myQ = QSqlQuery(self.db)
        myQ.exec("SELECT * FROM plans13")
        mdl = QSqlQueryModel()
        mdl.setQuery(myQ)
        self.table.setModel(mdl)
        self.table.resizeColumnsToContents();
        self.table.show()

    def ins(self):
        myQ = QSqlQuery(self.db)
        name = self.combo_box.currentText()
        ex = "SELECT prodid FROM products13 WHERE name = '%s'"%(name)
        myQ.exec(ex)
        myQ.next()
        ind = myQ.record().value(0)
        ex = "SELECT price FROM products13 WHERE name = '%s'" %(name)
        myQ.exec(ex)
        myQ.next()
        price = myQ.record().value(0)
        total = self.spin_num_of_prod.value() * price
        myQ.exec("SELECT strftime('%Y',date('now'))")
        myQ.next()
        year = myQ.record().value(0)
        myQ.exec("SELECT strftime('%m',date('now'))")
        myQ.next()
        month = myQ.record().value(0)
        ex = "INSERT INTO sales13 VALUES (%d, %s, %s, %d)"%(ind, year, month, total)
        print(ex)
        myQ.exec(ex)
        self.show_sl()


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if (__name__ == "__main__"):
    application()