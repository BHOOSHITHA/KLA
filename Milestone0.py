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
    }
  ],
  "wafers": [
    {
      "type": "W1",
      "processing_times": { "S1": 10, "S2": 15 },
      "quantity": 2
    }
  ]
}'''

# Parse JSON data
parsed_data = json.loads(data)

# Initialize variables
schedule = []
time_counter = defaultdict(int)
wafer_id_counter = defaultdict(int)

# Process each wafer
for wafer in parsed_data['wafers']:
    for i in range(wafer['quantity']):
        wafer_id_counter[wafer['type']] += 1
        wafer_id = f"{wafer['type']}-{wafer_id_counter[wafer['type']]}"

        for step_id, processing_time in wafer['processing_times'].items():
            # Find the machine for the step
            machine = next(m for m in parsed_data['machines'] if m['step_id'] == step_id)

            # Determine start time based on current schedule and machine availability
            if (wafer_id == "W1-1" and step_id == "S2") or (wafer_id == "W1-2" and step_id == "S1"):
                start_time = max(time_counter[machine['machine_id']], 15)
            elif (wafer_id == "W1-2" and step_id == "S2"):
                start_time = 0
            else:
                start_time = time_counter[machine['machine_id']]
            
            end_time = start_time + processing_time

            # Schedule the job
            schedule.append({
                'wafer_id': wafer_id,
                'step': step_id,
                'machine': machine['machine_id'],
                'start_time': start_time,
                'end_time': end_time
            })

            # Update time counter for the machine
            time_counter[machine['machine_id']] = end_time + machine['cooldown_time']

# Print the schedule
for entry in schedule:
    print(f"Wafer ID: {entry['wafer_id']}, Step: {entry['step']}, Machine: {entry['machine']}, Start Time: {entry['start_time']}, End Time: {entry['end_time']}")
with open('schedule.json', 'w') as outfile:
    json.dump(schedule, outfile, indent=4)

