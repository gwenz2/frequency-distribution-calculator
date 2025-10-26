import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math


class FrequencyDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Frequency Distribution Table Generator - Gwen Balajediong")
        
        # Start in fullscreen/maximized
        self.root.state('zoomed')  # Windows maximized
        
        # Data storage
        self.raw_data = []
        self.results = {}
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Frequency Distribution Calculator", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Data Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(input_frame, text="Enter data (comma or space separated):").grid(row=0, column=0, sticky=tk.W)
        
        self.data_entry = scrolledtext.ScrolledText(input_frame, width=70, height=5)
        self.data_entry.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Statistics Section
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_text = tk.Text(stats_frame, width=70, height=6, state='disabled')
        self.stats_text.grid(row=0, column=0)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Frequency Distribution Table", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(results_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_tree = ttk.Treeview(results_frame, yscrollcommand=tree_scroll.set, height=15)
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll.config(command=self.results_tree.yview)
        
        # Define columns
        columns = ('Class Interval', 'Class Boundaries', 'Class Mark', 'Frequency', 
                   '<cF', '>cF', 'rF (%)', '<rF (%)', '>rF (%)')
        self.results_tree['columns'] = columns
        
        self.results_tree.column('#0', width=0, stretch=tk.NO)
        for col in columns:
            self.results_tree.column(col, anchor=tk.CENTER, width=100)
            self.results_tree.heading(col, text=col, anchor=tk.CENTER)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
    def parse_input(self):
        """Parse input data from text area"""
        text = self.data_entry.get('1.0', tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter some data!")
            return False
        
        try:
            # Replace commas with spaces and split
            text = text.replace(',', ' ')
            self.raw_data = [float(x) for x in text.split() if x.strip()]
            
            if len(self.raw_data) == 0:
                messagebox.showerror("Error", "No valid numbers found!")
                return False
                
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid data! Please enter only numbers.")
            return False
    
    def calculate(self):
        """Main calculation function"""
        if not self.parse_input():
            return
        
        # Get basic statistics
        n = len(self.raw_data)
        highest = max(self.raw_data)
        lowest = min(self.raw_data)
        data_range = highest - lowest
        
        # Calculate number of classes (Sturges' formula)
        k = 1 + (3.3 * math.log10(n))
        k = math.ceil(k)
        
        # Calculate class width
        class_width = math.ceil(data_range / k)
        
        # Store statistics
        self.results = {
            'n': n,
            'highest': highest,
            'lowest': lowest,
            'range': data_range,
            'k': k,
            'class_width': class_width
        }
        
        # Display statistics
        self.display_statistics()
        
        # Process frequency distribution
        self.process_frequency_distribution()
        
    def display_statistics(self):
        """Display basic statistics"""
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', tk.END)
        
        stats = f"""Total raw data: {self.results['n']}
Highest Value: {self.results['highest']}
Lowest Value: {self.results['lowest']}
Range: {self.results['range']}
Number of Classes (K): {self.results['k']}
Class Width (C): {self.results['class_width']}"""
        
        self.stats_text.insert('1.0', stats)
        self.stats_text.config(state='disabled')
    
    def process_frequency_distribution(self):
        """Process and display frequency distribution table"""
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        class_width = self.results['class_width']
        lowest = self.results['lowest']
        highest = self.results['highest']
        
        classes = []
        lower_ci = lowest
        
        # Create classes
        while lower_ci < highest or (not classes):
            upper_ci = lower_ci + class_width - 1
            
            # Class boundaries
            lower_cb = lower_ci - 0.5
            upper_cb = upper_ci + 0.5
            
            # Class mark
            class_mark = (lower_cb + upper_cb) / 2
            
            # Calculate frequency
            frequency = sum(1 for x in self.raw_data if lower_ci <= x <= upper_ci)
            
            classes.append({
                'lower_ci': lower_ci,
                'upper_ci': upper_ci,
                'lower_cb': lower_cb,
                'upper_cb': upper_cb,
                'class_mark': class_mark,
                'frequency': frequency
            })
            
            lower_ci += class_width
            
            # Break if we've covered all data
            if upper_ci >= highest:
                break
        
        # Calculate cumulative frequencies
        total_freq = sum(c['frequency'] for c in classes)
        cum_freq = 0
        
        for cls in classes:
            cum_freq += cls['frequency']
            cls['cum_freq_less'] = cum_freq
        
        cum_freq_greater = total_freq
        for cls in classes:
            cls['cum_freq_greater'] = cum_freq_greater
            cum_freq_greater -= cls['frequency']
        
        # Calculate relative frequencies
        cum_rf = 0
        for cls in classes:
            cls['rel_freq'] = (cls['frequency'] / total_freq) * 100
            cum_rf += cls['rel_freq']
            cls['cum_rf_less'] = cum_rf
        
        cum_rf_greater = sum(c['rel_freq'] for c in classes)
        for cls in classes:
            cls['cum_rf_greater'] = cum_rf_greater
            cum_rf_greater -= cls['rel_freq']
        
        # Display in table
        for cls in classes:
            class_interval = f"{int(cls['lower_ci'])} - {int(cls['upper_ci'])}"
            class_boundaries = f"{cls['lower_cb']:.1f} - {cls['upper_cb']:.1f}"
            class_mark = f"{cls['class_mark']:.2f}"
            frequency = f"{int(cls['frequency'])}"
            cum_freq_less = f"{int(cls['cum_freq_less'])}"
            cum_freq_greater = f"{int(cls['cum_freq_greater'])}"
            rel_freq = f"{cls['rel_freq']:.2f}"
            cum_rf_less = f"{cls['cum_rf_less']:.2f}"
            cum_rf_greater = f"{cls['cum_rf_greater']:.2f}"
            
            self.results_tree.insert('', tk.END, values=(
                class_interval, class_boundaries, class_mark, frequency,
                cum_freq_less, cum_freq_greater, rel_freq, cum_rf_less, cum_rf_greater
            ))
    
    def clear_all(self):
        """Clear all inputs and results"""
        self.data_entry.delete('1.0', tk.END)
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.config(state='disabled')
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.raw_data = []
        self.results = {}


def main():
    root = tk.Tk()
    app = FrequencyDistributionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
