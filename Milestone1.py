# import json
# from collections import defaultdict

# # JSON data
# data = '''{
#   "steps": [
#     {
#       "id": "S1",
#       "parameters": { "P1": [ 100, 200 ] },
#       "dependency": null
#     },
#     {
#       "id": "S2",
#       "parameters": { "P1": [ 100, 200 ] },
#       "dependency": null
#     }
#   ],
#   "machines": [
#     {
#       "machine_id": "M1",
#       "step_id": "S1",
#       "cooldown_time": 5,
#       "initial_parameters": { "P1": 100 },
#       "fluctuation": { "P1": 5 },
#       "n": 20
#     },
#     {
#       "machine_id": "M2",
#       "step_id": "S2",
#       "cooldown_time": 5,
#       "initial_parameters": { "P1": 100 },
#       "fluctuation": { "P1": 5 },
#       "n": 20
#     },
#     {
#       "machine_id": "M3",
#       "step_id": "S2",
#       "cooldown_time": 5,
#       "initial_parameters": { "P1": 100 },
#       "fluctuation": { "P1": 5 },
#       "n": 20
#     }
#   ],
#   "wafers": [
#     {
#       "type": "W1",
#       "processing_times": {
#         "S1": 10,
#         "S2": 15
#       },
#       "quantity": 3
#     }
#   ]
# }'''

# # Parse JSON data
# parsed_data = json.loads(data)

# # Initialize variables
# schedule = []
# time_counter = defaultdict(int)
# wafer_id_counter = defaultdict(int)
# machine_available_times = defaultdict(int)

# # Process each wafer
# for wafer in parsed_data['wafers']:
#     for i in range(wafer['quantity']):
#         wafer_id_counter[wafer['type']] += 1
#         wafer_id = f"{wafer['type']}-{wafer_id_counter[wafer['type']]}"

#         for step_id, processing_time in wafer['processing_times'].items():
#             # Find the machine for the step
#             suitable_machines = [m for m in parsed_data['machines'] if m['step_id'] == step_id]
#             machine = min(suitable_machines, key=lambda m: machine_available_times[m['machine_id']])

#             start_time = machine_available_times[machine['machine_id']]
#             end_time = start_time + processing_time

#             # Schedule the job
#             schedule.append({
#                 'wafer_id': wafer_id,
#                 'step': step_id,
#                 'machine': machine['machine_id'],
#                 'start_time': start_time,
#                 'end_time': end_time
#             })

#             # Update machine availability time
#             machine_available_times[machine['machine_id']] = end_time + machine['cooldown_time']

# # Print the schedule
# for entry in schedule:
#     print(f"Wafer ID: {entry['wafer_id']}, Step: {entry['step']}, Machine: {entry['machine']}, Start Time: {entry['start_time']}, End Time: {entry['end_time']}")

# with open('schedule1.json', 'w') as outfile:
#     json.dump(schedule, outfile, indent=4)

import json
from collections import defaultdict

# JSON data
data = '''{
  "steps": [
    {
      "id": "S1",
      "parameters": { "P1": [ 100, 200 ] },
      "dependency": null
    },
    {
      "id": "S2",
      "parameters": { "P1": [ 100, 200 ] },
      "dependency": null
    }
  ],
  "machines": [
    {
      "machine_id": "M1",
      "step_id": "S1",
      "cooldown_time": 5,
      "initial_parameters": { "P1": 100 },
      "fluctuation": { "P1": 5 },
      "n": 20
    },
    {
      "machine_id": "M2",
      "step_id": "S2",
      "cooldown_time": 5,
      "initial_parameters": { "P1": 100 },
      "fluctuation": { "P1": 5 },
      "n": 20
    },
    {
      "machine_id": "M3",
      "step_id": "S2",
      "cooldown_time": 5,
      "initial_parameters": { "P1": 100 },
      "fluctuation": { "P1": 5 },
      "n": 20
    }
  ],
  "wafers": [
    {
      "type": "W1",
      "processing_times": {
        "S1": 10,
        "S2": 15
      },
      "quantity": 3
    }
  ]
}'''

# Parse JSON data
parsed_data = json.loads(data)

# Initialize variables
schedule = []
time_counter = defaultdict(int)
wafer_time_counter = defaultdict(int)
wafer_id_counter = defaultdict(int)
machine_available_times = defaultdict(int)

# Process each wafer
for wafer in parsed_data['wafers']:
    for i in range(wafer['quantity']):
        wafer_id_counter[wafer['type']] += 1
        wafer_id = f"{wafer['type']}-{wafer_id_counter[wafer['type']]}"

        # Process each step in sequence
        for step_id, processing_time in wafer['processing_times'].items():
            # Find the machine for the step
            suitable_machines = [m for m in parsed_data['machines'] if m['step_id'] == step_id]
            machine = min(suitable_machines, key=lambda m: machine_available_times[m['machine_id']])

            start_time = max(machine_available_times[machine['machine_id']], wafer_time_counter[wafer_id])
            end_time = start_time + processing_time

            # Schedule the job
            schedule.append({
                'wafer_id': wafer_id,
                'step': step_id,
                'machine': machine['machine_id'],
                'start_time': start_time,
                'end_time': end_time
            })

            # Update machine and wafer times
            machine_available_times[machine['machine_id']] = end_time + machine['cooldown_time']
            wafer_time_counter[wafer_id] = end_time

# Print the schedule
for entry in schedule:
    print(f"Wafer ID: {entry['wafer_id']}, Step: {entry['step']}, Machine: {entry['machine']}, Start Time: {entry['start_time']}, End Time: {entry['end_time']}")

# Save the schedule as a JSON file
with open('schedule1.json', 'w') as outfile:
    json.dump(schedule, outfile, indent=4)
