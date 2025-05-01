import pandas as pd

# File paths
input_file = 'ChalkData_ClassTutorial.xlsx'
output_file = 'ChalkData_ClassTutorial_cleaned.xlsx'

# Load the Excel file
raw_df = pd.read_excel(input_file)

# Set proper column headers (row 5 in the Excel sheet)
raw_df.columns = raw_df.iloc[4]
data_df = raw_df[6:154].copy()
data_df.reset_index(drop=True, inplace=True)

# Drop unwanted columns (keep only first 21, and then drop by specific indices)
data_df.drop(data_df.columns[21:], axis=1, inplace=True)
data_df.drop(data_df.columns[[4, 6, 17, 18, 19]], axis=1, inplace=True)

# Rename columns to meaningful names
data_df.columns = [
    'Well', 'Formation', 'Depth_m', 'Depth_ft', 'Porosity',
    'GrainDensity', 'BulkDensityDry', 'BulkDensitySat',
    'VpDry', 'VsDry', 'VpSat', 'VsSat',
    'CarbonatePct', 'QuartzPct', 'ClayPct', 'Texture'
]

# Drop rows with missing values in measurement columns
data_df.dropna(subset=data_df.columns[4:], inplace=True)
data_df.reset_index(drop=True, inplace=True)

# Drop rows where all mineral contents are zero
invalid_minerals = (data_df['CarbonatePct'] + data_df['QuartzPct'] + data_df['ClayPct']) == 0
data_df.drop(index=data_df[invalid_minerals].index, inplace=True)
data_df.reset_index(drop=True, inplace=True)

# Sort by depth (in feet)
data_df.sort_values(by='Depth_ft', ascending=True, inplace=True)
data_df.reset_index(drop=True, inplace=True)

# Create a row with units
units_row = pd.DataFrame({
    'Well': [''],
    'Formation': [''],
    'Depth_m': ['metre'],
    'Depth_ft': ['feet'],
    'Porosity': ['%'],
    'GrainDensity': ['g/cc'],
    'BulkDensityDry': ['g/cc'],
    'BulkDensitySat': ['g/cc'],
    'VpDry': ['km/s'],
    'VsDry': ['km/s'],
    'VpSat': ['km/s'],
    'VsSat': ['km/s'],
    'CarbonatePct': ['%'],
    'QuartzPct': ['%'],
    'ClayPct': ['%'],
    'Texture': ['']
})

# Prepend the units row to the cleaned data
cleaned_df = pd.concat([units_row, data_df], ignore_index=True)

# Ensure depth columns don't have any remaining NaNs (precaution)
cleaned_df['Depth_ft'].fillna(0, inplace=True)
cleaned_df['Depth_m'].fillna(0, inplace=True)

# Save cleaned data to Excel
cleaned_df.to_excel(output_file, index=False)