import csv
import uuid
import os
import matplotlib.pyplot as plt

class line:
    stn_line_1 = [
    ['station_id','station_name','line_no.','order'],
    [11, 'Mansarovar','1','1'],
    [21, 'New Aatish Market','1','2'],
    [31, 'Vivek Vihaar','1','3'],
    [41, 'Shyam Nagar','1','4'],
    [51, 'Ram Nagar','1','5'],
    [61, 'Civil Lines','1','6'],
    [71, 'Railway Station','1','7'],
    [81, 'Sindhi Camp','1,2','8'],
    [91, 'Chand Pole','1','9'],
    [110, 'Choti Chaupar','1','10'],
    [111, 'Badi Chaupar','1','11']
] 
    
    

    stn_line_2 = [
    ['station_id','station_name','line_no.','order'],
    [12, 'Sanganer','2','1'],
    [22, 'Durgapura','2','2'],
    [32, 'Gopal Pura','2','3'],
    [42, 'Tonk Phatak','2','4'],
    [52, 'SMS Stadium','2','5'],
    [62, 'SMS Hospital','2,3','6'],
    [72, 'Ajmeri Gate','2','7'],
    [82, 'Sindhi Camp','1,2','8'],
    [92, 'Subhash Nagar','2','9'],
    [102, 'Pani Pech','2','10'],
    [112, 'Ambabadi','2','11']
]

    stn_line_3= [
    ['station_id','station_name','line_no.','order'],
    [13, 'Jawahar Nagar','3','1'],
    [23, 'SMS Hospital','2,3','2'],
    [33, 'Ram Nagar','3','3'],
    [43, 'Hasanpura','3','4'],
    [53, 'Khatpura','3','5'],
    [63, 'Vaishali Nagar','3','6'],
    [73, 'Chitrakoot','3','7'],
    [83, 'Tagore Nagar','3','8']
]
    
    @classmethod
    def initialise_lines(cls):
        with open ("line_1.csv",'w',newline = '') as line_1:
            line1  = csv.writer(line_1)
            line1.writerows(cls.stn_line_1)

        with open ("line_2.csv",'w',newline = '') as line_2:
            line2  = csv.writer(line_2)
            line2.writerows(cls.stn_line_2)

        with open ("line_3.csv",'w',newline = '') as line_3:
            line3 = csv.writer(line_3)
            line3.writerows(cls.stn_line_3)
        
        with open ("stations.csv",'w',newline = '') as stn_list:
            station_list  = csv.writer(stn_list)
            station_list.writerows(line.stn_line_1)
            station_list.writerows(line.stn_line_2[1:])
            station_list.writerows(line.stn_line_3[1:])


class station:
    def __init__(self,station_id,station_name):
         self.station_id = station_id
         self.station_name = station_name
    
    @staticmethod
    def list_stations():
          with open("stations.csv",'r') as table:
            station_list = csv.reader(table)
            for line in station_list:
                print(f"{line[0]}",f"{line[1]}",f"({line[2]})")

class graph:
    def __init__(self,edges):
        self.edges = edges
        self.graph_dict = {}
        for start,end in edges: #defining dictionary
            if start in self.graph_dict:
                self.graph_dict[start].append(end)
            else: 
                self.graph_dict[start] = [end]
            
            if end in self.graph_dict:
                self.graph_dict[end].append(start)
            else:
                self.graph_dict[end] = [start]

    paths = []

    def show_paths(self,start,end,path=[]):
        path = path + [start]
        if start == end:
            return [path]
        
        if start not in self.graph_dict:
            return []
        
        paths = []

        for node in self.graph_dict[start]:
            if node not in path:
                new_paths = self.show_paths(node,end,path)
                for p in new_paths:
                    paths.append(p)
        return paths


    def shortest_path(self,start,end,path=[]):
        path = path + [start]
        if start == end:
            return path
        
        if start not in self.graph_dict:
            return []
        
        shortest = None
        for node in self.graph_dict[start]:
            if node not in path:
                sp = self.shortest_path(node, end, path)
                if sp:
                    if shortest is None or len(sp) < len(shortest):
                        shortest = sp

        return shortest
    # implementing dfs here for the sake of simplicity since it would work 
    # just fine for small data like this but may need to switch to
    # bfs for better efficiency for the larger data since in this case we 
    # just need the the shortest path and not all the possible paths

    #from collections import deque

# def shortest_path(self, start, end):
#     if start not in self.graph_dict or end not in self.graph_dict:
#         return []

#     visited = set()
#     queue = deque([[start]])  # queue of paths
#     while queue:
#         path = queue.popleft()
#         station = path[-1]

#         if station == end:
#             return path

#         if station not in visited:
#             visited.add(station)
#             for neighbor in self.graph_dict.get(station, []):
#                 new_path = list(path)
#                 new_path.append(neighbor)
#                 queue.append(new_path)
#     return []

    def calculate_fare(self, start, end):
        path = self.shortest_path(start, end)
        if not path:
            return None
        fare = (len(path) - 1) * 10
        return fare
    
    def line_no(self,station):
        with open("stations.csv",'r') as table:
            station_list = csv.reader(table)
            for line in station_list:
                if station == line[1]:
                    line_no = line[2].split(',')
                    return line_no
        return []

    def get_instructions(self, start, end):
        path = self.shortest_path(start, end)
        if not path or len(path) < 2:
            return ["Invalid path or same station."]

        instructions = []
        current_line = None

        for i in range(len(path) - 1):
            station = path[i]
            next_station = path[i + 1]
            line_current = self.line_no(station)
            line_next = self.line_no(next_station)
            common_lines = set(line_current).intersection(set(line_next))

            if current_line is None:
                current_line = list(common_lines)[0] if common_lines else line_current[0]
                instructions.append(f"Board Line {current_line} at {station}.")

            if not common_lines:
                next_line = line_next[0]
                instructions.append(f"Change to Line {next_line} at {station}.")
                current_line = next_line

        instructions.append(f"Arrive at {end} (Line {current_line}).")

        return instructions



routes = [
            ("Sanganer","Durgapura"),
            ("Durgapura","Gopal Pura"),
            ("Gopal Pura","SMS Stadium"),
            ("SMS Stadium","SMS Hospital"),
            ("SMS Hospital","Ajmeri Gate"),
            ("Ajmeri Gate","Sindhi Camp"),
            ("Sindhi Camp","Subhash Nagar"),
            ("Subhash Nagar","Pani Pech"),
            ("Pani Pech","Ambabadi"),
            ("Mansarovar","New Aatish Market"),
            ("New Aatish Market","Vivek Vihaar"),
            ("Vivek Vihaar","Shyam Nagar"),
            ("Shyam Nagar","Ram Nagar"),
            ("Ram Nagar","Civil Lines"),
            ("Civil Lines","Railway Station"),
            ("Railway Station","Sindhi Camp"),
            ("Sindhi Camp","Chand Pole"),
            ("Chand Pole","Choti Chaupar"),
            ("Choti Chaupar","Badi Chaupar"),
            ("Jawahar Nagar","SMS Hospital"),
            ("SMS Hospital","Ram Nagar"),
            ("Ram Nagar","Hasanpura"),
            ("Hasanpura","Khatpura"),
            ("Khatpura","Vaishali Nagar"),
            ("Vaishali Nagar","Chitrakoot"),
            ("Chitrakoot","Tagore Nagar")
            
        ]

class metro_map:
    def __init__(self, routes):
        self.routes = routes

    def show_map(self):
        positions = {
            "Mansarovar": (0, 0),
            "New Aatish Market": (1, 0),
            "Vivek Vihaar": (2, 0),
            "Shyam Nagar": (3, 0),
            "Ram Nagar": (4, 0),
            "Civil Lines": (5, 0),
            "Railway Station": (6, 0),
            "Sindhi Camp": (7, 0),
            "Chand Pole": (8, 0),
            "Choti Chaupar": (9, 0),
            "Badi Chaupar": (10, 0),

            "Sanganer": (0, 3),
            "Durgapura": (1, 3),
            "Gopal Pura": (2, 3),
            "SMS Stadium": (3, 3),
            "SMS Hospital": (4, 2),
            "Ajmeri Gate": (5, 2),
            "Subhash Nagar": (6, 2),
            "Pani Pech": (7, 2),
            "Ambabadi": (8, 2),

            "Jawahar Nagar": (4, 4),
            "Hasanpura": (5, 4),
            "Khatpura": (6, 4),
            "Vaishali Nagar": (7, 4),
            "Chitrakoot": (8, 4),
            "Tagore Nagar": (9, 4),
        }

        line1_color = 'red'
        line2_color = 'blue'
        line3_color = 'green'

        intersections = ["Sindhi Camp", "SMS Hospital", "Ram Nagar"]

        plt.figure(figsize=(10, 6))

        for start, end in self.routes:
            x_values = [positions[start][0], positions[end][0]]
            y_values = [positions[start][1], positions[end][1]]
            if start in ["Mansarovar", "Badi Chaupar", "New Aatish Market", "Vivek Vihaar"]:
                color = line1_color
            elif start in ["Sanganer", "Ambabadi", "Subhash Nagar"]:
                color = line2_color
            else:
                color = line3_color
            plt.plot(x_values, y_values, color=color, linewidth=2)

        for station, (x, y) in positions.items():
            if station in intersections:
                plt.scatter(x, y, color='yellow', edgecolor='black', s=100, zorder=3)
            else:
                plt.scatter(x, y, color='black', s=60, zorder=2)
            plt.text(x, y + 0.15, station, fontsize=8, ha='center')

        plt.title("~~~ JAIPUR METRO MAP ~~~", fontsize=14, weight='bold')
        plt.axis('off')
        plt.plot([], [], color='red', label='Line 1')
        plt.plot([], [], color='blue', label='Line 2')
        plt.plot([], [], color='green', label='Line 3')
        plt.scatter([], [], color='yellow', edgecolor='black', s=100, label='Interchange Station')
        plt.legend()

        plt.show()

metro_graph = graph(routes)

class ticket:
    def __init__(self, customer_name, customer_age, customer_gender, p, d):
        self.customer_name = customer_name
        self.customer_age = customer_age
        self.customer_gender = customer_gender
        self.pick_up_station_id = p
        self.drop_off_station_id = d

        pick_up_station = drop_off_station = None
        with open("stations.csv", 'r') as table:
            station_list = csv.reader(table)
            next(station_list)  
            for line in station_list:
                if p == int(line[0]):
                    pick_up_station = line[1]
                if d == int(line[0]):
                    drop_off_station = line[1]

        self.pick_up_station = pick_up_station
        self.drop_off_station = drop_off_station
        self.id = str(uuid.uuid4())[:8]
        self.price = metro_graph.calculate_fare(self.pick_up_station, self.drop_off_station)

        self.save_ticket_to_csv()

    @classmethod
    def purchase_ticket(cls):
        customer_name = input("Enter your name: ")
        customer_age = input("Enter your age: ")
        customer_gender = input("Enter your gender: ")
        p = int(input("Enter pick-up station ID: "))
        d = int(input("Enter drop-off station ID: "))

        print("\n~~~ TICKET ISSUED FOR " + f"{customer_name.upper()} ~~~")
        return cls(customer_name, customer_age, customer_gender, p, d)

    def save_ticket_to_csv(self):
        file_exists = os.path.isfile("tickets.csv")

        with open("tickets.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "Ticket ID", "Customer Name", "Age", "Gender",
                    "Pick-Up Station", "Drop-Off Station", "Fare (Rs)"
                ])

            writer.writerow([
                self.id,
                self.customer_name,
                self.customer_age,
                self.customer_gender,
                self.pick_up_station,
                self.drop_off_station,
                self.price
            ])

    def view_ticket(self):
        print("\n~~~ JAIPUR METRO TICKET ~~~")
        print(f"Ticket ID: {self.id}")
        print(f"Customer Name: {self.customer_name.upper()}")
        print(f"Age: {self.customer_age}")
        print(f"Gender: {self.customer_gender.upper()}")
        print(f"Pick-Up Station: {self.pick_up_station}")
        print(f"Drop-Off Station: {self.drop_off_station}")
        print(f"Fare: Rs. {self.price}")


def show_menu():
    print("1.","Purchase ticket")
    print("2.","View ticket")
    print("3.","See path between stations")
    print("4.","Show metro map")
    print("5.","exit")    
    
    
def main():
    if not os.path.exists("stations.csv"):
        line.initialise_lines()

    station.list_stations()
    print("\n~~~JAIPUR METRO~~~")

    t1 = None

    while True:
        show_menu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input>> Please enter a number")
            continue


        if choice == 1:
            t1 = ticket.purchase_ticket()

        elif choice == 2:
            if not t1:
                print("Please purchase a ticket first.")
                continue
            t1.view_ticket()

        elif choice == 3:
            if not t1:
                print("Please purchase a ticket first.")
                continue

            print("\nShortest Path:")
            path = metro_graph.shortest_path(t1.pick_up_station, t1.drop_off_station)
            print(" → ".join(path))

            print("\nTravel Instructions:")
            for step in metro_graph.get_instructions(t1.pick_up_station, t1.drop_off_station):
                print("-", step)

        elif choice == 4:
            metro = metro_map(routes)
            metro.show_map()
    
        elif choice == 5:
            break



if __name__ == "__main__":
    main()
    
