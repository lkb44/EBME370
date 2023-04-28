import random
import pandas as pd
from docx import Document
from docx.shared import Inches

# Define the age and gender categories with their respective thresholds
categories = {
    'Age 6 Boy': 250.81,
    'Age 7 Boy': 288.04,
    'Age 8 Boy': 229.35,
    'Age 9 Boy': 221.45,
    'Age 10 Boy': 220.31,
    'Age 6 Girl': 296.45,
    'Age 7 Girl': 257.98,
    'Age 8 Girl': 251.28,
    'Age 9 Girl': 266.11,
    'Age 10 Girl': 229.47
}

# Generate the data by looping 50 times and randomly selecting age and gender
data = []
for i in range(50):
    age_gender = random.choice(list(categories.keys()))
    age, gender = age_gender.split()
    generated_freq = random.uniform(150, 350) # Generate a frequency between 150 and 350
    expected_freq = categories[age_gender]
    data.append([gender, age, round(generated_freq, 2), expected_freq])

# Convert the data to a pandas dataframe
df = pd.DataFrame(data, columns=['Gender', 'Age', 'Generated Frequency', 'Expected Frequency'])

# Create a Word document and add a table to it
document = Document()
table = document.add_table(rows=51, cols=4)
table.style = 'Table Grid'
# Add the headers to the first row of the table
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Gender'
hdr_cells[1].text = 'Age'
hdr_cells[2].text = 'Generated Frequency'
hdr_cells[3].text = 'Expected Frequency'

# Add the data to the table
for i, row in df.iterrows():
    cells = table.rows[i+1].cells
    cells[0].text = row['Gender']
    cells[1].text = row['Age']
    cells[2].text = str(row['Generated Frequency'])
    cells[3].text = str(row['Expected Frequency'])

# Save the Word document
document.save('/Users/leobao/Documents/Academic Documents/2022-2023/EBME 380/frequency_table.docx')
