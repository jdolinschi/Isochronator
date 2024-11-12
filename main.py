import tkinter as tk
from tkinter import ttk
import numpy as np
import pyaudio
import threading
import time


class IsochronicToneGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Isochronic Tone Generator")
        self.geometry("350x450")  # Adjust size to accommodate new layout
        # Set minimum size of window
        self.minsize(350, 450)
        self.maxsize(350, 450)
        self.running = False
        self.paused = False
        self.stream = None
        self.lock = threading.Lock()

        # Audio stream variables
        self.sample_rate = tk.IntVar(value=48000)
        self.volume = tk.DoubleVar(value=0.5)
        self.buffer_size = tk.IntVar(value=4096)
        self.phase = 0
        self.pulse_phase = 0

        # Initialize variables for random changes
        self.last_change_time = 0
        self.change_amount = 0

        self.vary_randomly = tk.BooleanVar(value=True)
        self.vary_interval_start = tk.DoubleVar(value=30)
        self.vary_interval_end = tk.DoubleVar(value=60)
        self.vary_amount = tk.DoubleVar(value=1.0)

        self.change_interval = np.random.uniform(self.vary_interval_start.get(), self.vary_interval_end.get())

        # Define Variables with tracing
        self.frequency = tk.DoubleVar(value=220)
        self.start_pulse_freq = tk.DoubleVar(value=15)
        self.final_pulse_freq = tk.DoubleVar(value=40)
        self.ramp_time = tk.DoubleVar(value=180)
        self.current_pulse_freq = self.start_pulse_freq.get()
        self.initial_pulse_freq = self.start_pulse_freq.get()
        self.target_pulse_freq = self.final_pulse_freq.get()
        self.transition_start_time = 0
        self.transition_duration = 3
        self.use_ramp = tk.BooleanVar(value=True)

        self.init_ui()

    def init_ui(self):
        # Frames for presets, inputs, controls, and buttons
        presets_frame = tk.Frame(self)
        inputs_frame = tk.Frame(self)
        controls_frame = tk.Frame(self)
        buttons_frame = tk.Frame(self)
        status_frame = tk.Frame(self)

        presets_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        inputs_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ns")
        controls_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ns")
        buttons_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        status_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Presets Dropdown
        # Presets Dropdown
        self.presets = {
            "Custom": {
                "description": "",
                "start_pulse_freq": 15,
                "final_pulse_freq": 40
            },
            "Delta waves (0.5 to 4 Hz)": {
                "description": "Associated with deep sleep, relaxation, and healing",
                "start_pulse_freq": 0.25,
                "final_pulse_freq": 2.25
            },
            "Theta waves (4 to 8 Hz)": {
                "description": "Associated with deep relaxation, meditation, creativity, and emotional connection",
                "start_pulse_freq": 2,
                "final_pulse_freq": 6
            },
            "Low Alpha (8 to 10 Hz)": {
                "description": "Promotes a relaxed state of mind",
                "start_pulse_freq": 4,
                "final_pulse_freq": 9
            },
            "High Alpha (10 to 13 Hz)": {
                "description": "Promotes a more alert and focused state",
                "start_pulse_freq": 5,
                "final_pulse_freq": 11.5
            },
            "Low Beta (13 to 18 Hz)": {
                "description": "Promotes relaxed focus and improved attentiveness",
                "start_pulse_freq": 6.5,
                "final_pulse_freq": 15.5
            },
            "Mid Beta (18 to 24 Hz)": {
                "description": "Promotes increased alertness and logical thinking",
                "start_pulse_freq": 9,
                "final_pulse_freq": 21
            },
            "High Beta (24 to 30 Hz)": {
                "description": "May cause anxiety or restlessness",
                "start_pulse_freq": 12,
                "final_pulse_freq": 27
            },
            "Gamma waves (30 to 50 Hz)": {
                "description": "Associated with higher cognitive functions, such as perception and consciousness",
                "start_pulse_freq": 15,
                "final_pulse_freq": 40
            }
        }

        self.selected_preset = tk.StringVar(value="Custom")
        self.preset_dropdown = ttk.Combobox(presets_frame, textvariable=self.selected_preset,
                                            values=list(self.presets.keys()), state="readonly", width=30)
        self.preset_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.preset_dropdown.bind("<<ComboboxSelected>>", self.update_preset)

        self.preset_info = tk.Text(presets_frame, height=3, width=40, wrap=tk.WORD, state="disabled")
        self.preset_info.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.update_preset_info()

        # Input Fields
        tk.Label(inputs_frame, text="Tone Frequency (Hz):").grid(row=0, column=0, sticky="w")
        self.frequency_entry = tk.Entry(inputs_frame, textvariable=self.frequency)
        self.frequency_entry.grid(row=1, column=0, sticky="w")

        tk.Label(inputs_frame, text="Start Pulse Frequency (Hz):").grid(row=2, column=0, sticky="w")
        self.start_pulse_freq_entry = tk.Entry(inputs_frame, textvariable=self.start_pulse_freq)
        self.start_pulse_freq_entry.grid(row=3, column=0, sticky="w")

        tk.Label(inputs_frame, text="Final Pulse Frequency (Hz):").grid(row=4, column=0, sticky="w")
        self.final_pulse_freq_entry = tk.Entry(inputs_frame, textvariable=self.final_pulse_freq)
        self.final_pulse_freq_entry.grid(row=5, column=0, sticky="w")

        tk.Label(inputs_frame, text="Ramp Time (s):").grid(row=6, column=0, sticky="w")
        self.ramp_time_entry = tk.Entry(inputs_frame, textvariable=self.ramp_time)
        self.ramp_time_entry.grid(row=7, column=0, sticky="w")

        # Control Fields
        tk.Label(controls_frame, text="Volume:").grid(row=0, column=0, sticky="w")
        self.volume_slider = ttk.Scale(controls_frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=self.volume)
        self.volume_slider.grid(row=1, column=0, sticky="ew")

        tk.Label(controls_frame, text="Sample Rate:").grid(row=2, column=0, sticky="w")
        common_sample_rates = [8000, 16000, 22050, 44100, 48000, 96000, 192000]
        self.sample_rate_combobox = ttk.Combobox(controls_frame, textvariable=self.sample_rate,
                                                 values=common_sample_rates, state="readonly", width=10)
        self.sample_rate_combobox.grid(row=3, column=0, sticky="ew")

        tk.Label(controls_frame, text="Buffer Size:").grid(row=4, column=0, sticky="w")
        common_buffer_sizes = [1024, 2048, 4096, 8192, 16384, 32768]
        self.buffer_size_combobox = ttk.Combobox(controls_frame, textvariable=self.buffer_size,
                                                 values=common_buffer_sizes, state="readonly", width=10)
        self.buffer_size_combobox.grid(row=5, column=0, sticky="w")

        # Use Ramp Checkbox
        self.use_ramp_checkbox = tk.Checkbutton(controls_frame, text="Use Ramp", variable=self.use_ramp,
                                                command=self.update_ramp_widgets)
        self.use_ramp_checkbox.grid(row=6, column=0, sticky="w")

        # 'Vary Randomly' Checkbox
        self.vary_randomly_checkbox = tk.Checkbutton(controls_frame, text="Vary Randomly", variable=self.vary_randomly,
                                                     command=self.update_vary_widgets)
        self.vary_randomly_checkbox.grid(row=7, column=0, sticky="w")

        # New Vary Interval Frame
        vary_interval_frame = tk.Frame(inputs_frame)
        vary_interval_frame.grid(row=9, column=0, sticky="ew")

        # Inside this frame, create two entries and a label
        self.vary_interval_start_entry = tk.Entry(vary_interval_frame, textvariable=self.vary_interval_start, width=5)
        self.vary_interval_end_entry = tk.Entry(vary_interval_frame, textvariable=self.vary_interval_end, width=5)
        to_label = tk.Label(vary_interval_frame, text="to")

        # Position the entries and label within the frame
        self.vary_interval_start_entry.grid(row=0, column=0, sticky="ew", padx=(0, 0))
        to_label.grid(row=0, column=1)
        self.vary_interval_end_entry.grid(row=0, column=2, sticky="ew", padx=(0, 0))

        # Ensure the frame columns distribute space evenly
        vary_interval_frame.columnconfigure(0, weight=1)
        vary_interval_frame.columnconfigure(1, weight=0)  # Minimize the space for 'to' label
        vary_interval_frame.columnconfigure(2, weight=1)

        # Relabel the Vary Interval to match the new layout
        tk.Label(inputs_frame, text="Vary Interval (s):").grid(row=8, column=0, sticky="w")

        # Vary Amount Entry
        tk.Label(inputs_frame, text="Vary Amount (±Hz):").grid(row=10, column=0, sticky="w")
        self.vary_amount_entry = tk.Entry(inputs_frame, textvariable=self.vary_amount)
        self.vary_amount_entry.grid(row=11, column=0, sticky="w")

        # Buttons
        self.play_button = ttk.Button(buttons_frame, text="▶", command=self.start_tone_generation)
        self.pause_button = ttk.Button(buttons_frame, text="⏸", command=self.pause_tone_generation)
        self.stop_button = ttk.Button(buttons_frame, text="⏹", command=self.stop_tone_generation)

        self.play_button.grid(row=0, column=0, padx=5)
        self.pause_button.grid(row=0, column=1, padx=5)
        self.stop_button.grid(row=0, column=2, padx=5)

        # Status Display
        self.current_freq_label = tk.Label(status_frame, text="Current Pulse Frequency: 0.00 Hz")
        self.current_freq_label.grid(row=0, column=0, sticky="ew")

    def update_vary_widgets(self):
        if self.vary_randomly.get():
            self.vary_interval_start_entry.config(state="normal")
            self.vary_interval_end_entry.config(state="normal")
            self.vary_amount_entry.config(state="normal")
        else:
            self.vary_interval_start_entry.config(state="disabled")
            self.vary_interval_end_entry.config(state="disabled")
            self.vary_amount_entry.config(state="disabled")

    def update_preset(self, event=None):
        preset = self.presets[self.selected_preset.get()]
        self.start_pulse_freq.set(preset["start_pulse_freq"])
        self.final_pulse_freq.set(preset["final_pulse_freq"])
        self.ramp_time.set(180)
        self.update_preset_info()

    def update_preset_info(self, event=None):
        self.preset_info.config(state="normal")
        self.preset_info.delete("1.0", tk.END)
        self.preset_info.insert(tk.END, self.presets[self.selected_preset.get()]["description"])
        self.preset_info.config(state="disabled")

    def start_tone_generation(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.change_interval = np.random.uniform(self.vary_interval_start.get(),
                                                     self.vary_interval_end.get())
            self.last_change_time = 0
            self.current_pulse_freq = self.start_pulse_freq.get()
            self.target_pulse_freq = self.final_pulse_freq.get()
            threading.Thread(target=self.generate_tone, daemon=True).start()
            self.disable_entries()
        elif self.paused:
            self.paused = False
            self.start_time += time.time() - self.pause_time
            with self.lock:
                self.stream.start_stream()

    def pause_tone_generation(self):
        if self.running and not self.paused:
            self.paused = True
            self.pause_time = time.time()
            with self.lock:
                self.stream.stop_stream()

    def stop_tone_generation(self):
        self.running = False
        self.paused = False
        with self.lock:
            if self.stream is not None:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
        self.enable_entries()

    def generate_tone(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=self.sample_rate.get(),
                             output=True,
                             frames_per_buffer=self.buffer_size.get(),
                             stream_callback=self.audio_callback)
        self.start_time = time.time()
        with self.lock:
            self.stream.start_stream()

        while self.running:
            if not self.paused:
                time.sleep(0.1)
                self.update_current_freq()

        with self.lock:
            if self.stream is not None:
                self.stream.stop_stream()
                self.stream.close()
                p.terminate()

    def audio_callback(self, in_data, frame_count, time_info, status):
        with self.lock:
            if not self.paused:
                current_time = time.time() - self.start_time

                if self.use_ramp.get() and current_time <= self.ramp_time.get():
                    self.current_pulse_freq = self.start_pulse_freq.get() + (
                            self.final_pulse_freq.get() - self.start_pulse_freq.get()) * (
                                                      current_time / self.ramp_time.get())
                else:
                    if self.vary_randomly.get() and current_time - self.last_change_time >= self.change_interval:
                        self.target_pulse_freq = self.final_pulse_freq.get() + np.random.uniform(-self.vary_amount.get(),
                                                                                                  self.vary_amount.get())
                        self.transition_start_time = current_time
                        self.change_interval = np.random.uniform(self.vary_interval_start.get(),
                                                                 self.vary_interval_end.get())
                        self.last_change_time = current_time

                    # Calculate the transition progress if in transition
                    if current_time - self.transition_start_time < self.transition_duration:  # NEW
                        progress = (current_time - self.transition_start_time) / self.transition_duration  # NEW
                        progress = max(0, min(1, progress))  # Clamp progress to [0, 1]  # NEW
                        sigmoid = lambda x: 1 / (1 + np.exp(-x))  # NEW
                        transition_factor = sigmoid(
                            (progress - 0.5) * 10)  # Adjust the 10 for sharper or smoother transitions  # NEW
                        self.current_pulse_freq = (
                                                              1 - transition_factor) * self.current_pulse_freq + transition_factor * self.target_pulse_freq  # NEW
                    else:  # If not in transition, use the target frequency directly
                        self.current_pulse_freq = self.target_pulse_freq  # NEW

                t = np.arange(frame_count) / self.sample_rate.get()
                tone = np.sin(2 * np.pi * self.frequency.get() * t + self.phase)
                pulse = (np.sin(2 * np.pi * self.current_pulse_freq * t + self.pulse_phase) + 1) / 2
                self.phase += 2 * np.pi * self.frequency.get() * frame_count / self.sample_rate.get()
                self.pulse_phase += 2 * np.pi * self.current_pulse_freq * frame_count / self.sample_rate.get()

                self.phase %= 2 * np.pi
                self.pulse_phase %= 2 * np.pi
                audio_data = (tone * pulse * self.volume.get()).astype(np.float32)
            else:
                audio_data = np.zeros(frame_count, dtype=np.float32)

        return (audio_data.tobytes(), pyaudio.paContinue)

    def update_current_freq(self):
        self.current_freq_label.after(50, lambda: self.current_freq_label.config(
            text=f"Current Pulse Frequency: {self.current_pulse_freq:.2f} Hz"))

    def disable_entries(self):
        self.frequency_entry.config(state="disabled")
        self.start_pulse_freq_entry.config(state="disabled")
        self.final_pulse_freq_entry.config(state="disabled")
        self.ramp_time_entry.config(state="disabled")
        self.sample_rate_combobox.config(state="disabled")
        self.buffer_size_combobox.config(state="disabled")
        self.use_ramp_checkbox.config(state="disabled")
        self.preset_dropdown.config(state="disabled")
        self.vary_amount_entry.config(state="disabled")
        self.vary_interval_start_entry.config(state="disabled")
        self.vary_interval_end_entry.config(state="disabled")
        self.vary_randomly_checkbox.config(state="disabled")

    def enable_entries(self):
        self.frequency_entry.config(state="normal")
        self.start_pulse_freq_entry.config(state="normal")
        self.final_pulse_freq_entry.config(state="normal")
        self.ramp_time_entry.config(state="normal")
        self.sample_rate_combobox.config(state="normal")
        self.buffer_size_combobox.config(state="normal")
        self.use_ramp_checkbox.config(state="normal")
        self.preset_dropdown.config(state="readonly")
        self.vary_randomly_checkbox.config(state="normal")
        self.update_ramp_widgets()
        self.update_vary_widgets()

    def update_ramp_widgets(self):
        if self.use_ramp.get():
            self.start_pulse_freq_entry.config(state="normal")
            self.ramp_time_entry.config(state="normal")
        else:
            self.start_pulse_freq_entry.config(state="disabled")
            self.ramp_time_entry.config(state="disabled")


if __name__ == "__main__":
    app = IsochronicToneGeneratorApp()
    app.mainloop()
