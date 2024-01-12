import tkinter as tk
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading

stop_recording_event = threading.Event()

def start_recording():
    global recorded_data
    recorded_data = []
    print("Start recording...")
    try:
        def callback(indata, frames, time, status):
            if status:
                print(f"Error during recording: {status}")
                return
            recorded_data.append(indata.copy())

        with sd.InputStream(callback=callback):
            stop_recording_event.wait()  # Wait until the stop event is set

    except Exception as e:
        print(f"Error during recording: {e}")

    print("Recording stopped.")
    save_recording()  # Save the recorded data

def save_recording():
    global recorded_data
    try:
        if recorded_data:  # Check if the recorded_data list is not empty
            combined_data = np.concatenate(recorded_data, axis=0)
            write("demo.wav", 44100, combined_data)
            print("Recording saved.")
        else:
            print("No recorded data to save.")
    except Exception as e:
        print(f"Error during saving recording: {e}")

def start_recording_thread():
    global stop_recording_event
    stop_recording_event.clear()  # Reset the event before starting
    thread = threading.Thread(target=start_recording)
    thread.start()

def stop_recording():
    global stop_recording_event
    stop_recording_event.set()  # Set the event to signal stopping

root = tk.Tk()

start_button = tk.Button(root, text="Start Manohar", command=start_recording_thread, bg="green", padx=10, pady=10)
stop_button = tk.Button(root, text="Stop Manohar", command=stop_recording, bg="aqua", padx=10, pady=10)

start_button.pack(pady=5)  # Increased vertical padding
stop_button.pack(pady=3)   # Increased vertical padding

root.mainloop()
