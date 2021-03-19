import pandas as pd
from collections import OrderedDict
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import re

allareas = pd.read_csv("sect203_Determined_Areas_Only.csv", encoding='ISO-8859-1')
df = pd.DataFrame(data=allareas)

def state_selection(df, selection):
  unique_entries = list(df['NAMELSAD'].unique())
  total_pops = {u_entry: 0 for u_entry in unique_entries}
  for entry in total_pops.keys():
    df_match = df[df['NAMELSAD']==entry]
    total = None
    if selection == 'Total Population':
      df_match_vacit = df_match[df_match['LANGUAGE']==selection]['VACIT']
      df_match_mvacit = df_match[df_match['LANGUAGE']==selection]['MVACIT']
      total = df_match_vacit + df_match_mvacit
      try:
        total_pops[entry] += int(total)
      except:
        continue
    else:
      df_match_pop = df_match[df_match['LANGUAGE']==selection]['POP']
      total = df_match_pop
      try:
        total_pops[entry] += int(total)
      except:
        continue
  return total_pops

ethnicity_list = list(df['LANGUAGE'].unique())

for ethnicity in ethnicity_list:
  with open(f'{ethnicity}.csv', 'w+') as fh:
    writerObj = csv.writer(fh)
    ordered = OrderedDict(sorted(state_selection(df, ethnicity).items(), key=lambda x: x[1]))
    ordered_list = list(ordered.items())
    top_ten = ordered_list[-10:-1]
    location_names = [element[0] for element in top_ten]
    location_count = [element[1] for element in top_ten]
    writerObj.writerow(location_names)
    writerObj.writerow(location_count)

listOfLocations = ['Alaskan Athabascan','American Indian (All other American Indian Tribes)','American Indian (Apache)',
'American Indian (Pueblo)','Asian Indian', 'Cambodian','Chinese (including Taiwanese)','Filipino','Hispanic','Inupiat',
'Korean','Total Population','Vietnamese',"Yup'ik"]

for loc in listOfLocations:
  with open(f"{loc}.csv",'r') as fh:
    reader = csv.reader(fh)
    coords = list(reader)
    x = coords[0]
    y = [int(x) for x in coords[1]]
    plt.figure(figsize=(15,10))
    bars = plt.bar(x=x, height=y)
    plt.xticks(rotation=45)
    plt.ylim(0,max(y)+.10*max(y))
    locs, labels = plt.xticks()
    for i in range(len(y)):
      plt.annotate(s=str(y[i]), xy=(locs[i],y[i]+.02*max(y)), ha='center')
    plt.title(f'Top {len(x)} region(s): {loc}', fontdict = {'fontsize' : 16})
    plt.tight_layout()
    plt.savefig(f"{loc}.png")
    plt.show()    
