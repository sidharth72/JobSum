with open('requirements.txt', 'r') as file:
    lines = file.readlines()

# Remove version specifications
lines = [line.split('==')[0] if '==' in line else line.split('>=')[0] if '>=' in line else line.split('<=')[0] if '<=' in line else line for line in lines]

with open('requirements.txt', 'w') as file:
    file.write('\n'.join(lines))
