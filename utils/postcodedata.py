import pandas as pd

def read_postcode_data(path):

    PCD = [] #0
    latitude = [] #6
    longitude = [] #7
    persons = [] #8
    females = [] #9
    males = [] #10

    with open(path) as f:
        next(f)

        for line in f:

            l = line.rstrip().split(",")
            PCD.append(l[0])
            latitude.append(float(l[7]))
            longitude.append(float(l[6]))

            if len(l[8]) != 0:
                persons.append(int(l[8]))
            else:
                persons.append(0)

            if len(l[9]) != 0:
                females.append(int(l[9]))
            else:
                females.append(0)

            if len(l[10]) != 0:
                males.append(l[10])
            else:
                males.append(0)


    df = pd.DataFrame({"PC" : PCD, "Latitude": latitude,
                       "Longitude": longitude, "Persons": persons,
                       "Females": females, "Males": males})

    return df
