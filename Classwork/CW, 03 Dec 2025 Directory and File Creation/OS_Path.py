import os

# Check if 'logs' folder already exists
if os.path.exists('logs'):
    print("The 'logs' folder already exists. Exiting.")
    exit()

# Create the 'logs' folder
os.mkdir('logs')
print("Created 'logs' folder successfully.")

# Create the file path
file_path = os.path.join('logs', 'data.log')

# Create and write to the file
with open(file_path, 'w') as f:
    for i in range(5):
        f.write("Test Log\n")

print("Created 'data.log' and wrote 'Test Log' 5 times.")