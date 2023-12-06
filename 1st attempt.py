# Read all employee data from the file
employee_data = []
with open("employee_data.txt", "r") as file:
    employee_data = file.readlines()

# Organize the data by date and number of packages delivered
organized_data = {}
for line in employee_data:
    full_name, employee_id, packages_delivered, date = line.strip().split(',')
    key = (date, int(packages_delivered))
    
    if key not in organized_data:
        organized_data[key] = []
    
    organized_data[key].append(line)

# Create a new text file to store the organized data
organized_filename = "organized_employee_data.txt"
with open(organized_filename, "w") as file:
    for key in sorted(organized_data.keys()):
        for line in organized_data[key]:
            file.write(line)

print("Additional employee data has been added and organized in 'organized_employee_data.txt'.")