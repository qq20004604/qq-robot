import re

HOST = '172.17.0.1'
PORT = 5500

SUPERUSERS = {20004604}
# NICKNAME = {'奶茶', '小奶茶'}
COMMAND_START = {'', re.compile(r'^>+\s*')}
COMMAND_SEP = {'#', '.', re.compile(r'#|::?')}
