import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont
import sys

########################################

class Client(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.body = QtWidgets.QTextEdit()
        self.labelPassword = QtWidgets.QLabel("G-mail Password: ")
        self.labelTo = QtWidgets.QLabel("To: ")
        self.labelFrom = QtWidgets.QLabel("From: ")
        self.labelSubject = QtWidgets.QLabel("Subject: ")
        self.labelBody = QtWidgets.QLabel("Body Text: ")
        self.lineTo = QtWidgets.QLineEdit("Their g-mail")
        self.lineFrom = QtWidgets.QLineEdit("Your g-mail")
        self.lineSubject = QtWidgets.QLineEdit("Subject goes here...")
        self.linePassword = QtWidgets.QLineEdit()
        self.linePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.send = QtWidgets.QPushButton("Send")
        self.welcomeText = QtWidgets.QLabel("E-mail Client for G-mail")

        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.welcomeText)
        v_box.addWidget(self.labelPassword)
        v_box.addWidget(self.linePassword)
        v_box.addWidget(self.labelTo)
        v_box.addWidget(self.lineTo)
        v_box.addWidget(self.labelFrom)
        v_box.addWidget(self.lineFrom)
        v_box.addWidget(self.labelSubject)
        v_box.addWidget(self.lineSubject)
        v_box.addWidget(self.labelBody)
        v_box.addWidget(self.body)
        v_box.addWidget(self.send)

        h_box = QtWidgets.QHBoxLayout()

        h_box.addLayout(v_box)

        self.setLayout(h_box)

        font = QFont()
        font.setPointSize(10)
        self.body.setFont(font)

        font_2 = QFont()
        font_2.setPointSize(20)
        self.welcomeText.setFont(font_2)

        self.body.setText("Your main text goes here...")

class WarningPage(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.warningLabel = QtWidgets.QLabel()
        self.button_i_accept = QtWidgets.QPushButton("I Accept, Proceed.")

        self.warningLabel.setText("""Warning! This E-mail client only supports g-mail, \nif you enter another mail (@protonmail, @mail2tor etc.) it is not going to work! \nAlso, please activate the setting 'Access Unsafe Applications' of your account before processing. \n\nNote: And also, you have to disable 2FA to activate the setting 'Access Unsafe Applications', sorry for bothering.""")

        font_3 = QFont()
        font_3.setPointSize(15)
        self.warningLabel.setFont(font_3)

        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.warningLabel)
        v_box.addWidget(self.button_i_accept)

        h_box = QtWidgets.QHBoxLayout()

        h_box.addLayout(v_box)

        self.setLayout(h_box)

class Window(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.client = Client()
        self.warning = WarningPage()
        self.setCentralWidget(self.warning)
        self.setGeometry(600, 300, 750, 400)

        self.warning.button_i_accept.clicked.connect(self.proceed)
        self.client.send.clicked.connect(self.sendMail)

        self.setWindowTitle("Mail Client")
        self.setWindowIcon(QtGui.QIcon("Mail-icon.png"))

        self.show()

    def proceed(self):

        self.setCentralWidget(self.client)

    def sendMail(self):

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()

        server.starttls()

        server.login(self.client.lineFrom.text(), self.client.linePassword.text())

        msg = MIMEMultipart()

        msg["To"] = self.client.lineTo.text()
        msg["From"] = self.client.lineFrom.text()
        msg["Subject"] = self.client.lineSubject.text()

        msg.attach(MIMEText(self.client.body.toPlainText(), "plain"))

        mailText = msg.as_string()
        server.sendmail(self.client.lineFrom.text(), self.client.lineTo.text(), mailText)

        server.quit()

app = QtWidgets.QApplication(sys.argv)

window = Window()

sys.exit(app.exec_())
