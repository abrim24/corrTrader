__author__ = 'andy'

import pdb
import numpy as np
import yahoo_finance as y
from pandas import *


def main():
    #goog = DataReader('GOOG',  'yahoo', datetime(2000,1,1), datetime(2012,1,1))
    #print(goog['Adj Close'])
    #exit(1)

    yahoo = y.Share('YHOO')

    sectorsTxt = ['it','energy','financials','industrials','healthcare','consumerdisc','consumerstaples']
    it = ['CTSH','ADP','PYPL','YHOO','AVGO','EBAY','BRCM','GLW','MU','VMW']
    energy = ['PSX','APC','HAL','WMB','VLO','MPC','BHI','SE','DVN','APA']
    financials = ['CB','MMC','BBT','CME','STT','EQR','AFL','ALL','DFS','BEN']
    industrials = ['PCP','EMR','AAL','CSX','DE','ITW','ETN','NSC','WM','CMI']
    healthcare = ['SYK','BDX','HUM','VRTX','CAH','HCA','ILMN','BAX','MYL','BXLT']
    consumerdisc = ['CMCSK','TSLA','CBS','CCL','LVS','VIAB','FOX','TRI','DISH','VIA']
    consumerstaples = ['MDLZ','COST','CL','KHC','KMB','RAI','KR','GIS','ADM','EL']

    sectors = [it,energy,financials,industrials,healthcare,consumerdisc,consumerstaples]

    print energy

    print yahoo.get_price()
    print yahoo.get_open()
    print yahoo.get_prev_close()

    histdata = yahoo.get_historical('2015-10-01','2015-10-12')
    tickPrices = []
    for i in histdata: tickPrices.append(float(i['Adj_Close']))
    print histdata
    print tickPrices
    #exit(1)

    sectorPrices = []
    i=0
    for sector in sectors:
        print "Sector: " + str(sectorsTxt[i])
        prices=[]
        for ticker in sector:
            tickerPrices = y.Share(ticker).get_historical('2015-09-01','2015-10-13')
            cleanPrices =[]
            for j in tickerPrices: cleanPrices.append(float(j['Adj_Close']))
            prices.append(cleanPrices)
        sectorPrices.append(prices)
        i+=1

    highcorrs = []
    highpairs = []
    a=0
    for i in sectorPrices:
        b=0
        highcorr=0.0
        highpair=''
        for j in sectorPrices[a]:
            c=0
            for k in sectorPrices[a]:
                if b!=c:
                    corr = np.corrcoef(sectorPrices[a][b],sectorPrices[a][c])[1,0]
                    if corr > highcorr:
                        highcorr= corr
                        highpair= str(sectors[a][b] + ',' + sectors[a][c])
                        print "corr: " , corr
                        print "highcorr: " , highcorr
                c+=1
            b+=1
        a+=1
        highcorrs.append(highcorr)
        highpairs.append(highpair)

    print sectorPrices

    #print np.corrcoef(sectorPrices[0],sectorPrices[1])[1,0]
    print highcorrs
    print highpairs

    print np.corrcoef(sectorPrices[0][1],sectorPrices[0][4])[1,0]

if __name__ == "__main__": main()
