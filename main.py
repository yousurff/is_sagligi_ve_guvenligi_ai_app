import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from ui.login_window import LoginWindow
from ui.main_menu import MainMenuWindow

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    # login screen
    login = LoginWindow(on_success=lambda: stack.setCurrentIndex(1))
    stack.addWidget(login)

    # main menu (after login)
    menu = MainMenuWindow()
    stack.addWidget(menu)

    stack.setCurrentIndex(0)
    stack.resize(300, 370)
    stack.setMinimumSize(300, 370)
    stack.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()