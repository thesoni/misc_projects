import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
    
dates_str = ['1/1/2020', '2/1/2020', '3/1/2020', '12/31/2020']
dates_obj = []

y = [5,10,600,10]

for d in dates_str:
    datetime_object = datetime.strptime(d, '%m/%d/%Y')
    dates_obj.append(datetime_object)

dates_matplot = matplotlib.dates.date2num(dates_obj)

plt.plot_date(dates_matplot,y)
plt.show()
