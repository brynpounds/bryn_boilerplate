# ./DNAC-CompMon-Data/CSW-9300-CORE.base2hq.com_run_config.txt

# Open the Cisco configuration file
with open('./DNAC-CompMon-Data/CSW-9300-CORE.base2hq.com_run_config.txt', 'r') as config_file:

    # Read all the lines in the file
    lines = config_file.readlines()

    # Ask the user for the string to search for
    search_string = input('Enter the string to search for: ')

    # Find all sections that contain the search string
    matching_sections = []
    current_section = []
    for line in lines:
        if search_string in line:
            current_section.append(line)
        elif current_section:
            matching_sections.append(current_section)
            current_section = []
    if current_section:
        matching_sections.append(current_section)

    # Print out each matching section
    for section in matching_sections:
        for line in section:
            print(line.strip())
