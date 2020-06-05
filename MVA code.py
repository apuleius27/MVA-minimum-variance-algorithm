"""
Copyright (c) 2020 apuleius27

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: "Minimum Variance Algorithm (MVA)"
Created: 2020-05-19
@author: Mike Massari (apuleius27)
Version: v7.0
Language: Python
Platform: Standalone
"""


"""
-The following is the code for the MVA.

-The code is written as a function in order to make it highly reusable.

-The following code is provided 'as is' and it will not work out-of-the-box,
but it needs to be adapted to one's specific needs and software usage.

-The imports related to iexfinance provide a clearer understanding of the algorithm.

-The code is provided with large chunks of commented software.
The reason for leaving the code so messy is because it gives better understanding 
of my thinking process and it may help in one's implementation of the MVA.
However, it can be easily deleted as the MVA will work anyway.

-IMPORTANT: the parameter passed to the MVA function - 'toplist' - needs to be a tuple.
"""



'''Imports related to iexfinance'''
import os
import iexfinance as iex
from iexfinance.stocks import Stock, get_historical_data


# SET ENVIRONMENT VARIABLES

#set token - iex cloud
os.environ['IEX_TOKEN'] = '' #test data - insert own token

#set output format to 'pandas' - default is 'json'
os.environ['IEX_OUTPUT_FORMAT'] = 'pandas'

#set environ to sandbox (which uses test data) - to disable, uncomment delete environ
os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
#del os.environ['IEX_API_VERSION']





'''Imports'''
import pandas as pd
import numpy as np
import math
import scipy.stats as stats

from datetime import datetime, timedelta
import collections




"""
# Implementation of - Minimum Variance Algorithm (MVA)

IMPORTANT: the parameter 'toplist' needs to be a tuple
"""

def GetMinvarWeights(toplist):

    # PARAMETER
    minvarLookback = 20   # example lookback period for MVA
    
    
    toplist_symbols = []
    for s in toplist:
        toplist_symbols.append(s)
        
    toplist_symbols.sort()
        
    weights = {}
    if len(toplist) > 0:
        #if length of list is 1 then weight should be 100% to that security
        if len(toplist) == 1:
            weights[toplist[0]]=1.0
        else:
            
            '''
            end = datetime.now()
            N = 10
            start = datetime.now() - timedelta(days=N)
            c.f = get_historical_data(spy, start,end)
            assert(0)
            '''
    
            # Get the data we need
            end = datetime.now()
            N = minvarLookback + minvarLookback * 1/2 #conservative in order to account for days when market is closed   
            start = datetime.now() - timedelta(days=N)
            
            h = get_historical_data(toplist_symbols, start, end, close_only=True)
    
            h = h.xs('close', axis=1, level=1, drop_level=True)
            
            """
            try:
                h = h['close'].unstack(level=0)
                 
            except:
                df = pd.DataFrame(index=h.index.levels[1], columns=h.index.levels[0])
                
                #df_sorted = pd.DataFrame(columns=toplist, index=h.index.levels[1])
                #df_sorted = df
                
                # I have to sort because 'h' shows index not sorted, but instead it is. Indeed:
                # h.index.levels[0] is sorted
                h = h.sort_index()
    
                i = 0 # row
                j = 0 # column
                k = int(len(h.loc[:]['close']) / len(h.index.levels[0]))
                n = int(len(h.loc[:]['close']))
    
                for m in range(0, n):
                    try:
                        df.iloc[i][j] = h.iloc[m]['close']
                        i = i + 1
                        if i == k:
                            i = 0
                            j = j + 1
                    except:
                        pass
    
                h = df
                
                '''
                n = len(toplist)
                i = 0
                j = 0
                
                for stock in toplist:
                    for j in range(0, n):
                        if str(stock) == str(h.columns.values[j]):
                            df_sorted.iloc[:,i] = h.iloc[:,j]
                            i = i + 1
                
                h = df_sorted
                '''
                
                """
            
            
            pct_change = h.pct_change()
            
            #calculate covariance matrix
            cov = pct_change.dropna().cov()

            
            '''
            if (len(cov.index)) > 3:
                #self.Debug('Cov: {}'.format(cov))
                self.Debug('Cov shape: {}'.format(cov.shape))
                self.Debug('Cov index len: {}'.format(len(cov.index)))
                #self.Debug(cov.ix[7,7])
                '''
                
            #avg pairwise covariance
            avg_cov = cov.mean()
            
            '''
            print(type(h.columns.values[0]))
            print((h.columns.values[0]))
            print(type(avg_cov.index.values[0]))
            print((avg_cov.index.values[0]))
            print(type(toplist[0]))
            print((toplist[0]))
            print(type(toplist_symbols[0]))
            print((toplist_symbols[0]))
            '''
            
            
            '''
            s = []
            for i in avg_cov.index:
                #s.append(str(i)) # append ticker and code
                #self.Debug(str(i))
    
                s.append(str(i).rsplit()[0])  # append only ticker
                #self.Debug(str(i).rsplit()[0])
            
            avg_cov2 = avg_cov.reindex([s])
            for i in range(len(avg_cov.index)):
                avg_cov2.iloc[i] = avg_cov.iloc[i]
            avg_cov = avg_cov2
            
            '''
            
            
            #'''
            avg_cov2 = avg_cov.reindex(toplist)
            for i in range(0, len(avg_cov.index)):
                avg_cov2.iloc[i] = avg_cov.iloc[i]
            avg_cov = avg_cov2
            #'''
            
            
            
            i=0
            gauss_conv = {}
            inv_var = {}
            
            for s in toplist:
                #gaussian conversion
                gauss_conv[s] = 1-stats.norm.cdf((avg_cov[s]-avg_cov.mean())/avg_cov.std())
                #inverse variance
                try:
                    #inv_var[s] = 1.0/cov.ix[i,i]
                    inv_var[s] = 1.0/cov.iloc[i,i]
                    #print(inv_var[s])
                except:
                    inv_var[s] = 0
                    #print(s)
                    
                #print('s and inv_var[s]: {}, {}'.format(s, inv_var[s]))
                i += 1
            #print(i)
                
                
            gc = pd.Series(gauss_conv,name='Symbol')
            iv = pd.Series(inv_var, name='Symbol')
            #inverse variance weight
            inv_var_weight = iv/iv.sum()
            #print('inv_var_weight: {}'.format(inv_var_weight))
            #proportional average covar weight
            avg_covar_weight = gc/gc.sum()
            #print('avg_covar_weight: {}'.format(avg_covar_weight))
            #product of proportional average covar weight and inverse variance weight
            prod_avg_covar_inv_var = avg_covar_weight * inv_var_weight
            #print('prod_avg_covar_inv_var: {}'.format(prod_avg_covar_inv_var))
            
            #final weights
            
            '''
            # It takes correct weights, no need to do other calculations
            if (i > 5):
                self.Debug('start')
                weights_sum = 0
                num_nan = 0
                for s in toplist:
                    if math.isnan( prod_avg_covar_inv_var[s] / prod_avg_covar_inv_var.sum() ):
                        num_nan = num_nan + 1
                        
                    else:
                        weights_sum = weights_sum + ( prod_avg_covar_inv_var[s] / prod_avg_covar_inv_var.sum() )
                self.Debug(weights_sum)
                self.Debug(num_nan)
                self.Debug('end')
                assert(0)
                '''
                
            
            for s in toplist:
                if math.isnan( prod_avg_covar_inv_var[s] / prod_avg_covar_inv_var.sum() ):
                    weights[s] = 0
                    print(s)
                else:
                    weights[s] = prod_avg_covar_inv_var[s] / prod_avg_covar_inv_var.sum()
                #self.Debug('prod_avg_covar_inv_var[s]: {}'.format(prod_avg_covar_inv_var[s]))
                #self.Debug('prod_avg_covar_inv_var.sum(): {}'.format(prod_avg_covar_inv_var.sum()))
                
                #log.info(" symbol: " + str(s.symbol) + " w: " + str(context.weights[s]) )
                #log.info(context.weights)
                #self.Debug(self.weights[s])
            #log.info(context.weights)
            print('\nResults will be in the form of a python dictionary: {security:weight}\n')
            print(weights)





