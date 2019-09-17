from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from classes import constants, ui_util


class About(QDialog):
    """Окно 'О программе'"""
    def __init__(self):
        QDialog.__init__(self)

        ui_util.load_ui(self, 'about')
        ui_util.init_ui(self)

        version_text = "Версия: %s" % constants.VERSION
        create_text = 'С легкостью изучайте новые колоды, предложенные сообществом.'
        description_text = constants.DESCRIPTION
        mail_text = 'Почта для замечаний и предложений'
        description_html = """
            <html><head/><body>
                <hr />
                <p align="center">
                    <span style="font-size:10pt; font-weight:600;">%s</span>
                </p>
                <p align="center" style="font-size:10pt;">
                    %s <br /> <a href="mailto:%s"><span style="text-decoration: none; color:#55aaff;">%s</span></a>.
                </p>
            </body></html>""" % (create_text, description_text, constants.AUTHOR_EMAIL, mail_text)
        author_html = """
            <html><head/><body style="font-size:11pt; font-weight:400; font-style:normal;">
                <hr />
                <p align="center" style=" margin:12px 0; -qt-block-indent:0; text-indent:0px;">
                    <span style=" font-size:10pt; font-weight:600;">%s </span>
                </p>
            </body></html>
        """ % constants.COPYRIGHT

        # Устанавливаем информацию о версии программы, авторе и описание
        self.lbl_about_description.setText(description_html)
        self.lbl_about_autor.setText(author_html)
        self.lbl_version.setText(version_text)
        self.lbl_version.setAlignment(Qt.AlignCenter)

    @staticmethod
    def btn_license_click():
        """Открыть окно 'Лицензия'"""
        win = License()
        win.exec_()


class License(QDialog):
    """Окно 'Лицензия'"""
    def __init__(self):
        QDialog.__init__(self)

        ui_util.load_ui(self, 'license')
        ui_util.init_ui(self)

        # Инициализация лицензии
        license_file = QFile(':/license.txt')
        license_file.open(QFile.ReadOnly)
        license_text = bytes(license_file.readAll()).decode('UTF-8')
        self.text_browser.setText(license_text)
        license_file.close()

        # Прокручиваем текст в начало документа
        cursor = self.text_browser.textCursor()
        cursor.setPosition(0)
        self.text_browser.setTextCursor(cursor)
