import re
from osbot_utils.helpers.safe_str.Safe_Str__Text import Safe_Str__Text

# this is a small extension of Safe_Str__Text which also supports the ' and / chars
class Str__Description(Safe_Str__Text):
    regex = re.compile(Safe_Str__Text.regex.pattern[:-1] + "'/]")