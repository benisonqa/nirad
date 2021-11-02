import csv
import json


def csv_parser(filename):
    try:
        data_list = list()
        with open(filename, 'r', newline='') as mycsv:
            reader = csv.DictReader(mycsv)
            for row in reader:
                val = []
                for k, v in row.items():
                    if v:
                        val.append(True)
                    else:
                        val.append(False)
                if any(val):
                    data_list.append(json.loads(json.dumps(row)))

        stripped_list = list()
        for x in range(len(data_list)):
            for k, v in data_list[x].items():
                if v == '':
                    v = ''.join([val for (key, val) in data_list[x-1].items() if k == key])
                data_list[x][k] = v
            stripped_list.append({a: b.strip() for (a, b) in data_list[x].items()})

        return stripped_list
    except Exception as E:
        print("CSV file is missing or not formatted properly")
        assert False, "Format the CSV file properly and retry"


def filter_data(all_data, filter_list):
    for elements in filter_list:
        for k, v in elements.items():
            if k == "FILE":
                segment = v.split('/')[-1]
    pass
