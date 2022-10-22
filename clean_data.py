import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm


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
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler("clean_data.log", "w")
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)

    def clean_data(self):
        logging.info(f"loading dataframe")
        # select only columns of interest
        self.df_numeric = self.df[['caseid_new', 'ppagecat', 'ppincimp']].rename({'caseid_new': 'id',
                                                                                  'ppagecat': 'age',
                                                                                  'ppincimp': 'income'}, axis=1)
        self.df_categorical = self.df[['ppgender', 'ppeducat', 'ppwork',
                                       'pppartyid3', 'ppreg9',
                                       'ppmarit', 'q24_met_online',
                                       'relationship_quality']].rename(
            columns={'ppgender': 'gender', 'ppeducat': 'educ',
                     'ppwork': 'job_status', 'pppartyid3': 'political_aff', 'ppreg9': 'region',
                     'ppmarit': 'marital_status',
                     'q24_met_online': 'met_online'})
        self.df_numeric_encoded = pd.get_dummies(self.df_numeric)
        self.df_categorical_encoded = pd.get_dummies(self.df_categorical)
        # print(self.df_categorical_encoded.head())
        # print(self.df_numeric_encoded.head())
        # print(self.df_categorical_encoded.describe())
        # print(self.df_numeric_encoded.describe())
        # cleaning null
        # print(self.df_categorical.isnull().sum())
        # print(self.df_numeric.isnull().sum())

    def gender(self):
        # Visualize gender representative
        female_count = self.df_categorical_encoded['gender_female'].value_counts()[
            self.df_categorical_encoded['gender_female'] == 1].values[0]
        male_count = self.df_categorical_encoded['gender_female'].value_counts()[
            self.df_categorical_encoded['gender_female'] == 1].values[1]
        gender = pd.DataFrame({'gender': ['female', 'male'], 'count': [female_count, male_count]})
        sns.barplot(x='gender', y='count', data=gender, palette='hls')
        plt.show()

    def political(self):
        # Visualize political representative
        democrat_count = self.df_categorical_encoded['political_aff_democrat'].value_counts()[1]
        republican_count = self.df_categorical_encoded['political_aff_republican'].value_counts()[1]
        other_count = self.df_categorical_encoded['political_aff_other'].value_counts()[1]
        party_aff = pd.DataFrame({'political_party': ['democrat', 'republican', 'other'],
                                  'count': [democrat_count, republican_count, other_count]})
        sns.barplot(x='political_party', y='count', data=party_aff, palette="hls")
        plt.xlabel('Political Party Affiliation')
        plt.ylabel('Count')
        plt.title('Political Party Affiliation Representation')
        plt.legend()
        plt.show()

    def pivot(self):
        logging.info("creating pivot tables")
        full_df = pd.concat([self.df_numeric, self.df_categorical], axis=1)
        t1 = full_df.pivot_table(values=["id"], index=["region", "income"], aggfunc='count')
        # print(t1)
        t2 = full_df.pivot_table(values=["id"], index=["marital_status", "met_online"], aggfunc='count')
        # print(t2)
        t3 = full_df.pivot_table(values=["id"], index=["political_aff", "age"], aggfunc='count')
        print(t3)

        # interesting question, what season or month did you meet your significant other?
        #TODO: viz of map/region, pull month met data, pairpolt, (ggqqplot) normalize plot for numeric values
        # income, pivot_tables, regplot, avg age vs income, missing data?

    def age(self):
        age_col_df = self.df_numeric_encoded.iloc[2:, :8]
        age_col_df.drop(labels='id', axis=1, inplace=True)
        count_df = pd.DataFrame({'count':  age_col_df.sum()})
        count_df.rename(index={'cat_age_18-24':'18-24','cat_age_25-34':'25-34',
                               'cat_age_35-44':'35-44','cat_age_45-54':'45-54',
                               'cat_age_55-64':'55-64','cat_age_65-74':'65-74',
                               'cat_age_75+':'75+'}, inplace=True)
        count_df.reset_index(inplace=True)
        count_df.rename(columns={'index': 'age'}, inplace=True)
        sns.barplot(x='age', y='count', data=count_df, palette='hls')
        plt.show()


    def pair(self):
        sns.pairplot(self.df_numeric_encoded)




if __name__ == '__main__':
    m = Main()
    m.log_config()
    m.clean_data()
    m.gender()
    m.political()
    m.pivot()
    m.age()
    # m.pair()
