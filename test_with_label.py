from tkinter import *
from customtkinter import *
import threading

class GUI(CTk):
    def __init__(self, *args, **kwargs):
        
        """
        Initializing window
        """
        

        super().__init__(*args, **kwargs, )
        self.geometry("1000x800")
        
        self.grid_rowconfigure((0,1),weight=1,uniform="a")
        self.grid_columnconfigure((0,1), weight=1, uniform="a")
        
        
        self.label1 = CTkLabel(self, text="Hey", font=(None, 20))
        self.label2 = CTkLabel(self, text="Hey", font=(None, 1))
        self.label1.grid(row=0, column=0, sticky="we")
        self.label2.grid(row=0, column=1, sticky="we")
        
        self.button = CTkButton(self, text="push me", command=self.test)
        self.button.grid(row=1,column = 0, columnspan=2)
        self.size = 20
        self.size1 = 0
    
    def test(self):
        self.shrink()
        self.expand()
    
    def expand(self):
        if self.size1 < 20:
            self.size1 += 1
            self.label2.configure(font=(None, self.size1))
            self.after(25, lambda: self.expand())
        else:
            self.size1 = 0
    
    def shrink(self):
        if self.size > 1:
            self.size -= 1
            self.label1.configure(font=(None, self.size))
            self.after(25, lambda: self.shrink())
        else:
            self.size = 20

        

        
        

def main():
    theme_path = os.path.expanduser("theme/Hades.json")
    set_default_color_theme(theme_path)
    
    app = GUI()
    setup_thread = threading.Thread(target=app.mainloop())
    setup_thread.start()
    app.mainloop()
    
if __name__ == main():
    main()