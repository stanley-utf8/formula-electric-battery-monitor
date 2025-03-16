#!/usr/bin/env python3
"""
Battery Data Simulator

This script simulates battery data by updating CSV files with realistic values.
It's a simple alternative to CAN bus simulation for initial development.
"""

import csv
import random
import time
import os
import math
from typing import Dict, List, Any

def read_csv(filename: str) -> Dict[str, float]:
    """Read a CSV file with Name,Data format and return as dictionary"""
    data = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    try:
                        data[row[0]] = float(row[1])
                    except ValueError:
                        data[row[0]] = row[1]
    except FileNotFoundError:
        print(f"Warning: File {filename} not found. Creating new file.")
    return data

def write_csv(filename: str, data: Dict[str, Any]) -> None:
    """Write dictionary data to a CSV file with Name,Data format"""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Data"])
        for key, value in data.items():
            writer.writerow([key, value])

def update_main_page_data() -> None:
    """Update the main page data file with realistic values"""
    data = read_csv("main_page.csv")
    
    # If file didn't exist, initialize with default values
    if not data:
        data = {
            "current": 0.0,
            "voltage": 0.0,
            "max_temp": 0.0,
            "avg_temp": 0.0,
            "max_cell_voltage": 0.0,
            "min_cell_voltage": 0.0,
            "total_voltage": 0.0,
            "soc": 0.0
        }
    
    # Update values with realistic changes
    data["current"] += random.uniform(-5, 5)
    if abs(data["current"]) < 0.5:
        data["current"] = random.choice([-1, 1]) * random.uniform(0.5, 5)
    data["current"] = max(-150, min(150, data["current"]))
    
    # Voltage changes based on current
    voltage_change = -0.05 * (data["current"] / 100.0)
    data["total_voltage"] += voltage_change + random.uniform(-0.2, 0.2)
    data["total_voltage"] = max(300, min(400, data["total_voltage"]))
    data["voltage"] = data["total_voltage"]  # For display purposes
    
    # SOC changes based on current
    soc_change = -0.01 * (data["current"] / 10.0)
    data["soc"] += soc_change + random.uniform(-0.05, 0.05)
    data["soc"] = max(0, min(100, data["soc"]))
    
    write_csv("main_page.csv", data)
    return data

def update_module_data(module_num: int) -> None:
    """Update a module data file with realistic values"""
    filename = f"module_{module_num}_data.csv"
    data = read_csv(filename)
    
    # If file didn't exist, initialize with default values
    if not data:
        data = {
            # Cell voltages
            "Cell_1_Voltage": 3.0,
            "Cell_2_Voltage": 3.0,
            "Cell_3_Voltage": 3.0,
            "Cell_4_Voltage": 3.0,
            "Cell_5_Voltage": 3.0,
            "Cell_6_Voltage": 3.0,
            "Cell_7_Voltage": 3.0,
            "Cell_8_Voltage": 3.0,
            "Cell_9_Voltage": 3.0,
            "Cell_10_Voltage": 3.0,
            "Cell_11_Voltage": 3.0,
            # Temperatures
            "Temp_1": 60.0,
            "Temp_2": 60.0,
            "Temp_3": 60.0,
            "Temp_4": 60.0,
            "Temp_5": 60.0,
            "Temp_6": 60.0,
            "Temp_7": 60.0,
            "Temp_8": 60.0,
            # Module stats
            "Module_SOC": 0.0,
            "Module_Max_Voltage": 3.0,
            "Module_Min_Voltage": 3.0,
            "Module_Max_Temp": 60.0,
            "Module_Avg_Temp": 60.0,
            "Module_Status": 13
        }
    
    # Update cell voltages
    for i in range(1, 12):
        key = f"Cell_{i}_Voltage"
        data[key] += random.uniform(-0.002, 0.002)
        data[key] = max(3.0, min(4.2, data[key]))
    
    # Update temperatures
    for i in range(1, 9):
        key = f"Temp_{i}"
        data[key] += random.uniform(-0.1, 0.1)
        data[key] = max(20, min(60, data[key]))
    
    # Update summary data
    data["Module_Max_Voltage"] = max(data[f"Cell_{i}_Voltage"] for i in range(1, 12))
    data["Module_Min_Voltage"] = min(data[f"Cell_{i}_Voltage"] for i in range(1, 12))
    data["Module_Max_Temp"] = max(data[f"Temp_{i}"] for i in range(1, 9))
    data["Module_Avg_Temp"] = sum(data[f"Temp_{i}"] for i in range(1, 9)) / 8
    
    # Calculate SOC based on average cell voltage
    avg_voltage = sum(data[f"Cell_{i}_Voltage"] for i in range(1, 12)) / 11
    data["Module_SOC"] = min(100, max(0, (avg_voltage - 3.0) / 1.2 * 100))
    
    # Update status based on conditions
    status = 1  # Default: OK
    if data["Module_Max_Voltage"] > 4.15:
        status |= 2  # High voltage warning
    if data["Module_Min_Voltage"] < 3.2:
        status |= 4  # Low voltage warning
    if data["Module_Max_Temp"] > 45:
        status |= 8  # High temperature warning
    data["Module_Status"] = status
    
    write_csv(filename, data)

def main():
    """Main function to run the simulator"""
    print("Battery Data Simulator")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Update main page data
            main_data = update_main_page_data()
            
            # Update all module data
            for module_num in range(1, 13):
                update_module_data(module_num)
            
            # Print status
            print(f"Updated data: {time.strftime('%H:%M:%S')} - "
                  f"Voltage: {main_data['total_voltage']:.1f}V, "
                  f"Current: {main_data['current']:.1f}A, "
                  f"SOC: {main_data['soc']:.1f}%")
            
            # Wait before next update
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 