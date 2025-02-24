# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:46:40 2024

@author: Zarina Davletova  zdavleto
"""
# graph for the school_data 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px

#bar chart for data from University Health Center 
school_data = pd.read_csv('school_data.csv') #read school data
print(school_data)
x = school_data['Category'] 
y = school_data['Count']

plt.figure(figsize=(10,6))
bars = plt.bar(x, y, color = ['skyblue', 'purple', 'green', 'lightcoral'])

plt.xlabel('Category') # x label
plt.ylabel('Count') # y label
plt.title('Carnegie Mellon University Health Insurance Enrollment Data')
plt.xticks(rotation = 45)
plt.bar_label(bars)

#figures from survey data

pio.renderers.default='browser' #display graph in browser

survey = pd.read_csv('survey_data.csv')

#pie chart for the percentage of international and domestic students
student_type_count = survey['student_type'].value_counts().reset_index() #counts the occurences of each unique value
student_type_count.columns = ['student_type', 'count']  # Rename columns for clarity
fig = px.pie(student_type_count, 
             names='student_type', 
             values='count', 
             title='Distribution of Student Types in Survey Responses',
             color_discrete_sequence=['skyblue', 'lightcoral'])
fig.show()

#bar plot for year in school
student_year = survey['year_in_school'].value_counts().reset_index()
student_year.columns = ['year_in_school', 'count']
student_year['percentage'] = (student_year['count'] / student_year['count'].sum()) * 100 #calculate percenatges
fig = px.bar(student_year, 
             x='year_in_school', 
             y='count', 
             title='Distribution of Students by Year in School',
             color = 'year_in_school', 
             text=student_year['percentage'].map(lambda x: f"{x:.1f}%"),  # Format percentage for text
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.show()

#pie  chart for schools attending
school_count = survey['school'].value_counts().reset_index()
school_count.columns = ['school', 'count'] 
school_count['percentage'] = (school_count['count'] / school_count['count'].sum()) * 100
fig = px.pie(school_count, 
             names='school', 
             values='count', 
             title='Distribution of Students by School',
             color_discrete_sequence=px.colors.qualitative.Set3,
             hover_data=['percentage'])

fig.update_traces(textinfo='percent+label')  
fig.show()



# pie chart primary health insurance type
insurance_count = survey['health_insurance'].value_counts().reset_index()
insurance_count.columns = ['insurance_type', 'count'] 
insurance_count['percentage'] = (insurance_count['count'] / insurance_count['count'].sum()) * 100

fig = px.pie(insurance_count, 
             names='insurance_type', 
             values='count', 
             title='Distribution of Students by Primary Health Insurance Type',
             color_discrete_sequence=px.colors.qualitative.Set3,
             hover_data=['percentage'])  # Show percentage on hover

fig.update_traces(textinfo='percent+label')  # Show percentage and label
fig.show()



#bar chart for not choosing school insurance
split_responses = survey['why_not_school_insurance '].dropna().str.split(';') #splits the answers in 1 row that are followed by ';'
all_responses = [response.strip() for sublist in split_responses for response in sublist] #creates list of responses 
responses_df = pd.DataFrame(all_responses, columns=['reason'])
reason_count = responses_df['reason'].value_counts().reset_index()
reason_count.columns = ['reason', 'count']  
total_responses = reason_count['count'].sum()
reason_count['percentage'] = (reason_count['count'] / total_responses) * 100

fig = px.bar(reason_count, 
             y='reason',  
             title='Reasons for Not Choosing School Health Insurance',
             color='reason', 
             text=reason_count['percentage'].map(lambda x: f'{x:.1f}%'),  
             color_discrete_sequence=px.colors.qualitative.Set3,
             orientation='h')  # Set orientation to horizontal

fig.show()

#use of school health insrurance
use_of_insurance_count = survey['use_of_school_insurance'].value_counts().reset_index()
use_of_insurance_count.columns = ['response', 'count']  
total_responses = use_of_insurance_count['count'].sum()
use_of_insurance_count['percentage'] = (use_of_insurance_count['count'] / total_responses) * 100

fig = px.bar(use_of_insurance_count, 
             x='response', 
             y='percentage', 
             title='Use of School Health Insurance (Yes/No)',
             text=use_of_insurance_count['percentage'].map(lambda x: f'{x:.1f}%'),  
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.update_traces(textposition='outside')
fig.show()



#types of services 
split_services = survey['types_of_service'].dropna().str.split(';')
all_services = [service.strip() for sublist in split_services for service in sublist]
services_df = pd.DataFrame(all_services, columns=['service'])
service_count = services_df['service'].value_counts().reset_index()
service_count.columns = ['service', 'count']  
total_services = service_count['count'].sum()
service_count['percentage'] = (service_count['count'] / total_services) * 100
fig = px.bar(service_count, 
             x='percentage',  
             y='service',
             title='Types of Services Used through School Health Insurance',
             text=service_count['percentage'].map(lambda x: f'{x:.1f}%'),  
             color='service', 
             color_discrete_sequence=px.colors.qualitative.Set3,
             orientation='h') # horizontal orientation for bars
fig.show()



#frequency of usage
frequency_count = survey['frequency'].value_counts().reset_index()
frequency_count.columns = ['frequency', 'count']  # Rename columns for clarity
fig = px.pie(frequency_count, 
             names='frequency', 
             values='count', 
             title='Frequency of School Health Insurance Usage in the Past Year',
             color_discrete_sequence=px.colors.qualitative.Set3)

fig.update_traces(textinfo='percent+label')
fig.show()

#challenges 
challenges_count = survey['challenges'].value_counts().reset_index()
challenges_count.columns = ['challenges', 'count']  # Rename columns for clarity
fig = px.pie(challenges_count, 
             names='challenges', 
             values='count', 
             title='Distribution of Challenges Faced When Using School Health Insurance',
             color_discrete_sequence=px.colors.qualitative.Set3)

fig.update_traces(textinfo='percent+label')
fig.show()

#satisfaction with school insurance 
satisfaction_count = survey['satisfaction_with_sch_insurance'].value_counts().reset_index()
satisfaction_count.columns = ['satisfaction', 'count']  # Rename columns for clarity

fig = px.pie(satisfaction_count, 
             names='satisfaction', 
             values='count', 
             title='Distribution of Satisfaction with School Health Insurance',
             color_discrete_sequence=px.colors.qualitative.Set3)

fig.update_traces(textinfo='percent+label')
fig.show()

#different option
# Splits the 'different_option' column, clean up the individual options, and stack them
different_options_split = survey['different_option'].str.split(';', expand=True).stack()
different_options_count = different_options_split.value_counts().reset_index()
different_options_count.columns = ['option', 'count'] 
total_count = different_options_count['count'].sum() 
different_options_count['percentage'] = (different_options_count['count'] / total_count * 100).round(2)
fig = px.bar(different_options_count, 
             x='percentage',  
             y='option',
             title='Distribution of Different Options Chosen (Percentage)',
             color='option',  
             text=different_options_count['percentage'].map(lambda x: f'{x:.1f}%'),  
             color_discrete_sequence=px.colors.qualitative.Set3, 
             orientation='h')  

fig.update_traces(texttemplate='%{text}%', textposition='outside') #Updates the plot to display percentages outside the bars
fig.show()

# pie chart for question about the program 
question_count = survey['question_about_program'].value_counts().reset_index() 
question_count.columns = ['question', 'count']  

fig = px.pie(question_count, 
             names='question', 
             values='count', 
             title='Do you think it will be helpful to have a program which can answer your concern about the services and coverage for your school insurance?',
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.update_traces(textinfo='percent+label')
fig.show()




