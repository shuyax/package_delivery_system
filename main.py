# Student ID: 010722731

import csv
import queue
import requests
import json

#A. . HASH TABLE
class HashTable:
    def __init__(self,total_num_packages):
        self.total_num_packages = total_num_packages
        try:
            with open('data','r') as file:
                self.data = json.load(file)
                print('fetched the data list from the data file')
        except:
            self.data = [None] * (self.total_num_packages + 1)
            print('created data list')
        

    def get_coordinates(self, address,zipcode):
        url = 'https://nominatim.openstreetmap.org/search'
        address_list = address.split(' ')
        if address_list[1].upper() in ['N', 'S', 'W', 'E']:
           address_list.pop(1)
        house_number = address_list[0]
        road = ' '.join(address_list[1:])
        params = {
            'street': house_number + ', ' + road,
            'postalcode': zipcode,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1
        }
        headers = {
            'User-Agent': 'Package Delivery System/1.0 (your@email.com)'  # Replace with your app name and email
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            if response.text.strip():  # Check if response is not empty
                data = response.json()
                if data:
                    return [float(data[0]['lat']), float(data[0]['lon'])]
            print(address, "No data found for the given address.")
        except requests.exceptions.RequestException as e:
            print(address, f"Request failed: {e}")
        except ValueError:
            print(address, "Failed to decode JSON.")
        return None

        
    # Inserts the specified key/value pair. If the key already exists, the 
    # corresponding value is updated. If inserted or updated, True is returned. 
    # If not inserted, then False is returned.
    def insert(self, key, delivery_address, delivery_deadline,delivery_city,delivery_zipcode, package_weight,delivery_status,delivery_time, delivery_state, special_notes=''):
        if self.data[key] == None:
            self.data[key] = [delivery_address, delivery_deadline,delivery_city,delivery_zipcode, package_weight,[delivery_status,delivery_time],self.get_coordinates(delivery_address,delivery_zipcode),delivery_state,special_notes]
            return True
        else:
            address = self.data[key][0]
            zipcode = self.data[key][3]
            coordinates = self.data[key][6] 
            if address == delivery_address and zipcode == delivery_zipcode:
                self.data[key] = [delivery_address, delivery_deadline,delivery_city,delivery_zipcode, package_weight,[delivery_status,delivery_time],coordinates,delivery_state,special_notes]
            else:
                self.data[key] = [delivery_address, delivery_deadline,delivery_city,delivery_zipcode, package_weight,[delivery_status,delivery_time],self.get_coordinates(delivery_address,delivery_zipcode),delivery_state,special_notes]
      
            
    # Searches for the specified key. If found, the key/value pair is removed 
    # from the hash table and True is returned. If not found, False is returned.
    def remove(self, key):
        if self.data[key] != None:
            self.data[key] = None
            #print(key, 'has been removed successfully')
        else:
            return False

    # B. . LOOK-UP FUNCTION
    # Searches for the key, returning the corresponding value if found, None if 
    # not found.
    def search(self, key):
        if self.data[key] != None:
            return self.data[key]
        else:
            #print('This package is not in the database')
            return None
    def __str__(self):
        # for item in self.data:
        #     print(item)
        # return ''
        return str(self.data)
    def get_data(self):
        return self.data
    def get_key(self):
        key = []
        for item in self.data:
            if item != None:
                key.append(self.data.index(item))
        return key


        
package_hash_table = HashTable(40)

delivery_status = ['at the hub', 'en route', 'delivered']
delivery_deadline_dict = {}
distance = []

# Load WGUPS package file from package_file
csvfile = open('package_file.csv')
csvreader = csv.reader(csvfile, delimiter=',')
headers = csvreader.__next__() 
for row in csvreader:
    package_id = int(row[0])
    address = row[1]
    package_hash_table.insert(package_id,address,row[5],row[2],row[4],row[6],delivery_status[0],'',row[3],row[7])
    # Track package ids with different delivery deadline
    if row[5] not in delivery_deadline_dict:
        delivery_deadline_dict[row[5]] = [package_id]
    else:
        delivery_deadline_dict[row[5]].append(package_id)
    if address not in distance:
        distance.append(address)

# print(package_hash_table)

with open('data', 'w') as file:
    json.dump(package_hash_table.get_data(), file)


# Customize the sorted funtion for sorting by time
def time_sort(time):
    if 'PM' in time:
        time = time.split(" ")[0]
        hours, minutes = map(int, time.split(":"))
        if hours != 12:
            hours = hours + 12
        else:
            hours = hours + 0
        return (hours, minutes)
    elif 'AM' in time:
        time = time.split(" ")[0]
        hours, minutes = map(int, time.split(":"))
        return (hours, minutes)
    elif 'EOD' in time:
        return (24,0)

# A function to convert time from tuple to string
def time_format(time):
    string = ''
    if time[0] < 12:
        string = str(time[0]) + ':' + str(time[1]) + ' AM'
        return string
    elif time[0] > 12:
        string = str(time[0] - 12) + ':' + str(time[1]) + ' PM'
        return string
    else:
        string = str(time[0]) + ':' + str(time[1]) + ' PM'
        return string



# Load WGUPS distance file from distance file
distance.append('HUB')
csvfile = open('distance.csv')
csvreader = csv.reader(csvfile, delimiter=',')
headers = csvreader.__next__() 
sheet = [headers]
for row in csvreader:
    sheet.append(row)
for key in distance:
    key_address = key.split(" ")[0]
    i = 1
    for row in sheet[1:]:
        distance_address = row[0].strip().split(" ")[0]
        if key_address == distance_address:
            row[0] = key
            headers[i] = key
        i += 1



# A function for getting the distance between two addresses
def get_distance(current_location,next_location):
    for location in sheet[0]:
        if current_location == location:
            row_index = sheet[0].index(location)            
    i = 1
    for row in sheet[1:]:
        if row[0] == next_location:
            col_index = i
        i += 1
    if sheet[row_index][col_index] != '':
        distance = float(sheet[row_index][col_index])
    else:
        distance = float(sheet[col_index][row_index])
    return distance

# A function to return the location which is closest to the current location
def get_min_distance(current_location, location_list):
    min_distance = 140
    for location in location_list:
        if min_distance > get_distance(current_location,location):
            #and get_distance(current_location,location) != 0.0
            min_distance = get_distance(current_location,location)
            next_location = location
    return (next_location, min_distance)

truck_speed = 18

# A function to return the time of arriving current location from previous location
def current_time(previous_time, min_distance, speed=truck_speed):
    previous_hours = time_sort(previous_time)[0]
    previous_minutes = time_sort(previous_time)[1]
    duriation_hour = min_distance // speed
    duriation_minute = min_distance / speed * 60
    current_hours = previous_hours + duriation_hour
    current_minutes = previous_minutes + duriation_minute
    if current_minutes > 60:
        current_hours += current_minutes // 60
        current_minutes = current_minutes % 60
    return(int(current_hours), int(current_minutes))



total_packages_allowed = 16
truck1_num_package = 0
truck2_num_package = 0
truck1_queue = queue.Queue()
truck2_queue = queue.Queue()
milage = 0
truck1_current_location = 'HUB'
truck2_current_location = 'HUB'
truck1_previous_time = '8:00 AM'
truck2_previous_time = '9:05 AM'
truck1_loading_time = [time_sort(truck1_previous_time)]
truck2_loading_time = [time_sort(truck2_previous_time)]


# Sort package id by delivery dealine 
# Keep track the delivery time of packages on each truck seperately
for key in sorted(delivery_deadline_dict, key=time_sort):
    #print(delivery_deadline_dict[key])
    # Load packages for truck1
    min_distance = 140
    # A list to track the delivery addresses of packages which can be delivered by either truck
    location_list = []
    # A list to track the delivery addresses of packages which can only be delivered by truck2
    location_list_truck2 = []
    # A list to track the delivery addresses of packages which can only be delivered by truck1
    location_list_truck1 = []
    delivery_together = [20,13,15,19,14,16]
    for id in delivery_deadline_dict[key]:
        # Packages with special notes that those packages have to be on truck2
        if id == 3 or id == 18 or id ==36 or id == 38:
            location_list_truck2.append(package_hash_table.search(id)[0])
        elif id == 6 or id == 25 or id == 28 or id == 32:
            location_list_truck2.append(package_hash_table.search(id)[0])
        # A list for tracking all packages that have to be loaded on the same truck at the same time
        elif id == 20 or id == 13 or id == 15 or id == 19 or id == 14 or id == 16:
            location_list_truck1.append(package_hash_table.search(id)[0])
        else:
            location_list.append(package_hash_table.search(id)[0])

    while len(location_list) > 0 or len(location_list_truck1) > 0 or len(location_list_truck2) > 0:
        # Check if truck1 has more space for loading packages
        if truck1_num_package < total_packages_allowed and len(location_list + location_list_truck1) > 0:
            # Check if truck 1 still has enough space for all packages that need to be loaded together
            if total_packages_allowed - truck1_num_package > len(location_list_truck1):
                truck1_next_location = get_min_distance(truck1_current_location, location_list + location_list_truck1)[0]
                min_distance = get_min_distance(truck1_current_location, location_list + location_list_truck1)[1]
                for id in delivery_deadline_dict[key]:
                    if package_hash_table.search(id)[0] == truck1_next_location:
                        next_id = id
            else:
                for address in location_list_truck1:
                    truck1_next_location = get_min_distance(truck1_current_location, location_list_truck1)[0]
                    min_distance = get_min_distance(truck1_current_location, location_list_truck1)[1]
                    for id in delivery_deadline_dict[key]:
                        if package_hash_table.search(id)[0] == address:
                            next_id = id
            # Skip package#9 if the current time is before 10:20 AM becuase package#9's correct address will not be available until 10:20 AM
            if next_id == 9 and time_sort(truck1_previous_time) < (10,20):
                pass
            # If time is after 10:20 AM and the package is package#9, reset package#9's address to the correct address
            elif next_id == 9 and time_sort(truck1_previous_time) > (10,20) and package_hash_table.search(9)[0] == '300 State St':
                location_list[location_list.index(package_hash_table.search(9)[0])] = '450 S State St'
                package_hash_table.search(9)[0] = '450 S State St'
                package_hash_table.search(9)[3] = '84111'
            else:
                # Check if put the package will cause missing deadline
                if time_sort(key) >= current_time(truck1_previous_time, min_distance):
                    if current_time(truck1_previous_time, min_distance)[0] < 12:
                        truck1_previous_time = str(current_time(truck1_previous_time, min_distance)[0]) + ':' + str(current_time(truck1_previous_time, min_distance)[1]) + ' AM'
                    else:
                        truck1_previous_time = str(current_time(truck1_previous_time, min_distance)[0] - 12) + ':' + str(current_time(truck1_previous_time, min_distance)[1]) + ' PM'
                    #print('truck1: ',truck1_previous_time, truck1_next_location, next_id)
                    truck1_queue.put(next_id)
                    truck1_num_package += 1
                    milage += min_distance
                    # Remove the next location from the location list or truck 1 location list which are the locations that to be decided for delivery
                    try:
                        location_list.remove(truck1_next_location)
                    except:
                        location_list_truck1.remove(truck1_next_location)
                    # Remove the packge information from the delivery_deadline_dict since the package is added to the  delivery list
                    delivery_deadline_dict[key].remove(next_id)
                    # Set current location to the next location for next iterating
                    truck1_current_location = truck1_next_location
                    package_hash_table.search(next_id)[5][0] = delivery_status[1] + ' on truck 1'
                    package_hash_table.search(next_id)[5][1] = truck1_previous_time
                else:
                    if not (next_id in delivery_together) and not(truck1_next_location in location_list_truck1):
                        truck2_next_location = truck1_next_location
                        min_distance = get_distance(truck2_current_location, truck2_next_location)
                        # Check if the total number of packages in truck1 is over 16  the packaged will not be delivered over the delivery deadline
                        if truck2_num_package < total_packages_allowed and time_sort(key) >= current_time(truck2_previous_time, min_distance):
                            if current_time(truck2_previous_time, min_distance)[0] < 12:
                                truck2_previous_time = str(current_time(truck2_previous_time, min_distance)[0]) + ':' + str(current_time(truck2_previous_time, min_distance)[1]) + ' AM'
                            else:
                                truck2_previous_time = str(current_time(truck2_previous_time, min_distance)[0] - 12) + ':' + str(current_time(truck2_previous_time, min_distance)[1]) + ' PM'
                            print('truck2: ',truck2_previous_time, truck2_next_location, next_id)
                            truck2_queue.put(next_id)
                            truck2_num_package += 1
                            milage += min_distance
                            # Remove the next location from the location list or truck 1 location list which are the locations that to be decided for delivery
                            try:
                                location_list.remove(truck2_next_location)
                            except:
                                location_list_truck2.remove(truck2_next_location)
                            delivery_deadline_dict[key].remove(next_id)
                            truck2_current_location = truck2_next_location
                            package_hash_table.search(next_id)[5][0] = delivery_status[1] + ' on truck 2'
                            package_hash_table.search(next_id)[5][1] = truck2_previous_time
        # Check if truck2 has more space for loading packages
        elif truck2_num_package < total_packages_allowed:
            truck2_next_location = get_min_distance(truck2_current_location, location_list + location_list_truck2)[0]
            min_distance = get_min_distance(truck2_current_location, location_list + location_list_truck2)[1]
            for id in delivery_deadline_dict[key]:
                if package_hash_table.search(id)[0] == truck2_next_location:
                    next_id = id
            # Skip package#9 if the current time is before 10:20 AM becuase package#9's correct address will not be available until 10:20 AM
            if next_id == 9 and time_sort(truck2_previous_time) < (10,20):
                pass
            elif next_id == 9 and time_sort(truck2_previous_time) > (10,20) and package_hash_table.search(9)[0] == '300 State St':
                location_list[location_list.index(package_hash_table.search(9)[0])] = '450 S State St'
                package_hash_table.search(9)[0] = '450 S State St'
                package_hash_table.search(9)[3] = '84111'
            else:
                if truck2_num_package < total_packages_allowed and time_sort(key) >= current_time(truck2_previous_time, min_distance):
                    # Reset the time format
                    if current_time(truck2_previous_time, min_distance)[0] < 12:
                        truck2_previous_time = str(current_time(truck2_previous_time, min_distance)[0]) + ':' + str(current_time(truck2_previous_time, min_distance)[1]) + ' AM'
                    else:
                        truck2_previous_time = str(current_time(truck2_previous_time, min_distance)[0] - 12) + ':' + str(current_time(truck2_previous_time, min_distance)[1]) + ' PM'
                    #print('truck2: ',truck2_previous_time, truck2_next_location, next_id)
                    truck2_queue.put(next_id)
                    truck2_num_package += 1
                    milage += min_distance
                    # Remove the next location from the location list or truck 1 location list which are the locations that to be decided for delivery
                    try:
                        location_list.remove(truck2_next_location)
                    except:
                        location_list_truck2.remove(truck2_next_location)
                    delivery_deadline_dict[key].remove(next_id)
                    truck2_current_location = truck2_next_location
                    package_hash_table.search(next_id)[5][0] = delivery_status[1] + ' on truck 2'
                    package_hash_table.search(next_id)[5][1] = truck2_previous_time

        # Both trucks are fully loaded. After delivering all packages, the trucks should return to Hub to reload
        if truck1_num_package == 16 and truck2_num_package == 16:
            milage += get_distance(truck1_current_location, 'HUB') + get_distance(truck2_current_location, 'HUB')
            truck1_previous_time = current_time(truck1_previous_time, get_distance(truck1_current_location, 'HUB'))
            truck1_previous_time_tuple = truck1_previous_time
            truck2_previous_time = current_time(truck2_previous_time, get_distance(truck2_current_location, 'HUB'))
            truck2_previous_time_tuple = truck2_previous_time

            # Reset both trucks' previous times to the correct format
            if truck1_previous_time[0] < 12:
                truck1_previous_time = str(truck1_previous_time[0]) + ':' + str(truck1_previous_time[1]) + ' AM'
            elif truck1_previous_time[0] > 12:
                truck1_previous_time = str(truck1_previous_time[0] - 12) + ':' + str(truck1_previous_time[1]) + ' PM'
            else:
                truck1_previous_time = '12' + ':' + str(truck1_previous_time[1]) + ' AM'
            if truck2_previous_time[0] < 12:
                truck2_previous_time = str(truck2_previous_time[0]) + ':' + str(truck2_previous_time[1]) + ' AM'
            elif truck2_previous_time[0] > 12:
                truck2_previous_time = str(truck2_previous_time[0] - 12) + ':' + str(truck2_previous_time[1]) + ' PM'
            else:
                truck2_previous_time = '12' + ':' + str(truck2_previous_time[1]) + ' PM'
            # Append the loading time to the list for each truck
            truck1_loading_time.append(time_sort(truck1_previous_time))
            truck2_loading_time.append(time_sort(truck2_previous_time))
            
            # Reset the location to Hub
            truck1_current_location = 'HUB'
            truck2_current_location = 'HUB'

            # Reset the total number of packages on each truck to 0
            truck1_num_package = 0
            truck2_num_package = 0

            # Check if there are remaining packages in Hub to be delivered
            for key in sorted(delivery_deadline_dict, key=time_sort):
                location_list = []
                location_list_truck2 = []
                for id in delivery_deadline_dict[key]:
                    if id == 3 or id == 18 or id ==36 or id == 38:
                        location_list_truck2.append(package_hash_table.search(id)[0])
                    elif id == 6 or id == 25 or id == 28 or id == 32:
                        location_list_truck2.append(package_hash_table.search(id)[0])
                    else:
                        location_list.append(package_hash_table.search(id)[0])
                
                while len(location_list) > 0  or len(location_list_truck2) > 0:
                    # Check which truck returns to Hub earlier and if there are packages that have to be delivered by truck 2
                    if truck1_previous_time_tuple < truck2_previous_time_tuple and len(location_list_truck2) == 0:
                        if truck1_num_package < total_packages_allowed:
                            truck1_next_location = get_min_distance(truck1_current_location, location_list)[0]
                            min_distance = get_min_distance(truck1_current_location, location_list)[1]
                            for id in delivery_deadline_dict[key]:
                                if package_hash_table.search(id)[0] == truck1_next_location:
                                    next_id = id
                            # Skip package#9 if the current time is before 10:20 AM becuase package#9's correct address will not be available until 10:20 AM
                            if next_id == 9 and time_sort(truck2_previous_time) < (10,20):
                                pass
                            elif next_id == 9 and time_sort(truck2_previous_time) > (10,20) and package_hash_table.search(9)[0] == '300 State St':
                                location_list[location_list.index(package_hash_table.search(9)[0])] = '450 S State St'
                                package_hash_table.search(9)[0] = '450 S State St'
                                package_hash_table.search(9)[3] = '84111'
                            else:        
                                if time_sort(key) >= current_time(truck1_previous_time, min_distance):
                                    # Reset the time format
                                    if current_time(truck1_previous_time, min_distance)[0] < 12:
                                        truck1_previous_time = str(current_time(truck1_previous_time, min_distance)[0]) + ':' + str(current_time(truck1_previous_time, min_distance)[1]) + ' AM'
                                    elif current_time(truck1_previous_time, min_distance)[0] > 12:
                                        truck1_previous_time = str(current_time(truck1_previous_time, min_distance)[0] - 12) + ':' + str(current_time(truck1_previous_time, min_distance)[1]) + ' PM'
                                    else:
                                        truck1_previous_time = '12' + ':' + str(current_time(truck1_previous_time, min_distance)[1]) + ' PM'
                                    #print('truck1: ',truck1_previous_time, truck1_next_location, next_id)
                                    truck1_queue.put(next_id)
                                    truck1_num_package += 1
                                    milage += min_distance
                                    # Remove the next location from the location list or truck 1 location list which are the locations that to be decided for delivery
                                    location_list.remove(truck1_next_location)
                                    delivery_deadline_dict[key].remove(next_id)
                                    truck1_current_location = truck1_next_location
                                    package_hash_table.search(next_id)[5][0] = delivery_status[1] + ' on truck 1'
                                    package_hash_table.search(next_id)[5][1] = truck1_previous_time
                    else:  
                        truck2_next_location = get_min_distance(truck2_current_location, location_list + location_list_truck2)[0]
                        min_distance = get_min_distance(truck2_current_location, location_list + location_list_truck2)[1]
                        for id in delivery_deadline_dict[key]:
                            if package_hash_table.search(id)[0] == truck2_next_location:
                                next_id = id
                        # Skip package#9 if the current time is before 10:20 AM becuase package#9's correct address will not be available until 10:20 AM
                        if next_id == 9 and time_sort(truck2_previous_time) < (10,20):
                            pass
                        elif next_id == 9 and time_sort(truck2_previous_time) > (10,20) and package_hash_table.search(9)[0] == '300 State St':
                            location_list[location_list.index(package_hash_table.search(9)[0])] = '450 S State St'
                            package_hash_table.search(9)[0] = '450 S State St'
                            package_hash_table.search(9)[3] = '84111'
                        else:        
                            if truck2_num_package < total_packages_allowed and time_sort(key) >= current_time(truck2_previous_time, min_distance):
                                # Reset the time format
                                if current_time(truck2_previous_time, min_distance)[0] < 12:
                                    truck2_previous_time = str(current_time(truck2_previous_time, min_distance)[0]) + ':' + str(current_time(truck2_previous_time, min_distance)[1]) + ' AM'
                                elif current_time(truck2_previous_time, min_distance)[0] > 12:
                                    truck2_previous_time = str(current_time(truck2_previous_time, min_distance)[0] - 12) + ':' + str(current_time(truck2_previous_time, min_distance)[1]) + ' PM'
                                else:
                                    truck2_previous_time = '12' + ':' + str(current_time(truck2_previous_time, min_distance)[1]) + ' PM'
                                #print('truck2: ',truck2_previous_time, truck2_next_location, next_id)
                                truck2_queue.put(next_id)
                                truck2_num_package += 1
                                milage += min_distance
                                # Remove the next location from the location list or truck 1 location list which are the locations that to be decided for delivery
                                try:
                                    location_list.remove(truck2_next_location)
                                except:
                                    location_list_truck2.remove(truck2_next_location)
                                delivery_deadline_dict[key].remove(next_id)
                                truck2_current_location = truck2_next_location
                                package_hash_table.search(next_id)[5][0] = delivery_status[1] + ' on truck 2'
                                package_hash_table.search(next_id)[5][1] = truck2_previous_time



# A function for checking status for all packages at a specific time
def delivery_status_display():
    # D. . INTERFACE
    time = input('Enter the time you want to search for:')
    time = time_sort(time)
    truck1_display_list = []
    truck2_display_list = []
    keys = package_hash_table.get_key()

    if time < (10,20):
        package_hash_table.search(9)[0] = '300 State St'
        package_hash_table.search(9)[3] = '84103'
    else:
        package_hash_table.search(9)[0] = '450 S State St'
        package_hash_table.search(9)[3] = '84111'

    for key in keys:
        estimated_delivery_time = time_sort(package_hash_table.search(key)[5][1])
        truck = package_hash_table.search(key)[5][0][-1]
        display = ''
        # Check whether the package is in truck 1 or 2
        # Check if the search time is in the first round delivery or second round
        # Check if the packages which are in the same round of delivery is delivered or not yet based on the time
        if truck == '1' and time < truck1_loading_time[1] and time > truck1_loading_time[0]:
            if time_sort(package_hash_table.search(key)[5][1]) < truck1_loading_time[1]:
                if time >= estimated_delivery_time:
                    package_hash_table.search(key)[5][0] = delivery_status[2]
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
                else:
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Estimated Delivery Time: ' + package_hash_table.search(key)[5][1] 
            else:
                package_hash_table.search(key)[5][0] = delivery_status[0]
                if time >= estimated_delivery_time:
                    package_hash_table.search(key)[5][0] = delivery_status[2]
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
                else:
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Estimated Delivery Time: ' + package_hash_table.search(key)[5][1]
            truck1_display_list.append(display)
        # Check whether the package is in truck 1 or 2
        # Check if the search time is in the first round delivery or second round
        # Check if the packages which are in the same round of delivery is delivered or not yet based on the time
        elif truck == '1' and time > truck1_loading_time[1]:
            if time_sort(package_hash_table.search(key)[5][1]) < truck1_loading_time[1]:
                package_hash_table.search(key)[5][0] = delivery_status[2]
                display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
            else:
                if time >= estimated_delivery_time:
                    package_hash_table.search(key)[5][0] = delivery_status[2]
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
                else:
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
            truck1_display_list.append(display)    
        # Check whether the package is in truck 1 or 2
        # Check if the search time is in the first round delivery or second round
        # Check if the packages which are in the same round of delivery is delivered or not yet based on the time
        elif truck == '1' and time < truck1_loading_time[0]:
            package_hash_table.search(key)[5][0] = delivery_status[0]
            display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Estimated Delivery Time: ' + package_hash_table.search(key)[5][1]
            truck1_display_list.append(display) 
        # Check whether the package is in truck 1 or 2
        # Check if the search time is in the first round delivery or second round
        # Check if the packages which are in the same round of delivery is delivered or not yet based on the time
        elif truck == '2' and time < truck2_loading_time[1] and time > truck2_loading_time[0]:
            if time_sort(package_hash_table.search(key)[5][1]) < truck2_loading_time[1]:
                if time >= estimated_delivery_time:
                    package_hash_table.search(key)[5][0] = delivery_status[2]
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
                else:
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Estimated Delivery Time: ' + package_hash_table.search(key)[5][1]
            else:
                package_hash_table.search(key)[5][0] = delivery_status[0]
                display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Estimated Delivery Time: ' + package_hash_table.search(key)[5][1]    
            truck2_display_list.append(display)
        # Check whether the package is in truck 1 or 2
        # Check if the search time is in the first round delivery or second round
        # Check if the packages which are in the same round of delivery is delivered or not yet based on the time
        elif truck == '2' and time < truck2_loading_time[0]:
            package_hash_table.search(key)[5][0] = delivery_status[0]
            display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Estimated Delivery Time: ' + package_hash_table.search(key)[5][1]    
            truck2_display_list.append(display)
        # Check whether the package is in truck 1 or 2
        # Check if the search time is in the first round delivery or second round
        # Check if the packages which are in the same round of delivery is delivered or not yet based on the time
        elif truck == '2' and time > truck2_loading_time[1]:
            if time_sort(package_hash_table.search(key)[5][1]) < truck2_loading_time[1]:
                package_hash_table.search(key)[5][0] = delivery_status[2]
                display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
            else: 
                if time >= estimated_delivery_time:
                    package_hash_table.search(key)[5][0] = delivery_status[2]
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Delivery Time: ' + package_hash_table.search(key)[5][1]    
                else:
                    display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] + '; Delivery Status: ' + package_hash_table.search(key)[5][0] + '; Estimated Delivery Time: ' + package_hash_table.search(key)[5][1]
            truck2_display_list.append(display)
    print('Truck 1: ')
    for item in truck1_display_list:
        print(item)
    print('Truck 2: ')
    for item in truck2_display_list:    
        print(item)

# A function for checking status for a specific package
def delivery_status_by_package():
    #D. . INTERFACE
    package_id = input('Enter the package id you want to search for:')
    package_id = int(package_id)
    package_hash_table.search(package_id)
    delivery_time = time_sort(package_hash_table.search(package_id)[5][1])
    truck = package_hash_table.search(package_id)[5][0][-1]
    print('Package ID: ' + str(package_id))
    print('Delivery Address: ' + package_hash_table.search(package_id)[0]) 
    print('Delivery Deadline: ' + package_hash_table.search(package_id)[1])
    print('Delivery City: ' + package_hash_table.search(package_id)[2])
    print('Delivery Zipcode: ' + package_hash_table.search(package_id)[3])
    print('Package Weight: ' + package_hash_table.search(package_id)[4])
    print('Delivery Status: ')    
    # Check whether the package is in truck 1 or 2
    # Check if the search time is in the first round delivery or second round
    if truck == '1' and delivery_time < truck1_loading_time[1] and delivery_time > truck1_loading_time[0]:
        print(f'    Before {time_format(truck1_loading_time[0])}: {delivery_status[0]}')
        print(f'    Between {time_format(truck1_loading_time[0])} and {time_format(truck1_loading_time[1])}: {delivery_status[1]} on Truck 1')
        print(f'    After {time_format(truck1_loading_time[1])}: {delivery_status[2]}')
    elif truck == '1' and delivery_time > truck1_loading_time[1]:
        print(f'    Before {time_format(truck1_loading_time[1])}: {delivery_status[0]}')
        print(f'    Between {time_format(truck1_loading_time[1])} and {time_format(delivery_time)}: {delivery_status[1]} on Truck 1')
        print(f'    After {time_format(delivery_time)}: {delivery_status[2]}')
    elif truck == '2' and delivery_time < truck2_loading_time[1] and delivery_time > truck2_loading_time[0]:
        print(f'    Before {time_format(truck2_loading_time[0])}: {delivery_status[0]}')
        print(f'    Between {time_format(truck2_loading_time[0])} and {time_format(truck2_loading_time[1])}: {delivery_status[1]} on Truck 2')
        print(f'    After {time_format(truck2_loading_time[1])}: {delivery_status[2]}')
    elif truck == '2' and delivery_time > truck2_loading_time[1]:
        print(f'    Before {time_format(truck2_loading_time[1])}: {delivery_status[0]}')
        print(f'    Between {time_format(truck2_loading_time[1])} and {time_format(delivery_time)}: {delivery_status[1]} on Truck 2')
        print(f'    After {time_format(delivery_time)}: {delivery_status[2]}')

# A function for checking the delivery status for all packages
def all_delivery_status():
    keys = package_hash_table.get_key()
    for key in keys:
        delivery_time = time_sort(package_hash_table.search(key)[5][1])
        truck = package_hash_table.search(key)[5][0][-1]
        display = 'Package ID: ' + str(key) + '; Delivery Address: ' + package_hash_table.search(key)[0]+ '; Delivery Deadline: ' + package_hash_table.search(key)[1] + '; Delivery City: ' + package_hash_table.search(key)[2] + '; Delivery Zipcode: ' + package_hash_table.search(key)[3] + '; Package Weight: ' + package_hash_table.search(key)[4] 
        print(display, end = ' ')
        print('Delivery Status: ', end = '')
        # Check whether the package is in truck 1 or 2
        # Check if the search time is in the first round delivery or second round
        if truck == '1' and delivery_time < truck1_loading_time[1] and delivery_time > truck1_loading_time[0]:
            print(f'Before {time_format(truck1_loading_time[0])}: {delivery_status[0]};', end = ' ')
            print(f'Between {time_format(truck1_loading_time[0])} and {time_format(truck1_loading_time[1])}: {delivery_status[1]} on Truck 1;', end = ' ')
            print(f'After {time_format(truck1_loading_time[1])}: {delivery_status[2]}')    
        elif truck == '1' and delivery_time > truck1_loading_time[1]:
            print(f'Before {time_format(truck1_loading_time[1])}: {delivery_status[0]}', end = ' ')
            print(f'Between {time_format(truck1_loading_time[1])} and {time_format(delivery_time)}: {delivery_status[1]} on Truck 1', end = ' ')
            print(f'After {time_format(delivery_time)}: {delivery_status[2]}')
        elif truck == '2' and delivery_time < truck2_loading_time[1] and delivery_time > truck2_loading_time[0]:
            print(f'Before {time_format(truck2_loading_time[0])}: {delivery_status[0]}', end = ' ')
            print(f'Between {time_format(truck2_loading_time[0])} and {time_format(truck2_loading_time[1])}: {delivery_status[1]} on Truck 2', end = ' ')
            print(f'After {time_format(truck2_loading_time[1])}: {delivery_status[2]}')
        elif truck == '2' and delivery_time > truck2_loading_time[1]:
            print(f'Before {time_format(truck2_loading_time[1])}: {delivery_status[0]}', end = ' ')
            print(f'Between {time_format(truck2_loading_time[1])} and {time_format(delivery_time)}: {delivery_status[1]} on Truck 2', end = ' ')
            print(f'After {time_format(delivery_time)}: {delivery_status[2]}')
        #print()


# A. print the hash table
#print('Hash Table:')
#print(package_hash_table)
# B. Print the result of searching a package by id from the hash table
#print('The look up function of the Hash Table:')
#print(package_hash_table.search(20))

# user_input = input('Please select: 1. Search by package Id; 2. Search by a specific time; 3. Check all package status; Enter Your choice here: ')

# if user_input == '1':
#     # Print the result of searching by package id
#     delivery_status_by_package()
# elif user_input == '2':
#     # Print the result of searching all packages at a specific time
#     delivery_status_display()
# elif user_input == '3':
#     # Print the result of the status of all packages
#     all_delivery_status()
# else:
#     print('Your selection is invalid')
# Print the total milage
print('Total Milage: ',round(milage,2))

