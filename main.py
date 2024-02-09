# main.py
from controller import AppController
from customtkinter import CTk
def main():
    app = AppController()
    app.setup_initial_gui_state()
    app.run()

if __name__ == '__main__':
    main() 