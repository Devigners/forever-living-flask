import regex as re

i = 'C9™ - Forever Aloe Vera Gel-Canada'
a = re.sub(r'[-]+', '-', i.replace('®', '').replace(
    '™', '').replace('-', '').replace(' ', '-').lower())
print(a)
