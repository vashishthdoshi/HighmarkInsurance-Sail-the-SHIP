
"""
File: Part 2 - cost and coverage

@author: zhuoyuanyang(zhuoyuay) & joannachang(joannac2)
"""

# Import libraries we need 
import requests
import json
import concurrent.futures
import pandas as pd
import re

# Load CMS(Centers for Medicare & Medicaid Services) data for Mode 1 
# define the original API url
headers = {'Content-Type': 'application/json'}
url = "https://data.cms.gov/data-api/v1/dataset/92396110-2aed-4d63-a6a2-5d6207d46a29/data"

# filter data of Pittsburgh using zipcode contains 152 & state is PA
url_pitts = url + "?filter[example][condition][path]=Rndrng_Prvdr_Zip5&filter[example][condition][operator]=STARTS_WITH&filter[example][condition][value]=152&filter[Rndrng_Prvdr_State_Abrvtn]=PA"

# get to know the data size
url_getsize = url + '/stats' +"?filter[example][condition][path]=Rndrng_Prvdr_Zip5&filter[example][condition][operator]=STARTS_WITH&filter[example][condition][value]=152&filter[Rndrng_Prvdr_State_Abrvtn]=PA"
response = requests.get(url_getsize)
if response.status_code == 200:
    data = json.loads(response.content.decode('utf-8'))
    total_rows = data.get('found_rows')
    print('The data size is:  ',total_rows)  # output should be 38232

# load the data page by page; as the API only permits getting 5，000 rows of data per time 
def fetch_data(offset):
    size = 5000
    offset_url = url_pitts + "&size="+str(size)+"&offset="+ str(offset)
    offset_response = requests.get(offset_url,headers = headers)
    if offset_response.status_code == 200:
        return json.loads(offset_response.content.decode('utf-8'))
    else:
        print(f"Request failed at offset {offset}")
        return {}
# create multiple threads to get the data at the same time and restore result(which is a list of dicts) into a list
with concurrent.futures.ThreadPoolExecutor() as executor:
    offsets = [i for i in range(0, total_rows, 5000)]
    results = list(executor.map(fetch_data, offsets))

# aggregate the data from the list; each result here is a list of dicts, and a dict is a data point
data = []
for result in results:
    data.extend(result)

# check the headers of the data
if isinstance(data, list) and len(data) > 0:
    headers = list(data[0].keys())
    print("headers:",headers)
        
    # check the data size
    total_records = len(data)
    print("#total data: ", total_records) #should be 38232
        
else:
    print("The data is empty or the format is incorrect")

# convert to a DataFrame, and check the DataFrame
df = pd.DataFrame(data)
print(df.info())
print(df.head())
# check how many unique HCPCS Code in the table
print(len(df['HCPCS_Cd'].unique())) # should be 1882

# Compute the average cost for each unique HCPCS code, at the same time ,count the frequency of each code
df['Avg_Sbmtd_Chrg'] = pd.to_numeric(df['Avg_Sbmtd_Chrg'], errors='coerce') # convert the object to int
df['Avg_Mdcr_Alowd_Amt'] = pd.to_numeric(df['Avg_Mdcr_Alowd_Amt'], errors='coerce') # convert the object to int
df_avgcost = df.groupby(['HCPCS_Cd','HCPCS_Desc']).agg({
    'Avg_Sbmtd_Chrg':'mean',
    'Avg_Mdcr_Alowd_Amt':'mean',
    'HCPCS_Cd':'count'})
df_avgcost = df_avgcost.round(1)
df_avgcost = df_avgcost.rename(columns={'Avg_Sbmtd_Chrg':'Billed Amount','Avg_Mdcr_Alowd_Amt':'Medicare Allowed Amount','HCPCS_Cd': 'Count'})
print(df_avgcost.info())
print(df_avgcost.head())


# Mode 1 data preparation; see what are the most 50 common used services
df_sorted = df_avgcost.sort_values('Count',ascending=False).head(50).sort_index(level='HCPCS_Desc', ascending=True)
print(df_sorted)
    #group the most common charge mannually and design a keyword:table dict.
df_sorted = df_sorted.reset_index() # convert the index to colomns
    #define the keywords
category_keywords = {
    'X-ray':['X-ray'],'Ultrasound':['Ultrasound','Ultrasonic'],'ecg':['Routine electrocardiogram'],
    'Office visit':['office'],'vein blood collection':['Insertion of needle into vein'],
    'hospital stay':['hospital inpatient care','Hospital discharge day management'],'vaccine':['vaccine','vac'],
    'Emergency department':['Emergency'],'ct':['ct scan'],'Anesthesia':['Anesthesia'],'others':['nursing','critical']}
    # create the keyword:table dict
category_tables = {key: pd.DataFrame(columns=df_sorted.columns) for key in category_keywords} 
for idx,row in df_sorted.iterrows():   
    description = row['HCPCS_Desc'].lower()
    for category, keywords in category_keywords.items():
        if any(keyword.lower() in description for keyword in keywords):
            row_df = pd.DataFrame([row], columns=df_sorted.columns)
            category_tables[category] = pd.concat([category_tables[category], row_df],ignore_index=True)
# prepare the menu which will be used in the main program
categories = list(category_tables.keys())

# Mode 3 data preparation; match user input with description keywords and return a new table
def search_related_charges(key):
    key_lower = key.lower()  # Convert input to lowercase for case-insensitive matching
    matching_data = df_avgcost[df_avgcost.index.get_level_values('HCPCS_Desc').str.contains(key_lower, case=False, na=False, regex=True)]  # Perform fuzzy matching
    matching_data = matching_data.sort_values('Count', ascending=False)
    return matching_data


# Mode 2 data preparation. Read Highmark coverage file into pandas Dataframe
# Open and read the CSV file
csv_file = 'Copayment_Table.csv'
highmark = pd.read_csv(csv_file)

# Set pandas options to display full DataFrame
pd.set_option('display.expand_frame_repr', False)  # Expand to see all the columns
pd.set_option('display.max_rows', None)  # Expand to see all the rows

# Create a dictionary of category of services
category_service = {
    1: 'Outpatient Medical Care Services',
    2: 'Preventive Care Services',
    3: 'Hospital and Medical/Surgical Services (including maternity)',
    4: 'Therapy, Habilitative and Rehabilitative Services',
    5: 'Mental Health/ Substance Abuse Services',
    6: 'Other Services'
}

# Main program
while True:
    # Ask the user how they want to proceed, there are 4 modes
    # Mode 1: Cost for common health services in PA (by menu)
    # Mode 2: Highmark health services (by menu)
    # Mode 3: Key in health services you want to know (by keywords)
    # Mode 4: Exit the program
    try:
        mode = int(input("Would you like to:\n1. Get cost information for common health services in PA\n2. Get Highmark health services coverage information\n3. Enter a health service you would like to know\n4. Exit\nEnter 1, 2, 3, or 4: "))
        
        if mode == 4: # Mode 4: Exit
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and the program
            
        # Mode 1: Cost for common health services in PA (by menu)
        if mode == 1:
            print("Please select a service category by entering the corresponding number:")
            for idx, category in enumerate(categories, 1):
                print(f"{idx}. {category}")
            # 1st choice: category(HCPCS codes)
            while True:
                try:
                    catecode = int(input("Enter the number corresponding to your choice: "))
                    if 1 <= catecode <= len(categories):
                        selected_category = categories[catecode - 1]
                        print(f"You selected: {selected_category}")
                        print(category_tables[selected_category]['HCPCS_Desc'])
                        break
                    else:
                        print(f"Please select a valid number between 1 and {len(categories)}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
            # 2nd choice: specific health services under the category chosen from 1st step
            while True:
                try:
                    servicecode = int(input("Please select a specific service by entering the corresponding number:"))
                    if servicecode in category_tables[selected_category].index:
                        # Look up through the category_table and retrieve its Billed Amount (the amount that the healthcare provider charges for the service before any insurance or Medicare adjustments), 
                                                                        # and Medicare Allowed Amount (this is the amount Medicare or insurance deems appropriate for the service)
                        service = category_tables[selected_category].loc[servicecode,['HCPCS_Desc','Billed Amount','Medicare Allowed Amount']]
                        print(service)
                        break
                    else:
                        print("Please select a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        
        # Mode 2: User can choose Highmark health services they want to know (by menu) 
        elif mode == 2: 
            # Look at the services provided and covered by Highmark
            print("Health services provided and covered by Highmark:")
            for key, value in category_service.items():
                print("%d: %s" % (key, value))

            # Step 1: Ask the user to choose a category
            while True:
                try:
                    user_input = int(input("Please choose a category (1-6): "))

                    # Validate input
                    if user_input < 1 or user_input > 6:
                        raise ValueError("Input must be between 1 and 6.")

                except ValueError as e:
                    print("Invalid input: %s. Please try again." % e)
                    
                else:
                    # Move on to the subcategory based on the user's choice
                    print("You selected: %s" % category_service[user_input])

                    # Print out the subcategory based on the user's choice
                    if user_input == 1:
                        subcategory_of_services = highmark['Benefit'].iloc[13:19]
                        print("Subcategory of Outpatient Medical Care Services:")
                    elif user_input == 2:
                        subcategory_of_services = highmark['Benefit'].iloc[20:32]
                        print("Subcategory of Preventive Care Services(4):")
                    elif user_input == 3:
                        subcategory_of_services = highmark['Benefit'].iloc[31:42]
                        print("Subcategory of Hospital and Medical/Surgical Services:")
                    elif user_input == 4:
                        subcategory_of_services = highmark['Benefit'].iloc[43:54]
                        print("Subcategory of Therapy, Habilitative and Rehabilitative Services:")
                    elif user_input == 5:
                        subcategory_of_services = highmark['Benefit'].iloc[55:57]
                        print("Subcategory of Mental Health/Substance Abuse Services:")
                    elif user_input == 6:
                        subcategory_of_services = highmark['Benefit'].iloc[58:71]
                        print("Subcategory of Other Services:")

                    # Print the subcategory services with numbers
                    for idx, service in enumerate(subcategory_of_services):
                        print("%d: %s" % (idx + 1, service))

                    # Step 2: Ask the user to choose a subcategory
                    while True:
                        try:
                            subcategory_choice = int(input("Please choose a subcategory number: ")) - 1

                            # Validate the choice
                            if subcategory_choice < 0 or subcategory_choice >= len(subcategory_of_services):
                                raise ValueError("Invalid subcategory number.")

                            # Get the selected subcategory service
                            selected_service = subcategory_of_services.iloc[subcategory_choice]

                            # Get the corresponding 'Network' value for the selected service
                            copayment_info = highmark[highmark['Benefit'] == selected_service]['Network'].values[0]
                            
                            # Show Highmark coverage information 
                            print("Highmark coverage information for '%s' within network: %s" % (selected_service, copayment_info))
                            break  # Exit the subcategory selection loop

                        except ValueError as e:
                            print("Invalid input: %s. Please try again." % e)
                    break  # Exit the category selection loop
        
        # Mode 3: Search health services you want to know (by keywords)
        # It shows two information about the service asked: Highmark coverage info & Medicare Allowed Amount in PA
        elif mode == 3:  
            
            # Extract services from 'Benefit' column and remove NaN
            health_services = highmark['Benefit'].dropna().tolist()  
            
            # Step 1: Ask users to input a question
            while True:
                try:
                    service_asked = input('Enter the health service you want to ask about (or type "exit" to quit): ').strip()

                    # Exit condition
                    if service_asked.lower() == "exit":
                        print("Exiting the search!")
                        break

                except Exception as e:
                    print("Error: %s. Please try again." % e)

                else:
                    found = False

                    for service in health_services:
                        # Ensure service is a valid string (ignore non-strings like floats or NaN)
                        if isinstance(service, str):
                            service = service.strip()  # Trim any extra whitespace

                            # Use regex to search for a match (case insensitive)
                            if re.search(re.escape(service_asked), service, re.IGNORECASE):
                                found = True
                                # Check if there's a match in the DataFrame for the service
                                matched_data = highmark[highmark['Benefit'] == service]
                                if not matched_data.empty:  # If the DataFrame is not empty
                                    copayment_info = matched_data['Network'].values[0]
                                    print("Service: '%s' within network coverage infomation: %s" % (service_asked, copayment_info))
                                    
                                    # Search related charges from df_avgcost
                                    output = search_related_charges(service_asked).head(15)
                                    if output.empty:
                                        print("No charge price info available for '%s'." % service_asked)
                                    else:
                                        print("Related charge price information for '%s':" % service_asked)
                                        print(pd.DataFrame(output.index.tolist(), columns=['HCPCS Code', 'Description']).to_string(index=False))
                                   
                                    # Step 2: Ask users to select a HCPCS code to get Billed Amount and Medicare Allowed Amount 
                                    while True:
                                        code = input('Please select a HCPCS code from the table: ')
                                        if code in output.index:
                                            oneoutput = output.loc[code, ['Billed Amount', 'Medicare Allowed Amount']]
                                            print(oneoutput)
                                            
                                            # Show the whole information about the service asked again.
                                            # Highmark coverage info and Medicare Allowed Amount
                                            discount_price = float(oneoutput['Medicare Allowed Amount'].iloc[0])
                                            print("Highmark coverage for %s is %s, with average Medicare Allowed Amount $%.1f." % (service_asked, copayment_info, discount_price))
                                            break
                                        else:
                                            print('This code is not listed in the table. Please type again.')
                                        
                                else:
                                    print("No coverage info available for '%s'." % service_asked)
                                    
                                break  # Stop after the first match is found
                    break  # Exit Mode 3 loop and return to main menu after search is done
                    if not found:
                        print("Sorry, no matching health service found. Please try again.")
    
    except ValueError as e:
        print("Invalid input: %s. Please enter 1, 2, 3, or 4" % e)

