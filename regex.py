#1
import re

pattern = r'ab*'

text = "ab abb a abbbb ac"

matches = re.findall(pattern, text)
print(matches)

#2
import re

pattern = r'ab{2,3}'

text = "abb abbb abbbb a"

matches = re.findall(pattern, text)
print(matches)

#3
import re

pattern = r'[a-z]+_[a-z]+'

text = "hello_world my_variable_name test_Test"

matches = re.findall(pattern, text)
print(matches)


#4
import re

pattern = r'[A-Z][a-z]+'

text = "Hello world Python Programming"

matches = re.findall(pattern, text)
print(matches)

#5
import re

pattern = r'a.*b'

text = "acb a123b axxxb ab"

matches = re.findall(pattern, text)
print(matches)

#6
import re

text = "Hello, world. Python is fun"

result = re.sub(r'[ ,.]', ':', text)

print(result)

#7
import re

text = "snake_case_string"

result = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), text)

print(result)

#8
import re

text = "HelloWorldPython"

result = re.split(r'(?=[A-Z])', text)

print(result)

#9
import re

text = "HelloWorldPython"

result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

print(result)

#10
import re

text = "camelCaseStringExample"

result = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

print(result)