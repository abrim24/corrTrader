__author__ = 'andy'

import pdb
import numpy as np
import yahoo_finance as y
from pandas import *
import matplotlib.pyplot as plot
from multiprocessing import Pool
import itertools as i

class MultiagentSystem(object):

    def __init__(self, start, end):
        self.startDate = start
        self.endDate = end

        #init stock sectors and other variables
        self.numAgents = 7
        self.numHighAgents = 2
        self.sectorsTxt = ['it','energy','financials','industrials','healthcare','consumerdisc','consumerstaples']
        self.it = ['CTSH','ADP','PYPL','YHOO','AVGO','EBAY','BRCM','GLW','MU','VMW']
        self.energy = ['PSX','APC','HAL','WMB','VLO','MPC','BHI','SE','DVN','APA']
        self.financials = ['CB','MMC','BBT','CME','STT','EQR','AFL','ALL','DFS','BEN']
        self.industrials = ['PCP','EMR','AAL','CSX','DE','ITW','ETN','NSC','WM','CMI']
        self.healthcare = ['SYK','BDX','HUM','VRTX','CAH','HCA','ILMN','BAX','MYL','BXLT']
        self.consumerdisc = ['CMCSK','TSLA','CBS','CCL','LVS','VIAB','FOX','TRI','DISH','VIA']
        self.consumerstaples = ['MDLZ','COST','CL','KHC','KMB','RAI','KR','GIS','ADM','EL']
        self.sectors = [self.it,self.energy,self.financials,self.industrials,self.healthcare,self.consumerdisc,self.consumerstaples]

        self.agentGetPricesRef=agentGetPricesRef

    def runAgents(self):
        agentPool = Pool(self.numAgents)

        sectors = self.sectors
        sectorsTxt = self.sectorsTxt
        startDate = self.startDate
        endDate = self.endDate

        sectorPrices = agentPool.map(self.agentGetPricesRef,i.izip(sectors,sectorsTxt, i.repeat(self.startDate),i.repeat(self.endDate)))
        #sectorPrices2 = self.getSectorPrices(sectors,sectorsTxt,startDate,endDate)

        print "sectorPrices: ", sectorPrices
        #print "sectorPrices2: ", sectorPrices2

        #if sectorPrices == sectorPrices2: print "the same"
        #else: print "not the same"

        highcorrs,highpairs,highidxs = self.findHighCorrs(sectors,sectorPrices)

        print highcorrs
        print highpairs

        #printing all the highest correlations
        #self.printCorrs(sectors,sectorPrices,highcorrs,highpairs)

        newStocks=[]
        newStocks2=[]
        for stock in highpairs:
            pair = stock.split(',')
            newStocks.append(pair[0])
            newStocks2.append(pair[1])

        #recalculating correlations with highest correlating stocks
        sectors = []
        sectorsTxt = ['High Pair Set 1','High Pair Set 2']
        sectors.append(newStocks)
        sectors.append(newStocks2)

        print "sectors: ", sectors
        agentPool = Pool(self.numHighAgents)
        sectorPrices = agentPool.map(self.agentGetPricesRef,i.izip(sectors,sectorsTxt,i.repeat(self.startDate),i.repeat(self.endDate)))
        #getSectorPrices(sectors,sectorsTxt,startDate,endDate)

        print "sectorPrices: ", sectorPrices

        highcorrs,highpairs,highidxs=self.findHighCorrs(sectors,sectorPrices)


        #print np.corrcoef(sectorPrices[0],sectorPrices[1])[1,0]
        print "highcorrs: ", highcorrs
        print "highpairs: ", highpairs
        print "highidxs: ", highidxs

        highidx=highidxs[0]

        #printing all the highest correlations
        self.printCorrs(sectors,sectorPrices,highcorrs,highpairs)

        self.findLeader(sectorPrices[highidx[0][0]][highidx[0][1]], sectorPrices[highidx[1][0]][highidx[1][1]], highcorrs[0],highpairs[0])


    def getSectorPrices(self,sectors,sectorsTxt,startDate,endDate):
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
        return sectorPrices

    def findHighCorrs(self,sectors,sectorPrices):
        highcorrs = []
        highpairs = []
        highidxs = []
        highx = 0
        highy = 0
        a=0
        for i in sectorPrices:
            b=0
            highcorr=0.0
            highpair=''
            highidx=[]
            for j in sectorPrices[a]:
                c=0
                for k in sectorPrices[a]:
                    if b!=c:
                        corr = np.corrcoef(sectorPrices[a][b],sectorPrices[a][c])[1,0]
                        if corr > highcorr:
                            highcorr= corr
                            highpair= str(sectors[a][b] + ',' + sectors[a][c])
                            highidx=[[a,b],[a,c]]
                            #print "corr: " , corr
                            #print "highcorr: " , highcorr
                    c+=1
                b+=1
            a+=1
            highcorrs.append(highcorr)
            highpairs.append(highpair)
            highidxs.append(highidx)
        return highcorrs,highpairs,highidxs

    def printCorrs(self,sectors,sectorPrices,highcorrs,highpairs):
        i=0
        plt=plot
        for sec in sectors:
            pairs=highpairs[i].split(',')
            plt.plot(sectorPrices[i][sec.index(pairs[0])], label=str(pairs[0]), linewidth=5.0)
            plt.plot(sectorPrices[i][sec.index(pairs[1])], label=str(pairs[1]), linewidth=5.0)
            plt.title(str(pairs[0] + " " + pairs[1] + " Correlation: " + str(highcorrs[i])),fontsize=20.0)
            plt.xticks([2,19],[self.startDate,self.endDate])
            plt.legend()
            plt.show()
            i+=1

    def findLeader(self,A=[],B=[],corrAB=0,highpair=''):
        pairs=highpair.split(',')
        length = min(len(A),len(B))
        print "A: ", A
        print "B: ", B
        print "length: ", length
        corr=0.0
        corrs=[]
        prevCorr=0.0
        deltasA=[]
        deltasB=[]
        deltaA=0.0
        deltaB=0.0
        prevA=0.0
        prevB=0.0
        for i in range(length):
            if i>=0: #prime the delta vals
                corr=np.corrcoef(A[i-30:i],B[i-30:i])[1,0]
                deltaA=A[i]/A[i-1]
                deltaB=B[i]/B[i-1]
                deltasA.append(deltaA)
                deltasB.append(deltaB)
                print "prevCorr: ", prevCorr
                print "corr: ", corr
                print "corrAB: ", corrAB
                print "deltaA: ", deltaA
                print "deltaB: ", deltaB
                prevCorr=corr
                print "i: ", i
        plt=plot
        plt.plot(deltasA, label=str(pairs[0] + " Deltas"), linewidth=5.0)
        plt.plot(deltasB, label=str(pairs[1] + " Deltas"), linewidth=5.0)
        plt.title(str(pairs[0] + " " + pairs[1] + " Deltas"),fontsize=20.0)
        plt.xticks([2,19],[self.startDate,self.endDate])
        plt.legend()
        plt.show()

        return

#Python won't serialize a method inside a class for pooling. This allows me to do it outside of the class.
def agentGetPrices(sector,sectorTxt,startDate,endDate):
    print sectorTxt, " Agent is running..."
    prices=[]
    for ticker in sector:
        tickerPrices = y.Share(ticker).get_historical(startDate,endDate)
        cleanPrices =[]
        for j in tickerPrices: cleanPrices.append(float(j['Adj_Close']))
        prices.append(cleanPrices)
    return prices

def agentGetPricesRef(arg):
    return agentGetPrices(*arg)

def main():
    august= MultiagentSystem('2015-08-01','2015-08-31')
    september = MultiagentSystem('2015-09-01','2015-09-30')
    october = MultiagentSystem('2015-10-01','2015-10-31')
    november = MultiagentSystem('2015-11-01','2015-11-30')
    december = MultiagentSystem('2015-12-01','2015-12-12')
    months = [august,september,october,november,december]
    #months = [november,december]
    for i in months: i.runAgents()


if __name__ == "__main__": main()
