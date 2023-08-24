
sp_500 = []
ndq_100 = []

with open("tickers_sp.rtf") as file_sp:
    for line in file_sp:
        sp_500.append(line.replace('\n', ''))
    
with open("tickers_nasdaq.rtf") as file_ndq:
    for line in file_ndq:
        ndq_100.append(line.replace('\n', ''))

rep = set(sp_500).intersection(ndq_100)

for i in rep:
    sp_500.remove(i)

print(set(sp_500).intersection(ndq_100))