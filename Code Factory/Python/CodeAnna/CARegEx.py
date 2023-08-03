
# Statement Line
CODE_STMT = "(?P<labl>\w+:)?\s+(?P<inst>[A-Z1-2()<>=*/+-]+)?\s+(?P<addr>[^;\n]+)?\s*(?://(?P<comm>[^\n]*))?"
# New Network
NWRK = "\s*(?P<netw>NETWORK)\s*"
# Block
# Block Begin
BLCK_BGIN = "\s*(?P<begn>BEGIN)\s*"	
# Block End
BLCK_BEND = "\s*(?P<end>END_FUNCTION|END_DATA_BLOCK|END_TYPE)\s*"
# Block Type
TYPE = "\s*(?P<bloc>FUNCTION|DATA_BLOCK|TYPE) *[\"']?(?P<val>[^\"'\]\#]*)[\"'].*"
# Block or Network Title
TITL = "\s*(?P<titl>TITLE) *= *(?P<val>.*)?"
# Author
AUTH = "\s*(?P<auth>AUTHOR)\s*:\s*[\"']?(?P<val>[^\"'\]\#]*)[\"']?.*"
# Version
VERS = "\s*(?P<ver>VERSION)\s*:\s*[\"']?(?P<val>[^\"'\]\#]*)[\"']?.*" 


# Needs to be tested
BLCK = "((?:ORGANIZATION|FUNCTION|DATA)_BLOCK)\s+(\w+)\s*(.*?)\n((?:(?!END_\2).)*)END_\2"

STD = "^(\s*\/\/.*)?$|^(\s*)?function\s+\w+\s*\([^)]*\)\s*\{.*\}$|^(\s*)?if\s*\((.*)\)\s*\{.*\}$|^(\s*)?else\s*\{.*\}$|^(\s*)?for\s*\([^;]*;\s*[^;]*;\s*[^)]*\)\s*\{.*\}$|^(\s*)?while\s*\((.*)\)\s*\{.*\}$|^(\s*)?switch\s*\([^)]*\)\s*\{.*\}$|^(\s*)?case\s+.*\s*\:.*$|^(\s*)?default\s*\:.*$|^(\s*)?break\s*;.*$"



