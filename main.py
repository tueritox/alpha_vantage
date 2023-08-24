import formulas as f
import pandas as pd

def main():
    """Please enter the ticker"""
    t = input("Please enter the ticker you would like to obtain information from: ")
    t = t.upper()

    #Create all the dataframes for each set of information
    #b_s, rat = f.balance_sheet(t)
    #c_f = f.cash_flow(t)
    #i_s = f.income_statement(t)
    o, des = f.overview(t)
    p = f.price(t)

    #Download all the data into an excel
    with pd.ExcelWriter(t+'.xlsx') as writer:
        des.to_excel(writer, sheet_name= 'Description') 
        p.to_excel(writer, sheet_name='Price')
        o.to_excel(writer, sheet_name= 'Overview') 
        #i_s.to_excel(writer, sheet_name= 'Income Statement') 
        #b_s.to_excel(writer, sheet_name= 'Balance Sheet')
        #rat.to_excel(writer, sheet_name= 'Balance Sheet', startrow= 1, startcol= 8)
        #c_f.to_excel(writer, sheet_name= 'Cash Flow') 
        
    
    print('An Excel file has been created for you with all the data from the ticker', t)
        
        

if __name__ == '__main__':
    main()