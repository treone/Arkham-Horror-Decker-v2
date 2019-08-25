from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QAction

from utility.app_wrapper import App


class Actions:
    def __init__(self, parent):
        self.new_letter = QAction(App.symbol.mystic, "&New Letter", parent)
        self.new_letter.setShortcut(QKeySequence.New)
        self.new_letter.setStatusTip("Create a new form letter")
        # # self.new_letter.triggered.connect(parent.new_letter)

        self.save = QAction(App.symbol.seeker, "&Save...", parent)
        self.save.setShortcut(QKeySequence.Save)
        self.save.setStatusTip("Save the current form letter")
        # self.save.triggered.connect(parent.save)

        self.print = QAction(App.symbol.survivor, "&Print...", parent)
        self.print.setShortcut(QKeySequence.Print)
        self.print.setStatusTip("Print the current form letter")
        # self.print.triggered.connect(parent.print_)

        self.print1 = QAction(App.symbol.rogue, "&Print...", parent)
        self.print1.setShortcut(QKeySequence.Print)
        self.print1.setStatusTip("Print the current form letter")
        # self.print.triggered.connect(parent.print_)

        self.print2 = QAction(App.symbol.guardian, "&Print...", parent)
        self.print2.setShortcut(QKeySequence.Print)
        self.print2.setStatusTip("Print the current form letter")
        # self.print.triggered.connect(parent.print_)

        self.undo = QAction(QIcon(':/images/undo.png'), "&Undo", parent)
        self.undo.setShortcut(QKeySequence.Undo)
        self.undo.setStatusTip("Undo the last editing action")
        # self.undo.triggered.connect(parent.undo)

        self.quit = QAction("&Quit", parent)
        self.quit.setShortcut("Ctrl+Q")
        self.quit.setStatusTip("Quit the application")
        # self.quit.triggered.connect(parent.close)

        self.about = QAction("&About", parent)
        self.about.setStatusTip("Show the application's About box")
        # self.about.triggered.connect(parent.about)

        self.about_qt = QAction("About &Qt", parent)
        self.about_qt.setStatusTip("Show the Qt library's About box")
        # self.about_qt.triggered.connect(QApplication.instance().aboutQt)
