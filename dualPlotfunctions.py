# putting these functions all together

def convertForDualPlot(df,basename,baseList,betavalues,smoothing=False):
    """ function to convert a particular set of related features into a format that can be 
    plotted as a dual plot of beta parameters and distributions
    
    input: df = root data frame
           basename = basename of the feature(class)
           baseList = list of features used as the baseline for each feature(class)
           betavalues = array of model betavalues (must be same length as df.columns)
           normed = flag to show if plot the percentages or raw counts.
    
    To do: fix the smoothing function -- currently not operational
    """ 
    #colorname = 'cadetblue'
    #Parse the dataframe based upon an input columnName
    missingBin = [c for c in baseList if c.startswith(basename)]
    # obtain categorical Column information
    newDF = getCategoricalCols2(df,basename,missingBin[0])
    # create a normed column
    nvals = len(df)
    newDF['pct'] = newDF['counts'].apply(lambda x: x/float(nvals))
       
    #find the corresponding betavalues
    # check length of columns and betavalues match
    try:
        len(df.columns)== len(betavalues)
        print "match"
        
        bvalues = []
        for a in newDF.position.values:
            try:
                a = int(a)
                bvalues.append(betavalues[a])
            except:
                #if(smooth)
                bvalues.append(0.0)
                
                # could replace with np.NaN for plotting purposes
        #pass

        newDF['beta']=bvalues
        # find the corresponding betavalues
        
    except:
        print "wrong lengths: {0} and {1}".format(len(df.columns),len(betavalues))
        return (-1)
    
    # fix the order of the bins
    reorderDF = fixBinOrder3(newDF)
    return reorderDF
    
# function to get the categorical columns info
def getCategoricalCols2(df,basename,missingBin):
    # I also want the positions of these within the columnsListing
    #returns a dataframe
    myCategoricals = {}
    nBinned = 0
    for i in xrange(len(df.columns)):
    #for cname in df.columns:
        cname = df.columns[i]
        if cname.startswith(basename):
            ccount = sum(df[cname])
            myCategoricals[cname] = [ccount,i]
            nBinned+=ccount
    
    print len(myCategoricals)
    nbaseCat = len(df)-nBinned#sum(myCategoricals.values())
    myCategoricals[missingBin]=[nbaseCat,np.nan]
    categoryDF = pd.DataFrame(myCategoricals,index=['counts','position']).T
    #print sum(myCategoricals.values()), len(df)
    return categoryDF

# function to reorder the dataframe 
def fixBinOrder3(df,flagString = 0):
    # function to determine type of ending:
    fieldSplit = df.index[0].split('_')
    prefix = fieldSplit[0]
    ending = fieldSplit[1]
    # first check if there is a decimal:
    if len(ending.split('.')) > 1:
        #print "dealing with a float"
        myType = float
    else:
        # check that it is in [0-9]
        try: 
            value = int(ending)
            #print "dealing with an integer"
            myType = int
        except:
            #print "dealing with a string"
            myType = str
            flagString = 1
    
    initialOrder = list(df.index)
        
    if flagString:
        # just use the sort_index directly
        df = df.sort_index()
        #neworder = sort(initialOrder)
    else:
        # create a new index that involves the numeric part & sort on that
        if myType == int:
            df['indx2'] = [int(c.split('_')[1]) for c in list(df.index)]
            df = df.sort_index(by='indx2')
            df.drop('indx2',axis=1,inplace=True)
        else:
            df['indx2'] = [int(c.split('_')[1].split('.')[0]) for c in list(df.index)]
            df = df.sort_index(by='indx2')
            df.drop('indx2',axis=1,inplace=True)
    return df

# function to make the plot
def makeDualPlot2(df,color='darkred',normed=True,smoothed=False):
    """
    input is a transformed dataframe -- the output of convertForDualPlot
    normed = True means fraction of values are plotted, False measn raw counts
    """
    figure(figsize=(10,5))
    left,width=0.07,0.95
    bottom, height = 0.07, 0.75
    bottom_1, height_1 = 0.75,0.23
    # define 2 parts:
    # count_ax for the distribution
    # beta_ax for the betas
    count_ax = axes([left,bottom,width,height])
    beta_ax = axes([left,bottom_1,width,height_1])
    x = np.arange(0,len(df))+1
    if normed:
        count_ax.bar(x,df['pct'].values,color=color)
        count_ax.set_ylabel('Percentage',fontsize=14)
    else:
        count_ax.bar(x,df['counts'].values,color=color)
        count_ax.set_ylabel('Counts',fontsize=14)
    count_ax.grid(True)
    
    tmp=count_ax.get_xticklabels()
    if tmp != len(df):
        count_ax.set_xticks(np.arange(min(x), max(x)+1, 1.0))
    #print len(tmp)
    count_ax.set_xticklabels(list(df.index))
    
    # now deal with beta parameters
    beta_ax.plot(x,df['beta'].values,color=color,marker='o',lw=2)
    beta_ax.set_ylabel(r'$\beta$-values',fontsize=14)
    beta_ax.axhline(y=0,color='black')
    beta_ax.set_xticks(np.arange(min(x), max(x), 1.0))
    beta_ax.grid(True)
    setp( beta_ax.get_xticklabels(), visible=False)
    return
    