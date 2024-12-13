import pandas as pd
import json

# Load the JSON data
with open('DataEngineeringQ2.json', 'r') as f:
    data = json.load(f)

# Initialize an empty list to store each flattened record
flattened_data = []

# Iterate over each entry in the JSON array
for entry in data:
    # Extract patient details and consultation data (medicines)
    patient_details = entry['patientDetails']
    consultation_data = entry['consultationData']
    medicines = consultation_data['medicines']

    # Flatten the patient details
    patient_df = pd.json_normalize(patient_details)

    # Flatten medicines list inside consultation data
    medicines_df = pd.json_normalize(medicines)

    # Combine patient details and medicines (you can choose how to join)
    combined_df = pd.concat([patient_df, medicines_df], axis=1)

    # Append the combined data for this entry
    flattened_data.append(combined_df)

# Combine all the flattened entries into one DataFrame
final_df = pd.concat(flattened_data, ignore_index=True)

# Display the columns and first few rows to inspect the structure
print(final_df.columns)
print(final_df.head())

from datetime import datetime

# Convert birthDate to age, adjusting the format to handle the timestamp
final_df['age'] = final_df['birthDate'].apply(
    lambda x: (datetime.now() - datetime.strptime(str(x), '%Y-%m-%dT%H:%M:%S.%fZ')).days // 365 if pd.notnull(x) else None
)
print(final_df)
# Count the number of adults (ages 20 to 59)
adult_count = final_df[(final_df['age'] >= 20) & (final_df['age'] <= 59)].shape[0]

print(adult_count)

# Calculate the average number of medicines prescribed per patient
average_medicines = final_df['medicineName'].notna().groupby(final_df.index).sum().mean()
print(round(average_medicines, 2))
# Find the 3rd most frequently prescribed medicine
medicine_counts = final_df['medicineName'].value_counts()
third_most_frequent_medicine = medicine_counts.index[2] if len(medicine_counts) >= 3 else None
print(third_most_frequent_medicine)
# Calculate the percentage of missing values for specified columns
missing_percentage = final_df[['firstName', 'lastName', 'birthDate']].isnull().mean() * 100
print(f"{round(missing_percentage['firstName'], 2)}, {round(missing_percentage['lastName'], 2)}, {round(missing_percentage['birthDate'], 2)}")
# Impute missing gender values with the mode (most frequent value)
mode_gender = final_df['gender'].mode()[0]
final_df['gender'].fillna(mode_gender, inplace=True)

# Calculate the percentage of females
female_percentage = (final_df['gender'] == 'Female').mean() * 100
print(round(female_percentage, 2))
# Calculate the percentage distribution of active vs inactive medicines
active_percentage = (final_df['isActive'] == True).mean() * 100
inactive_percentage = 100 - active_percentage
print(f"{round(active_percentage, 2)}, {round(inactive_percentage, 2)}")