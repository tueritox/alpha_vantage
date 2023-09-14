import formulas as f
import pandas as pd
import time

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
    #count the number of tickers CHECKED
    tick_count = 0
    #count the number of tickers DOWNLOAD
    tick_down = 0

    #open the file where the companies with info downloaded are counted
    #if I am starting a new process I have to clean this rtf file, else leave it like it is
    pro_list = []

    #append all the contest to a list to compare
    with open('procesadas.rtf') as file_pro:
        for i in file_pro:
            pro_list.append(i.replace('\n', ''))
        file_pro.close()

    #open and populate de S&P list with the tickers
    with open("tickers_sp.rtf") as infile:
        for line in infile:
            sp_500.append(line.replace('\n', ''))
        infile.close()

    #open and populate de NASDAQ list with the tickers
    with open("tickers_nasdaq.rtf") as file_ndq:
        for line in file_ndq:
            ndq_100.append(line.replace('\n', ''))    
        file_ndq.close()

    #there are companies repeated in both lists so this must be cleaned
    #compare the lists and obtain the repeated values
    rep = set(sp_500).intersection(ndq_100)

    #loop through the list and eliminate this values
    #I do it on the S6P list because is longer
    for i in rep:
        sp_500.remove(i)

    total = sp_500 + ndq_100

    #get the intersection of the total list to dowload and the ones dowload already
    pro_rep = set(pro_list).intersection(total)

    #remove the repeated (already downloaded)
    for i in pro_rep:
        total.remove(i)

    #start looking at the data for every company one by one
    for i in total:
        p = f.price(i)
        #check to see if it is worth downloading the data
        #if the security margin for the graham ratio es more than 0 download the data, else continue
        if int(p['Security Margin Graham']) > 0:
            i_s = f.income_statement(i)
            o, des = f.overview(i)
            
            #covert ticker to upper case
            ticker = i.upper()
            
            #Download all the data into an excel
            with pd.ExcelWriter(ticker+'.xlsx') as writer:
                des.to_excel(writer, sheet_name= 'Description') 
                p.to_excel(writer, sheet_name='Price')
                o.to_excel(writer, sheet_name= 'Overview') 
                i_s.to_excel(writer, sheet_name= 'Income Statement') 

            with open('download.rtf', 'a') as down:
                down.write(i+'\n')
                down.close()

            #display the last ticker download
            print('The last ticker DOWNLOAD is: ', i)
            #count and display the number of tickers CHECKED
            tick_down += 1
            print(tick_down, 'is the number of companies info DOWNLOAD.' )
        
        #count and display the number of tickers CHECKED
        tick_count += 1
        print(tick_count, 'is the number of companies info CHECKED.' )

        #display the last ticker checked
        print('The last ticker CHECKED is: ', i)

        #write in the rtf the new processed companies
        with open('procesadas.rtf', 'a') as processed:
            processed.write(i+'\n')
            processed.close()

        #sleep for 65 seconds
        time.sleep(65)
        if tick_count < 21:
            continue
        else:
            cont_script = input('Wanna continue? Press Y else N: ')
            if cont_script.upper() == 'Y':
                continue
            else:
                break
    
if __name__ == '__main__':
    main()
