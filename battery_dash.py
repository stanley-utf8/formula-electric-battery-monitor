import pygame
from collections import defaultdict
import csv

pygame.init()

window = pygame.display.set_mode((900,500))
pygame.display.set_caption("Batteries Dash")
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

TOTAL_PAGES = 13
MAIN_PAGE = 0


title_font = pygame.font.Font(None, 36)
module_font = pygame.font.Font(None, 28)

# Dictionary of all text labels
LABELS = {
    'main_menu': "Batteries Dashboard:",
    'current': "Current:",
    'voltage': "Voltage:",
    'max_temp': "Max Temp:",
    'avg_temp': "Avg Temp:",
    'max_cell_voltage': "Max Cell Voltage:",
    'min_cell_voltage': "Min Cell Voltage:",
    'total_voltage': "Total Voltage:",
    'soc': "SOC:"
}

MODULES = {
    1: "Module 1",
    2: "Module 2",
    3: "Module 3",
    4: "Module 4",
    5: "Module 5",
    6: "Module 6",
    7: "Module 7",
    8: "Module 8",
    9: "Module 9",
    10: "Module 10",
    11: "Module 11",
    12: "Module 12",
}


voltages = 11
temps = 8
MODULE_LABELS = {
    'voltages': [f'Voltage {i}:' for i in range(1, voltages + 1)],
    'temps': [f'Temp {i}:' for i in range(1, temps + 1)],
    'soc': "SOC:",
    'max_voltage': "Max Voltage:",
    'min_voltage': "Min Voltage:",
    'max_temp': "Max Temp:",
    'total_voltage': "Total Voltage:",
    'avg_temp': "Avg Temp:",
    'state_of_charge': "State of Charge:"
}
# Pre-render all text surfaces
main_menu_text = {key: module_font.render(text, True, white) for key, text in LABELS.items()}
module_keys_text = {key: title_font.render(text, True, white) for key, text in MODULES.items()}
module_text = {}

for key, item in MODULE_LABELS.items():
    if isinstance(item, list):
        module_text[key] = [module_font.render(text, True, white) for text in item]
    else:
        module_text[key] = module_font.render(item, True, white)


def parse_module_limits(file_path):
    limits_dict = defaultdict(list)
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if row:  # Check if row is not empty
                    key = row[0].strip()
                    values = [float(val.strip()) for val in row[1:] if val.strip()] # Mapped to: 'Upper_Red_Limit,Upper_Orange_Limit,Lower_Red_Limit,Lower_Orange_Limit'
                    limits_dict[key].extend(values)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except csv.Error as e:
        print(f"Error parsing CSV file: {e}")
    return limits_dict

module_limits = parse_module_limits('./battery_limits.csv')

def parse_module_data(file_path):
    data_dict = defaultdict(float)
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if row:
                    key = row[0].strip()
                    values = float(row[1].strip())
                    data_dict[key] = values
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except csv.Error as e:
        print(f"Error parsing CSV file: {e}")
    return data_dict
            

def get_csv(csv_path):
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            return reader
    except FileNotFoundError:
        print(f"Error: {csv_path} not found")
    except csv.Error as e:
        print(f"Error parsing CSV file: {e}")

def render_main_page():
        try: 
            main_page_data = parse_module_data('./main_page.csv')
        except:
            main_page_data = defaultdict(float)

        text_rect = main_menu_text['main_menu'].get_rect(midtop=(window.get_width()/2, 20))
        window.blit(title_font.render("Batteries Dashboard:", True, white), text_rect)
        # Left column text positioning with consistent rectangles
        main_menu_items = [
            ('current', 'current', 'A'),
            ('avg_temp', 'avg_temp', '°C'),
            ('max_temp', 'max_temp', '°C'),
            ('max_cell_voltage', 'max_cell_voltage', 'V'),
            ('min_cell_voltage', 'min_cell_voltage', 'V'),
            ('total_voltage', 'total_voltage', 'V'),
            ('soc', 'soc', '%')
        ]

        for i, (label_key, data_key, unit) in enumerate(main_menu_items):
            text = main_menu_text[label_key]
            rect = text.get_rect(left=50, top=100 + i * 50)  # Consistent 50px spacing
            window.blit(text, rect)
             
            value = main_page_data.get(data_key, 0.0)  # Get value or default to 0.0

            if label_key == 'current':
                current_limits = module_limits.get('Current', 0.0)
                upper_red_limit, upper_orange_limit, lower_red_limit, lower_orange_limit = current_limits
                if value > upper_red_limit:
                    color = (255, 0, 0)
                elif value > upper_orange_limit:
                    color = (255, 165, 0)
                elif value < lower_red_limit:
                    color = (255, 0, 0)
                elif value < lower_orange_limit:
                    color = (255, 165, 0)
                else:
                    color = (0, 255, 0)
            elif label_key == 'total_voltage':
                total_voltage_limits = module_limits.get('Total_Voltage', 0.0)
                upper_red_limit, upper_orange_limit, lower_red_limit, lower_orange_limit = total_voltage_limits
                
                if value > upper_red_limit:
                    color = (255, 0, 0)
                elif value > upper_orange_limit:
                    color = (255, 165, 0)
                elif value < lower_red_limit:
                    color = (255, 0, 0)
                elif value < lower_orange_limit:
                    color = (255, 165, 0)
                else:
                    color = (255, 255, 255)    
            
            elif label_key == 'soc':
                soc_limits = module_limits.get('Module_SOC', 0.0)
                upper_red_limit, upper_orange_limit, lower_red_limit, lower_orange_limit = soc_limits
                
                if label_key == 'state_of_charge' :
                    if value > upper_red_limit:
                        color = (255, 0, 0)
                    elif value > upper_orange_limit:                         
                        color = (255, 165, 0)
                    elif value < lower_red_limit:                         
                        color = (255, 0, 0)
                    elif value < lower_orange_limit:
                        color = (255, 165, 0)
                    else:                                                              
                        color = (0, 255, 0)
            else:
                color = (255, 255, 255)

            value_surface = module_font.render(f"{value:.2f}{unit}", True, color)  
            value_rect = value_surface.get_rect(left=rect.right + 10, top=rect.top)
            window.blit(value_surface, value_rect)
                


def render_module(module_key):
    # Get data for current module
    try:
        module_data = parse_module_data(f'./module_{module_key}_data.csv')  # Assuming this is your data file format
    except:
        module_data = defaultdict(float)  # Default values if file not found

    module_title = module_keys_text[module_key].get_rect(midtop=(window.get_width()/2, 20))
    window.blit(module_keys_text[module_key], module_title)

    # Left column - Voltages
    voltages_text = module_text['voltages']
    for i in range(voltages):
        # Render label
        voltage_text = voltages_text[i]
        voltage_rect = voltage_text.get_rect(left=50, top=75 + i * 35)
        window.blit(voltage_text, voltage_rect)
        
        # Render value
        value = module_data.get(f'Cell_{i+1}_Voltage', 0.0)  # Get value or default to 0.0
        cell_voltage_limits = module_limits.get('Cell_Voltage', 0.0)
        upper_red_limit = cell_voltage_limits[0]
        upper_orange_limit = cell_voltage_limits[1]
        lower_red_limit = cell_voltage_limits[2]
        lower_orange_limit = cell_voltage_limits[3]
        # Color voltage values based on limits
        if value > upper_red_limit:  # Upper red limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 0, 0))  # Red
        elif value > upper_orange_limit:  # Upper orange limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 165, 0))  # Orange
        elif value < lower_red_limit:  # Lower red limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 0, 0))  # Red
        elif value < lower_orange_limit:  # Lower orange limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 165, 0))  # Orange
        else:  # Within normal range
            value_surface = module_font.render(f"{value:.2f}V", True, (0, 255, 0))  # Green
        value_rect = value_surface.get_rect(left=voltage_rect.right + 10, top=voltage_rect.top)
        window.blit(value_surface, value_rect)
    
    # Middle column - Temperatures
    temps_text = module_text['temps']
    cell_temp_limits = module_limits.get('Cell_Temp', 0.0)
    upper_red_limit = cell_temp_limits[0]
    upper_orange_limit = cell_temp_limits[1]
    lower_red_limit = cell_temp_limits[2]
    lower_orange_limit = cell_temp_limits[3]
    for i in range(8):
        # Render label
        temp_text = temps_text[i]
        temp_rect = temp_text.get_rect(midtop=(window.get_width()/2 - 50, 75 + i * 35))
        window.blit(temp_text, temp_rect)
        
        # Render value
        value = module_data.get(f'Temp_{i+1}', 0.0)
        if value > upper_red_limit:  # Upper red limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 0, 0))  # Red
        elif value > upper_orange_limit:  # Upper orange limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 165, 0))  # Orange
        elif value < lower_red_limit:  # Lower red limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 0, 0))  # Red
        elif value < lower_orange_limit:  # Lower orange limit
            value_surface = module_font.render(f"{value:.2f}V", True, (255, 165, 0))  # Orange
        else:  # Within normal range
            value_surface = module_font.render(f"{value:.2f}V", True, (0, 255, 0))  # Green

        value_rect = value_surface.get_rect(left=temp_rect.right + 10, top=temp_rect.top)
        window.blit(value_surface, value_rect)
    
    # Right column - Stats
    right_column_x = window.get_width() - 100
    right_stats = [
        ('state_of_charge', 'Module_SOC', '%'),
        ('max_voltage', 'Module_Max_Voltage', 'V'),
        ('min_voltage', 'Module_Min_Voltage', 'V'),
        ('max_temp', 'Module_Max_Temp', '°C'),
        ('avg_temp', 'Module_Avg_Temp', '°C')
    ]
    
    state_of_charge_threshold = module_limits.get('Module_SOC', 0.0)
    for i, (label_key, data_key, unit) in enumerate(right_stats):
        # Render label
        stat_text = module_text[label_key]
        stat_rect = stat_text.get_rect(right=right_column_x, top=75 + i * 35)
        window.blit(stat_text, stat_rect)
        
        # Render value
        value = module_data.get(data_key, 0.0)
        if label_key == 'state_of_charge' :
            if value > state_of_charge_threshold[0]:
                value_surface = module_font.render(f"{value:.1f}{unit}", True, (255, 0, 0))  # Red
            elif value > state_of_charge_threshold[1]:                         
                value_surface = module_font.render(f"{value:.1f}{unit}", True, (255, 165, 0))  # Orange
            elif value < state_of_charge_threshold[2]:                         
                value_surface = module_font.render(f"{value:.1f}{unit}", True, (255, 0, 0))  # Red
            elif value < state_of_charge_threshold[3]:
                value_surface = module_font.render(f"{value:.1f}{unit}", True, (255, 165, 0))  # Orange
            else:                                                              
                value_surface = module_font.render(f"{value:.1f}{unit}", True, (0, 255, 0))  # Green
        else:                                                                  
            value_surface = module_font.render(f"{value:.2f}{unit}", True, (255, 255, 255))  # White
        value_rect = value_surface.get_rect(left=stat_rect.right + 10, top=stat_rect.top)
        window.blit(value_surface, value_rect)

def main():
    running = True
    current_page = 0

    # Ask user if they want to run with simulator
    user_input = input("Run with battery data simulator? (y/n): ").lower()
    if user_input == 'y':
        try:
            # Import and start battery simulator in a separate thread
            import threading
            from battery_data_simulator import main as run_simulator
            simulator_thread = threading.Thread(target=run_simulator, daemon=True)
            simulator_thread.start()
            print("Battery simulator started...")
        except ImportError:
            print("Warning: Battery simulator not found. Running without simulation.")

    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_CTRL) or event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    current_page = (current_page + 1) % TOTAL_PAGES
                elif event.key == pygame.K_LEFT:
                    current_page = (current_page - 1) % TOTAL_PAGES

        window.fill(black)

        if current_page == 0:
            render_main_page()
        else: 
            render_module(current_page)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()