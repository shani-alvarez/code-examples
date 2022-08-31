import tkinter as tk
from GraphicalUserInterface import GraphicalUserInterface

# This class initialises the program interface.
    
class Initialiser(object):
    
    def main():
        # Creates a window for the interface and sets its specifications
        root = tk.Tk()
        # Creates a new GraphicalUserInterface object
        gui = GraphicalUserInterface(root)
        # Starts/opens interface
        root.mainloop()
        
    if __name__ == "__main__":
        main()
        