from alpha_vantage_key import key
import requests
import pandas as pd

#alpha vantage key constant
K = key()

#risk free rate (SPAIN) - used for Graham Intrinsic Value
RF = 3.75
#avg yield corporate AAA bonds - used for Graham Intrinsic Value
Y = 5

#first function to obtain all the basic data of the ticker
#this then will create the first part of the excel that will
#have the main info to decide whether the invest is sound or not
def overview(ticker):
    t = str(ticker)
    #connection to alpha vantage API
    #request of overview data
    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ t +'&apikey='+ K
    r = requests.get(url)
    data = r.json()

    #get the relevant information from alpha vantage
    revenue = round(float(data['RevenueTTM']) / 1000000, 2) 
    gross_margin = round((float(data['GrossProfitTTM']) / float(data['RevenueTTM'])) * 100, 2)
    peratio = data['PERatio']
    try:
        pegratio = round(float(data['PEGRatio']), 2)
    except:
        pegratio = 0
    try:
        growth_5y = round(float(data['PERatio']) / float(data['PEGRatio']), 2)
    except:
        growth_5y = 0
    psratio = data['PriceToSalesRatioTTM']
    book_value = data['BookValue']
    pbookratio =data['PriceToBookRatio']
    dividends_share = data['DividendPerShare']
    eps = data['EPS']
    revenue_share = data['RevenuePerShareTTM']
    roe = data['ReturnOnEquityTTM']
    roa = round(float(data['ReturnOnAssetsTTM']) * 100, 2)
    profit_margin = round(float(data['ProfitMargin']), 2)
    operating_margin = round(float(data['OperatingMarginTTM']), 2)
    ebitda = data['EBITDA']
    ebitda_shares = round(float(data['EBITDA']) / float(data['SharesOutstanding']), 2)
    beta = data['Beta']
    fifty_two_h = data['52WeekHigh']
    fifty_two_l = data['52WeekLow']
    dividend_date = data['DividendDate']
    shares = data['SharesOutstanding']

    #description data
    asset_type = data['AssetType']
    name = data['Name']
    desc = data['Description']
    exchange = data['Exchange']
    currency = data['Currency']
    country = data['Country']
    sector = data['Sector']
    industry = data['Industry']

    #create de data frame with all the information
    overview_df = pd.DataFrame({'TICKER': t, 'Revenue [millions]': revenue, 'Gross Margin [%]': gross_margin, 
                        'P/E Ratio': peratio, 'P/E/G Ratio': pegratio,
                        'Growth 5 years [%]': growth_5y, 'P/S Ratio':psratio, 
                        'Book Value per Share': book_value, 'P/B Ratio': pbookratio,
                        "Dividens per Share": dividends_share, 'EPS': eps,
                        'Revenue per Share': revenue_share, 'ROE': roe, 'ROA': roa,
                        'Profit Margin [%]': profit_margin, 'Operating Margin [%]': operating_margin,
                        'EBITDA': ebitda, 'EBITDA per Share': ebitda_shares, 'Beta': beta,
                        '52W High': fifty_two_h, '52W Low': fifty_two_l, 'Dividend Date': dividend_date,
                        'Shares Outstanding': shares
                        }, index=[0])
    
    #create df with description
    description_df = pd.DataFrame({'Ticker': t,'Asset type': asset_type, 'Name': name, 'Description': desc,
                                   'Exchange': exchange, 'Currency': currency, 'Country': country,
                                   'Sector': sector, 'Industry': industry}, index=['DATA'])
    
    overview_df = overview_df.fillna(0)
    overview_df = overview_df.replace(to_replace = "None", value = 0)

    description_df = description_df.T

    return overview_df, description_df

#function to obtain the cash flow of the ticker    
def cash_flow(ticker):
    """Please enter the TICKER you would like to view the Cash Flow"""
    t = str(ticker)
    url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol='+ t +'&apikey='+ K
    r = requests.get(url)
    data = r.json()

    #select only the annual reports
    tkt = data['annualReports']
    
    #lists to store the data
    fiscalDateEnding = []
    reportedCurrency = []
    operatingCashflow = []
    paymentsForOperatingActivities = []
    proceedsFromOperatingActivities = []
    changeInOperatingLiabilities = []
    changeInOperatingAssets = []
    depreciationDepletionAndAmortization = []
    capitalExpenditures = []
    changeInReceivables = []
    changeInInventory = []
    profitLoss = []
    cashflowFromInvestment =[]
    cashflowFromFinancing = []
    proceedsFromRepaymentsOfShortTermDebt = []
    paymentsForRepurchaseOfCommonStock = []
    paymentsForRepurchaseOfEquity = []
    paymentsForRepurchaseOfPreferredStock = []
    dividendPayout = []
    dividendPayoutCommonStock = []
    dividendPayoutPreferredStock = []
    proceedsFromIssuanceOfCommonStock = []
    proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet = []
    proceedsFromIssuanceOfPreferredStock = []
    proceedsFromRepurchaseOfEquity = []
    proceedsFromSaleOfTreasuryStock = []
    changeInCashAndCashEquivalents = []
    changeInExchangeRate = []
    netIncome = []

    #browse through the dictionary and append the data to the lists 
    for i in tkt:
        fiscalDateEnding.append(i['fiscalDateEnding'])
        reportedCurrency.append(i['reportedCurrency'])
        operatingCashflow.append(i['operatingCashflow'])
        paymentsForOperatingActivities.append(i['paymentsForOperatingActivities'])
        proceedsFromOperatingActivities.append(i['proceedsFromOperatingActivities'])
        changeInOperatingLiabilities.append(i['changeInOperatingLiabilities'])
        changeInOperatingAssets.append(i['changeInOperatingAssets'])
        depreciationDepletionAndAmortization.append(i['depreciationDepletionAndAmortization'])
        capitalExpenditures.append(i['capitalExpenditures'])
        changeInReceivables.append(i['changeInReceivables'])
        changeInInventory.append(i['changeInInventory'])
        profitLoss.append(i['profitLoss'])
        cashflowFromInvestment.append(i['cashflowFromInvestment'])
        cashflowFromFinancing.append(i['cashflowFromFinancing'])
        proceedsFromRepaymentsOfShortTermDebt.append(i['proceedsFromRepaymentsOfShortTermDebt'])
        paymentsForRepurchaseOfCommonStock.append(i['paymentsForRepurchaseOfCommonStock'])
        paymentsForRepurchaseOfEquity.append(i['paymentsForRepurchaseOfEquity'])
        paymentsForRepurchaseOfPreferredStock.append(i['paymentsForRepurchaseOfPreferredStock'])
        dividendPayout.append(i['dividendPayout'])
        dividendPayoutCommonStock.append(i['dividendPayoutCommonStock'])
        dividendPayoutPreferredStock.append(i['dividendPayoutPreferredStock'])
        proceedsFromIssuanceOfCommonStock.append(i['proceedsFromIssuanceOfCommonStock'])
        proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet.append(i['proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet'])
        proceedsFromIssuanceOfPreferredStock.append(i['proceedsFromIssuanceOfPreferredStock'])
        proceedsFromRepurchaseOfEquity.append(i['proceedsFromRepurchaseOfEquity'])
        proceedsFromSaleOfTreasuryStock.append(i['proceedsFromSaleOfTreasuryStock'])
        changeInCashAndCashEquivalents.append(i['changeInCashAndCashEquivalents'])
        changeInExchangeRate.append(i['changeInExchangeRate'])
        netIncome.append(i['netIncome'])

    #create de data frame with the cash flow information
    cash_flow_df = pd.DataFrame({'Date': fiscalDateEnding,'Currency': reportedCurrency, 
                       'Operating CF': operatingCashflow,
                       'Payment Ops Activities': paymentsForOperatingActivities,
                       'Proceeds from Ops Activities': proceedsFromOperatingActivities,
                       'Change in Ops Liabilities': changeInOperatingLiabilities,
                       'Change in Ops Assets': changeInOperatingAssets,
                       'Depreciation & Amortization': depreciationDepletionAndAmortization,
                       'CAPEX': capitalExpenditures, 'Change in Receivables': changeInReceivables,
                       'Change in Inventory': changeInInventory, 'Profit & Loss': profitLoss,
                       'CF from Investment': cashflowFromInvestment,'CF from Financing': cashflowFromFinancing,
                       'Proceeds from Repayment of Short Term Debt': proceedsFromRepaymentsOfShortTermDebt,
                       'Payments for Repurchase of Common Stock': paymentsForRepurchaseOfCommonStock,
                       'Payments for Repurchase of Equity': paymentsForRepurchaseOfEquity,
                       'Payments for Repurchase of Preferred Stock': paymentsForRepurchaseOfPreferredStock,
                       'Dividens Payout': dividendPayout,
                       'Dividend Payout Common Stock': dividendPayoutCommonStock, 
                       'Dividend Payout Preferred Stock': dividendPayoutPreferredStock,
                       'Proceeds from Issuance of Common Stock': proceedsFromIssuanceOfCommonStock, 
                       'Proceeds from Issuance of Preferred Stock': proceedsFromIssuanceOfPreferredStock,
                       'Proceeds from Issuance of Long Term Debt & Capital Securities Net': proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet,
                       'Proceeds from Repurchase of Equity': proceedsFromRepurchaseOfEquity, 
                       'Proceeds from Sale of Treasury Stock': proceedsFromSaleOfTreasuryStock,
                       'Change in Cash & Cash Equivalents': changeInCashAndCashEquivalents, 
                       'Change in Exchange Rate': changeInExchangeRate,
                       'Net Income': netIncome})
    
    cash_flow_df = cash_flow_df.T
    cash_flow_df = cash_flow_df.fillna(0)
    cash_flow_df = cash_flow_df.replace(to_replace = "None", value = 0)

    return cash_flow_df

#function to obtain the income statement of the ticker
def income_statement(ticker):
    """Please enter the TICKER you would like to view the Income Statement"""
    t = str(ticker)
    url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+ t +'&apikey='+ K
    r = requests.get(url)
    data = r.json()

    #select only the annual reports
    tkt = data['annualReports']
    
    #lists to store the data
    fiscalDateEnding = []
    reportedCurrency = []
    grossProfit = []
    totalRevenue = []
    costOfRevenue = []
    costofGoodsAndServicesSold = []
    operatingIncome = []
    sellingGeneralAndAdministrative = []
    researchAndDevelopment = []
    operatingExpenses = []
    investmentIncomeNet = []
    netInterestIncome = []
    interestIncome =[]
    interestExpense = []
    nonInterestIncome = []
    otherNonOperatingIncome = []
    depreciation = []
    depreciationAndAmortization = []
    incomeBeforeTax = []
    incomeTaxExpense = []
    interestAndDebtExpense = []
    netIncomeFromContinuingOperations = []
    comprehensiveIncomeNetOfTax = []
    ebit = []
    ebitda = []
    netIncome = []

    #browse through the dictionary and append the data to the lists 
    for i in tkt:
        fiscalDateEnding.append(i['fiscalDateEnding'])
        reportedCurrency.append(i['reportedCurrency'])
        grossProfit.append(i['grossProfit'])
        totalRevenue.append(i['totalRevenue'])
        costOfRevenue.append(i['costOfRevenue'])
        costofGoodsAndServicesSold.append(i['costofGoodsAndServicesSold'])
        operatingIncome.append(i['operatingIncome'])
        sellingGeneralAndAdministrative.append(i['sellingGeneralAndAdministrative'])
        researchAndDevelopment.append(i['researchAndDevelopment'])
        operatingExpenses.append(i['operatingExpenses'])
        investmentIncomeNet.append(i['investmentIncomeNet'])
        netInterestIncome.append(i['netInterestIncome'])
        interestIncome.append(i['interestIncome'])
        interestExpense.append(i['interestExpense'])
        nonInterestIncome.append(i['nonInterestIncome'])
        otherNonOperatingIncome.append(i['otherNonOperatingIncome'])
        depreciation.append(i['depreciation'])
        depreciationAndAmortization.append(i['depreciationAndAmortization'])
        incomeBeforeTax.append(i['incomeBeforeTax'])
        incomeTaxExpense.append(i['incomeTaxExpense'])
        interestAndDebtExpense.append(i['interestAndDebtExpense'])
        netIncomeFromContinuingOperations.append(i['netIncomeFromContinuingOperations'])
        comprehensiveIncomeNetOfTax.append(i['comprehensiveIncomeNetOfTax'])
        ebit.append(i['ebit'])
        ebitda.append(i['ebitda'])
        netIncome.append(i['netIncome'])

    #create the df with the dara in the lists
    income_statement_df = pd.DataFrame({'Date': fiscalDateEnding, 'Currency': reportedCurrency, 
                       'Gross Profit': grossProfit, 'Total Revenue': totalRevenue, 
                       'Cost of Revenue': costOfRevenue, 'COGS': costofGoodsAndServicesSold, 
                       'Operating Income': operatingIncome,
                       'Selling General & Administrative': sellingGeneralAndAdministrative, 
                       'R&D': researchAndDevelopment, 'OPEX': operatingExpenses,
                       'Investment Income Net': investmentIncomeNet, 'Net Interest Income': netInterestIncome,
                       'Interest Income': interestIncome, 'Interest Expenses': interestExpense, 
                       'Non Interest Income': nonInterestIncome,
                       'Other Non Operating Income': otherNonOperatingIncome, 'Depreciation': depreciation,
                       'Depreciation & Amortization': depreciationAndAmortization, 
                       'Income Before Tax': incomeBeforeTax, 'Income Tax Expense': incomeTaxExpense, 
                       'Interest & Debt Expense': interestAndDebtExpense,
                       'Net Income from Continuing Ops': netIncomeFromContinuingOperations,
                       'Comprehensive Income Net of Tax': comprehensiveIncomeNetOfTax,
                       'EBIT': ebit, 'EBITDA': ebitda, 'Net Income': netIncome})
    
    income_statement_df = income_statement_df.T
    income_statement_df = income_statement_df.fillna(0)
    income_statement_df = income_statement_df.replace(to_replace = "None", value = 0)

    return income_statement_df

#function to obtain the balance sheet of the ticker
def balance_sheet(ticker):
    """Please enter the TICKER you would like to view the Balance Sheet"""
    t = str(ticker)
    url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol='+ t +'&apikey='+ K
    r = requests.get(url)
    data = r.json()

    #select only the annual reports
    tkt = data['annualReports']

    #lists to store the data    
    fiscalDateEnding = []
    reportedCurrency = []
    totalAssets = []
    totalCurrentAssets = []
    cashAndCashEquivalentsAtCarryingValue = []
    cashAndShortTermInvestments = []
    inventory = []
    currentNetReceivables = []
    totalNonCurrentAssets = []
    propertyPlantEquipment = []
    accumulatedDepreciationAmortizationPPE = []
    intangibleAssets = []
    intangibleAssetsExcludingGoodwill =[]
    goodwill = []
    investments = []
    longTermInvestments = []
    shortTermInvestments = []
    otherCurrentAssets = []
    otherNonCurrentAssets = []
    totalLiabilities = []
    totalCurrentLiabilities = []
    currentAccountsPayable = []
    deferredRevenue = []
    currentDebt = []
    shortTermDebt = []
    totalNonCurrentLiabilities = []
    capitalLeaseObligations = []
    longTermDebt = []
    currentLongTermDebt = []
    longTermDebtNoncurrent = []
    shortLongTermDebtTotal = []
    otherCurrentLiabilities = []
    otherNonCurrentLiabilities = []
    totalShareholderEquity = []
    treasuryStock = []
    retainedEarnings = []
    commonStock = []
    commonStockSharesOutstanding = []
    #browse through the dictionary and append the data to the lists 
    for i in tkt:
        fiscalDateEnding.append(i['fiscalDateEnding'])
        reportedCurrency.append(i['reportedCurrency'])
        totalAssets.append(i['totalAssets'])
        totalCurrentAssets.append(i['totalCurrentAssets'])
        cashAndCashEquivalentsAtCarryingValue.append(i['cashAndCashEquivalentsAtCarryingValue'])
        cashAndShortTermInvestments.append(i['cashAndShortTermInvestments'])
        currentNetReceivables.append(i['currentNetReceivables'])
        inventory.append(i['inventory'])
        totalNonCurrentAssets.append(i['totalNonCurrentAssets'])
        propertyPlantEquipment.append(i['propertyPlantEquipment'])
        accumulatedDepreciationAmortizationPPE.append(i['accumulatedDepreciationAmortizationPPE'])
        intangibleAssets.append(i['intangibleAssets'])
        intangibleAssetsExcludingGoodwill.append(i['intangibleAssetsExcludingGoodwill'])
        goodwill.append(i['goodwill'])
        investments.append(i['investments'])
        longTermInvestments.append(i['longTermInvestments'])
        shortTermInvestments.append(i['shortTermInvestments'])
        otherCurrentAssets.append(i['otherCurrentAssets'])
        otherNonCurrentAssets.append(i['otherNonCurrentAssets'])
        totalLiabilities.append(i['totalLiabilities'])
        totalCurrentLiabilities.append(i['totalCurrentLiabilities'])
        currentAccountsPayable.append(i['currentAccountsPayable'])
        deferredRevenue.append(i['deferredRevenue'])
        currentDebt.append(i['currentDebt'])
        shortTermDebt.append(i['shortTermDebt'])
        totalNonCurrentLiabilities.append(i['totalNonCurrentLiabilities'])
        capitalLeaseObligations.append(i['capitalLeaseObligations'])
        longTermDebt.append(i['longTermDebt'])
        currentLongTermDebt.append(i['currentLongTermDebt'])
        longTermDebtNoncurrent.append(i['longTermDebtNoncurrent'])
        shortLongTermDebtTotal.append(i['shortLongTermDebtTotal'])
        otherCurrentLiabilities.append(i['otherCurrentLiabilities'])
        otherNonCurrentLiabilities.append(i['otherNonCurrentLiabilities'])
        totalShareholderEquity.append(i['totalShareholderEquity'])
        treasuryStock.append(i['treasuryStock'])
        retainedEarnings.append(i['retainedEarnings'])
        commonStock.append(i['commonStock'])
        commonStockSharesOutstanding.append(i['commonStockSharesOutstanding'])
# Después creo el df usando las listas que creé
    balance_sheet_df = pd.DataFrame({'Date': fiscalDateEnding, 'Currency': reportedCurrency, 'Total Assets': totalAssets,
                       'Total Current Assets': totalCurrentAssets, 
                       'Cash and Cash Equivalents at Carrying Value': cashAndCashEquivalentsAtCarryingValue,
                       'Cash and Short Term Investments': cashAndShortTermInvestments, 
                       'Current Net Receivables': currentNetReceivables, 'Inventory': inventory, 
                       'Total Non Current Assets': totalNonCurrentAssets, 
                       'Property, Plant & Equipment': propertyPlantEquipment,
                       'Accumulated Depreciation & Amortization PPE': accumulatedDepreciationAmortizationPPE, 
                       'Intangible Assets': intangibleAssets,
                       'Intangible Assets Excluding Goodwill': intangibleAssetsExcludingGoodwill, 
                       'Goodwill': goodwill, 'Investments': investments, 
                       'Long Term Investments': longTermInvestments,
                       'Short Term Investments': shortTermInvestments, 
                       'Other Current Assets': otherCurrentAssets,
                       'Other Non Current Assets': otherNonCurrentAssets, 
                       'Total Liabilities': totalLiabilities,
                       'Total Current Liabilities': totalCurrentLiabilities, 
                       'Current Accounts Payable': currentAccountsPayable, 'Deferred Revenue': deferredRevenue, 
                       'Short Term Debt': shortTermDebt, 
                       'Total Non Current Liabilities': totalNonCurrentLiabilities, 'Current Debt': currentDebt, 
                       'Capital Lease Obligations': capitalLeaseObligations, 'Long Term Debt': longTermDebt,
                       'Current Long Term Debt': currentLongTermDebt, 
                       'Long Term Debt Non Current': longTermDebtNoncurrent,
                       'Short Long Term Debt Total': shortLongTermDebtTotal, 
                       'Other Current Liabilities': otherCurrentLiabilities,
                       'Total Shareholder Equity': totalShareholderEquity, 'Treasury Stock': treasuryStock,
                       'Other Non Current Liabilities': otherNonCurrentLiabilities, 
                       'Retained Earnings': retainedEarnings, 'Common Stock': commonStock, 
                       'commonStockSharesOutstanding': commonStockSharesOutstanding})
    balance_sheet_df = balance_sheet_df.T
    balance_sheet_df = balance_sheet_df.fillna(0)
    balance_sheet_df = balance_sheet_df.replace(to_replace = "None", value = 0)

    current_ratio = round(float(balance_sheet_df.loc[['Total Current Assets'], 0])
                    / float(balance_sheet_df.loc[['Total Current Liabilities'], 0]), 2)
    working_capital = round((((float(balance_sheet_df.loc[['Total Current Assets'], 0])
                    - float(balance_sheet_df.loc[['Total Current Liabilities'], 0]))) / 10000), 2)
    quick_ratio = round(((float(balance_sheet_df.loc[['Total Current Assets'], 0]))
                         - float(balance_sheet_df.loc[['Inventory'], 0]))
                    / float(balance_sheet_df.loc[['Total Current Liabilities'], 0]), 2)
    debt_asset_ratio = round(float(balance_sheet_df.loc[['Total Liabilities'], 0])
                    / float(balance_sheet_df.loc[['Total Assets'], 0]), 2)
    debt_equity_ratio = round(float(balance_sheet_df.loc[['Total Liabilities'], 0])
                    / float(balance_sheet_df.loc[['Total Shareholder Equity'], 0]), 2)
    
    ratios_df = pd.DataFrame({'Current Ratio': current_ratio, 'Working Capital (x10.000)': working_capital,
                              'Quick Ratio': quick_ratio, 'Debt-to-Assets Ratio': debt_asset_ratio, 
                              'Debt-to-Equity Ratio': debt_equity_ratio}, index=[0])

    return balance_sheet_df, ratios_df

#price formula with price, and graham and fair value indicators
def price(ticker):
    t = str(ticker)
    #request for price data (GLOBAL_QUOTES)
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+ t +'&apikey='+ K
    r = requests.get(url)
    data = r.json()

    #select the global quote
    tkt = data['Global Quote']

    #lists to complete
    open = []
    last_close = []
    high = []
    low = []
    price = []
    
    #browse the global quote data amd append to lists
    open = tkt['02. open']
    last_close = tkt['08. previous close']
    high = tkt['03. high']
    low = tkt['04. low']
    price = float(tkt['05. price'])

    #bring values from overview for the next formulas
    #request of overview data
    url1 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ t +'&apikey='+ K
    r1 = requests.get(url1)
    data1 = r1.json()

    #extract the needed values from the data frame
    p_b = float(data1['PriceToBookRatio'])
    g = round(float(data1['PERatio']) / float(data1['PEGRatio']), 2)

    #obtain the AVG EPS of the last ten years
    #variable to store the EPS
    eps = 0

    #connection to alpha vantage
    url2 = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='+ t +'&apikey='+ K
    r2 = requests.get(url2)
    data2 = r2.json()

    #access the annual earnings per share
    ern = data2['annualEarnings']

    #lists to complete with the data
    fiscalDateEnding = []
    reportedEPS = []

    #browse and append through the data
    for i in ern:
        fiscalDateEnding.append(i['fiscalDateEnding'])
        reportedEPS.append(i['reportedEPS'])

    #check how many data points there are
    #if there are less than ten years use all, if more, use last 10
    if len(reportedEPS) > 10:
        for i in range(10):
            eps += float(reportedEPS[i])
        eps = eps/10
        years_eps = 'More than ten'
    else:
        for i in range(len(reportedEPS)):
            eps += float(reportedEPS[i])
        eps = eps/len(reportedEPS)
        years_eps = len(reportedEPS)

    #FAIR VALUE FORMULA (proxy)
    #EPS=Ernings per share (last)
    #PR=Price (actual)
    #PB=Price to book value (last)
    #22.5 comes from 15x EPS and 1.5x P/B
    if (eps*(price/p_b)) < 0:
        f_v = 0
    else:
        f_v = (22.5*eps*(price/p_b))**(1/2)

    #ACID Graham intrinsic value formula for ticker price
    graham = (eps*(8.5+2*g)*RF)/Y
    a_graham = (eps*(7+g)*RF)/Y
    
    #Security margins for fair value, and both grahams formulas
    sec_mar_fv = round(((f_v/price)-1)*100, 2) 
    sec_mar_gr = round(((graham/price)-1)*100, 2)
    sec_mar_a_gr = round(((a_graham/price)-1)*100, 2)

    #create the data frame with all the data
    price_df = pd.DataFrame({'TICKER': t, 'Price': price, 'Open': open, "Last day close": last_close,
                            'High': high, 'Low': low, 'Fair Value': f_v, 
                            'Security Margin FV': sec_mar_fv, "Growth [%]": g, "EPS [avg]": eps,
                            'Graham': graham, 'Security Margin Graham': sec_mar_gr,
                            'Graham ACID': a_graham, 'Security Margin Graham ACID': sec_mar_a_gr,
                            'Years of EPS': years_eps}, index=[0])

    return price_df
