'''
This program will clean HTML files
runs through web crawler dataset
'''
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def main():
    print("HTML cleaner")
    inFile = open('Self-driving car - Wikipedia.txt',
                  'r',  encoding='utf8', errors="ignore")
    outFile = open('clean.txt', 'w', encoding='utf-8')
    data = inFile.read()
    cleanData = cleanhtml(data)
    outFile.write(cleanData)

    inFile.close()
    outFile.close()


main()
