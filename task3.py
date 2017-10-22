import sys
from urllib import urlopen
from BeautifulSoup import BeautifulSoup as bs
import re
import string

from stop_words import get_stop_words

import math

if len(sys.argv)>1:
    input = sys.argv[1]
else:
    print "No input file provided"
    exit()

fName = "processed_file_%n%.txt"
count = 0

contents = []
dictionary = {}


def process_link(link):
    global count
    global contents

    print "Start precessing " + link

    soap = bs(urlopen(link))
    content = soap.prettify()

    content = re.sub('<.*?>', '', content).lower()

    content = content.translate(None, string.punctuation)

    name = fName.replace("%n%", str(count))
    contents.append(content)
    #with open(name, "w") as f:
    #   f.write(content)
    count += 1

    print "Processing finished successfully.\n"


def add_to_dict(text):
    global dictionary
    for e in text:
        if e != "":
            dictionary[e] = 1


def calculate_angle(first, second):
    first_m = calculate_module(first)
    second_m = calculate_module(second)
    down = first_m * second_m
    top = 0.0
    for i in range(0, len(first)):
        top += first[i] * second[i]
    return top/down

def calculate_module(vec):
    module = 0.0
    for x in vec:
        module += x*x;
    return math.sqrt(module)

with open(input, "r") as f:
    lines = f.readlines()
    for line in lines:
        if line.strip() != "":
            process_link(line.strip())


articles = []
for content in contents:
    words = content.split()
    add_to_dict(words)
    articles.append(words)

alphabet_size = len(dictionary.keys())
print "There are " + str(alphabet_size) + " unique words in all articles\n"

for stop in get_stop_words("en"):
    dictionary.pop(stop, None)

alphabet_size = len(dictionary.keys())
print "There are " + str(alphabet_size) + " unique words without stop words in all articles\n"

values = []

for words in articles:
    vs = []
    for w in dictionary.keys():
        n = words.count(w)
        v = n / float(len(words))
        vs.append(v)
    values.append(vs)

results = []

for i in range(0, len(values) - 1):
    for j in range(i + 1, len(values)):
        angle = calculate_angle(values[i], values[j])
        r = [ str(i+1) + " and " + str(j+1), angle]
        results.append(r)

results.sort(key=lambda x: x[1])


for i in range(0, 10):
    r1 = results[i]
    r2 = results[len(results) - i - 1]
    print "Angle beetween %s : %f" % (r1[0], r1[1])
    print "Angle beetween %s : %f\n" % (r2[0], r2[1])
