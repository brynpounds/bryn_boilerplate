
import re
import sys

# Prompt the user for the interface name
interface_name = input("Enter the interface name (e.g. GigabitEthernet1/0/1): ")

# Read the configuration file
with open("./DNAC-CompMon-Data/CSW-9300-CORE.base2hq.com_run_config.txt", "r") as f:
    config_lines = f.readlines()
    #config_lines = [line.strip() for line in f.readlines()]

# Search for the interface section based on a regular expression pattern
pattern = r"interface {}\n".format(interface_name)
try:
    start_index = config_lines.index(pattern)
except ValueError:
    print("Error: interface {} not found in configuration file".format(interface_name))
    sys.exit(1)

end_index = len(config_lines)
for i in range(start_index+1, len(config_lines)):
    if re.match(r"interface \S+", config_lines[i]):
        end_index = i
        break

# Display the interface configuration
print("".join(config_lines[start_index:end_index]))

