import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns

class Main:

    def __init__(self):
        self.df = pd.read_csv("HCMST.csv", low_memory=False)
        logging.info("loading csv as dataframe")
        self.df_numeric = pd.DataFrame()
        self.df_categorical = pd.DataFrame()
        self.df_categorical_encoded = pd.DataFrame()
        self.df_numeric_encoded = pd.DataFrame()

    def log_config(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler("clean_data.log", "w")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)

    def clean_data(self):
        logging.info(f"loading dataframe")
        # select only columns of interest
        self.df_numeric = self.df[['caseid_new', 'ppagecat', 'ppincimp']]
        print(self.df_numeric.head())
        self.df_categorical = self.df[['ppgender', 'ppeducat', 'ppwork',
                                       'pppartyid3', 'ppreg9',
                                       'ppmarit', 'q24_met_online',
                                       'relationship_quality']]
        print(self.df_categorical.head())
        # encode categorical
        self.df_numeric_encoded = pd.get_dummies(self.df_numeric)
        print(self.df_numeric_encoded)
        self.df_categorical_encoded = pd.get_dummies(self.df_categorical)
        print(self.df_categorical_encoded)

        # cleaning null
        print(self.df_categorical.isnull().sum())


    def viz(self):
        pass
        # test normalization
        # print(self.clean_df.isnull().sum())
        # self.clean_df = self.clean_df.dropna(how='any', axis=0)
        # print(self.clean_df.isnull().sum())
        # fig, axs = plt.subplots(figsize=(6, 7))
        # plt.xlabel('Gender', ha='center')
        # plt.ylabel('Values', ha='center')
        # plt.xticks(ha='center')
        # plt.title('Gender Population')
        # axs.legend()
        # plt.bar(x=['female', 'male'], height=self.clean_df['gender'].value_counts())
        # plt.show()

        # sns.regplot(x=self.encoded_df['age'], y=self.encoded_df['income'], data=self.df_orig_short)
        # plt.tight_layout()
        # plt.show()






def main():
    m = Main()
    m.log_config()
    m.clean_data()
    m.viz()


if __name__ == '__main__':
    main()
