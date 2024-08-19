import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = r'C:\Users\swoya\OneDrive\Desktop\UVIC_Semesters\Summer24\CSC 411\Storyteling\faculty_yearly_growth_rates.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Set the years and faculties for plotting
years = data.columns[1:]
faculties = data['Faculty']

# Create the clustered bar graph without any annotations
fig, ax = plt.subplots(figsize=(14, 8))

# Set the positions and width for the bars
bar_width = 0.2
positions = list(range(len(years)))

# Define colors
law_color = 'red'
cmap_blue = plt.get_cmap('Blues')

# Define transparency for the specific years
transparency = {'2014': 0.3, '2015': 0.3, '2016': 0.3, '2019': 0.3, '2021': 0.3}

# Plot bars for each year
for j, year in enumerate(years):
    year_data = data.set_index('Faculty').iloc[:, j]
    sorted_faculties = year_data.sort_values(ascending=False).index.tolist()
    law_position = sorted_faculties.index('Law')
    
    # Determine the top faculties to display based on the position of Law
    if law_position == 0:
        top_faculties = sorted_faculties[:3]
    elif law_position == 1:
        top_faculties = [sorted_faculties[0], sorted_faculties[1], sorted_faculties[2]]
    elif law_position == 2:
        top_faculties = sorted_faculties[:3]
    else:
        top_faculties = sorted_faculties[:3] + ['Law']

    for i, faculty in enumerate(top_faculties):
        faculty_data = data[data['Faculty'] == faculty].iloc[0, j + 1]
        bar_position = j + bar_width * (i - len(top_faculties) / 2)

        if faculty == 'Law':
            color = law_color
            alpha = transparency.get(year, 1.0)
        else:
            norm = plt.Normalize(year_data.min(), year_data.max())
            color = cmap_blue(norm(faculty_data))
            alpha = transparency.get(year, 1.0)

        ax.bar(bar_position, faculty_data, width=bar_width, color=color, alpha=alpha)

# Set the x-ticks and labels
ax.set_xticks([p for p in positions])
ax.set_xticklabels(years, rotation=45)

# Add a sentence below the main title
plt.annotate("compared to other faculties", 
             xy=(0.0, 0.93), xycoords='figure fraction', fontsize=10, color='black',ha='left', va='center')

# Set the labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Average Salary Growth Rate (%)')
plt.suptitle('We don\'t see a higher growth rate in average salary of the Law faculty\n\n', x=0.0, ha='left', fontsize=16)
plt.title('Average Salaries Growth Rate Over Time (2014-2023)', fontsize=12, pad=14, loc='left')
#ax.set_title('Average Salary Growth Rate by Faculty (2014-2023)')

# Adjust the y-axis origin to -10 and x-axis origin to 2014
ax.set_ylim([-10, ax.get_ylim()[1]])
ax.set_xlim([-0.5, len(years) - 0.5])

# Add a horizontal line at y=0
ax.axhline(y=0, color='gray', linestyle='--')

# Save plot to an image file
plt.savefig('average_salary_growth_rate_by_faculty_no_annotations.png')

# Show plot
plt.show()
