import formulas as f
import pandas as pd
import time

def main():
    """This function will download BALANCE SHEET and CASH FLOW STATEMENT for the tickers
    that the user enters. It will check if there is already an excel file on each one, and
    if there is one it will append to that excel, so all the data is in the same place."""

    #ticker list that the user enters
    tick_list = []
    ticker = input("Inserte el/los tickers que quiere mas informacion. Para terminar deje vacio este campo y apriete ENTER: ")

    #loop to accept as many tickers as the user wants
    while ticker != "":
        tick_list.append(ticker.upper())    
        ticker = input("Inserte el/los tickers que quiere mas informacion. Para terminar deje vacio este campo y apriete ENTER: ")
    
    #list of the companies already with an excel with info download
    down_list = []

    with open("download.rtf") as file_down:
        for line in file_down:
            down_list.append(line.replace('\n', ''))
        file_down.close()
    
    for i in tick_list:
        #check if there is an excel download on the ticker asked
        if i in down_list:
            #look for the balance sheet and cash flow
            b_s, ratios = f.balance_sheet(i)
            cash = f.cash_flow(i)
            #Download all the data into an excel
            with pd.ExcelWriter(i+'.xlsx', mode='a') as writer:
                b_s.to_excel(writer, sheet_name= 'Balance Sheet') 
                ratios.to_excel(writer, sheet_name='Balance Sheet Ratios')
                cash.to_excel(writer, sheet_name= 'Cash Flow Statement')
            time.sleep(61) 
        #if there is no excel for the ticker, we have to download all the data and create the excel
        #this will take a lot of time, taking into account the restrictions given by the API
        else:
            #download first part of the data
            i_s = f.income_statement(i)
            o, des = f.overview(i)
            p = f.price(i)
            cash = f.cash_flow(i)
            #Download all the data into an excel
            with pd.ExcelWriter(i+'.xlsx') as writer:
                des.to_excel(writer, sheet_name= 'Description') 
                p.to_excel(writer, sheet_name='Price')
                o.to_excel(writer, sheet_name= 'Overview') 
                i_s.to_excel(writer, sheet_name= 'Income Statement')
                cash.to_excel(writer, sheet_name= 'Cash Flow Statement')
            #wait for the API to be ready
            time.sleep(61)
            #download the missing info
            b_s, ratios = f.balance_sheet(i)
            with pd.ExcelWriter(i+'.xlsx', mode='a') as writer:
                b_s.to_excel(writer, sheet_name= 'Balance Sheet') 
                ratios.to_excel(writer, sheet_name='Balance Sheet Ratios')
    
        
if __name__ == '__main__':
    main()
