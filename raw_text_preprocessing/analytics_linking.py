import pandas as pd

an = pd.read_stata('data/bran.sas7bdat')

an.to_csv('an.csv')