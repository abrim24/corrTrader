__author__ = 'andy'

import pdb
import numpy as np
import yahoo_finance as y
from pandas import *
import matplotlib.pyplot as plot



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
    startDate = '2015-08-01'
    endDate = '2015-10-29'
    histdata = yahoo.get_historical(startDate,endDate)
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
            tickerPrices = y.Share(ticker).get_historical(startDate,endDate)
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

    #printing all the highest correlations
    i=0
    plt=plot
    for sec in sectors:
        pairs=highpairs[i].split(',')
        plt.plot(sectorPrices[i][sec.index(pairs[0])], label=str(pairs[0]), linewidth=5.0)
        plt.plot(sectorPrices[i][sec.index(pairs[1])], label=str(pairs[1]), linewidth=5.0)
        plt.xlabel(str(pairs[0] + " " + pairs[1] + " Correlation: " + str(highcorrs[i])))
        plt.legend()
        plt.show()
        i+=1

    newStocks=[]
    newStocks2=[]
    for stock in highpairs:
        pair = stock.split(',')
        newStocks.append(pair[0])
        newStocks2.append(pair[1])

    #recalculating correlations with highest correlating stocks
    print "newStocks: ", newStocks
    sectors = []
    sectorsTxt = ['Pair1','Pair2']
    sectors.append(newStocks)
    sectors.append(newStocks2)
    sectorPrices = []
    i=0
    for sector in sectors:
        print "Sector: " + str(sectorsTxt[i])
        prices=[]
        for ticker in sector:
            tickerPrices = y.Share(ticker).get_historical(startDate,endDate)
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


    #printing all the highest correlations
    i=0
    plt=plot
    for sec in sectors:
        pairs=highpairs[i].split(',')
        plt.plot(sectorPrices[i][sec.index(pairs[0])], label=str(pairs[0]), linewidth=5.0)
        plt.plot(sectorPrices[i][sec.index(pairs[1])], label=str(pairs[1]), linewidth=5.0)
        plt.xlabel(str(pairs[0] + " " + pairs[1] + " Correlation: " + str(highcorrs[i])))
        plt.legend()
        plt.show()
        i+=1

if __name__ == "__main__": main()
