# announcements.py retrieves announcements from https://threeoakshighschool.wordpress.com/daily-announcements and converts it to array of strings
# (https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python)

# Imports
import urllib.request
from bs4 import BeautifulSoup
import re
import string

# Get html as string
url = "https://threeoakshighschool.wordpress.com/daily-announcements/"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

for script in soup(["script", "style"]):
    script.extract()

text = soup.get_text()

# Convert text with linebreaks
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)

# Extract only the announcements
text = text.partition('''\nANNOUNCEMENTS\n''')[2].partition("\nShare this:")[0] # It's possible that "Advertisements" will still show up?

# Save lines into array
lines = text.splitlines()

# Convert to 2D array
announcements = []
announcements.append([])
i = 0
j = 0
for line in lines:
    if line.endswith(':'):
        announcements.append([])
        i += 1
    announcements[i].append(line)

# Print array
for announcement in announcements:
    print(announcement)

# Final outputs
# Day
if announcements[0][1] == 'DAY 1':
    day = 1
elif announcements[0][1] == 'DAY 2':
    day = 2
else:
    day = None
print("It is currently day "+str(day))

# Date
date = announcements[0][0]
print("The date is " + string.capwords(date))


#print(text)