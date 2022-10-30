import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm
import scipy
pd.options.display.max_columns = None
import warnings
warnings.filterwarnings("ignore")
class Main:

    def __init__(self):
        logging.debug("loading .csv file as dataframe 1")
        self.df1 = pd.read_csv("HCMST.csv", low_memory=False)
        logging.debug("grab only the columns that are unique to csv")
        self.df1 = self.df1[['caseid_new', 'hhinc', 'pppartyid3', 'relationship_quality',
                             'q24_met_online', 'papreligion']].copy()
        logging.debug("loading .dta file as dataframe 2")
        self.df2 = pd.read_stata('HCMST2017.dta')
        logging.debug("merging dataframes")
        self.full_df = pd.concat([self.df1, self.df2], axis=1)

        self.df_numeric = pd.DataFrame()
        self.df_numeric_encoded = pd.DataFrame()
        self.df_categorical = pd.DataFrame()
        self.df_categorical_encoded = pd.DataFrame()


    def log_config(self) -> None:
        """
        setup logging config
        Return: None
        """
        logger = logging.getLogger()
        logger.setLevel(logging.ERROR)
        # TODO remove in final ipynb submission
        fh = logging.FileHandler("clean_data.log", "w")
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)

    def clean_data(self):
        logging.debug("paring down full dataframe into relevant columns")
        # select only columns of interest
        self.df_numeric = self.full_df[['ppage', 'ppagecat', 'hhinc']].rename(
            {'ppage': 'age', 'ppagecat': 'cat_age'}, axis=1)

        self.df_categorical = self.full_df[['ppgender', 'ppeducat', 'ppincimp',
                                            'ppwork', 'pppartyid3', 'ppreg9',
                                            'ppmarit', 'q24_met_online',
                                            'papreligion', 'relationship_quality']].rename(
            columns={'ppgender': 'gender',
                     'ppeducat': 'educ',
                     'ppincimp': "incomecat",
                     'ppwork': 'job_status',
                     'pppartyid3': 'political_aff',
                     'ppreg9': 'region',
                     'papreligion': 'religion',
                     'w6_otherdate_app_2': 'app_used',
                     'ppmarit': 'marital_status',
                     'q24_met_online': 'met_online'})
        # self.df_numeric.fillna(0, inplace=True)
        self.df_numeric['hhinc'] = self.df_numeric['hhinc'].astype(int)
        # self.df_numeric['age'] = self.df_numeric['age'].astype(int)
        self.df_numeric_encoded = pd.get_dummies(self.df_numeric)
        self.df_categorical_encoded = pd.get_dummies(self.df_categorical)
        # print(self.df_categorical_encoded.head())
        # print(self.df_numeric_encoded.head())
        # print(self.df_categorical_encoded.describe())
        # print(self.df_numeric_encoded.describe())
        # cleaning nulls
        # print(self.df_categorical.isnull().sum())
        # print(self.df_numeric.isnull().sum())
        print(self.df_numeric.dtypes)
        print(self.df_categorical.dtypes)

    def gender(self):
        # Visualize gender representative
        female_count = self.df_categorical['gender'].value_counts()['Female']
        male_count = self.df_categorical['gender'].value_counts()['Male']
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
        big_df = pd.concat([self.df_numeric, self.df_categorical], axis=1)
        t1 = big_df.pivot_table(values=["hhinc"], index=["region"], aggfunc=np.mean)
        # print(t1)
        t2 = big_df.pivot_table(values=["id"], index=["marital_status", "met_online"], aggfunc='count')
        # print(t2)
        t3 = big_df.pivot_table(values=["id"], index=["political_aff", "cat_age"], aggfunc='count')
        print(t1)

        # interesting question, what season or month did you meet your significant other?
        # TODO: viz of map/region, pull month met data, pairpolt, (ggqqplot) normalize plot for numeric values
        # income, pivot_tables, regplot, avg age vs income, missing data?

    def age(self):
        age_col_df = self.df_numeric_encoded.iloc[2:, :10]
        age_col_df.drop(labels='id', axis=1, inplace=True)
        age_col_df.drop(labels='age', axis=1, inplace=True)
        age_col_df.drop(labels='hhinc', axis=1, inplace=True)
        count_df = pd.DataFrame({'count': age_col_df.sum()})
        count_df.rename(index={'cat_age_18-24': '18-24', 'cat_age_25-34': '25-34',
                               'cat_age_35-44': '35-44', 'cat_age_45-54': '45-54',
                               'cat_age_55-64': '55-64', 'cat_age_65-74': '65-74',
                               'cat_age_75+': '75+'}, inplace=True)
        count_df.reset_index(inplace=True)
        count_df.rename(columns={'index': 'age'}, inplace=True)
        sns.barplot(x='age', y='count', data=count_df, palette='hls')
        plt.show()

    def relplot(self):
        """
        plot pairwise relationships
        """
        sns.relplot(x='age', y='hhinc', kind='line', data=self.df_numeric)
        # sns.pairplot(self.df_numeric, x_vars=['age'], y_vars=['hhinc'], palette='hls', hue='hhinc', height=5)
        plt.show()

    def ols(self):
        model = sm.OLS(self.df_categorical_encoded['met_online_met offline'], self.df_numeric['hhinc'])
        results = model.fit()
        print(results.params)
        print(results.summary())

    def shapiro(self):
        np.random.seed(1)
        print(scipy.stats.shapiro(self.df_categorical_encoded['political_aff_democrat']))
        print(scipy.stats.shapiro(self.df_categorical_encoded['political_aff_republican']))
        print(scipy.stats.shapiro(self.df_categorical_encoded['political_aff_other'].sample(n=500)))

    def qqplot(self):
        sm.qqplot(data=self.df_categorical['political_aff'], line='45')
        plt.show()

if __name__ == '__main__':
    m = Main()
    m.log_config()
    m.clean_data()
    # general stats EDA
    m.gender()
    m.political()
    # m.pivot()
    # m.age()
    # m.pair()
    m.ols()
    m.shapiro()
    m.qqplot()
