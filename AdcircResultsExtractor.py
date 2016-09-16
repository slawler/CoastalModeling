#--NOAA API
datum     = "msl"                             #Datum
units     = "english"                         #Units
time_zone = "lst_ldt"                         #Time Zone
fmt       = "json"                             #Format
url       = 'http://tidesandcurrents.noaa.gov/api/datagetter'
product   = 'water_level'


#---fort.15
dateline = 'YYYY,MM,DD,HH24,StormNumber,BLAdj'


#---fort.61( --or: .71,.72)
fort = 'fort.61'
nullval = '-99999.000000'
intvl = 1800


#---Add Noaa Station Dictionary

#---Class Objects
class AdcircOutput(object):
    """
       ReadsFort takes as input standard ADCIRIC output files (*.63, *.61, etc.)
       and extracts timeseries data to a pandas dataframe.
       
    """
    def __init__(self, infile, stn):
        self.infile = infile
        self.stn = stn

    def parameters(self):
        """ Define """
        with open('fort.15','r') as f:
            for i in range(0,30):
                line = f.readline().strip().split()
                if dateline in line:
                    date = line[1]+'/'+line[2]+'/'+line[0]
                    
        with open(self.infile ,'r') as f:
            for i in range(0,5):
                line = f.readline().strip().split()
            freq = intvl
            
        return date, freq #,periods
                  
    def tseries(self, params, node_names):
        """ Define """
        import fileinput
        import pandas as pd

        self.params = params
        self.node_names = node_names
        self.idx = pd.date_range(start=self.params[0], periods = self.params[2], freq='{}s'.format(self.params[1]))

        for line in fileinput.input(self.infile):
            s = line.strip().split(' ')[0]
            if s in self.stn:
                data = line.strip().split()[1]
                self.stn[s].append(float(data))

        df = pd.DataFrame.from_dict(self.stn).rename(columns =self.node_names)
        df.replace(to_replace=nullval,value=0,inplace=True)
        df = df.set_index(self.idx)
        return df
        
    def to_api(self, product, gage):
        """ Define """
        self.product = product
        self.gage = gage
        from datetime import datetime
        first      = datetime.date(self.idx[0]).strftime('%Y%m%d')
        last       =  datetime.date(self.idx[-1]).strftime('%Y%m%d')
        api_params = {'begin_date': first+" 00:00", 'end_date': last+" 00:00",
                    'station': gage,'product':product,'datum':datum,
                    'units':units,'time_zone':time_zone,'format':fmt,
                    'application':'web_services' }
        
        return api_params
            
    def noaa_data(self, gage):
        """ Define """
        self.gage = gage 
      
        import requests
        import pandas as pd 
             
        pred=[];obsv=[];t=[]        
        try:  
            r = requests.get(url, params = self.to_api(product, gage))
            jdata =r.json()
            
            for j in jdata['data']:
                t.append(str(j['t']))
                obsv.append(str(j['v']))
                pred.append(str(j['s']))        
                
            dtm = pd.to_datetime(t)    
            df_o = pd.DataFrame(obsv, index = dtm, columns = ['observed'])
            df_p = pd.DataFrame(pred, index = dtm, columns = ['predicted'])
            df = df_p.merge(df_o, how='outer', left_index=True, right_index=True)
            df['observed']=df['observed'].astype(float)
            df['predicted']=df['predicted'].astype(float)             
            return df

        except:
            return 'No Data'
            
    def PlotResults(self,df,col): 
        self.df = df
        self.col = col
        
        import matplotlib.pyplot as plt
        print "\t\tPlotting: ", self.col
        ax = self.df.plot(x = self.df.index, y = [self.col, 'predicted' ,'observed'])
        fig = ax.get_figure()
        fig.savefig('{}.jpg'.format(self.col))
        plt.show(block = False)
        plt.close(fig)
    







