from datetime import datetime

# date = datetime.today().strftime('%d')
# conv=int(date)*100
# topn=str(conv)
# print(topn)

date = datetime.today().strftime('%Y_%m_%d')
filename='Sales'+'_'+str(date)
print(filename)