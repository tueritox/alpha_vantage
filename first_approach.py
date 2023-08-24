import formulas as f
import pandas as pd

def main():
    """This function will browse one by one the stocks in the list
        and make a first approach to the possibility of an investment
        in the company, according to the KPIs obtained. After identifying
        these companies, a better due diligence must be done."""
    
    #first get the lists of stocks for the S&P500 and NASDAQ100 from the rtf files
    #list for S&P
    sp_500 = []
    #list for NASDAQ
    ndq_100 = []

    #open and populate de S&P list with the tickers
    with open("tickers_sp.rtf") as infile:
        for line in infile:
            sp_500.append(line.replace('\n', ''))

    #open and populate de NASDAQ list with the tickers
    with open("tickers_nasdaq.rtf") as file_ndq:
        for line in file_ndq:
            ndq_100.append(line.replace('\n', ''))    

    #there are companies repeated in both lists so this must be cleaned
    #compare the lists and obtain the repeated values
    rep = set(sp_500).intersection(ndq_100)

    #loop through the list and eliminate this values
    #I do it on the S6P list because is longer
    for i in rep:
        sp_500.remove(i)

    t = []
    


if __name__ == '__main__':
    main()