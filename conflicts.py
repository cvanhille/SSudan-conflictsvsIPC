import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

if __name__ == "__main__":

  sts=["Western Bahr el Ghazal","Northern Bahr el Ghazal","Warrap","Lakes","Upper Nile","Jonglei","Unity","Central Equatoria","Western Equatoria","Eastern Equatoria","Gogrial"]
  months=pd.date_range(start="20130730",end="20150930",freq="M")
  periodstart=months[0:len(months)-1]
  periodsend=months[1:len(months)]
  conflicts=pd.DataFrame(np.zeros((len(periodstart),len(sts))),index=periodstart,columns=sts)
  IPCS=pd.DataFrame(np.zeros((len(periodstart),len(sts)-1)),index=periodstart,columns=sts[:len(sts)-1])
  totalconflicts=pd.Series(np.zeros(len(sts)),index=sts)
  data=pd.read_csv("ACLED - 1900-01-01-2018-07-11-South_Sudan.csv")
  dates=data['event_date']
  states=data['admin1']
  pss=dt.datetime.date(periodstart[0])
  pee=dt.datetime.date(periodsend[len(periodsend)-1])

  for i in range(len(dates)):
    d=dt.datetime.date(dt.datetime.strptime(dates[i],"%d %B %Y"))

    for j in range(len(periodstart)):
      ps=dt.datetime.date(periodstart[j])
      pe=dt.datetime.date(periodsend[j])

      if d>=ps and d<pe:
        conflicts.at[periodstart[j],states[i]]=conflicts.at[periodstart[j],states[i]]+1

    if d>=pss and d<pee:
      totalconflicts.at[states[i]]=totalconflicts.at[states[i]]+1

  normalizedconflicts=conflicts/totalconflicts*100

  for i in range(len(sts)):
    plt.xticks(rotation=70)
    plt.plot(periodstart,conflicts[sts[i]])
    plt.title(sts[i])
    plt.xlabel("Time period")
    plt.ylabel("Conflicts")
    str1=sts[i]+" - Conflicts.png"
    plt.savefig(str1)
    plt.clf()
    plt.xticks(rotation=70)
    plt.title(sts[i])
    plt.xlabel("Time period")
    plt.ylabel("% of total conflicts in the state")
    plt.plot(periodstart,normalizedconflicts[sts[i]])
    plt.legend()
    str2=sts[i]+" - Conflicts %"+".png"
    plt.savefig(str2)
    plt.clf()

  for i in range(len(sts)-1):
    stripc=sts[i]+".csv"
    ipc=pd.read_csv(stripc,sep=";")
    datesipc=ipc["Periodstart"]
    criticipc=ipc["IPC>=3"]
    
    for k in range(len(datesipc)):    
      dipc=dt.datetime.date(dt.datetime.strptime(datesipc[k],"%d/%m/%Y"))

      for j in range(len(periodstart)):
        ps=dt.datetime.date(periodstart[j])
        pe=dt.datetime.date(periodsend[j])

        if dipc<pe:
          IPCS.at[periodstart[j],sts[i]]=criticipc[k]

  for i in range(len(sts)-1):
    plt.xticks(rotation=70)
    plt.plot(periodstart,IPCS[sts[i]],label="IPC")
    plt.title(sts[i])
    plt.xlabel("Time period")
    plt.ylabel("% of population in IPC crisis or above")
    str1=sts[i]+" - IPC.png"
    plt.savefig(str1)
    plt.xlabel("Time period")
    plt.ylabel("%")
    plt.plot(periodstart,normalizedconflicts[sts[i]],label="Conflicts")
    plt.legend()
    str2=sts[i]+" - IPC - Conflicts"+".png"
    plt.savefig(str2)
    plt.clf()
