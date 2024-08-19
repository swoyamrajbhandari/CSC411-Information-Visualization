import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = r'C:\Users\swoya\OneDrive\Desktop\UVIC_Semesters\Summer24\CSC 411\Storyteling\storytelling-data.csv' 
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Extract relevant columns: Faculty and yearly salaries from 2013 to 2023
relevant_columns = ['Faculty'] + [str(year) for year in range(2013, 2024)]
faculty_salaries = data[relevant_columns]

# Drop rows with missing faculty information
faculty_salaries = faculty_salaries.dropna(subset=['Faculty'])

# Calculate the average salary per faculty per year
average_salaries = faculty_salaries.groupby('Faculty').mean().reset_index()

# Calculate the growth rate from 2013 to 2023 for each faculty
average_salaries['Growth Rate (%)'] = ((average_salaries['2023'] - average_salaries['2013']) / average_salaries['2013']) * 100

# Apply a logarithmic transformation for a more pronounced gradient effect
norm_growth_rate = np.log1p(average_salaries['Growth Rate (%)'] - average_salaries['Growth Rate (%)'].min())
norm_growth_rate = (norm_growth_rate - norm_growth_rate.min()) / (norm_growth_rate.max() - norm_growth_rate.min())

# Extract relevant columns for the line plot
plot_columns = [str(year) for year in range(2013, 2024)]

# Line plot of average salaries over the years for each faculty with LAW faculty in red and others in gradient blue
plt.figure(figsize=(12, 8))

# Plot other faculties first
for i, faculty in enumerate(average_salaries['Faculty']):
    if faculty != 'Law':
        color = plt.cm.Blues(norm_growth_rate[i])
        plt.plot(plot_columns, average_salaries[average_salaries['Faculty'] == faculty][plot_columns].values.flatten(), label=faculty, color=color)
        plt.text(plot_columns[-1], average_salaries[average_salaries['Faculty'] == faculty][plot_columns].values.flatten()[-1], 
                 f"{faculty} ({average_salaries['Growth Rate (%)'][i]:.2f}%)", fontsize=9, color=color, va='center')

# Plot Law faculty last to ensure it's on top
law_data = average_salaries[average_salaries['Faculty'] == 'Law'][plot_columns].values.flatten()
law_growth_rate = average_salaries[average_salaries['Faculty'] == 'Law']['Growth Rate (%)'].values[0]
plt.plot(plot_columns, law_data, label='Law', color='red')
plt.text(plot_columns[-1], law_data[-1], f"Law ({law_growth_rate:.2f}%)", fontsize=9, color='red', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

# Annotate initial and final salary for Law faculty with a $ sign
initial_salary = law_data[0]
final_salary = law_data[-1]
plt.annotate(f"${initial_salary:,.0f}", (plot_columns[0], initial_salary), textcoords="offset points", fontsize=8, xytext=(0,10), ha='center', color='red')
plt.annotate(f"${final_salary:,.0f}", (plot_columns[-1], final_salary), textcoords="offset points", fontsize=8, xytext=(0,10), ha='center', color='red')

# Add annotation text on the left side of the graph
plt.annotate("A decade ago, the employees at UVic's Law faculty\nhad the lowest average salary", 
             xy=(0.02, 0.62), xycoords='axes fraction', fontsize=8, color='black', ha='left', va='center')

# Add annotation text on the right side of the graph
plt.annotate("After a decade, the average salary of the Law faculty\nhas seen a high growth rate(%)\nsurpassing most of the other faculties in its average salary.", 
             xy=(0.56, 0.3), xycoords='axes fraction', fontsize=8, color='black', ha='left', va='center')

# Add a sentence below the main title
plt.annotate("compared to other faculties", 
             xy=(0.0, 0.93), xycoords='figure fraction', fontsize=10, color='black',ha='left', va='center')

plt.suptitle('We see a higher growth rate in average salary of the Law faculty\n', x=0.0, ha='left', fontsize=16)
plt.title('Average Faculty Salaries Over Time', fontsize=12, pad=12, loc='left')

plt.xlabel('Year')
plt.ylabel('Average Salary($)')
plt.xticks(rotation=45)
plt.xlim('2013', '2023')  # Set the x-axis to start from 2013 to 2023
plt.ylim(0, 200000)  # Set the y-axis range from 0 to 200000
plt.yticks(range(0, 200001, 20000))  # Set y-axis ticks with 20000 increment
plt.tight_layout()
plt.show()
