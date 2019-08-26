import os
from PyQt5.QtCore import QFile, QTextStream, Qt, QFileInfo, QByteArray
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from classes import ui_util
from classes.app import App, get_app
from classes.helper_function import get_icon
from classes.constants import APP_NAME, PATH
from classes.logger import log
from view.helpers.actions import Actions
from view.widgets.paragraphs import ParagraphsWidget
from view.widgets.statistics import StatisticsWidget


class MainWindow(QMainWindow):
    """Главное окно"""

    ui_path = os.path.join(PATH, 'view', 'ui', 'main_window.ui')

    def __init__(self):
        QMainWindow.__init__(self)
        self.current_file = ''
        self.recent_menu = None

        # set window on app for reference during initialization of children
        get_app().window = self

        # Load UI from designer
        ui_util.load_ui(self, self.ui_path)

        # Init Ui
        ui_util.init_ui(self)

        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

        self.setWindowIcon(get_icon('app.svg'))
        self.restore_window_settings()
        self.actions = Actions(self)
        self.create_toolbars()
        self.create_dock_windows()
        self.set_current_file('')
        self.show()

    def restore_window_settings(self):
        """Загрузка настроек размера и положения окна"""
        self.restoreGeometry(App.settings.value("Geometry", QByteArray()))
        self.restoreState(App.settings.value("Window State", QByteArray()))

    def save_window_settings(self):
        """Сохранение настроек размера и положения окна"""
        App.settings.setValue("Geometry", self.saveGeometry())
        App.settings.setValue("Window State", self.saveState())

    def create_toolbars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.actions.new_letter1)
        self.fileToolBar.addAction(self.actions.new_letter)
        self.fileToolBar.addAction(self.actions.save)
        self.fileToolBar.addAction(self.actions.print)
        self.fileToolBar.addAction(self.actions.print1)
        self.fileToolBar.addAction(self.actions.print2)

    def create_dock_windows(self):
        dock = StatisticsWidget(self)
        self.view_menu.addAction(dock.toggleViewAction())

        dock = ParagraphsWidget(self)
        self.view_menu.addAction(dock.toggleViewAction())

    def closeEvent(self, event):
        log.info('------------------ Выключение ------------------')
        if self.maybe_save():
            self.save_window_settings()
            event.accept()
        else:
            event.ignore()

    def maybe_save(self):
        is_modified = False
        if is_modified:
            ret = QMessageBox.warning(self, APP_NAME, "У вас остались несохраненные изменения.\n"
                                                      "Хотите ли вы сохранить измененния?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.save()
            if ret == QMessageBox.Cancel:
                return False
        return True

    def save(self):
        if self.current_file:
            return self.save_file(self.current_file)
        return self.save_as()

    def save_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self)
        if file_name:
            return self.save_file(file_name)
        return False

    def save_file(self, file_name):
        file = QFile(file_name)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, APP_NAME, "Запись в файл невозможна %s:\n%s." % (file_name, file.errorString()))
            return False

        out_file = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out_file << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.set_current_file(file_name)
        self.statusBar().showMessage("Файл сохранен", 2000)
        return True

    def set_current_file(self, file_name):
        self.current_file = file_name
        self.setWindowModified(False)

        if self.current_file:
            shown_name = self.stripped_name(self.current_file)
        else:
            shown_name = 'untitled.txt'
        self.setWindowTitle("%s[*]" % shown_name)

    def stripped_name(self, full_file_name):
        return QFileInfo(full_file_name).fileName()
