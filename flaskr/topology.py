# Some topology configuration information and commands

# hostnames
RTA = 'RTA'
RTB = 'RTB'
RTC = 'RTC'
PC2 = 'pc2'
PC1 = 'pc1'

valid_hosts = {RTA, RTB, RTC}

rta_profile = {
    'hostname': RTA,
    'ip': '172.16.0.2',
    'password': '123456'
}

rtb_profile = {
    'hostname': RTB,
    'ip': '172.16.0.3',
    'password': '123456'
}

rtc_profile = {
    'hostname': RTC,
    'ip': '172.16.0.4',
    'password': '123456'
}

pc1_profile = {
    'hostname': PC1,
    'ip': '192.168.3.2',
    'password': '123456'
}

pc2_profile = {
    'hostname': PC2,
    'ip': '10.0.0.11',
    'password': '123456'
}

router_profiles = [rta_profile, rtb_profile, rtc_profile]

# commands to be executed on RTA
_commands_rta = [
    'configure terminal',
    'interface f0/0',
    'ip address 192.168.3.1 255.255.255.0',
    'no shutdown',
    'interface s0/0/0',
    'ip address 192.168.1.1 255.255.255.252',
    'no shutdown',
    'exit',
    'ip route 192.168.1.32 255.255.255.224 192.168.1.2',
    'exit',
    'exit'
]

# commands to be executed on RTB
_commands_rtb = [
    "configure terminal",
    "interface f0/0",
    "ip address 10.0.0.1 255.0.0.0",
    "no shutdown",
    "interface s0/0/0",
    "ip address 192.168.1.2 255.255.255.252",
    "no shutdown",
    "clock rate 9600",
    'exit',
    'ip route 0.0.0.0 0.0.0.0 192.168.1.1',
    'ip nat inside source static 10.0.0.2 192.168.1.34',
    'ip nat inside source static 10.0.0.11 192.168.1.35',
    'interface f0/0',
    'ip nat inside',
    'interface s0/0/0',
    'ip nat outside',
    'exit',
    'exit',
    'exit'
]

# commands to be executed on RTC
_commands_rtc = [
    'configure terminal',
    'interface f0/0',
    'ip address 10.0.0.2 255.0.0.0',
    'no shutdown',
    'exit',
    'ip route 0.0.0.0 0.0.0.0 10.0.0.1',
    'exit',
    'exit'
]

commands = {
    RTA: _commands_rta,
    RTB: _commands_rtb,
    RTC: _commands_rtc
}

test_commands = {
    RTB: [
        ('show ip nat translations', b'192.168.1.35')
    ],
    PC2: [
        ('ping 192.168.3.2', '(0% 丢失)'.encode('gbk'))
    ],
    PC1: [
        ('ping 10.0.0.0', '(100% 丢失)'.encode('gbk')),
        ('ping 192.168.1.35', '(0% 丢失)'.encode('gbk')),
    ]
}
