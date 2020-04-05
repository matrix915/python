import json
import csv
from collections import OrderedDict
from datetime import datetime,timezone

with open('animal-map.json') as jsonfile:
    input_json = json.load(jsonfile)

with open('animal-map.json') as f:
    temp_json = json.load(f)

add = []
add = []

def ordered(d, desired_key_order):
    return OrderedDict([(key, d[key]) for key in desired_key_order])

def add_element(row, add, json_temp, flag, temp):
    with open('species.csv') as csvfile:
        input_csv = csv.reader(csvfile)
        j=0
        for i in input_csv:
            result = i[4].find(json_temp[row])
            if result > 0:
                if temp == False:
                    add.append({
                        'value' : i[5],
                        'line' : i[0]
                    })
                else:                    
                    if flag == 1:
                        add.append({
                            'value' : i[5],
                            'line' : i[0]
                        })
                    else:
                        add[j]['value'] = add[j]['value'] + ' ' + i[5]
                        add[j]['line'] = add[j]['line'] + ', ' + i[0]
                        j += 1


International = input_json['International']
temp_Inter = temp_json['International']
for row1 in International:
    country = International[row1]
    for row2 in country:
        StandRefer = country[row2]
        for row3 in StandRefer:
            EnSizeName = StandRefer[row3]
            flag = 0
            for row4 in EnSizeName:
                if row4 == 'matching-key-fragment-01' or row4 == 'matching-key-fragment-02':
                    flag += 1
                    add_element(row4, add, EnSizeName, flag, True)
                    temp_Inter[row1][row2][row3] = add
                    continue
                SCWL = EnSizeName[row4]
                flag = 0
                for row5 in SCWL:
                    print(SCWL[row5])
                    if row5 == 'matching-key-fragment-01' or row5 == 'matching-key-fragment-02':
                        if row4 != 'Length':
                            add = []
                            add_element(row5, add, SCWL, flag, False)
                            temp_Inter[row1][row2][row3][row4] = add
                            add = []
                            break
                        else:
                            flag += 1
                            add_element(row5, add, SCWL, flag, True)
                            temp_Inter[row1][row2][row3][row4] = add
                            if flag == 2:
                                add = []
                            continue
                    Total = SCWL[row5]
                    flag = 0
                    add = []
                    for row6 in Total:
                        if row6 == 'matching-key-fragment-01' or row6 == 'matching-key-fragment-02':
                            flag += 1
                            add_element(row6, add, Total, flag, True)
                            temp_Inter[row1][row2][row3][row4][row5] = add
                        if flag == 2:
                            add = []

temp_json['Type'] = 'Resource List'
input_json['Generated'] = input_json.pop('Version')
del temp_json['Provider']
del temp_json['report-type']
del temp_json['report-format']

now_utc = datetime.now(timezone.utc)
time=str(now_utc)
date=time[0:16]+" UTC"

temp_json['Generated'] = date

desired_order=("Type","Generated", "International")
middle = ordered(temp_json, desired_order)
temp_json = middle

with open('final.json', 'w') as f:
    json.dump(temp_json, f, indent=2)

