from ESIOS import *


if __name__ == '__main__':
    # Request arguments
    start_ = '2015-12-01T00:00:01'
    end_ = '2015-12-31T23:59:00'

    # The token is unique: You should ask for yours to: Consultas Sios <consultasios@ree.es>
    token = '5c7f9ca844f598ab7b86bffcad08803f78e9fc5bf3036eef33b5888877a04e38'

    esios = ESIOS(token, True)

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
    ax1.set_ylabel('€')

    # secondary axis
    ax2 = ax1.twinx()
    df[names[0:3]].plot(ax=ax2)  # others
    ax2.set_ylabel('€')

    plt.show()