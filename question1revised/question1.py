import pandas as pd


def same_timeseries(ts1, ts2):
    """
    return True if timeseries ts1 == timeseries ts2.

    :param ts1: pandas Dataframe object
    :param ts2: pandas Dataframe object
    :return: True if ts1 and ts2 are at least identical (Allowed Difference - 0.00001).
    """
    if len(ts1) == len(ts2):
        return (sum(ts1.values - ts2.values) < 10**-5).all()
    else:
        return False


def find_differences(bbg_df, quandl_df, csv_file_path=None):
    """
    prints or saves to csv the differences between two timeseries files.

    :param bbg_df: pandas Dataframe object
    :param quandl_df: pandas Dataframe object
    :param csv_file_path: path to save the output csv file (default=None)
    If csv_file_path is not None, will save the output to a csv file.
    :return: None.

    for each ticker find the start date of data from both sources,
    and prints True/False if prices series match since the common start date.

    Compare (BBG 'price' to quandl 'close price')

    CSV output example:
    
        Ticker, Quantle Start Date, BBG Start Date, Match since common start date?
        DOC US Equity ,2000-01-01, 1990-01-01, True
        ABO US Equity ,1999-01-01, 1990-01-01, False
        ...
        ...
        ...
        ABO US Equity ,1999-01-01, 1990-01-01, False
    
    """
    
    # write your code here.

    bbgheader_list = [x for x in bbg_df.columns.values.tolist() if x[1]=='price']
    bbg_df_price_only = bbg_df.filter(items= bbgheader_list)
    # print(bbg_df_price_only)

    quandlheader_list = [x for x in quandl_df.columns.values.tolist() if x[1]=='Close']
    quandl_df_price_only = quandl_df.filter(items= quandlheader_list)


    df_match = pd.read_csv('../question1revised/match_final.csv', header=None)

    missing = 0
    output = []

    for i in range(len(df_match[0])):
        try:
            bbg_first_date, quandl_first_date = bbg_df_price_only[df_match[1][i]].first_valid_index(), \
                                                quandl_df_price_only[df_match[0][i]].first_valid_index()

            start = max(quandl_first_date, bbg_first_date)

            complist = bbg_df_price_only[df_match[1][i]][start:].join(quandl_df_price_only[df_match[0][i]][start:])

            complist= complist.dropna()


            ticker = df_match.iloc[i][0]

            output.append([ticker, quandl_first_date, bbg_first_date, all(complist['price'] == complist['Close'])])

        except:
            try:
                output.append([df_match.iloc[i][0], 'Nan', bbg_df_price_only[df_match[1][i]].first_valid_index(),False])
            except:
                try:
                    output.append([df_match.iloc[i][0], quandl_df_price_only[df_match[0][i]].first_valid_index(), 'Nan',False])
                except:
                    output.append(
                        [df_match.iloc[i][0], 'Nan', 'Nan', False])


    result = pd.DataFrame(output, columns=['Ticker','Quandl Start Date', 'BBG Start Date', 'Match'])

    # save csv if file path was specified:
    if csv_file_path:
        result.to_csv('../question1revised/'+ csv_file_path)

    print(result)

if __name__=="__main__":
    bbg_df = pd.read_csv("../question1revised/bbg_data_final.csv", header=[0,1], index_col=0)
    quandl_df = pd.read_csv("../question1revised/quandl_data_final.csv", header=[0,1], index_col=0)

    find_differences(bbg_df, quandl_df, "output.csv")