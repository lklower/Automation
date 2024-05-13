from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
import sys


# noinspection PyArgumentList
class WindowForm(QMainWindow):

    def __init__(self):
        super(WindowForm, self).__init__()

        self.stacked_contents = None

        self.initGeometry()
        self.setWindowTitle('PyQt5 GUI Tutorial')
        self.setStyleSheet("WindowForm{background-color: #0f0f0f;}")
        self.contant_widget: QWidget
        self.setObjectName('window_form')

        menu_widget = QWidget()
        menu_widget.setStyleSheet("QWidget{border-right: 1px solid #555555; background-color: qlineargradient(x1:1, y1:1, x2:1, y2:0, stop:0 #313131, stop:1 #111111);}"
                                  "QPushButton{text-align: left; color: #656565;font-size: 10pt; font-weight: normal; border-radius: 5px; border: 1px solid #454545; padding: 10px;"
                                  "background-color: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #f9f9f9, stop: 0.4 #f1f1f1, stop:1 #afafaf);}"
                                  "QPushButton::pressed{border: 1px solid #9f9f9f;}")
        menu_widget.setMinimumSize(200, 300)
        menu_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        menu_list = QVBoxLayout(menu_widget)
        menu_list.setSpacing(10)

        home_btn = QPushButton('\rHome', menu_widget)
        home_btn.setObjectName('home')
        home_btn.setIcon(QIcon('icons/windows-platform.png'))
        home_btn.setCursor(QCursor(Qt.PointingHandCursor))
        home_btn.clicked.connect(lambda: self.menu_btn_clicked(0))
        project_btn = QPushButton('\rData Analysis', menu_widget)
        project_btn.setCursor(QCursor(Qt.PointingHandCursor))
        project_btn.setIcon(QIcon('icons/google-analytics.png'))
        project_btn.clicked.connect(lambda: self.menu_btn_clicked(1))
        contact_btn = QPushButton('\rReport', menu_widget)
        contact_btn.setIcon(QIcon('icons/file.png'))
        contact_btn.setCursor(QCursor(Qt.PointingHandCursor))
        contact_btn.clicked.connect(lambda: self.menu_btn_clicked(2))
        pakhee_btn = QPushButton('\rNg Pak Hee', menu_widget)
        pakhee_btn.setIcon(QIcon('icons/user.png'))
        pakhee_btn.setCursor(QCursor(Qt.PointingHandCursor))
        members_btn = QPushButton('\rUsers', menu_widget)
        members_btn.setIcon(QIcon('icons/group.png'))
        members_btn.setCursor(QCursor(Qt.PointingHandCursor))
        members_btn.clicked.connect(lambda: self.menu_btn_clicked(3))

        menu_list.addWidget(home_btn)
        menu_list.addWidget(project_btn)
        menu_list.addWidget(contact_btn)
        menu_list.addWidget(pakhee_btn)
        menu_list.addWidget(members_btn)

        menu_list.setContentsMargins(5, 20, 10, 10)
        menu_list.setAlignment(members_btn, Qt.AlignTop)

        contant_widget = QWidget()
        contant_widget.setStyleSheet("border: None; background: #252525;")
        contant_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contant_widget = contant_widget

        home_content: QWidget = QWidget()
        home_content.setStyleSheet("background-color: red;")
        data_analysis_content: QWidget = QWidget()
        data_analysis_content.setStyleSheet("background-color: yellow;")
        report_content: QWidget = QWidget()
        report_content.setStyleSheet("background-color: blue;")
        members_content: QWidget = QWidget()
        members_content.setStyleSheet("background-color: #909090;")

        contents_layout = QVBoxLayout()
        contents_layout.setContentsMargins(1, 1, 1, 1)
        self.stacked_contents: QStackedWidget = QStackedWidget()
        self.stacked_contents.addWidget(home_content)
        self.stacked_contents.addWidget(data_analysis_content)
        self.stacked_contents.addWidget(report_content)
        self.stacked_contents.addWidget(members_content)
        self.stacked_contents.setCurrentWidget(home_content)
        contents_layout.addWidget(self.stacked_contents)
        contant_widget.setLayout(contents_layout)

        chat_widget = QWidget()
        chat_widget.setStyleSheet("QWidget{border-left: 1px solid #454545; background-color: qlineargradient(x1:1, y1:1, x2:1, y2:0, stop:0 #313131, stop:1 #111111);}")
        chat_widget.setMinimumSize(300, self.rect().height())
        chat_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        left_layout = QHBoxLayout()
        left_layout.setObjectName('left_layout')
        left_layout.setSpacing(3)
        left_layout.setContentsMargins(1, 1, 1, 1)
        left_layout.addWidget(menu_widget, stretch=1)
        left_layout.addWidget(contant_widget, stretch=3)
        left_layout.addWidget(chat_widget, stretch=1)

        left_widget: QWidget = QWidget()
        left_widget.setObjectName('left_widget')
        left_widget.setLayout(left_layout)

        self.setCentralWidget(left_widget)

    def initGeometry(self):
        screen: QDesktopWidget = QDesktopWidget().screenGeometry()
        width: int = min(screen.width(), 800)
        height: int = min(screen.height(), 700)

        self.setMinimumSize(width, height)

        x: int = (screen.width() - width) // 2
        y: int = (screen.height() - height) // 2

        self.setGeometry(0, 0, screen.width(), screen.height())

    def menu_btn_clicked(self, index: int):
        self.stacked_contents.setCurrentIndex(index)


app = QApplication(sys.argv)

window = WindowForm()
window.showMaximized()


sys.exit(app.exec_())
