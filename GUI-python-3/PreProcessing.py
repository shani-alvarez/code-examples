import pandas as pd
import numpy as np
import re

# This class provides the calculations and data analysis functions that can be selected from the GUI
class PreProcessing:
    
    # Initialiser
    def __init__(self):
        self.data1 = 0
        self.data2 = 0
        self.data3 = 0
    
    # Gets the datasets
    def getDataset(self, df_in):
        if df_in == 'self.data1':
            return self.data1
        elif df_in == 'self.data2':
            return self.data2
        elif df_in == 'self.data3':
            return self.data3
        else:
            return None
    
    #Loads the datasets from the files    
    def loadFiles(self, files):
        try:
            self.data1 = pd.read_csv(files[0])
            self.data2 = pd.read_csv(files[1])        
            self.data3 = pd.read_csv(files[2])
        except:
            error = 'Unable to load files.'
            return error
    
    # Saves the datasets in JSON format
    def saveFiles(self, save_dir1, save_dir2, save_dir3):
        try:
            self.data1.to_json(save_dir1)
            self.data2.to_json(save_dir2)
            self.data3.to_json(save_dir3)
        except:
            error = 'No directories were selected for saving.'
            return error

    # Provides information on the datasets
    def infoDatasets(self):
        datasets = [self.data1, self.data2, self.data3]
        info_datasets = []
        for df in datasets:
            info = str("*****************************************************************" + "\n \n" + 
                 "This dataset has " + str(df.shape[0]) + " entries and " + str(df.shape[1]) + " columns." + "\n \n"+ 
                 "The columns of this dataset are: \n " + str(df.columns.to_list()) + "\n \n" +
                 "The columns of this dataset have the following data types: \n" + str(df.dtypes)+ "\n \n"+ 
                 "This dataset has the following number of NA values in columns: \n" + str(df.isna().sum())+ "\n \n"+
                 "This dataset has the following number of duplicate rows: \n" + str(df.duplicated().sum())+ "\n \n")
            info_datasets.append(info)
        return ' '.join(info_datasets)
    
    # Removes NA values from a dataset
    def removeNAs(self, df_in):
        df_in.dropna(inplace = True)
    
    # Checks for NA values in a dataset
    def checkNAValues(self, df_in):
        info = str("Number of NA values in each column of the dataset: \n" + str(df_in.isna().sum())+ "\n \n")
        return info
    
    # Checks for duplicate rows in a dataset
    def checkDuplicateRows(self, df_in):
        info = str("Number of duplicate rows in the dataset: \n" + str(df_in.duplicated().sum())+ "\n \n")
        return info
    
    # Checks for the program status column inactive values
    def checkProgramStatus(self, df_in):
        try:
            info = 'There are ' + str((df_in['PROGRAM STATUS'] == 'INACTIVE').value_counts()[True]) + ' rows with inactive program status.'
            return info
        except:
            error = 'This dataset does not have PROGRAM STATUS as column. The check cannot be implemented.'
            return error
   
    # Removes duplicate rows in a dataset
    def removeDuplicates(self, df_in):
        df_in.drop_duplicates(inplace = True)

    # Fills the Grade column according to the Score column values when applicable
    def scoreToGradeFillNa(self, data):
        try:
            dic_grades = {}
            unique_grades = list(data.GRADE.unique())
            data["GRADE"] = np.where(pd.isnull(data.GRADE), data.SCORE, data.GRADE) 
            lst = list(data[data['GRADE'].apply(lambda x: type(x) in [int, np.int64, float, np.float64])].GRADE.unique())
            lst_scores = [x for x in lst if ~np.isnan(x)]
            dic_grades = self.scoreToGrade(lst_scores)
            for grade in unique_grades:
                dic_grades[grade] = grade
            data["GRADE"] = data["GRADE"].map(dic_grades) 
            return str('Operation succesful!' + '\n\n' + 'In column GRADE, the rows with NAs were filled by taking into account the SCORE and adding more categorical values that correspond to an (A-F) score.' +  '\n\n' + 'This way, less rows are removed that used to contain an NA.' + '\n\n')
        except:
            error = str('This dataset does not have GRADE and SCORE as columns. Operations cannot be implemented.')
            return error
    
    # Transforms scores into grades based on a categorization
    def scoreToGrade(self, list_in):
        dic = {}
        for i in list_in:
            if i<50:
                dic[i] = 'F'
            elif 50 <= i < 60:
                dic[i] = 'E'
            elif 60 <= i < 70:
                dic[i] = 'D'
            elif 70 <= i < 80:
                dic[i] = 'C'
            elif 80 <= i < 90:
                dic[i] = 'B'
            elif 90 <= i <= 100:
                dic[i] = 'A'
            else:
                dic[i] = np.nan
        return dic

    # Performs the removal of the Program status column inactive values
    def programStatusInactive(self, data):
        try:
            data = data[data['PROGRAM STATUS'] != 'INACTIVE']
            return 'All rows with program status of inactive have been removed.'
        except:
            error = 'This dataset does not have PROGRAM STATUS as column. Operations cannot be implemented.'
            return error
    
    # Manipulate the PE description column and creates the PE seats type column
    def typeSeatsColumn(self, data):
        try:
            data["PE SEATS TYPE"] = data["PE DESCRIPTION"]
            reg_comp = re.compile(r"\([^()]*\)")
            data["PE SEATS TYPE"] = [reg_comp.sub('', x) for x in data["PE SEATS TYPE"]]
            info = 'Operation succesful! New column PE SEATS TYPE was created.'
            return info
        except:
            error = 'This dataset does not have PE DESCRIPTION as column. Operations cannot be implemented.'
            return error
     
    # Sets a column's type to datetime
    def setToDateTime(self, data):
        try:
            data["ACTIVITY DATE"] = pd.to_datetime(data["ACTIVITY DATE"])
        except:
            error = 'This dataset does not have ACTIVITY DATE as column. Operations cannot be implemented.'
            outputError(error)

    # Creates a 'year' column in a dataset
    def setYearColumn(self, data):
        self.setToDateTime(data)
        data["YEAR"] = pd.DatetimeIndex(data["ACTIVITY DATE"]).year
     
    # Performs the statistics on the inspection score client requirement
    def statsInspectionScore(self, data, group):
        try:
            self.setYearColumn(data)
            if group == 'seating': 
                seating_mean = data.groupby(["YEAR", "PE SEATS TYPE"])["SCORE"].mean()
                seating_median = data.groupby(["YEAR", "PE SEATS TYPE"])["SCORE"].median()
                data.drop("YEAR", axis=1, inplace=True)
                return str("*****************************************************************" + "\n \n" + "MEAN SCORES PER YEAR:" + "\n \n" 
                           + str(seating_mean.to_string()) + "\n \n" + "MEDIAN SCORES PER YEAR:" + "\n \n" + str(seating_median.to_string()) + "\n")
            
            elif group == 'zip code':
                zip_mean = data.groupby(["YEAR", "Zip Codes"])["SCORE"].mean()
                zip_median = data.groupby(["YEAR", "Zip Codes"])["SCORE"].median()
                data.drop("YEAR", axis=1, inplace = True)
                return str("****************************************************************" + "\n \n" + "MEAN SCORES PER YEAR:" + "\n \n" 
                           + str(zip_mean.to_string()) + "\n \n" + "MEDIAN SCORES PER YEAR:" + "\n \n" + str(zip_mean.to_string()) + "\n")
            
            else:
                raise ValueError("That is not a valid option.")
            return 'ValueError: That is not a valid option.'
        
        except:
            error = 'This dataset does not have information needed to obtain the statistics for the inspection score.\nYou might want to run the pre-processing beforehand if you are sure this is the right dataset.'
            return error
      
    # Performs rhe visualization of the number of establishments that commited a type of violation
    def violsPerType(self, data1, data2):
        try:
            self.setYearColumn(data1)
            data_ids = data1[["YEAR", "SERIAL NUMBER", "FACILITY ID"]]
            data_merged = pd.merge(data_ids, data2, on='SERIAL NUMBER')
            data_grouped = data_merged.groupby(["YEAR", "VIOLATION CODE"])["FACILITY ID"].value_counts()
            years = data_grouped.index.unique(level='YEAR').to_list()
            dataframe_list = []
            for year in years:
                dic = {}
                df = data_grouped[year]
                for code in df.index.unique(level='VIOLATION CODE').to_list():
                    count = df[code].sum()
                    dic[code] = count
                code_count = pd.DataFrame(list(dic.items()), columns = ['VIOLATION CODE', 'NUMBER OF FACILITIES'])
                code_count.sort_values(by=['NUMBER OF FACILITIES'], ascending=False, inplace= True)
                code_count = code_count.reset_index(drop=True)
                code_count["YEAR"] = year
                dataframe_list.append(code_count)  
            final_df = pd.concat(dataframe_list, ignore_index=True)
            
            # Segregates by year
            def violsPerTypePerYear():
                df_year_list = []
                for year in years:
                    df_year = final_df[final_df['YEAR'] == year]
                    df_year = df_year.reset_index(drop=True)
                    df_year_list.append(df_year)    
                return df_year_list
            
            final_year_list = violsPerTypePerYear()
            return final_year_list, str(final_year_list)
        
        except:
            error = 'These datasets do not have SERIAL NUMBER or FACILITY ID as columns. Operations cannot be implemented.'
            return error

    def corrViolations(self, data1, data2):
        try:
            df1 = data1[["OWNER ID", "SERIAL NUMBER", "Zip Codes"]]
            df2 = data2[["SERIAL NUMBER"]]
            dff2 = pd.DataFrame(df2["SERIAL NUMBER"].value_counts()).reset_index() #Frequency of each serial number
            dff2.columns=["SERIAL NUMBER", "COUNT"]
            data_m = pd.merge(df1, dff2, on='SERIAL NUMBER') #Merge the 'inspections' dataset with the serial number count
            
            #Get the number of violations for each zip code
            zip_codes = data_m["Zip Codes"].unique()
            dic = {}
            for i in zip_codes:
                ds = data_m[data_m["Zip Codes"] == i]
                dic[i] = ds["COUNT"].sum()
            dss = pd.DataFrame(list(dic.items()), columns = ['zip_codes', 'prod_viol_count'])

            #Get the number of owner ids for each zip code
            zip_codes1 = data1["Zip Codes"].unique()
            dic2 = {}
            for i in zip_codes1:
                dc = data1[data1["Zip Codes"] == i]
                dic2[i] = dc["OWNER ID"].count()
            dcc = pd.DataFrame(list(dic2.items()), columns = ['zip_codes', 'owner_count'])
            
            data_f = pd.merge(dss, dcc, on='zip_codes') #Merge the datasets
            return data_f
        
        except:
            error = 'These datasets do not have SERIAL NUMBER, OWNER ID or Zip Codes as columns. Operations cannot be implemented.'
            return error