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
import pickle
plt.style.use('ggplot')

if __name__ == '__main__':
    # Request arguments
    # end_ = datetime.datetime.today()
    # start_ = end_ - datetime.timedelta(days=7)
    start_ = datetime.datetime(2016, 1, 1)
    end_ = datetime.datetime(2017, 1, 1)

    # The token is unique: You should ask for yours to: Consultas Sios <consultasios@ree.es>

    token = '5c7f9ca844f598ab7b86bffcad08803f78e9fc5bf3036eef33b5888877a04e38'
    esios = ESIOS(token)

    # esios.save_indicators_table()

    indicators_ = list()
    # indicators_.append(677)  # Precio Regulación Terciaria subir
    # indicators_.append(676)  # Precio Regulación Terciaria bajar
    indicators_.append(634)  # Precio Banda de regulación secundaria
    indicators_.append(600)  # Precio mercado SPOT Diario
    # indicators_.append(631)  # Requerimientos Banda de regulación secundaria a bajar
    # indicators_.append(630)  # Requerimientos Banda de regulación secundaria a subir

    # indicators_.append(1293)  # Demanda real
    # indicators_.append(550)  # Generación T.Real C.Combinado
    # indicators_.append(547)  # Generación T.Real carbón
    # indicators_.append(1297)  # Generación T.Real Cogeneración y resto
    # indicators_.append(554)  # Generación T.Real enlace balear
    # indicators_.append(551)  # Generación T.Real eólica
    # indicators_.append(548)  # Generación T.Real fuel-gas
    # indicators_.append(546)  # Generación T.Real hidráulica
    # indicators_.append(553)  # Generación T.Real intercambios
    # indicators_.append(549)  # Generación T.Real nuclear
    # indicators_.append(10206)  # Generación T.Real Solar
    # indicators_.append(552)  # Generación T.Real solar
    # indicators_.append(1295)  # Generación T.Real Solar fotovoltaica
    # indicators_.append(1294)  # Generación T.Real Solar térmica
    # indicators_.append(1296)  # Generación T.Real Térmica renovable

    names = esios.get_names(indicators_)
    df_list, names = esios.get_multiple_series(indicators_, start_, end_)

    # save
    file_handler = open(str(indicators_) + ".pkl", "wb")
    pickle.dump([indicators_, df_list, names], file_handler)
    file_handler.close()

    # merge the DataFrames
    df_merged = esios.merge_series(df_list, names)
    xls_path = '2016_data.xlsx'

    writer = pd.ExcelWriter(xls_path)
    for i, df in enumerate(df_list):
        df.to_excel(writer, str(indicators_[i]))
    df_merged[names].to_excel(writer, 'Merged')
    writer.save()

    # # plot
    # fig = plt.figure(figsize=(12, 8))
    #
    # ax1 = fig.add_subplot(211)
    # df[names[4]].plot(ax=ax1)  # demand
    # ax1.set_xlabel('time')
    # ax1.set_ylabel('MWh')
    #
    # # secondary axis
    # ax2 = fig.add_subplot(212, sharex=ax1)
    # df[names[0:4]].plot(ax=ax2)  # others
    # ax2.set_ylabel('€')
    #
    # for df, n in zip(df_list, names):
    #     print('name: ', n, df.columns.values)
    #     df[[n]].plot(marker='x')
    #
    # plt.show()
