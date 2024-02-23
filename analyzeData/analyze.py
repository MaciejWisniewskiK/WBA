import pandas as pd
import geopy.distance
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import bisect

def get_location(cords):
    return (round(float(cords[0]), 2), round(float(cords[1]), 2))

def get_mid_point_location(cords1, cords2):
    x = (float(cords1[0]) + float(cords2[0])) / 2
    y = (float(cords1[1]) + float(cords2[1])) / 2
    return get_location((x, y))


def get_data_by_bus_nr(file):
    df = pd.read_json(file)

    dict_by_nr = {}

    for ind in range(len(df[0])):

        if not df[0][ind]['nr'] in dict_by_nr:
            dict_by_nr[df[0][ind]['nr']] = []

        try:
            dict_by_nr[df[0][ind]['nr']].append((datetime.strptime(df[0][ind]['time'], '%Y-%m-%d %H:%M:%S'), df[0][ind]['lat'], df[0][ind]['lon']))
        except:
            continue
    
    return dict_by_nr


def get_data_by_line(file, line):
    df = pd.read_json(file)
    loc_times = []
    for ind in range(len(df[0])):
        if str(df[0][ind]['line']) != line:
            continue
        try:
            loc_times.append((get_location((df[0][ind]['lat'], df[0][ind]['lon'])), datetime.strptime(df[0][ind]['time'], '%Y-%m-%d %H:%M:%S')))
        except:
            continue
    return loc_times


def plot_speed_histogram(max_speeds):
    plt.hist(max_speeds, bins = 10, color = 'skyblue', edgecolor = 'black')
    plt.xlabel('Max speed in km/h')
    plt.ylabel('Number of buses')
    plt.title('Max speed histogram')
    plt.show()
    plt.clf()


def plot_speed_map(locations, min_fract_speeding, size_multiplier):
    x = []
    y = []
    sizes = []
    for loc in locations.keys():
        size = locations[loc][0] / locations[loc][1]
        if size >= min_fract_speeding:
            size *= 10
            x.append(loc[0])
            y.append(loc[1])
            sizes.append(size * size_multiplier)

    plt.scatter(x, y, s=sizes)
    plt.title('Where did the busses exceed 50km/h')
    plt.show()
    plt.clf()


def analyze_speed(file, speed_maps_data):
    data_by_nr = get_data_by_bus_nr(file)
    max_speeds = []
    locations = {}

    for nr in data_by_nr:
        data_by_nr[nr].sort()

        max_speed = 0

        for ind in range(1, len(data_by_nr[nr])):
            last_cords = (data_by_nr[nr][ind - 1][1], data_by_nr[nr][ind - 1][2])
            curr_cords = (data_by_nr[nr][ind][1], data_by_nr[nr][ind][2])
            dist = geopy.distance.geodesic(last_cords, curr_cords).km

            last_time = data_by_nr[nr][ind - 1][0]
            curr_time = data_by_nr[nr][ind][0]
            duration = (curr_time - last_time).total_seconds()

            # remove bugged data
            if duration == 0:
                continue
            
            curr_speed = dist * 3600 / duration

            # remove bugged data
            if curr_speed > 100:
                continue

            max_speed = max(max_speed, curr_speed)
            loc = get_mid_point_location(last_cords, curr_cords)

            if not loc in locations:
                locations[loc] = [0, 0]
            locations[loc][1] += 1

            if curr_speed > 50: 
                locations[loc][0] += 1

        if max_speed > 0:
            max_speeds.append(max_speed)


    plot_speed_histogram(max_speeds)
    for elem in speed_maps_data:
        plot_speed_map(locations, elem[0], elem[1])


def analyze_punctuality(file, line, stop_cords, stop_schedule, stop_name):
    bus_loc_times = get_data_by_line(file, line)
    stop_loc = get_location(stop_cords)
    stop_schedule.sort()
    stop_schedule_time = []
    for elem in stop_schedule:
        stop_schedule_time.append(elem.time())
    
    total_delay = timedelta(seconds=0)
    total_num = 0

    for elem in bus_loc_times:
        if elem[0] != stop_loc:
            continue

        real_time = elem[1].time()
        expected_time = stop_schedule_time[bisect.bisect_left(stop_schedule_time, real_time) - 1]

        total_delay += datetime.combine(date.today(), real_time) - datetime.combine(date.today(), expected_time) 
        total_num += 1
    
    avg_delay = total_delay.total_seconds()
    if total_num > 0:
        avg_delay /= total_num
    
    print("Autobusy linii " + str(line) + " spóźniały się średnio " + str(avg_delay) + " sekund na przystanku " + str(stop_name))



        

