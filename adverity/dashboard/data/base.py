import typing
import logging
import os

import pandas as pd
import pygal


class Plotter:
    def __init__(self, path):
        """ Loads data from file into pandas DataFrame """
        self._data = pd.read_csv(path)
        self._data["Date"] = pd.to_datetime(self._data.Date)

    @property
    def datasources(self) -> typing.List[str]:
        """ unique list of datasources """
        return list(self._data["Datasource"].unique())

    @property
    def campaigns(self) -> typing.List[str]:
        """ unique list of campaigns """
        return list(self._data["Campaign"].unique())

    @staticmethod
    def gen_name(datasources: typing.List[str], campaigns: typing.List[str]) -> str:
        """ generate name for chart  based on provided datasources and campaigns lists

        :param datasources: list of datasources names
        :param campaigns: list of campaigns names
        :returns: generated chart name
        """
        chunks = []
        chunks.append(
            ('Datasource "' + '", "'.join(datasources) + '"')
            if datasources
            else "All datasources"
        )
        chunks.append(
            ('Campaign "' + '", "'.join(campaigns) + '"')
            if campaigns
            else "All campaigns"
        )

        return "; ".join(chunks)

    @staticmethod
    def fill_datapoints(df: pd.DataFrame) -> pd.DataFrame:
        """ fills gaps in dates with 0

        :param df: dataframe
        :return: extended dataframe
        """
        min_date = df.index.min()
        max_date = df.index.max()

        if pd.isnull(min_date) or pd.isnull(max_date):
            raise ValueError

        date_range = pd.date_range(min_date, max_date)

        data = pd.DataFrame({"Date": date_range}).set_index("Date")

        return df.merge(data, on="Date", how="right").fillna(0).sort_values("Date")

    def plot(
        self, datasources: typing.List[str], campaigns: typing.List[str]
    ) -> typing.Union[str, bytes]:
        """ Generates uri containing encoded chart data


        :param datasources: list of datasources names
        :param campaigns: list of campaigns names
        :returns: uri encoded data
        """

        line_chart = pygal.Line()
        line_chart.title = self.gen_name(datasources, campaigns)
        # filtering
        df = self._data.copy()

        if datasources:
            df = df[df["Datasource"].isin(datasources)]

        if campaigns:
            df = df[df["Campaign"].isin(campaigns)]

        df = df.groupby("Date").agg({"Clicks": "sum", "Impressions": "sum"})

        try:
            merged = self.fill_datapoints(df)

        except ValueError:
            logging.warning("No data available")
        else:
            line_chart.x_labels = list(merged.index)
            line_chart.add("Clicks", list(merged["Clicks"]))
            line_chart.add("Impressions", list(merged["Impressions"]))

        return line_chart.render_data_uri()


path_to_datafile = os.path.join(os.path.dirname(__file__), "DAMKBAoDBwoDBAkOBAYFCw.csv")
data = Plotter(path_to_datafile)
