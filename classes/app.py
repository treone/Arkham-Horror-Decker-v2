import os
import sys
import locale
import platform
import traceback
from PyQt5.QtCore import QSettings, pyqtSlot, Qt
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QMessageBox, QStyleFactory
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from classes import project

try:
    # Включить High-DPI разрешение
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
except AttributeError:
    pass  # Заглушка для старых Qt5 версий


def get_app():
    """Возвращает текущий QApplication объект"""
    return QApplication.instance()


def get_settings():
    """Возвращает текущий объект настроек QApplication"""
    return QApplication.instance().settings


class App(QApplication):
    """
    Класс подготовки главного окна к запуску.
    """

    def __init__(self, *args):
        QApplication.__init__(self, *args)
        try:
            # Импорт модулей
            from classes import constants
            from classes.logger import log, reroute_output

            # Отметка начала сессии
            import time
            self.__start_time = time.time()  # Время начала инициализации
            log.info("------------------------------------------------")
            locale.setlocale(locale.LC_ALL, 'ru')
            log.info(time.strftime("%d %B %Y %H:%M:%S", time.localtime()).center(48))  # Пример: 26 Август 2019 16:14:04
            log.info('Запуск новой сессии'.center(48))

            from classes import symbols, ui_util

            # Перенаправляем stdout и stderr в логер
            reroute_output()
        except (ImportError, ModuleNotFoundError) as ex:
            tb = traceback.format_exc()
            QMessageBox.warning(None, "Ошибка импорта модулей",
                                "Модуль: %(name)s\n\n%(tb)s" % {"name": ex.name, "tb": tb})
            # Остановить запуск и выйти
            sys.exit()
        except Exception:
            sys.exit()

        # Запись служебной информации
        try:
            log.info("------------------------------------------------")
            log.info(("%s (version %s)" % (constants.APP_NAME, constants.VERSION)).center(48))
            log.info("------------------------------------------------")

            log.info("Платформа: %s" % platform.platform())
            log.info("Процессор: %s" % platform.processor())
            log.info("Тип: %s" % platform.machine())
            log.info("Python: %s" % platform.python_version())
            log.info("Qt5: %s" % QT_VERSION_STR)
            log.info("PyQt5: %s" % PYQT_VERSION_STR)
            log.info("------------------------------------------------")
        except Exception:
            pass

        log.info("Подключаем сигнал окончания сессии")
        self.aboutToQuit.connect(self.on_log_the_end)

        log.info("Подключаем переменные необходимые для правильной работы приложения")
        self.setApplicationName(constants.APP_NAME)
        self.setApplicationDisplayName(constants.APP_NAME_RUS)
        self.setOrganizationName(constants.AUTHOR)
        self.setApplicationVersion(constants.VERSION)

        log.info("Инициализация настроек")
        App.settings = QSettings()

        log.info("Инициализация иконок")
        App.symbol = symbols.Symbol()

        log.info("Инициализируем ловца необработанных исключений")
        from classes import exceptions
        sys.excepthook = exceptions.exception_handler

        log.info("Подключаем файл ресурсов приложения")
        from resources import resources
        resources.qInitResources()

        log.info("Подключаем обьект для хранения данных текущего проекта")
        self.project = project.ProjectDataStore()

        log.info("Установка темы Fusion")
        self.setStyle(QStyleFactory.create("Fusion"))

        log.info("Загружаем и устанавливаем шрифт приложения")
        try:
            font_path = ":/fonts/roboto.ttf"
            font_id = QFontDatabase.addApplicationFont(font_path)
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSizeF(12)
            QApplication.setFont(font)
        except Exception as ex:
            log.error("Ошибка установки шрифта roboto.ttf: %s" % str(ex))

        log.info("Загружаем кастомные шрифты")
        try:
            font_path = ":/fonts/medieval.ttf"
            medieval_font_id = QFontDatabase.addApplicationFont(font_path)
            medieval_font_family = QFontDatabase.applicationFontFamilies(medieval_font_id)[0]
            medieval_font = QFont(medieval_font_family)
            medieval_font.setPointSizeF(10.5)
            self.settings.setValue("Medieval Font", medieval_font)
        except Exception as ex:
            log.error("Ошибка установки шрифта medieval.ttf: %s" % str(ex))

        log.info("Создаем главное окно приложения")
        from view.main_window import MainWindow
        MainWindow()

        log.info("Восстанавливаем файл из резервной копии")
        # (это не может произойти до тех пор, пока главное окно не будет полностью загружено)
        self.main_window.recover_backup_signal.emit()

        log.info("------------------------------------------------")
        log.info("Инициализация приложения завершена".center(48))
        elapsed_time = time.time() - self.__start_time
        log.info(("Потребовалось времени: %.3f сек" % elapsed_time).center(48))
        log.info("------------------------------------------------")

    @pyqtSlot()
    def on_log_the_end(self):
        """Отметка об окончании основного потока QT"""
        try:
            from classes.logger import log
            import time
            log.info("------------------------------------------------")
            log.info('Сессия окончена'.center(48))
            log.info(time.strftime("%d %B %Y %H:%M:%S", time.localtime()).center(48))  # Пример: 26 Август 2019 16:14:04
            log.info("================================================")
        except Exception:
            pass
        # Возвращаем 0 в случае успеха
        return 0

    def run(self):
        """Запуск основного потока QT приложения"""
        res = self.exec()
        return res
