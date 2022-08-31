import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# This class creates the graphic for the client requirement of the number of establishments that commited a type of violation
class Graphics:
    
    # Creates the graphic for the client requirement of the number of establishments that commited a type of violation
    def violsPerTypeGraph(self, list_dfs):
        
        # Splits a dataframe in four
        def splitDataFrame(data):
            ranges = np.array_split(range(data.shape[0]+1), 4)
            list_data = []
            for ran in ranges:
                start = ran[0]
                end = ran[-1]
                list_data.append(data.loc[start:end])
            return list_data

        for df in list_dfs:
            year = df['YEAR'][0]
            df1 = splitDataFrame(df)[0]
            df2 = splitDataFrame(df)[1]
            df3 = splitDataFrame(df)[2]
            df4 = splitDataFrame(df)[3]

            fig, ax = plt.subplots(2,2, dpi=100)
            sns.barplot(x='NUMBER OF FACILITIES', y = 'VIOLATION CODE', data = df1, palette="Blues_d", ax=ax[0,0]).set_title("Number of establishments that have \n committed violations, " + str(year), fontsize=8)
            sns.barplot(x='NUMBER OF FACILITIES', y = 'VIOLATION CODE', data = df2, palette="Blues_d", ax=ax[0,1]).set_title("Number of establishments that have \n committed violations, " + str(year), fontsize=8)
            sns.barplot(x='NUMBER OF FACILITIES', y = 'VIOLATION CODE', data = df3, palette="Blues_d", ax=ax[1,0]).set_title("Number of establishments that have \n committed violations, " + str(year), fontsize=8)
            sns.barplot(x='NUMBER OF FACILITIES', y = 'VIOLATION CODE', data = df4, palette="Blues_d", ax=ax[1,1]).set_title("Number of establishments that have \n committed violations, " + str(year), fontsize=8)

            ax[0,0].tick_params(labelsize=4)
            ax[0,1].tick_params(labelsize=4)
            ax[1,0].tick_params(labelsize=4)
            ax[1,1].tick_params(labelsize=4)

            ax[0,0].set_ylabel('Violation code types', fontsize=6) 
            ax[0,1].set_ylabel('Violation code types', fontsize=6) 
            ax[0,0].set_xlabel('Number of establishments', fontsize=6)
            ax[0,1].set_xlabel('Number of establishments', fontsize=6)
            ax[1,0].set_ylabel('Violation code types', fontsize=6) 
            ax[1,1].set_ylabel('Violation code types', fontsize=6) 
            ax[1,0].set_xlabel('Number of establishments', fontsize=6)
            ax[1,1].set_xlabel('Number of establishments', fontsize=6)

            plt.tight_layout()
            plt.close(fig)
            return fig
    
    # Creates the graphic for the client requirement of the correlation between zip code and violations per vendor
    def corrViolationsGraph(self, data_in):
        fig, ax = plt.subplots(1,1, dpi=100)
        plot = sns.scatterplot(data_in.iloc[:, 1], data_in.iloc[:, 2]).set_title("Correlation between number of owners and number of violations per zip code", fontsize=8)
        ax.tick_params(labelsize=6)
        ax.set_xlabel('Number of violations per zip code', fontsize=7) 
        ax.set_ylabel('Number of vendors that have committed violations per zip code', fontsize=7)
        
        plt.tight_layout()
        fig = plot.get_figure()
        plt.close(fig)
        return fig    