import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
 

def plot_dr_ratio(portfolio_index, dr):
    """
	:param portfolio_index: pandas Dataframe object of the portfolio index
	:param dr: pandas Dataframe object of the DR ratio
	"""
	
	# do your magic here

    dplot = pd.DataFrame([portfolio_index,dr])
    dplot = dplot.T
    dplot.to_csv('../question2/output.csv')
    t = dplot.index.values
    print(dr)


    fig, axes = plt.subplots(2,1)

    ## comment t out for working graph
    # axes[0].plot_date(t, dplot[('Portfolio_Index', '1')].tolist())
    axes[0].plot(dplot[('Portfolio_Index', '1')].tolist())
    axes[0].set_ylabel('Portfolio Index', color='b')


    axes[1].plot(dplot[('DR', '')].tolist(), color='r')

    axes[1].set_ylabel('DR Ratio', color='r')

    plt.xlabel('Dates')
    plt.show()


def rolling_dr_ratio(df, rolling_window_size=200):
    """
	calculates and plots the dr ratio.
	
    :param df: the dataframe contains the daily total return price change, the weights and the portfolio index.
    :param rolling_window_size: default to 200 days.
    :return: None.
    """
    # some tests

    # calculate the rolling DR ratio
    # dr = ...

    # plot index and the rolling dr

    ## test if all weights sum up to 1
    if all(df.iloc[:,4:8]) == 1:
        df['DR'] = ''
        ## 200 day rolling
        for i in range(rolling_window_size,len(df.index)):
            ## vector of individual sigma
            roll_ind_sigma = np.std(df.iloc[i-rolling_window_size:i,0:4])
            ## weighting sum sigma
            weighted_ind_sig = np.sum(roll_ind_sigma*df.iloc[i,4:8].tolist())

            ## matrix of weighted returns
            roll_weighted_ret = df.iloc[i-rolling_window_size:i,0:4].multiply(df.iloc[i-rolling_window_size:i,4:8].values)
            ## rolling portfolio sigma
            portfolio_sig = np.std(roll_weighted_ret.sum(axis=1))

            df.iloc[i,9] = weighted_ind_sig / portfolio_sig

        plot_dr_ratio(df.iloc[rolling_window_size:len(df.index),-2], df.iloc[rolling_window_size:len(df.index),-1])

if __name__=="__main__":
    df = pd.read_csv("../question2/dr.csv", index_col=[0], header=[0,1], parse_dates=[0])
    rolling_dr_ratio(df)