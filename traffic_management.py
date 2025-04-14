#Author: Shavin De Silva
#Date: 26/11/2024
#Student ID: 20240198 / W2119859

# Task A: Input Validation
import csv
import tkinter as tk

def validate_date_input():
    #this gets the date as a valid input
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format DD: "))
            if 1 <= day <= 31:
                break
            #if the given intiger is out of range the below statment will be printed
            else:
                print(f"{day} is out of range. Please pick a number between 1 and 31.")
        
        #if the given value is not an integer the following statment will be printed
        except ValueError:
            print("Invalid input for day. Please enter an integer.")
     
    # this code block is used to get valid input for the month
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if 1 <= month <= 12:
                break
            else:
                print(f"{month} is out of range. Please pick a number between 1 and 12.")

        except ValueError:
            print("Invalid input for month. Please enter an integer.")
            
    #this code block is used to get valid input for the year
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:
                break
            else:
                print(f"{year} is out of range. Please pick a number between 2000 and 2024.")

        except ValueError:
            print("Invalid input for year. Please enter an integer.")

    return day, month, year    # Generate the file name in the expected format


def leap_year(year):  #checks if the year given is a leap yr or not
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400==0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def date_validation (day, month, year): #check if the given day matches with the given month   
    if month in (4, 6, 9, 11) and day > 30:
        print(f"{day} is invalid for the selected month ({month}).")
        return False
    
    elif month == 2:
        if leap_year(year):
            if day > 29:
                print(f"{day} is invalid for February in a leap year.")
                return False
            
        else:
            if day > 28:
                print(f"{day} is invalid for February in a non-leap year.")
                return False
            
    return True

def validate_continue_input():
    while True:
        re_run = input("Do you want to select another data file for a different date? Y/N: ").strip().upper()
        if re_run == "Y":
            return True
            
        elif re_run == "N":
            return False
        
        else:
            print("Invalid Input! try again")

# Task B: Processed Outcomes
def process_csv_data(file_name):
    try:
        #this reads the csv file 
        with open(file_name,'r') as file:
            reader = csv.DictReader(file) #converts the file into a dictionary line by line 
            data = list(reader) #gets all the values from the dictionary to a list
        
        #if the selected csv file doesnt have data this statment would be printed
        if not data:
            print("The file is empty.")
            return None
            
        print(f"""\n*******************************************
data file is selected {file_name}.
*******************************************
        """)   
        # The total number of vehicles passing through all junctions for the selected date.
        total_vehicles = len(data)
        
        # The total number of trucks passing through all junctions for the selected date.
        total_trucks = sum(1 for row in data if row['VehicleType'].lower() == 'truck')
        
        # The total number of electric vehicles passing through all junctions for the selected date.
        total_electric = sum(1 for row in data if row['elctricHybrid'].lower() == 'true')
        
        # The number of “two wheeled” vehicles through all junctions for the date (bikes, motorbike, scooters).
        two_wheel = sum(1 for row in data if row['VehicleType'] in ['Motorcycle', 'Bicycle', 'Scooter'])
        
        #The total number of busses leaving Elm Avenue/Rabbit Road junction heading north .
        busses_North = sum(1 for row in data if row['VehicleType'].lower() == 'buss' and
                           row['JunctionName'].lower() == 'elm avenue/rabbit road' and row['travel_Direction_out'].lower() == 'n' )
        
        # The total number of vehicles passing through both junctions without turning left or right.
        vehicals_turning = sum(1 for row in data if row['travel_Direction_in'] == row['travel_Direction_out'])
        
        # The percentage of all vehicles recorded that are Trucks for the selected date (rounded to an integer).
        trucks_percentage = round((total_trucks/total_vehicles)*100)
        
        # The average number Bicycles per hour for the selected date (rounded to an integer).
        avg_bicycle = sum(1 for row in data if row['VehicleType'].lower() == 'bicycle' )
        percentage_bicycle = round(avg_bicycle/24)
        
        # The total number of vehicles recorded as over the speed limit for the selected date.
        exceed_speed = sum(1 for row in data if int(row['JunctionSpeedLimit']) < int(row['VehicleSpeed']))
        
        # The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for the selected date.
        elm_total = sum(1 for row in data if row['JunctionName'].lower() == 'elm avenue/rabbit road')
        
        # The total number of vehicles recorded through only Hanley Highway/Westway junction for the selected date.
        hanley_total = sum(1 for row in data if row['JunctionName'].lower() == 'hanley highway/westway')
        
        # The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters (rounded to integer)
        elm_vehicles = sum(1 for row in data if row['JunctionName'].lower() == 'elm avenue/rabbit road')
        elm_scooter = sum(1 for row in data if row['JunctionName'].lower() == 'elm avenue/rabbit road' and row['VehicleType'].lower() == 'scooter')
        avg_scooter = round((elm_scooter/elm_vehicles)*100)
        
        # The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway.
        hanley_hour_count = {}
        for row in data:
            if "Hanley Highway/Westway" in row["JunctionName"]:
                hour = int(row["timeOfDay"].split(":")[0])
                hanley_hour_count[hour] = hanley_hour_count.get(hour, 0) + 1
        
        peak_hour_hanley = max(hanley_hour_count.values())       
            
        # The time or times of the peak (busiest) traffic hour (or hours) on Hanley Highway/Westway in the format Between 18:00 and 19:00.
        peak_hours = []
        for hour, count in hanley_hour_count.items():
            if count == peak_hour_hanley:
                peak_hours.append(hour)

        peak_hour_times = [f"Between {hour}:00 and {int(hour) + 1}:00" for hour in peak_hours]
        
        # The total number of hours of rain on the selected date.
        rainy_hours_set = set(
            row["timeOfDay"].split(":")[0]  
            for row in data 
            if "rain" in row["Weather_Conditions"].lower().strip()

        )

        rainy_hours = len(rainy_hours_set)
        
        
        #returning all calculated values as a list
        return [total_vehicles, total_trucks, total_electric, two_wheel, busses_North, vehicals_turning, trucks_percentage,
                percentage_bicycle, exceed_speed, elm_total, hanley_total, avg_scooter, peak_hour_hanley, peak_hour_times, rainy_hours]
    
    #if the given date is valid but no file related to that date this statment will be printed    
    except FileNotFoundError:
        print(f"File not found. Please ensure it exists.")
        return None
    

def display_outcomes(outcomes):
    #the values which were called earlier have been called using their indexes
    output = f"""
The total number of vehicles recorded for this date is: {outcomes[0]}
The total number of trucks recorded for this date is: {outcomes[1]}
The total number of electric vehicles recorded for this date is: {outcomes[2]}
The total number of two-wheeled vehicles recorded for this date is: {outcomes[3]}
The total number of busses leaving Elm Avenue/Rabbit Road heading north is: {outcomes[4]}
The total number of vehicles passing through both junctions without turning left or right is: {outcomes[5]}
The percentage of all vehicles recorded that are Trucks for this date is: {outcomes[6]}%
The average number of bicycles per hour for this date is: {outcomes[7]}
The total number of vehicles recorded as over the speed limit for this date is: {outcomes[8]}
The total number of vehicles recorded through only Elm Avenue/Rabbit Road junction for this date is: {outcomes[9]}
The total number of vehicles recorded through only Hanley Highway/Westway junction for this date is: {outcomes[10]}
{outcomes[11]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.
The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway :{outcomes[12]}. 
The time or times of the peak (busiest) traffic hour (or hours) on Hanley Highway/Westway: {outcomes[13]}.
The total number of hours of rain on the selected date: {outcomes[14]}. 

"""
    print(output)
    return output

# Task C: Save Results to Text File
def save_results_to_file(outcomes, new_name, file_name):
    #here it creates a new file and write the output from the earlier function on it
    with open(new_name, "a") as file:
        file.write(f"date file selected {file_name} ")
        file.write(display_outcomes(outcomes))
        file.write("\n"+ "*" * 60 + "\n")
    print(f"Results saved to '{new_name}' successfully!")

# Task D: Histogram Display
class HistogramApp:
    def __init__(self, traffic_data, date):
       
        self.traffic_data = traffic_data
        self.date = date
        self.root = None
        self.canvas = None

    def setup_window(self):
           
        self.root = tk.Tk()
        self.root.title("Histogram")
        self.canvas = tk.Canvas(self.root, width=1300, height=500, bg='cornsilk') 
        self.canvas.pack(fill=tk.BOTH,expand=True)

    def draw_histogram(self):

        hourly_counts = {'Elm Avenue/Rabbit Road': [0] * 24, 'Hanley Highway/Westway': [0] * 24} #intializing 24 zeros for each roads road
        for row in self.traffic_data:
            hour = int(row['timeOfDay'].split(':')[0])
            junction = row['JunctionName']
            if junction in hourly_counts:
                hourly_counts[junction][hour] += 1

        #finds the largest value on both roads
        max_value = max(max(hourly_counts['Elm Avenue/Rabbit Road']),
                        max(hourly_counts['Hanley Highway/Westway']))
        scale = 400 / max_value if max_value > 0 else 1
        bar_width = 15 #width of each bar
        gap = 20 #gap between each groups
        x_offset = 50  #distance from left
        y_offset = 450 #distacnce from bottem


        self.canvas.create_line(x_offset, y_offset, 1200, y_offset)  # X-axis 

        # Bars and X-axis labels
        for i in range(24):
            # Elm Avenue/Rabbit Road bars
            elm_bar_height = hourly_counts['Elm Avenue/Rabbit Road'][i] * scale
            self.canvas.create_rectangle(
                x_offset + i * (2 * bar_width + gap), y_offset - elm_bar_height,
                x_offset + i * (2 * bar_width + gap) + bar_width, y_offset,
                fill="salmon", outline="black"
            )
            
            if elm_bar_height > 0:
                self.canvas.create_text(
                    x_offset + i * (2 * bar_width + gap) + bar_width // 2, y_offset - elm_bar_height - 10,
                    text=str(hourly_counts['Elm Avenue/Rabbit Road'][i]),
                    font=("Arial", 8), fill="salmon"
                )
            
            # Hanley Highway/Westway bars
            hanley_bar_height = hourly_counts['Hanley Highway/Westway'][i] * scale
            self.canvas.create_rectangle(
                x_offset + i * (2 * bar_width + gap) + bar_width, y_offset - hanley_bar_height,
                x_offset + i * (2 * bar_width + gap) + 2 * bar_width, y_offset,
                fill="lightgreen", outline="black"
            )
            
            if hanley_bar_height > 0:
                self.canvas.create_text(
                    x_offset + i * (2 * bar_width + gap) + 3 * bar_width // 2, y_offset - hanley_bar_height - 10,
                    text=str(hourly_counts['Hanley Highway/Westway'][i]),
                    font=("Arial", 8), fill="lightgreen"
                )
            
            # X-axis labels 0 to 23
            self.canvas.create_text(x_offset + i * (2 * bar_width + gap) + bar_width, y_offset + 10, text=str(i), font=('Arial', 8))

        # Add labels
        self.canvas.create_text(600, 20, text=f"Histogram of vehical frequency per Hour ({self.date})", font=('Arial', 14, 'bold'))
        self.canvas.create_text(600, 480, text="Hour 00:00 to 24:00", font=('Arial', 12,'bold'))


    def add_legend(self):

        self.canvas.create_rectangle(30, 30, 50, 50, fill="salmon")
        self.canvas.create_text(60, 40, text="Elm Avenue/Rabbit Road", anchor='w',font=('bold',10))

        self.canvas.create_rectangle(30, 70, 50, 90, fill="lightgreen")
        self.canvas.create_text(60, 80, text="Hanley Highway/Westway", anchor='w',font=('bold',10))

    def run(self):

        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

class MultiCSVProcessor:
    def __init__(self):

        self.current_data = None  # To store traffic data for the current dataset

    def load_csv_file(self, file_name):
        #opens the csv file
        try:
            with open(file_name, 'r') as file:
                reader = csv.DictReader(file)
                self.current_data = list(reader)
                if not self.current_data:
                    print(f"Error: The file '{file_name}' is empty.")
                    return False
                return True
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            return False

    def clear_previous_data(self):
        #clears the data from the previous run
        if self.current_data:
            print('Previous data cleared')
            self.current_data.clear()

    def handle_user_interaction(self):

        while True:
                re_run = input("Do you want to select another data file for a different date? Y/N: ").strip().upper()
                if re_run == "Y":
                    return True
                    
                elif re_run == "N":
                    return False
                
                else:
                    print("Invalid Input! try again")


    def process_files(self):

        while True:
            # Input date and validate
            day, month, year = validate_date_input()
            file_name = f'traffic_data{day:02d}{month:02d}{year}.csv'

            if date_validation(day, month, year):
                # Load and process the CSV file
                self.clear_previous_data()
                if self.load_csv_file(file_name):
                    # Process outcomes and display histogram
                    outcomes = process_csv_data(file_name)
                    if outcomes:
                        save_results_to_file(outcomes, "results.txt", file_name)
                        date_string = f"{day:02d}/{month:02d}/{year}"
                        histogram_app = HistogramApp(self.current_data, date_string)
                        histogram_app.run()
            else:
                print("Invalid date. Please try again.")

            # Check if the user wants to continue
            if not self.handle_user_interaction():
                print("Exiting program.")
                break

def main():
    app = MultiCSVProcessor()
    app.process_files()

main()

# if you have been contracted to do this assignment please do not remove this line