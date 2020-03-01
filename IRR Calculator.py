#IMPORTS
import pandas as pd
import numpy as np
from tkinter import *
import math
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

#VARIABLES FOR UI
main = Tk()
main.title("Inv")
main.geometry('700x450')
DealTitle = StringVar()
ExitSharePrice = StringVar()
MonthsToExit = StringVar()
ShareValue = StringVar()
LatestPreferredShareValue = StringVar()
CollateralShares = StringVar()
FinancingAmount = StringVar()
StockFee = StringVar()
PaymentinKind = StringVar()

#TERMS 
Terms = { "Hurdle" : 0.15,
        "Carried_Interest" : 0.10,
         "Equity_Incentive": 0.11,
        " Advance_Rate" : 0.07,
         "Contract_Fee": 0.05}

#ARRAYS TO STORE DATA
Deal_Titles = []
IRRs = []
IRRgross = []
Months = []
Expc = []
Ext = []
Coll = []
LTV =[]

#CALCULATIONS
def calculatePayment():
    
    #GET THE ENTRIES FROM UI
    Deal_Title = DealTitle.get()
    Exit_Share_Price = float(ExitSharePrice.get())
    Months_to_Exit = float(MonthsToExit.get())
    Share_Value = float(ShareValue.get())
    Latest_Preferred_Share_Value = float(LatestPreferredShareValue.get())
    Collateral_Shares = float(CollateralShares.get())
    Financing_Amount = float(FinancingAmount.get())
    Stock_Fee = float(StockFee.get())
    Payment_in_Kind = float(PaymentinKind.get())

    #CALCULATIONS NECESSARY
    Discount_to_Pref = (100 - (Share_Value/Latest_Preferred_Share_Value)*100)
    Collateral_Amount = Collateral_Shares * Latest_Preferred_Share_Value
    Loan_to_Value = Financing_Amount / Collateral_Amount
    Stock_Component = Stock_Fee * Collateral_Shares * Exit_Share_Price
    Interest_Component = (((1+(1+Payment_in_Kind)**(1/12)-1)**Months_to_Exit)-1 )* Financing_Amount
    Available_Collateral = Collateral_Shares * Exit_Share_Price
    Sumx = (Interest_Component + Stock_Component + Financing_Amount)
    Expected_Return = min(Available_Collateral, Sumx)
    IRR = ((Expected_Return / Financing_Amount) ** (1/(Months_to_Exit/12))) - 1
    if Terms["Hurdle"] > IRR:
        Net_IRR = IRR
    else:
        Net_IRR = max(Terms["Hurdle"], IRR * (1 - Terms["Carried_Interest"]))
    Carry_Value = IRR - Net_IRR

    #DISPLAY RESULTS
    lblLTV = Label(main, text = '$ %.2f' % Loan_to_Value).grid(row = 1, column = 6, padx = 0, pady = 10)
    lblStockComponent = Label(main, text = '$ %.2f' % Stock_Component).grid(row = 2, column = 6, padx = 0, pady = 10)
    lblInterestComponent = Label(main, text = '$ %.2f' % Interest_Component).grid(row = 3, column = 6, padx = 0, pady = 10)
    lblAvailableCollateral = Label(main, text = '$ %.2f' % Available_Collateral).grid(row = 4, column = 6, padx = 0, pady = 10)
    lblExpectedReturn = Label(main, text = '$ %.2f' % Expected_Return).grid(row = 5, column = 6, padx = 6, pady = 10)
    lblIRR = Label(main, text = ' %.4f' % IRR).grid(row = 6, column = 6, padx = 0, pady = 10)
    lblNetIRR = Label(main, text = ' %.4f' % Net_IRR).grid(row = 7, column = 6, padx = 0, pady = 10)
    lblCarryValue = Label(main, text = ' %.4f' % Carry_Value).grid(row = 8, column = 6, padx = 0, pady = 10)

    #STORE THE RESULTS
    Deal_Titles.append(Deal_Title)
    IRRgross.append(IRR*100)
    IRRs.append(Net_IRR*100)
    Months.append(MonthsToExit)
    Expc.append(Expected_Return)
    LTV.append(Loan_to_Value)
    Coll.append(Collateral_Amount)

    #PLOT ANY RESULT WANTED, IN THIS CASE IRR
    plt.plot(Deal_Titles, IRRgross, marker='o', linewidth=4)
    plt.xlabel("Scenarios")
    plt.ylabel("Gross IRR")
    plt.show()
    return

#WRITE DESIRED VARIABLES TO EXCEL    
def writetoexcel():
    df = pd.DataFrame(data= {'Gross IRR': IRRgross}, index = Deal_Titles)
    df.to_csv("scenarios.csv")

#LABELS AND ENTRIES FOR INPUTS
lblDealTitle = Label(main, text = 'DealTitle').grid(row = 0, column = 0, padx = 0, pady = 10)
entDealTitle = Entry(main, textvariable = DealTitle).grid(row = 0, column = 1)
lblExitSharePrice = Label(main, text = 'ExitSharePrice').grid(row = 1, column = 0, padx = 0, pady = 10)
entExitSharePrice = Entry(main, textvariable = ExitSharePrice).grid(row = 1, column = 1)
lblMonthsToExit = Label(main, text = 'MonthsToExit').grid(row = 3, column = 0, padx = 0, pady = 10)
entMonthsToExit = Entry(main, textvariable = MonthsToExit).grid(row = 3, column = 1)
lblShareValue = Label(main, text = 'ShareValue').grid(row = 4, column = 0, padx = 0, pady = 10)
entShareValue = Entry(main, textvariable = ShareValue).grid(row = 4, column = 1)
lblLatestPreferredShareValue = Label(main, text = 'LatestPreferredShareValue').grid(row = 5, column = 0, padx = 0, pady = 10)
entLatestPreferredShareValue = Entry(main, textvariable = LatestPreferredShareValue).grid(row = 5, column = 1)
lblCollateralShares = Label(main, text = 'CollateralShares').grid(row = 6, column = 0, padx = 0, pady = 10)
entCollateralShares = Entry(main, textvariable = CollateralShares).grid(row = 6, column = 1)
lblFinancingAmount = Label(main, text = 'FinancingAmount').grid(row = 7, column = 0, padx = 0, pady = 10)
entFinancingAmount = Entry(main, textvariable = FinancingAmount).grid(row = 7, column = 1)
lblStockFee = Label(main, text = 'StockFee').grid(row = 8, column = 0, padx = 0, pady = 10)
entStockFee = Entry(main, textvariable = StockFee).grid(row = 8, column = 1)
lblPaymentinKind = Label(main, text = 'PaymentinKind').grid(row = 9, column = 0, padx = 0, pady = 10)
entPaymentinKind = Entry(main, textvariable = PaymentinKind).grid(row = 9, column = 1)

#BUTTONS FOR FUNCTIONS
btn = Button(main, text = 'Calculate', command = calculatePayment).grid(row = 10, column = 1)
excelw = Button(main, text = 'Write to CSV', command = writetoexcel).grid(row = 10, column = 2)

#RESULT LABELS
lblLTV = Label(main, text = 'Loan_to_Value').grid(row = 1, column = 5, padx = 0, pady = 10)
lblStockComponent = Label(main, text = 'StockComponent').grid(row = 2, column = 5, padx = 0, pady = 10)
lblInterestComponent = Label(main, text = 'InterestComponent').grid(row = 3, column = 5, padx = 0, pady = 10)
lblAvailableCollateral = Label(main, text = 'AvailableCollateral').grid(row = 4, column = 5, padx = 0, pady = 10)
lblExpectedReturn = Label(main, text = 'ExpectedReturn').grid(row = 5, column = 5, padx = 5, pady = 10)
lblIRR = Label(main, text = 'IRR').grid(row = 6, column = 5, padx = 0, pady = 10)
lblNetIRR = Label(main, text = 'Net IRR').grid(row = 7, column = 5, padx = 0, pady = 10)
lblCarryValue = Label(main, text = 'CarryValue ').grid(row = 8, column = 5, padx = 0, pady = 10)


main.mainloop()
