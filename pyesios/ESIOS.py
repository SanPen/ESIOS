"""
ESIOS: API to access the Spanish electricity market data in pandas format

Copyright 2016 Santiago Peñate Vera <santiago.penate.vera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import json
import pickle
import urllib
import urllib.request
import warnings
import numpy as np
import pandas as pd

from pyesios.utils import time_diff_in_group
ALLOWED_TIMEGROUPS = ["minutes5", "minutes10", "minutes15", "hour", "day", "month", "year"]

class PandasDataBase:
    """
    This class saves the downloaded data locally and expends it
        incrementally upon download calls from esios
    """

    def __init__(self):
        print()


class ESIOS(object):
    def __init__(self, token):
        """
        Class constructor
        :param token: string given by the SIOS to you when asked to:
            Consultas Sios <consultasios@ree.es>
        """
        # The token is unique: You should ask for yours to:
        #   Consultas Sios <consultasios@ree.es>
        if token is None:
            raise ValueError(
                    "The token is unique: You should ask for yours to:"
                    "Consultas Sios <consultasios@ree.es>"
                )
        self.token = token

        self.allowed_geo_id = [3, 8741]  # España y Peninsula

        # standard format of a date for a query
        self.dateformat = "%Y-%m-%dT%H:%M:%S"

        # dictionary of available series
        self.__offer_indicators_list = list()
        self.__analysis_indicators_list = list()
        self.__indicators_name__ = dict()
        self.available_series = dict()

        print("Getting the indicators...")
        self.available_series = self.get_indicators()

    def __get_headers__(self):
        """
        Prepares the CURL headers
        :return: A dictionary with the headers.
        :rtype: dict
        """
        # Prepare the arguments of the call
        headers = dict()
        headers[
            "Accept"
        ] = "application/json; application/vnd.esios-api-v1+json"
        headers["Content-Type"] = "application/json"
        headers["Host"] = "api.esios.ree.es"
        headers["x-api-key"] = self.token
        headers["Cookie"] = ""
        return headers

    def get_indicators(self):
        """
        Get the indicators and their name.
        The indicators are the indices assigned to the available data series
        :return:
        """
        fname = "indicators.pickle"
        import os

        if os.path.exists(fname):
            # read the existing indicators file
            with open(fname, "rb") as input_file:
                (
                    all_indicators,
                    self.__indicators_name__,
                    self.__offer_indicators_list,
                    self.__analysis_indicators_list,
                ) = pickle.load(input_file)
        else:
            # create the indicators file querying the info to ESIOS
            """
            curl "https://api.esios.ree.es/offer_indicators" -X GET
            -H "Accept: application/json; application/vnd.esios-api-v1+json"
            -H "Content-Type: application/json"
            -H "Host: api.esios.ree.es"
            -H "Authorization:
            Token
            token=\"5c7f9ca844f598ab7b86bffcad08803f78e9fc5bf3036eef33b5888877a04e38\""
            -H "Cookie: "
            """
            all_indicators = dict()
            self.__indicators_name__ = dict()

            # This is how the URL is built
            url = "https://api.esios.ree.es/offer_indicators"

            # Perform the call
            req = urllib.request.Request(url, headers=self.__get_headers__())
            with urllib.request.urlopen(req) as response:
                try:
                    json_data = response.read().decode("utf-8")
                except Exception as e:
                    print(e)
                    json_data = response.readall().decode("utf-8")

                result = json.loads(json_data)

            # fill the dictionary
            indicators = dict()
            self.__offer_indicators_list = list()
            for entry in result["indicators"]:
                name = entry["name"]
                id_ = entry["id"]
                indicators[name] = id_
                self.__indicators_name__[id_] = name
                self.__offer_indicators_list.append([name, id_])

            all_indicators["indicadores de curvas de oferta"] = indicators

            """
            curl "https://api.esios.ree.es/indicators" -X GET
            -H "Accept: application/json; application/vnd.esios-api-v1+json"
            -H "Content-Type: application/json" -H "Host: api.esios.ree.es"
            -H "Authorization: Token token=\"your_token\""
            -H "Cookie: "
            """
            url = "https://api.esios.ree.es/indicators"

            req = urllib.request.Request(url, headers=self.__get_headers__())
            with urllib.request.urlopen(req) as response:
                try:
                    json_data = response.read().decode("utf-8")
                except Exception as e:
                    print(e)
                    json_data = response.readall().decode("utf-8")
                result = json.loads(json_data)

            # continue filling the dictionary
            indicators = dict()
            self.__analysis_indicators_list = list()
            for entry in result["indicators"]:
                name = entry["name"]
                id_ = entry["id"]
                indicators[name] = id_
                self.__indicators_name__[id_] = name
                self.__analysis_indicators_list.append([name, id_])

            all_indicators["indicadores de análisis "] = indicators

            # save the indictators
            with open(fname, "wb") as output_file:
                dta = [
                    all_indicators,
                    self.__indicators_name__,
                    self.__offer_indicators_list,
                    self.__analysis_indicators_list,
                ]
                pickle.dump(dta, output_file)

        return all_indicators

    def get_names(self, indicators_list):
        """
        Get a list of names of the given indicator indices
        :param indicators_list:
        :return:
        """
        names = list()
        for i in indicators_list:
            names.append(self.__indicators_name__[i])

        return np.array(names)

    def save_indicators_table(self, fname="indicadores.xlsx"):
        """
        Saves the list of indicators in an excel file for easy consultation
        :param fname:
        :return:
        """
        data = self.__offer_indicators_list + self.__analysis_indicators_list

        df = pd.DataFrame(data=data, columns=["Nombre", "Indicador"])

        df.to_excel(fname)

    def __get_query_json__(self, indicator, start_str, end_str, timegroup="hour", **options):
        """
        Get a JSON series
        :param indicator: series indicator
        :param start_str: Start date
        :param end_str: End date
        :return:
        """
        timegroup = options.pop("groupby", timegroup)

        if timegroup not in ALLOWED_TIMEGROUPS:
            warn_msg = f"{timegroup} not in allowed groups: {ALLOWED_TIMEGROUPS}. \n Defaulting to hour"
            warnings.warn(warn_msg)
            timegroup = "hour"

        # This is how the URL is built

        #  https://www.esios.ree.es/es/analisis/1293?vis=2&start_date=21-06-2016T00%3A00&end_date=21-06-2016T23%3A50&compare_start_date=20-06-2016T00%3A00&groupby=minutes10&compare_indicators=545,544#JSON
        url = (
            "https://api.esios.ree.es/indicators/"
            + indicator
            + "?start_date="
            + start_str
            + "&end_date="
            + end_str
            + "&groupby="
            + timegroup
        )
        for param, value in options.items():
            url += f"&{param}={value}"

        result = None
        req = urllib.request.Request(url, headers=self.__get_headers__())
        with urllib.request.urlopen(req) as response:
            try:
                json_data = response.read().decode("utf-8")
            except Exception as e:
                print(e)
                json_data = response.readall().decode("utf-8")
            result = json.loads(json_data)
        return result

    def _get_data(self, indicator, start, end, timegroup="hour", **options):
        """

        :param indicator: Series indicator
        :param start: Start date
        :param end: End date
        :return:
        """


        if isinstance(indicator, int):
            indicator = str(indicator)

        # get the JSON data
        result = self.__get_query_json__(
            indicator, start, end, timegroup=timegroup,**options
        )

        # transform the data
        d = result["indicator"]["values"]  # dictionary of values
        if len(d) > 0:
            df = pd.DataFrame(d)

            df["datetime_utc"] = pd.to_datetime(
                df["datetime_utc"]
            )  # convert to datetime

            df = df.set_index("datetime_utc")  # Set the index column

            # del df.index.name  # to avoid the index name bullshit

            return df
        else:
            return None

    def get_data(self, indicator, start, end, timegroup="hour",**options):
        """

        :param indicator: Series indicator
        :param start: Start date
        :param end: End date
        :return:
        """
        # The API does not work with more than 2 years hourly data
        # Lets assume that the problem is with 2*365*24 data point
        # Wall to prevent the multiple year error
        N_max = 2*365*24

        # check types: Pass to string for the url
        if isinstance(start, datetime.datetime):
            start_str = start.strftime(self.dateformat)
        else:
            start_str = start
            start = datetime.datetime.strptime(start, "%d-%m-%YT%H")

        if isinstance(end, datetime.datetime):
            end_str = end.strftime(self.dateformat)
        else:
            end_str = end
            end = datetime.datetime.strptime(end, "%d-%m-%YT%H")



        time_diff = time_diff_in_group(start, end, timegroup)

        if time_diff>N_max:
            # The dates are distribuited per max two years.
            # This is because the API breaks when asking more than two years at a time.

            # Create a date range with a frequency of 2 years
            date_range = pd.date_range(start=start_str, end=end_str, freq='1AS', inclusive="both")
            date_range = [f for f in date_range]
            if start<date_range[0]:
                date_range.insert(0, start)
            else:
                date_range[0] = start
            if end>date_range[-1]:
                date_range.append(end)
            else:
                date_range[-1] = end

            # Create a list to store the date pairs
            date_pairs = []
            all_dfs = []
            # Loop over the date range
            for i in range(len(date_range)-1):
                # Add the date pair to the list
                start_str = date_range[i].strftime(self.dateformat)
                # The API is not workinf for 2023 on
                # https://github.com/SanPen/ESIOS/issues/10
                if date_range[i+1].year>2022:
                    date_range[i+1] = date_range[i+1].replace(year=2022)
                    date_range[i+1] = date_range[i+1].replace(month=12)
                    # Set the time to the last minute of the day
                    date_range[i+1] = date_range[i+1].replace(hour=23, minute=59, second=59)
                    # Convert the datetime object back to a string
                    date_str = date_range[i+1].strftime("%Y-%m-%dT%H:%M:%S")

                end_str = date_range[i+1].strftime(self.dateformat)
                all_dfs.append(self._get_data(indicator, start_str, end_str,timegroup=timegroup, **options))
                date_pairs.append((date_range[i], date_range[i+1]))
            return pd.concat(all_dfs, ignore_index=True)
        else:
            return self._get_data(indicator, start_str, end_str,timegroup=timegroup, **options)

    def get_multiple_series(self, indicators, start, end, timegroup="hour",**options):
        """
        Get multiple series data
        :param indicators: List of indicators
        :param start: Start date
        :param end: End date
        :return:
        """

        df_list = list()
        names = list()
        for indicator in indicators:
            name = self.__indicators_name__[indicator]
            names.append(name)

            print("Parsing " + name)

            # download the series in a DataFrame
            df_new = self.get_data(indicator, start, end, timegroup=timegroup, **options)

            if df_new is not None:
                # the default name for the series is 'value' we must change it
                df_new.rename(columns={"value": name}, inplace=True)

                # save
                file_handler = open(str(indicator) + ".pkl", "wb")
                pickle.dump(df_new, file_handler)
                file_handler.close()

            df_list.append(df_new)

        return df_list, names

    @staticmethod
    def merge_series(df_list, names, pandas_sampling_interval="1H"):
        """
        Merge a list of separately downloaded DataFrames into a single one
        :param df_list: List of ESIOS downloaded DataFrames
        :param names: list with the names of the main series of each DataFrame
        :param pandas_sampling_interval: Pandas interval for resampling
            (1 hour as default)
        :return: Merged DataFrame
        """

        merged_df = None
        print("merging")
        for df, name in zip(df_list, names):
            # print(name)

            if df is not None:
                if name == "Precio mercado SPOT Diario":
                    df = df[df.geo_id == 3]  # pick spain only

                dfp = df[[name]].astype(
                    float
                )  # .resample(pandas_sampling_interval).pad()

                if merged_df is None:
                    merged_df = dfp
                else:
                    merged_df = merged_df.join(dfp)
            else:
                print(name, ": The dataFrame is None")

        return merged_df
