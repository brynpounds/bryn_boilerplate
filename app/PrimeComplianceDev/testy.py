import re

text = '''
interface GigabitEthernet1/0/1
 description Link - RTR-4331-BORDER - GigabitEthernet0/0/1
 no switchport
 ip address 10.0.1.5 255.255.255.254
 ip pim sparse-mode
 ip router isis 
 speed 1000
 duplex full
 service-policy output DNA-dscp#APIC_QOS_Q_OUT
!
interface GigabitEthernet1/0/10
 description PDU lan
 switchport access vlan 10
 switchport mode access
 switchport nonegotiate
 device-tracking attach-policy IPDT_POLICY
 ip flow monitor dnacmonitor input
 ip flow monitor dnacmonitor output
 speed 100
 duplex full
 et-analytics enable
 spanning-tree portfast
 service-policy input DNA-MARKING_IN
 service-policy output DNA-dscp#APIC_QOS_Q_OUT
 ip nbar protocol-discovery
!
interface GigabitEthernet1/0/11
 description PDU lan
 switchport access vlan 10
 switchport mode access
 switchport nonegotiate
 device-tracking attach-policy IPDT_POLICY
 ip flow monitor dnacmonitor input
 ip flow monitor dnacmonitor output
 speed 100
 duplex full
 et-analytics enable
 spanning-tree portfast
 service-policy input DNA-MARKING_IN
 service-policy output DNA-dscp#APIC_QOS_Q_OUT
 ip nbar protocol-discovery
!
interface GigabitEthernet1/0/12
 description PDU lan
 switchport access vlan 10
 switchport mode access
 switchport nonegotiate
 device-tracking attach-policy IPDT_POLICY
 ip flow monitor dnacmonitor input
 ip flow monitor dnacmonitor output
 speed 100
 duplex full
 et-analytics enable
 spanning-tree portfast
 service-policy input DNA-MARKING_IN
 service-policy output DNA-dscp#APIC_QOS_Q_OUT
 ip nbar protocol-discovery
!
'''

# Use regex to split the text into sections for each interface configuration.
sections = re.split(r'!\n', text)

# Create a list of interface configurations as strings.
interface_configs = []
for section_text in sections:
    if section_text.startswith('interface'):
        # Join the lines of the section together into a single string.
        interface_configs.append(section_text.strip() + '\n')

print(interface_configs[1])
