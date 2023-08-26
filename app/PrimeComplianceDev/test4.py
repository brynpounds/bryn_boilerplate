
# Open the Cisco configuration file
with open('./DNAC-CompMon-Data/CSW-9300-CORE.base2hq.com_run_config.txt', 'r') as config_file:

    # Read all the lines in the file
    lines = config_file.readlines()

    # Ask the user for the section of configuration to search for
    section = input('Enter the section of configuration to search for: ')

    # Find all the lines that contain the section of configuration
    matching_lines = []
    found_section = False
    for line in lines:
        if section in line:
            found_section = True
            matching_lines.append(line)
        elif found_section and not line.startswith(' '):
            break
        elif found_section:
            matching_lines.append(line)

    # Print out each matching line
    for line in matching_lines:
        print(line.strip())
