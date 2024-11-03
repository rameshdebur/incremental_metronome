import streamlit as st
import time
from sound_player import SoundPlayer

# Assuming the MetronomeInterface and SoundPlayer classes are already implemented
class MetronomeInterface:
    """Dummy implementation to simulate business logic"""
    def __init__(self):
        self.tasks = {
            'sit_to_stand': 3.0,
            'stand_to_walk': 3.0,
            'walk_to_turn': 3.0,
            'walk_back_to_chair': 3.0,
            'stand_to_sit': 3.0,
        }
        self.overall_time = sum(self.tasks.values())

    def set_task_time(self, task_key, new_time):
        self.tasks[task_key] = new_time
        self.overall_time = sum(self.tasks.values())

    def get_task_time(self, task_key):
        return self.tasks[task_key]

    def set_overall_time(self, new_time):
        ratio = new_time / self.overall_time
        for key in self.tasks:
            self.tasks[key] *= ratio
        self.overall_time = new_time

    def get_overall_time(self):
        return self.overall_time

    def get_bpm(self, task_key):
        task_time = self.get_task_time(task_key)
        return 60 / task_time if task_time != 0 else 0


# Streamlit GUI with business logic
st.title('Incremental Metronome - Streamlit Version')

# Initialize metronome interface
metronome = MetronomeInterface()
sound_player = SoundPlayer()

# Inputs for incremental time
st.header("Incremental Time Settings")
start_time = st.number_input("Start Time (s)", min_value=0.0, value=metronome.get_overall_time())
end_time = st.number_input("End Time (s)", min_value=0.0, value=0.0)
iterations = st.number_input("Iterations", min_value=1, value=5)
percentage = st.number_input("Increment/Decrement (%)", value=0)

# Input for individual task times
st.header("Task Times")
tasks = [
    ('Sit to Stand', 'sit_to_stand'),
    ('Stand to Walk', 'stand_to_walk'),
    ('Walk to Turn', 'walk_to_turn'),
    ('Walk Back to Chair', 'walk_back_to_chair'),
    ('Stand to Sit', 'stand_to_sit')
]
task_times = {}

for task_name, task_key in tasks:
    task_times[task_key] = st.number_input(f"{task_name} (s)", min_value=0.0, value=metronome.get_task_time(task_key))

# Update task times when the user changes them
for task_key in task_times:
    metronome.set_task_time(task_key, task_times[task_key])

# Start Metronome Button
if st.button('Start Metronome'):
    current_iteration = 0
    total_repeats = iterations
    current_time = start_time
    time_increment = (end_time - start_time) / (iterations - 1) if iterations > 1 else 0

    # Play each iteration
    for iteration in range(total_repeats):
        current_iteration += 1
        st.write(f"Iteration: {current_iteration}")

        # Update the overall time and adjust task times
        metronome.set_overall_time(current_time)
        st.write(f"Overall Time: {current_time:.2f} seconds")

        for task_name, task_key in tasks:
            task_time = metronome.get_task_time(task_key)
            st.write(f"{task_name}: {task_time:.2f} seconds")
            sound_player.play_task_sound(False)
            time.sleep(task_time)

        # Increment the overall time for the next iteration
        current_time += time_increment

    # End of metronome play
    sound_player.play_task_sound(True)
    st.write("Metronome completed.")

# Display the BPM for the overall time and each task
st.header("BPM (Beats Per Minute)")
overall_bpm = 60 / metronome.get_overall_time() if metronome.get_overall_time() != 0 else 0
st.write(f"Overall BPM: {overall_bpm:.2f}")

for task_name, task_key in tasks:
    bpm = metronome.get_bpm(task_key)
    st.write(f"{task_name} BPM: {bpm:.2f}")

