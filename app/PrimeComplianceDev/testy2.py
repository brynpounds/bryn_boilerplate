import re

def show_run_section_array(section_cfg):
    section_configs = []
    sections = ''.join(section_cfg)

    # Use regex to split the text into sections for each interface configuration.
    keywords  = ["line vty","class","event"]
    key = ""
    for keyword in keywords:
        if re.search(keyword, sections):
            key = keyword
            break
    
    if key in sections:
        section_configs = re.split(f'({key})', sections)
        print(section_configs)
        output_sections = []
        for i in range(0,(len(section_configs)-1)):
            if section_configs[i] == key:
                output_sections.append(section_configs[i] + section_configs[i+1])
        print(output_sections)
        section_configs = output_sections
    else:
        section_configs = re.split(r'!\n', sections)
    
    return section_configs

# Test the function with some example input
input_text = """line vty 0 4\n exec-timeout 0 0\n authorization exec CON-LAB\n logging synchronous\n login xxxxxx\n terminal-type mon\n length 0\n transport input ssh\n session-timeout 10\nline vty 5 15\n exec-timeout 0 0\n authorization exec CON-VTY\n logging synchronous\n login xxxxxx\n terminal-type mon\n length 0\n transport input ssh\n session-timeout 10\nline vty 16 31\n transport input ssh\n session-timeout 10\n access-class SSH_ACCESS in!"""

sections = show_run_section_array(input_text)
print(sections)
