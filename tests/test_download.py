import datetime
import json
import traceback
import pandas as pd
from pyesios import ESIOS
import pytest
import os
import numpy as np

token = os.getenv("ESIOS_API_TOKEN")


esios = ESIOS(token)

indicators_ = [632]

names = esios.get_names(indicators_)

indicators_df = {
    "indicators" : indicators_,
    "names":names,
}

dict_name_ind = {k:v for k,v in zip(indicators_, names)}

list_indicator = ['Asignación Banda de regulación secundaria a subir']
# If you have multiple indicators_df dictionaries, you can add them to this list
indicators_dfs = [indicators_df]

@pytest.mark.parametrize(
    "indicators_df,name",
    [(indicators_df, name) for indicators_df in indicators_dfs for name in list_indicator],
)
def test_indicator(indicators_df, name):
    assert indicators_df["names"] == name




start_ = "01-01-2017T00"
end_ = "01-01-2018T00"

df_test = pd.read_csv("tests/test_data/export_SecondaryReserveAllocationAUpward_2023-10-24_18 32.csv", sep=";")
df_test[list_indicator[0]] = df_test["value"]
@pytest.mark.parametrize(
    "indicators_, start_date, end_date",
    [(indicators_, start_, end_)],
)
def test_data_fecth(indicators_, start_date, end_date):
    start_date = datetime.datetime.strptime(start_, "%d-%m-%YT%H")
    end_date = datetime.datetime.strptime(end_, "%d-%m-%YT%H")

    dfmul = esios.get_multiple_series(indicators_, start_date, end_date)

    ff_df = dfmul[0][0]
    for i in range(len(dfmul[0])):
        df = dfmul[0][i]
        if type(df) == type(None):
            continue
        cols_to_use = list(df.columns.difference(ff_df.columns))
        if len(cols_to_use) == 0:
            continue
        cols_to_use.append([f for f in df.columns if "datetime" in f][0])
        ff_df = ff_df.merge(
            df[cols_to_use], on="datetime", how="left"
        ).reset_index(drop=True)


    for ind in indicators_:
        ind_name = dict_name_ind[ind]
        assert np.array_equal(ff_df[ind_name].values, df_test[ind_name].values)


