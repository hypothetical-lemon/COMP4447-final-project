# module to clean up the data from HCMST.csv
import pandas as pd
import logging


def log_config():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("clean_data.log", "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)


# load CSV
def load_data():
    df = pd.read_csv("HCMST.csv", low_memory=False)
    logging.info("loading csv as dataframe")
    return df


def clean_data(df):
    logging.info(f"loading dataframe")
    # select only columns of interest
    df_short = df[["caseid_new", "ppgender", "ppagecat",
                   "ppeducat", "ppwork", "ppincimp",
                   "ppmarit", "ppreg9", "q24_met_online",
                   "pppartyid3", "relationship_quality"]]
    logging.info("cleaning data")
    clean_df = pd.DataFrame()
    logging.debug("add Case ID")
    clean_df['case_id'] = df_short['caseid_new']
    logging.debug("add Gender")
    clean_df['gender'] = df_short['ppgender'].replace(["male", "female"], [0, 1])
    logging.debug("add Age Category")
    clean_df['age'] = df_short['ppagecat'].replace(["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"],
                                                   [0, 1, 2, 3, 4, 5, 6])
    logging.debug("add Education Level")
    clean_df["educ"] = df_short['ppeducat'].replace(
        ["less than high school", "high school", "some college", "bachelor's degree or higher"], [0, 1, 2, 3])
    logging.debug("add Employment Status")
    clean_df["work"] = df_short['ppwork'].replace(
        ["not working - on temporary layoff from a job", "not working - looking for work", "not working - other",
         "working - self-employed", "not working - disabled", "not working - retired", "working - as a paid employee"],
        [0, 1, 2, 3, 4, 5, 6])
    logging.debug("add Household Income")
    clean_df["income"] = df_short['ppincimp'].replace(
        ["less than $5,000", "$5,000 to $7,499", "$7,500 to $9,999", "$10,000 to $12,499", "$12,500 to $14,999",
         "$15,000 to $19,999", "$20,000 to $24,999", "$25,000 to $29,999", "$30,000 to $34,999", "$35,000 to $39,999",
         "$40,000 to $49,999", "$50,000 to $59,999", "$60,000 to $74,999", "$75,000 to $84,999", "$85,000 to $99,999",
         "$100,000 to $124,999", "$125,000 to $149,999", "$150,000 to $174,999", "$175,000 or more"],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    logging.debug("add Marital Status")
    clean_df["marital"] = df_short['ppmarit'].replace(
        ["separated", "widowed", "divorced", "living with partner", "never married", "married"], [0, 1, 2, 3, 4, 5])
    logging.debug("add Region")
    clean_df["region"] = df_short['ppreg9'].replace(
        ["east-south central", "new england", "mountain", "west-north central", "west-south central", "mid-atlantic",
         "east-north central", "pacific", "south atlantic"], [0, 1, 2, 3, 4, 5, 6, 7, 8])
    logging.debug("add Met Online")
    clean_df["met_online"] = df_short["q24_met_online"].replace(["met offline", "met online", r'^\s*$'],
                                                                [False, True, None])
    logging.debug("add Political Party")
    clean_df["poli_party"] = df_short["pppartyid3"].replace(["other", "republican", "democrat"], [0, 1, 2])
    logging.debug("add Relationship Quality")
    clean_df["quality"] = df_short["relationship_quality"].replace(
        ["very poor", "poor", "fair", "good", "excellent", r'^\s*$'], [0, 1, 2, 3, 4, None])
    print(clean_df.head(10))


def main():
    log_config()
    csv_df = load_data()  # loads data from CSV format
    clean_data(csv_df)


if __name__ == '__main__':
    main()
