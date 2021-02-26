#!/usr/bin/env python

import matplotlib.pyplot as plt
import pyart
import numpy as np
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def radar_cpmet(x):
    # ABRE O ARQUIVO
    radar = pyart.io.read( x )
    #print( radar.info() )   # imprime informações dos dados de radar
    #print( radar.fields )   # imprime as variáveis

    # obtendo informação de tempo
    units =  radar.time['units']
    units2 = units.split()
    data = np.datetime64( units2[2] )
    data_str = np.datetime_as_string( data, unit='m' ) 

    # estimativa de chuva
    tx_chuva = pyart.retrieve.est_rain_rate_z( radar )

    # objeto para dados de radar num mapa
    display = pyart.graph.RadarMapDisplay(radar)

    # criando figura com eixos georeferenciados
    fig, (ax1 , ax2) = plt.subplots( nrows=1, ncols=2, figsize=(9,9), sharey=True )
    ax1 = plt.axes( projection=ccrs.PlateCarree() )

    # adicionando estados ao mapa
    estados = cfeature.NaturalEarthFeature(category='cultural', scale='50m',
                                           facecolor='none', name='admin_1_states_provinces_shp')

    # inserindo no mapa
    ax1.add_feature( estados, linewidth=0.8, edgecolor='black' )

    # mostrando mapa
    ax1.coastlines( '50m', linewidth=0.8 )

    # PLOTA PPI DE UM GRAU
    elevacao = 1
    display.plot_ppi_map('reflectivity', elevacao, vmin=0, vmax=75., cmap='pyart_NWSRef', ax=ax1,
                         projection = ccrs.PlateCarree(), resolution='50m',
                         lon_lines=np.arange(-60, -48, 1), lat_lines=np.arange(-35, -24, 1),
                         title='Z 1 grau - Radar FAMET/UFPEL - '+data_str, colorbar_flag=False)
    display.plot_range_rings( [50,100,150,200,250], col='grey', ls='dotted' )
    display.set_aspect_ratio( aspect_ratio=1 )

    #plt.show()



    display.plot_ppi_map('velocity', elevacao, vmin=-20, vmax=20,cmap='pyart_NWSRef', ax=ax2,
                         projection = ccrs.PlateCarree(), resolution='50m',
                         lon_lines=np.arange(-60, -48, 1), lat_lines=np.arange(-35, -24, 1),
                         title='V - 1 grau - Radar FAMET/UFPEL - '+data_str, colorbar_flag=False)
    display.plot_range_rings( [50,100,150,200,250], col='grey', ls='dotted' )
    display.set_aspect_ratio( aspect_ratio=1 )




    # BARRA DE CORES
    colorbar_panel_axes = [0.25, 0.07, 0.6, 0.03]  # [ X1, y2, delta-x, delta-y ]
    cbax = fig.add_axes( colorbar_panel_axes )
    display.plot_colorbar( orient='horizontal',label='(dBZ)', cax=cbax) 

    #plt.savefig( '%s' %(dano), dpi=100)
    #plt.show()
