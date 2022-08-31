import os
import tkinter as tk

from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PreProcessing import PreProcessing
from Graphics import Graphics

# This class builds and sets the GUI for the program, as well as the functions that set the actions for each element of the GUI.
class GraphicalUserInterface:
    
    
    def __init__(self, window):
        self.proc = PreProcessing()
        self.graph = Graphics()
        
        ### Creates the elements of the GUI
        
        # Creates the main window
        self.window = window
        self.window.title("Prototype app")
        self.window.geometry('570x500')
        self.window.sourceFolder = ''
        self.window.sourceFile = ''
        
        # Creates the labels for file importing and loading
        self.label1 = tk.Label(self.window, text="None selected", padx=10, pady=10, anchor='w', wraplength=500)
        self.label1.grid(column=1, row=3)
        self.label2 = tk.Label(self.window, text="None selected", padx=10, pady=10, anchor='w', wraplength=500)
        self.label2.grid(column=1, row=4)
        self.label3 = tk.Label(self.window, text="None selected", padx=10, pady=10, anchor='w', wraplength=500)
        self.label3.grid(column=1, row=5)
        self.label_load = tk.Label(self.window, text="No files loaded", padx=10, pady=10, anchor='w')
        self.label_load.grid(column=1, row=8)
    
        # Creates the buttons that import the files
        self.b_chooseFile1 = tk.Button(self.window, text = "Import csv 1", width = 15, command = lambda: self.chooseFileButton(1))
        self.b_chooseFile1.grid(column=0, row=3, padx=10, pady=10)
        self.b_chooseFile1.width = 10
        self.b_chooseFile2 = tk.Button(self.window, text = "Import csv 2", width = 15, command = lambda: self.chooseFileButton(2))
        self.b_chooseFile2.grid(column=0, row=4, padx=10, pady=10)
        self.b_chooseFile2.width = 10
        self.b_chooseFile3 = tk.Button(self.window, text = "Import csv 3", width = 15, command = lambda: self.chooseFileButton(3))
        self.b_chooseFile3.grid(column=0, row=5, padx=10, pady=10)
        self.b_chooseFile3.width = 10

        # Creates the button for loading the files   
        self.b_loadFiles = tk.Button(self.window, text = "Load files", width = 15, command = self.loadFilesButton)
        self.b_loadFiles.grid(column=0, row=8, padx=10, pady=10)
        self.b_loadFiles.width = 10
        
        # Creates the button for saving the files   
        self.b_saveFiles = tk.Button(self.window, text = "Save files to JSON", width = 15, command = self.saveFilesButton)
        self.b_saveFiles.grid(column=0, row=20, padx=10, pady=10)
        self.b_saveFiles.width = 10

        # Creates a bar menu object with two menu tabs objects
        self.menu = tk.Menu(self.window)
        self.process_item = tk.Menu(self.menu, tearoff=0)
        self.analysis_item = tk.Menu(self.menu, tearoff=0)
        
        # Creates a menu item for the first tab
        self.process_item.add_command(label='Datasets information', command = self.infoDatasetsMenu)
        self.process_item.add_separator()
        
        # Creates the submenus for the Fill GRADE column menu item
        self.submenu2 = tk.Menu(self.process_item, tearoff=0)
        self.submenu2.add_command(label="Dataset 1", command = lambda: self.scoreToGradeFillNaMenu('self.data1'))
        self.submenu2.add_command(label="Dataset 2", command = lambda: self.scoreToGradeFillNaMenu('self.data2'))
        self.submenu2.add_command(label="Dataset 3", command = lambda: self.scoreToGradeFillNaMenu('self.data3'))
        self.process_item.add_cascade(label='Fill GRADE column', menu=self.submenu2, underline=0)
        self.process_item.add_separator()
        
        # Creates the submenus for the Remove NAs menu item
        self.submenu1 = tk.Menu(self.process_item, tearoff=0)
        self.submenu1.add_command(label="Dataset1", command = lambda: self.removeNAsMenu('self.data1'))
        self.submenu1.add_command(label="Dataset 2", command = lambda: self.removeNAsMenu('self.data2'))
        self.submenu1.add_command(label="Dataset3", command = lambda: self.removeNAsMenu('self.data3'))
        self.process_item.add_cascade(label='Remove NAs', menu=self.submenu1)
        self.process_item.add_separator()
        
        # Creates the submenus for the Remove duplicates menu item
        self.submenu3 = tk.Menu(self.process_item, tearoff=0)
        self.submenu3.add_command(label="Dataset 1", command = lambda: self.removeDuplicatesMenu('self.data1'))
        self.submenu3.add_command(label="Dataset 2", command = lambda: self.removeDuplicatesMenu('self.data2'))
        self.submenu3.add_command(label="Dataset 3", command = lambda: self.removeDuplicatesMenu('self.data3'))
        self.process_item.add_cascade(label='Remove duplicates', menu=self.submenu3, underline=0)
        self.process_item.add_separator()
        
        # Creates the submenus for the Remove inactive program status menu item
        self.submenu4 = tk.Menu(self.process_item, tearoff=0)
        self.submenu4.add_command(label="Dataset 1", command = lambda: self.programStatusInactiveMenu('self.data1'))
        self.submenu4.add_command(label="Dataset 2", command = lambda: self.programStatusInactiveMenu('self.data2'))
        self.submenu4.add_command(label="Dataset 3", command = lambda: self.programStatusInactiveMenu('self.data3'))
        self.process_item.add_cascade(label='Remove inactive program status', menu=self.submenu4, underline=0)
        self.process_item.add_separator()
        
        # Creates the submenus for the Manipulate PE DESCRIPTION column menu item
        self.submenu5 = tk.Menu(self.process_item, tearoff=0)
        self.submenu5.add_command(label="Dataset 1", command = lambda: self.typeSeatsColumnMenu('self.data1'))
        self.submenu5.add_command(label="Dataset 2", command = lambda: self.typeSeatsColumnMenu('self.data2'))
        self.submenu5.add_command(label="Dataset 3", command = lambda: self.typeSeatsColumnMenu('self.data3'))
        self.process_item.add_cascade(label='Manipulate PE DESCRIPTION column', menu=self.submenu5, underline=0)
        self.process_item.add_separator()

        # Creates the submenus for the Stats for inspection score per year menu item
        self.submenu6 = tk.Menu(self.analysis_item, tearoff=0)
        self.submenu6.add_command(label="Dataset 1, seating group", command = lambda: self.statsInspectionScoreMenu('self.data1', 'seating'))
        self.submenu6.add_command(label="Dataset 1, zip code group", command = lambda: self.statsInspectionScoreMenu('self.data1', 'zip code'))
        self.submenu6.add_command(label="Dataset 2, seating group", command = lambda: self.statsInspectionScoreMenu('self.data2', 'seating'))
        self.submenu6.add_command(label="Dataset 2, zip code group", command = lambda: self.statsInspectionScoreMenu('self.data2', 'zip code'))
        self.submenu6.add_command(label="Dataset 3, seating group", command = lambda: self.statsInspectionScoreMenu('self.data3', 'seating'))
        self.submenu6.add_command(label="Dataset 3, zip code group", command = lambda: self.statsInspectionScoreMenu('self.data3', 'zip code'))
        self.analysis_item.add_cascade(label='Stats for inspection score per year', menu=self.submenu6, underline=0)
        self.analysis_item.add_separator()

        # Creates the submenus for the Visualize violations per establishment menu item
        self.submenu7 = tk.Menu(self.analysis_item, tearoff=0)
        self.submenu7.add_command(label="Dataset 1 and Dataset 2", command = lambda: self.violsPerTypeMenu('self.data1', 'self.data2'))
        self.submenu7.add_command(label="Dataset 1 and Dataset 3", command = lambda: self.violsPerTypeMenu('self.data1', 'self.data3'))
        self.submenu7.add_command(label="Dataset2 and Dataset 3", command = lambda: self.violsPerTypeMenu('self.data2', 'self.data3'))
        self.analysis_item.add_cascade(label='Visualize violations per establishment', menu=self.submenu7, underline=0)
        self.analysis_item.add_separator()

        # Creates the submenus for the Visualize correlation (violations, ZIP) menu item
        self.submenu8 = tk.Menu(self.analysis_item, tearoff=0)
        self.submenu8.add_command(label="Dataset 1 and Dataset 2", command = lambda: self.corrViolationsMenu('self.data1', 'self.data2'))
        self.submenu8.add_command(label="Dataset 1 and Dataset 3", command = lambda: self.corrViolationsMenu('self.data1', 'self.data3'))
        self.submenu8.add_command(label="Dataset2 and Dataset 3", command = lambda: self.corrViolationsMenu('self.data2', 'self.data3'))
        self.analysis_item.add_cascade(label='Visualize correlation (violations, zip code)', menu=self.submenu8, underline=0)
        self.analysis_item.add_separator()

        # Creates the two menu tabs
        self.menu.add_cascade(label='Pre-processing', menu=self.process_item)
        self.menu.add_cascade(label='Data analysis', menu=self.analysis_item)
        self.window.config(menu=self.menu)
        
        # Creates a text box with a scrollbar for output
        self.v = tk.Scrollbar(self.window, orient='vertical') 
        self.v.grid(row=15, column=10)
        self.text_box = tk.Text(self.window, width = 65, height = 15, wrap = tk.WORD, yscrollcommand = self.v.set, state=tk.DISABLED) 
        self.text_box.grid(column=0, row=15, columnspan = 10, padx=10, pady=10) 
        self.v.config(command=self.text_box.yview)   
    
    # Function to open an explorer window and select the directory in which to save the files
    def saveFileDir(self):
        current_dir = os.getcwd()
        self.window.sourceFolder =  filedialog.asksaveasfilename(parent=self.window, initialdir= current_dir, defaultextension=".json", title='Save first dataset as', 
                                                          filetypes = (("JSON file (*.json)", "*.json"), ("All files (*.*)", "*.*")))
        dir_file1 = self.window.sourceFolder
        self.window.sourceFolder =  filedialog.asksaveasfilename(parent=self.window, initialdir= current_dir, defaultextension=".json", title='Save second dataset as', 
                                                          filetypes = (("JSON file (*.json)", "*.json"), ("All files (*.*)", "*.*")))
        dir_file2 = self.window.sourceFolder
        self.window.sourceFolder =  filedialog.asksaveasfilename(parent=self.window, initialdir= current_dir, defaultextension=".json", title='Save third dataset as', 
                                                          filetypes = (("JSON file (*.json)", "*.json"), ("All files (*.*)", "*.*")))
        dir_file3 = self.window.sourceFolder
        return dir_file1, dir_file2, dir_file3
    
    # Function that sets the action for the button that imports the files
    def chooseFileButton(self, button_number):
        try:
            current_dir = os.getcwd()
            self.window.sourceFile = filedialog.askopenfilename(parent=self.window, initialdir= current_dir, 
                                                           filetypes = (("CSV file (*.csv)", "*.csv"), ("All files (*.*)", "*.*")), 
                                                           title='Select a file')
            if ((button_number == 1) & (len(self.window.sourceFile) != 0)):
                self.label1.configure(text = self.window.sourceFile)
            elif ((button_number == 2) & (len(self.window.sourceFile) != 0)):
                self.label2.configure(text = self.window.sourceFile)
            elif ((button_number == 3) & (len(self.window.sourceFile) != 0)):
                self.label3.configure(text = self.window.sourceFile)
            else:
                None
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, 'No files were imported.')
            self.text_box.configure(state = tk.DISABLED)
    
    # Function that check the file extension of a given file path
    def checkFileExtension(self, files_paths):
        if all((path.endswith('.csv')) or (path.endswith('.csv')) for path in files_paths):
            return True
        else:
            return False
    
    # Function that gets the file paths from the labels showing in the GUI window
    def getFilePaths(self):
        files = [self.label1.cget('text'), self.label2.cget('text'), self.label3.cget('text')]
        return files
    
    # Function that sets the action for the button that loads the files selected
    def loadFilesButton(self):
        files = self.getFilePaths()
        if self.checkFileExtension(files):
            self.label_load.configure(text = "Files loaded!") 
            self.proc.loadFiles(files) # For pre-processing class
        else:
            self.label_load.configure(text = "One or more files are not .csv")
    
    # Function that sets the action for the button that saves the files
    def saveFilesButton(self):
        try:
            if self.saveFilesWarning():
                save_dirs = self.saveFileDir()
                self.proc.saveFiles(save_dirs[0], save_dirs[1], save_dirs[2])
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, 'No files were saved.')
            self.text_box.configure(state = tk.DISABLED)
    
    # Function that issues a warning, asking the user to accept or cancel saving the files
    def saveFilesWarning(self):
        return messagebox.askokcancel('Save files', 'The three datasets will be saved in their current state in JSON format. Are you sure you want to continue?')
    
    # Function that returns a generic error
    def error(self):
        return "There was an unexpected error and the operation was stopped."
    
    # Fucntion that sets the action for the menu option that provides information on the datasets
    def infoDatasetsMenu(self):
        try:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.proc.infoDatasets())
            self.text_box.configure(state = tk.DISABLED)
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, 'It seems there are no files uploaded.')
            self.text_box.configure(state = tk.DISABLED)
    
    # Fucntion that removes the NA values from a dataset    
    def removeNAsMenu(self, df_in):
        try:
            df_in = self.proc.getDataset(df_in)
            self.proc.removeNAs(df_in)
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, 'All rows containing NA values have been removed. \n\n' + self.proc.checkNAValues(df_in))
            self.text_box.configure(state = tk.DISABLED)
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.error())
            self.text_box.configure(state = tk.DISABLED)
    
    # Function that sets the action for the menu option that fills the grade column by using the score column
    def scoreToGradeFillNaMenu(self, df_in):
        try:
            df_in = self.proc.getDataset(df_in)
            info = self.proc.scoreToGradeFillNa(df_in)
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, info)
            self.text_box.configure(state = tk.DISABLED)
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.error())
            self.text_box.configure(state = tk.DISABLED)
    
    # Function that removes duplicate rows in a dataset
    def removeDuplicatesMenu(self, df_in):
        try:
            df_in = self.proc.getDataset(df_in)
            self.proc.removeDuplicates(df_in)
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, 'All duplicate rows have been removed. \n\n' + self.proc.checkDuplicateRows(df_in))
            self.text_box.configure(state = tk.DISABLED)
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.error())
            self.text_box.configure(state = tk.DISABLED)

    # Function that sets the action for the menu option that removes the entries labeled as inactive of the program status column
    def programStatusInactiveMenu(self, df_in):
        try:
            df_in = self.proc.getDataset(df_in)
            info = self.proc.programStatusInactive(df_in)
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, str(info + self.proc.checkProgramStatus(df_in)))
            self.text_box.configure(state = tk.DISABLED)
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.error())
            self.text_box.configure(state = tk.DISABLED)
    
    # Fucntion that sets the action for the menu option that manipulates the seats column, creats a new one with modified information
    def typeSeatsColumnMenu(self, df_in):
        try:
            df_in = self.proc.getDataset(df_in)
            info = self.proc.typeSeatsColumn(df_in)
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, info)
            self.text_box.configure(state = tk.DISABLED)
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.error())
            self.text_box.configure(state = tk.DISABLED)
   
    # Function that sets the action for the menu option that provides the statistics of the inspection score analysis
    def statsInspectionScoreMenu(self, df_in, group):
        try:
            df_in = self.proc.getDataset(df_in)
            info = self.proc.statsInspectionScore(df_in, group)
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, info)
            self.text_box.configure(state = tk.DISABLED)
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.error())
            self.text_box.configure(state = tk.DISABLED)
     
    # Function that sets the action for the menu option providing the graph visualization of the number violations per establishment
    def violsPerTypeMenu(self, df1_in, df2_in):
        try:
            df1_in = self.proc.getDataset(df1_in)
            df2_in = self.proc.getDataset(df2_in)
            graph = self.graph.violsPerTypeGraph(self.proc.violsPerType(df1_in, df2_in)[0])
            info = self.proc.violsPerType(df1_in, df2_in)[1]
            
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, info)
            self.text_box.configure(state = tk.DISABLED)
            
            win_pop = tk.Toplevel()
            win_pop.geometry('600x400')
            win_pop.wm_title("Graph")
            
            canvas = FigureCanvasTkAgg(graph, master = win_pop) 
            canvas.draw() 
            canvas.get_tk_widget().grid(row=1, column=1) 
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, 'These datasets do not have SERIAL NUMBER or FACILITY ID as columns. Operations cannot be implemented.')
            self.text_box.configure(state = tk.DISABLED)
            
            
    def corrViolationsMenu(self, df1_in, df2_in):
        try:
            df1_in = self.proc.getDataset(df1_in)
            df2_in = self.proc.getDataset(df2_in)
            data_corr = self.proc.corrViolations(df1_in, df2_in)
            corr_graph = self.graph.corrViolationsGraph(data_corr)
            
            win_pop1 = tk.Toplevel()
            win_pop1.geometry('600x400')
            win_pop1.wm_title("Correlation graph")
            
            canvas = FigureCanvasTkAgg(corr_graph, master = win_pop1) 
            canvas.draw() 
            canvas.get_tk_widget().grid(row=1, column=1)  
        except:
            self.text_box.configure(state = tk.NORMAL)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, 'These datasets do not have SERIAL NUMBER, OWNER ID or Zip Codes as columns. Operations cannot be implemented.')
            self.text_box.configure(state = tk.DISABLED)
   