"""
Example to use ESIOS
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
from ESIOS import *
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # Request arguments
    end_ = datetime.datetime.today()
    start_ = end_ - datetime.timedelta(days=30)

    # The token is unique: You should ask for yours to: Consultas Sios <consultasios@ree.es>

    token = '615e6d8c80629b8eef25c8f3d0c36094e23db4ed50ce5458f3462129d7c46dba'
    esios = ESIOS(token)

    # esios.save_indicators_table()

    #    indicators_ = [600, 672, 673, 674, 675, 676, 677, 680, 681, 682, 683, 767, 1192, 1193, 1293]
    indicators_ = list()
    # indicators_.append(682)  # Precio de Regulación Secundaria subir
    # indicators_.append(683)  # Precio de Regulación Secundaria bajar
    indicators_.append(600)  # Precio mercado SPOT Diario
    # indicators_.append(1293)  # Demanda real
    indicators_.append(551)  # Eólica T.Real
    # names = esios.get_names(indicators_)
    df_list, names = esios.get_multiple_series(indicators_, start_, end_)

    df_merged = esios.merge_series(df_list, names)  # merge the DataFrames into a single one

    df = df_merged[names]  # get the actual series and neglect the rest of the info

    # plot
    fig, ax1 = plt.subplots()

    df[names[0]].plot(ax=ax1)  # demand
    ax1.set_xlabel('time')
    ax1.set_ylabel('MW')

    # secondary axis
    ax2 = ax1.twinx()
    df[names[0::]].plot(ax=ax2)  # others
    ax2.set_ylabel('€')

plt.show()
