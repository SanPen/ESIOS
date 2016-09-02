from ESIOS import *
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # Request arguments
    start_ = '2015-12-01T00:00:01'
    end_ = '2015-12-31T23:59:00'

    # The token is unique: You should ask for yours to: Consultas Sios <consultasios@ree.es>

    token = '615e6d8c80629b8eef25c8f3d0c36094e23db4ed50ce5458f3462129d7c46dba'
    esios = ESIOS(token)

    # esios.save_indicators_table()

    #    indicators_ = [600, 672, 673, 674, 675, 676, 677, 680, 681, 682, 683, 767, 1192, 1193, 1293]
    indicators_ = list()
    indicators_.append(682)  # Precio de Regulación Secundaria subir
    indicators_.append(683)  # Precio de Regulación Secundaria bajar
    indicators_.append(600)  # Precio mercado SPOT Diario
    indicators_.append(1293)  # Demanda real
    names = esios.get_names(indicators_)
    dfmul, df_list, names = esios.get_multiple_series(indicators_, start_, end_)
    df = dfmul[names]  # get the actual series and neglect the rest of the info

    # plot
    fig, ax1 = plt.subplots()

    df[names[3]].plot(ax=ax1)  # demand
    ax1.set_xlabel('time')
    ax1.set_ylabel('MW')

    # secondary axis
    ax2 = ax1.twinx()
    df[names[0:3]].plot(ax=ax2)  # others
    ax2.set_ylabel('€')

    plt.show()