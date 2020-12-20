RTA = 'RTA'
RTB = 'RTB'
RTC = 'RTC'

valid_hosts = {RTA, RTB, RTC}

_commands_rta = [
    'configure terminal',
    'interface f0/0',
    'ip address 192.168.3.1 255.255.255.0',
    'no shutdown',
    'interface s2/0',
    'ip address 192.168.1.1 255.255.255.252',
    'no shutdown',
    'clock rate 9600',
    'exit',
    'ip route 192.168.1.32 255.255.255.224 192.168.1.2'
    'exit',
    'exit'
]

_commands_rtb = []

_commands_rtc = []


commands = {
    RTA: _commands_rta,
    RTB: _commands_rtb,
    RTC: _commands_rtc
}