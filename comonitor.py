#!/usr/bin/env python3
# pylint: disable=I1101, C0111


import sys
import platform
import logging
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore, QtGui

__version__ = '0.1.2'
__author__ = 'K. Dziadowiec <krzysztof.dziadoiwec@gmail.com>'

# OS ['Windows', 'Linux', 'Darwin']
PLATFORM = platform.system()

POPUP_HORIZONTAL_OFFSET = 5
POPUP_POSITION_THRESHOLD = 100


def initialize_logging(debug):
    app_logger = logging.getLogger('COMonitor')
    if debug:
        app_logger.setLevel(logging.DEBUG)
    else:
        app_logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    app_logger.addHandler(stream_handler)

    return app_logger


def create_dark_palette():
    dark_palette = QtGui.QPalette()
    dark_palette_opts = {
        QtGui.QPalette.Window: (16, 16, 24),
        QtGui.QPalette.Base: (37, 38, 43),
        QtGui.QPalette.AlternateBase: (37, 38, 43),
        QtGui.QPalette.Button: (37, 38, 43),
        QtGui.QPalette.ButtonText: (214, 218, 213),
        QtGui.QPalette.Text: (214, 218, 213),
        QtGui.QPalette.Highlight: (27, 149, 93),
        QtGui.QPalette.HighlightedText: (214, 218, 213),
    }
    for gui_element, color in dark_palette_opts.items():
        red, green, blue = color
        dark_palette.setColor(gui_element, QtGui.QColor(red, green, blue))

    return dark_palette


class View(QtWidgets.QWidget):
    """Window containing list of serial ports."""

    def __init__(self, screen_resolution):
        super(View, self).__init__()
        self.screen_resolution = screen_resolution

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon('resources/icons/icon.svg'))
        self.setWindowTitle('COMonitor')
        self.setFixedSize(110, 100)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.com_list_widget = QtWidgets.QListWidget()
        layout.addWidget(self.com_list_widget)

    def popup(self, geometry):
        """Adjust window position to the tray and show it."""
        pos = QtCore.QPoint(geometry.x(), geometry.y())

        screen_width = self.screen_resolution.width()
        screen_height = self.screen_resolution.height()

        def is_tray_on_bottom():
            return bool(screen_height - geometry.y() < POPUP_POSITION_THRESHOLD)

        def is_tray_on_top():
            return bool(geometry.y() < POPUP_POSITION_THRESHOLD)

        def is_tray_on_right():
            return bool(screen_width - geometry.x() < POPUP_POSITION_THRESHOLD)

        def is_tray_on_left():
            return bool(geometry.x() < POPUP_POSITION_THRESHOLD)

        if is_tray_on_bottom():
            dist_left = (self.width() - geometry.width()) / 2
            dist_right = self.height()
            self.adjust_position(pos, dist_left, dist_right)
        elif is_tray_on_top():
            dist_left = (self.width() - geometry.width()) / 2
            dist_right = -geometry.height()
            self.adjust_position(pos, dist_left, dist_right)
        elif is_tray_on_right():
            dist_left = self.width() + POPUP_HORIZONTAL_OFFSET
            dist_right = (self.height() - geometry.height()) / 2
            self.adjust_position(pos, dist_left, dist_right)
        elif is_tray_on_left():
            dist_left = -(geometry.width() + POPUP_HORIZONTAL_OFFSET)
            dist_right = (self.height() - geometry.height()) / 2
            self.adjust_position(pos, dist_left, dist_right)

        self.show()
        self.activateWindow()

    def adjust_position(self, pos, dist_left, dist_right):
        self.move(pos - QtCore.QPoint(dist_left, dist_right))


class Monitor(QtWidgets.QSystemTrayIcon):
    """Tray application monitoring connecting and disconnecting serial ports."""

    def __init__(self, screen_resolution):
        super(Monitor, self).__init__()
        self.setToolTip('COMonitor')

        self.setIcon(QtGui.QIcon('resources/icons/icon.svg'))

        # create view widget
        self.view = View(screen_resolution)

        # add click handler for left mouse click
        self.activated.connect(self.click_handler)

        # CONTEXT MENU
        menu = QtWidgets.QMenu()
        self.setContextMenu(menu)
        exit_action = menu.addAction('Exit')
        exit_action.triggered.connect(QtCore.QCoreApplication.exit)

        # initialize serial port list
        self.serial_ports = self.enumerate_serial_ports()
        self.fill_port_list()

        # check for updates periodically
        self.update_port_list()

    def update_port_list(self):
        logger.debug('Updating ports list')
        spl = self.enumerate_serial_ports()
        logger.debug('Current port list: %s', spl)
        diff_list = list(set(spl) - set(self.serial_ports))

        if not spl:
            logger.debug('New list is empty')

            # Update list
            self.serial_ports = spl

        elif len(spl) < len(self.serial_ports):
            diff_list = list(set(self.serial_ports) - set(spl))
            logger.info('These ports went missing: %s', diff_list)

            # Update list
            self.serial_ports = spl

            # Notify about disconected ports
            for port in diff_list:
                self.showMessage('Serial port disconnected!', port)

            self.fill_port_list()

        elif diff_list:
            logger.info('New ports: %s', diff_list)

            # Update list
            self.serial_ports = spl

            # Notify about new ports
            for port in diff_list:
                self.showMessage('New serial port detected!', port)

            self.fill_port_list()

        else:
            logger.debug('No new ports found')

        # check periodicaly for changes
        QtCore.QTimer.singleShot(1000, self.update_port_list)

    def fill_port_list(self):
        self.view.com_list_widget.clear()

        for port in self.serial_ports:
            self.view.com_list_widget.addItem(port)

    @staticmethod
    def enumerate_serial_ports():
        """Finds list of serial ports on this PC."""
        return [str(port[0]) for port in serial.tools.list_ports.comports()]

    def click_handler(self, val):
        if (val == self.Trigger or val == self.DoubleClick):
            self.show_view()

    def show_view(self):
        if self.view.isVisible():
            self.view.hide()
        else:
            self.view.popup(self.geometry())

    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

        app.setStyle('Fusion')
        dark_palette = create_dark_palette()
        app.setPalette(dark_palette)

        screen_resolution = app.desktop().screenGeometry()
        main = Monitor(screen_resolution)
        main.show()

        return app.exec_()


if __name__ == '__main__':
    logger = initialize_logging(debug=False)

    sys.exit(Monitor.run())
