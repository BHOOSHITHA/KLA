#edit filename in line 4 and line 93 before running to test for all milestones
import json
from collections import defaultdict

with open(r'Milestone2b.json', 'r') as file:
    data = json.load(file)

schedule = []
wafer_id_counter = defaultdict(int)  # Number of wafers processed of each type
machine_available_times = defaultdict(int)
wafer_time_counter = defaultdict(int)  # Time each wafer will be ready for the next step
machine_parameters = {m['machine_id']: m['initial_parameters'].copy() for m in data['machines']}  # Current parameters of each machine
machine_wafers_processed = defaultdict(int)  # No of wafers processed by each machine before the parameters fluctuate
machine_reset_times = defaultdict(lambda: -1)  # Time at which machine parameters reset after cooldown

# Check if machine parameters are within limits
def check_fluctuations(machine, step):
    for param, value in machine_parameters[machine['machine_id']].items():
        if not (data['steps'][int(step[-1]) - 1]['parameters'][param][0] <= value <= data['steps'][int(step[-1]) - 1]['parameters'][param][1]):
            return False
    return True

# Update machine parameters with fluctuation
def update_machine_parameters(machine):
    for param in machine_parameters[machine['machine_id']]:
        new_value = machine_parameters[machine['machine_id']][param] + machine['fluctuation'][param]
        # Ensure the new value is within the specified range
        param_range = data['steps'][int(machine['step_id'][-1]) - 1]['parameters'][param]
        machine_parameters[machine['machine_id']][param] = min(max(new_value, param_range[0]), param_range[1])

# Reset machine parameters after cooldown
def reset_machine_parameters(machine):
    machine_parameters[machine['machine_id']] = data['machines'][int(machine['machine_id'][-1]) - 1]['initial_parameters'].copy()

# Process each wafer
for wafer in data['wafers']:
    for i in range(wafer['quantity']):
        wafer_id_counter[wafer['type']] += 1
        wafer_id = f"{wafer['type']}-{wafer_id_counter[wafer['type']]}"

        # Process each step in sequence
        for step_id, processing_time in wafer['processing_times'].items():
            # Handle dependencies
            step_info = next(step for step in data['steps'] if step['id'] == step_id)
            if step_info['dependency']:
                dependent_step = step_info['dependency']
                wafer_dependency_end_time = max((entry['end_time'] for entry in schedule if entry['wafer_id'] == wafer_id and entry['step'] == dependent_step), default=0)
            else:
                wafer_dependency_end_time = 0

            # Find suitable machines for the step and check for fluctuations
            suitable_machines = [m for m in data['machines'] if m['step_id'] == step_id and check_fluctuations(m, step_id)]
            if not suitable_machines:
                print(f"No suitable machines found for step {step_id} with required parameters.")
                continue

            machine = min(suitable_machines, key=lambda m: machine_available_times[m['machine_id']])

            # Check if the machine needs to be reset after cooldown
            if machine_reset_times[machine['machine_id']] != -1 and machine_available_times[machine['machine_id']] >= machine_reset_times[machine['machine_id']]:
                reset_machine_parameters(machine)
                machine_reset_times[machine['machine_id']] = -1

            # Determine start time based on machine availability, previous steps, and dependencies
            start_time = max(machine_available_times[machine['machine_id']], wafer_time_counter[wafer_id], wafer_dependency_end_time)
            end_time = start_time + processing_time

            # Schedule the job
            schedule.append({
                'wafer_id': wafer_id,
                'step': step_id,
                'machine': machine['machine_id'],
                'start_time': start_time,
                'end_time': end_time
            })

            
            machine_available_times[machine['machine_id']] = end_time
            wafer_time_counter[wafer_id] = end_time

            # Update machine parameters and processed wafer count
            machine_wafers_processed[machine['machine_id']] += 1
            if machine_wafers_processed[machine['machine_id']] >= machine['n']:
                update_machine_parameters(machine)
                machine_wafers_processed[machine['machine_id']] = 0
                # Schedule cooldown and reset time
                machine_available_times[machine['machine_id']] += machine['cooldown_time']
                machine_reset_times[machine['machine_id']] = machine_available_times[machine['machine_id']]

for entry in schedule:
    print(f"Wafer ID: {entry['wafer_id']}, Step: {entry['step']}, Machine: {entry['machine']}, Start Time: {entry['start_time']}, End Time: {entry['end_time']}")

# Save as JSON
with open('schedule2b.json', 'w') as outfile:
    json.dump(schedule, outfile, indent=4)
