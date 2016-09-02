# ESIOS
Access to the ESIOS (Spanish electricity market entity) data

This API is made to make it painless to access the market published data.

First you need a token string. You should ask for yours to: Consultas Sios <consultasios@ree.es>
It looks like this
`'615e6d8c80629b8eef25c8f3d0c36094e23db4ed50ce5458f3462129d7c46dba'`

To use the ESIOS module, just do:

`from ESIOS import *`

`token = '615e6d8c80629b8eef25c8f3d0c36094e23db4ed50ce5458f3462129d7c46dba'`

`esios = ESIOS(token)`

`indicators_ = [1293, 600]  3 demand (MW) and SPOT price (€)`

'names = esios.get_names(indicators_)`

`dfmul, df_list, names = esios.get_multiple_series(indicators_, start_, end_)`

`df = dfmul[names]  # get the actual series and neglect the rest of the info`


![Image of some indicators on December 2015](https://github.com/SanPen/ESIOS/blob/master/example.png)