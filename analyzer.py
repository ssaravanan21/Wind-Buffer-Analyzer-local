import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import io
import plotly.graph_objs as go
import plotly.offline as pyo

def main():
    root = tk.Tk()
    root.title("Buffer File Analyzer")

    df = None
    error_label = None

    custom_column_names = {
            'Column1': 'Timestamp',  
            'Column2': 'Converter_UL1',
            'Column3': 'Converter_UL2',
            'Column4': 'Converter_UL3',
            'Column5': 'Converter_I1',
            'Column6': 'Converter_I2',
            'Column7': 'Converter_I3',
            'Column8': 'Converter_rectifier_U',
            'Column9_Derivative': 'Derivative of grid_frequency',  # New column name
            'Column9': 'Converter_grid_frequency',
            'Column10': 'Converter_active_power',
            'Column11': 'Converter_reactive_power',  
            'Column12': 'Converter_U_DC_positive',
            'Column13': 'Converter_U_DC_negative',
            'Column14': 'Converter_I_DC',
            'Column15': 'Converter_chopper_I',
            'Column16': 'Converter_DC_current_setpoint',
            'Column17': 'Converter_reactive_power_setpoint',
            'Column18': 'Acceleration_nacelle_x',
            'Column19': 'Acceleration_nacelle_y',
            'Column20': 'Acceleration_nacelle_effective_value',
            'Column21': 'Generator_speed_momentary',  
            'Column22': 'Overspeed_modul_generator_speed_1',
            'Column23': 'Overspeed_modul_generator_speed_2',
            'Column24': 'Yaw_position',
            'Column25': 'Wind_speed',
            'Column26': 'Pitch_capacitor_voltage_hi_1',
            'Column27': 'Pitch_capacitor_voltage_hi_2',
            'Column28': 'Pitch_capacitor_voltage_hi_3',
            'Column29': 'Pitch_capacitor_voltage_lo_1',
            'Column30': 'Pitch_capacitor_voltage_lo_2',
            'Column31': 'Pitch_capacitor_voltage_lo_3',  
            'Column32': 'Pitch_position_blade_1',
            'Column33': 'Pitch_position_blade_2',
            'Column34': 'Pitch_position_blade_3',
            'Column35': 'Pitch_error_code_1_1',
            'Column36': 'Pitch_error_code_1_2',
            'Column37': 'Pitch_error_code_2_1',
            'Column38': 'Pitch_error_code_2_2',
            'Column39': 'Pitch_error_code_3_1',
            'Column40': 'Pitch_error_code_3_2',
            'Column41': 'Pitch_supply_24V_DC_1',  
            'Column42': 'Pitch_supply_24V_DC_2',
            'Column43': 'Pitch_supply_24V_DC_3',
            'Column44': 'Pitch_rate_demand_1',
            'Column45': 'Pitch_rate_demand_2',
            'Column46': 'Pitch_rate_demand_3',
            'Column47': 'Gh_torque_demand',
            'Column48': 'Converter_state_err',
            'Column49': 'Pitch_error_code_1_3',
            'Column50': 'Pitch_error_code_2_3',
            'Column51': 'Pitch_error_code_3_3',  
            'Column52': 'Rated_blade_pos'
           
        }

    def load_data():
        nonlocal df
        nonlocal error_label

        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("Text Files", "*.txt")])

        if file_path:
            if file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
                error_label.config(text=f"Data upload successfully")
                print("Load Data")
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    content_lines = content.split('\n')
                    data_start_line = 3  # Adjust this line number as needed
                
                    # Create a DataFrame from the data lines with semicolon delimiter
                    data_lines = content_lines[data_start_line:]
                    df = pd.read_csv(io.StringIO('\n'.join(data_lines)), delimiter=';')

                # Add an extra row with column names 
                    column_names = [f"Column{i}" for i in range(1, 53)]
                    df.columns = column_names
                    error_label.config(text=f"Data upload successfully")
                    print("Load Data text")

        if 'Column1' not in df.columns:
            error_label.config(text="Column 'Column1' does not exist in the DataFrame.")

        if 'Column9' in df.columns:
            df['Column9'] = pd.to_numeric(df['Column9'], errors='coerce')
            df['Column9_Derivative'] = df['Column9'].diff()
        else:
            error_label.config(text="Column 'Column9' does not exist in the DataFrame.")

    def plot_data():
        if df is not None:
            selected_column_1 = column_1_combobox.get()
            selected_key_1 = [key for key, value in custom_column_names.items() if value == selected_column_1]

            if selected_key_1:
                selected_key_1 = selected_key_1[0]
                y_axis_label_1 = custom_column_names.get(selected_key_1)

                trace = go.Scatter(x=df['Column1'], y=df[selected_key_1], mode='lines', name=y_axis_label_1)
                layout = go.Layout(
                    title="Data Plot",
                    xaxis=dict(title="Time", fixedrange=False),
                    yaxis=dict(title=y_axis_label_1, autorange='reversed')
                )
                fig = go.Figure(data=[trace], layout=layout)

                # Add zoom and pan capabilities to the x-axis
                fig.update_xaxes(rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ))
                fig.update_layout(dragmode="zoom")

                pyo.plot(fig, filename=f"{y_axis_label_1}_plot.html", auto_open=True)
            else:
                error_label.config(text=f"Selected column '{selected_column_1}' not found in custom_column_names.")
        else:
            error_label.config(text="No data to plot. Please load data first.")
    def compare_columns():
        if df is not None:
            selected_column_1 = column_1_combobox.get()
            selected_key_1 = [key for key, value in custom_column_names.items() if value == selected_column_1]

            selected_column_2 = column_2_combobox.get()
            selected_key_2 = [key for key, value in custom_column_names.items() if value == selected_column_2]

            if selected_key_1 and selected_key_2:
                selected_key_1 = selected_key_1[0]
                selected_key_2 = selected_key_2[0]

                y_axis_label_1 = custom_column_names.get(selected_key_1)
                y_axis_label_2 = custom_column_names.get(selected_key_2)

                trace1 = go.Scatter(x=df['Column1'], y=df[selected_key_1], mode='lines', name=y_axis_label_1)
                trace2 = go.Scatter(x=df['Column1'], y=df[selected_key_2], mode='lines', name=y_axis_label_2)
                layout = go.Layout(title="Comparison Plot", xaxis=dict(title="Time",tickmode='linear',  # Use linear spacing for ticks
                            dtick=120,), yaxis=dict(title="Values",tickmode='linear',  # Use linear spacing for ticks
                            dtick=120,autorange='reversed'))
                fig = go.Figure(data=[trace1, trace2], layout=layout)

                pyo.plot(fig, filename="comparison_plot.html", auto_open=True)
            else:
                error_label.config(text="Invalid column selection. Please select valid columns.")
        else:
            error_label.config(text="No data to compare. Please load data first.")


    ui_frame = ttk.LabelFrame(root, text="")
    ui_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    load_button = ttk.Button(ui_frame, text="Load Data", command=load_data)
    load_button.pack(pady=5)

    plot_button = ttk.Button(ui_frame, text="Plot Data", command=plot_data)
    plot_button.pack(pady=5)

    compare_button = ttk.Button(ui_frame, text="Compare Columns", command=compare_columns)
    compare_button.pack(pady=5)

    error_label = ttk.Label(ui_frame, text="")
    error_label.pack(pady=5)

    # Create a custom style with a larger font size
    combobox_style = ttk.Style()
    combobox_style.configure("Large.TCombobox", font=("Arial", 32))

    # Create the first Combobox
    column_1_combobox = ttk.Combobox(ui_frame, style="Large.TCombobox", values=list(custom_column_names.values()),width=45)
    column_1_combobox.set('Timestamp')
    column_1_combobox.pack()

    # Create the second Combobox
    column_2_combobox = ttk.Combobox(ui_frame, style="Large.TCombobox", values=list(custom_column_names.values()),width=45)
    column_2_combobox.set('Converter_UL1')
    column_2_combobox.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
