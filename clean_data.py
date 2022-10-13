import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns

class Main:

    def __init__(self):
        self.df = pd.read_csv("HCMST.csv", low_memory=False)
        logging.info("loading csv as dataframe")
        self.encoded_df = pd.DataFrame()
        self.df_orig_short = pd.DataFrame()

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
        self.df_orig_short = self.df[["caseid_new", "ppgender", "ppagecat",
                            "ppeducat", "ppwork", "ppincimp",
                            "ppmarit", "ppreg9", "q24_met_online",
                            "pppartyid3", "relationship_quality"]]
        logging.info("cleaning data")
        logging.debug("add Case ID")
        self.encoded_df['case_id'] = self.df_orig_short['caseid_new']
        logging.debug("add Gender")
        self.encoded_df['gender'] = self.df_orig_short['ppgender'].replace(
            ["male", "female"],
            [0, 1])
        logging.debug("add Age Category")
        self.encoded_df['age'] = self.df_orig_short['ppagecat'].replace(
            ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"],
            [0, 1, 2, 3, 4, 5, 6])
        logging.debug("add Education Level")
        self.encoded_df["educ"] = self.df_orig_short['ppeducat'].replace(
            ["less than high school", "high school", "some college",
             "bachelor's degree or higher"], [0, 1, 2, 3])
        logging.debug("add Employment Status")
        self.encoded_df["work"] = self.df_orig_short['ppwork'].replace(
            ["not working - on temporary layoff from a job",
             "not working - looking for work", "not working - other",
             "working - self-employed", "not working - disabled",
             "not working - retired", "working - as a paid employee"],
            [0, 1, 2, 3, 4, 5, 6])
        logging.debug("add Household Income")
        self.encoded_df["income"] = self.df_orig_short['ppincimp'].replace(
            ["less than $5,000", "$5,000 to $7,499", "$7,500 to $9,999",
             "$10,000 to $12,499", "$12,500 to $14,999",
             "$15,000 to $19,999", "$20,000 to $24,999", "$25,000 to $29,999",
             "$30,000 to $34,999", "$35,000 to $39,999",
             "$40,000 to $49,999", "$50,000 to $59,999", "$60,000 to $74,999",
             "$75,000 to $84,999", "$85,000 to $99,999",
             "$100,000 to $124,999", "$125,000 to $149,999",
             "$150,000 to $174,999", "$175,000 or more"],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
        logging.debug("add Marital Status")
        self.encoded_df["marital"] = self.df_orig_short['ppmarit'].replace(
            ["separated", "widowed", "divorced", "living with partner",
             "never married", "married"], [0, 1, 2, 3, 4, 5])
        logging.debug("add Region")
        self.encoded_df["region"] = self.df_orig_short['ppreg9'].replace(
            ["east-south central", "new england", "mountain",
             "west-north central", "west-south central", "mid-atlantic",
             "east-north central", "pacific", "south atlantic"],
            [0, 1, 2, 3, 4, 5, 6, 7, 8])
        logging.debug("add Met Online")
        self.encoded_df["met_online"] = self.df_orig_short["q24_met_online"].replace(
            ["met offline", "met online", r'^\s*$'],
            [False, True, None])
        logging.debug("add Political Party")
        self.encoded_df["poli_party"] = self.df_orig_short["pppartyid3"].replace(
            ["other", "republican", "democrat"], [0, 1, 2])
        logging.debug("add Relationship Quality")
        self.encoded_df["quality"] = self.df_orig_short["relationship_quality"].replace(
            ["very poor", "poor", "fair", "good", "excellent", r'^\s*$'],
            [0, 1, 2, 3, 4, None])
        # cleaning null
        # print(self.df.isnull().sum())
        print(self.encoded_df.isnull().sum())
        # TODO add merged df of original and cleaned



    def viz(self):
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

        sns.regplot(x=self.encoded_df['age'], y=self.encoded_df['income'], data=self.df_orig_short)
        plt.tight_layout()
        plt.show()






def main():
    m = Main()
    m.log_config()
    m.clean_data()
    m.viz()


if __name__ == '__main__':
    main()
