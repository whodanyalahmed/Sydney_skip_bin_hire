import tkinter as tk
import tkinter
import app

class UI:
    # make input text , start and stop button
    def __init__(self):
        # make root
        root = tkinter.Tk()
        label = tk.Label(text="URL: ")
        # create text input
        entry = tk.Entry(width=50)
        label.pack()
        entry.pack()
        
        # create start button
        print(entry.get())
        start_button = tk.Button(text="Start", command=lambda: self.start(entry.get()))
        start_button.pack()
        # create stop button
        stop_button = tk.Button(text="Stop", command=lambda: self.stop())
        stop_button.pack()
        root.mainloop()

    # create start 
    def get_driver():
        global driver
        return driver

    def start(self, url):

        app.main(url)
    
    # create stop
    def stop(self):
        # stop the app
        global driver
        driver.quit()
    




# call UI
win = UI()
