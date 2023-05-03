#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from urllib.parse import quote

#CourseSyllabus namespace
CS = Namespace("http://schema.org/CourseSyllabus#")

# convert the input file to HTML for parsing
with open('consumer_log.txt', 'r') as file:
    text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    html = f'<html><body><pre>{text}</pre></body></html>'

with open('output.html', 'w') as file:
    file.write(html)

# parse the HTML to extract titles and subtitles
lis = soup.select('div.course-content li')

# create an RDF graph
g = Graph()
g.bind('cs', CS)

for li in lis:
    title = li.find('span', class_='hidden sectionname') 
    if title:
        title_text = title.text
        print('Title:', title_text)
        subtitles = li.find_all('span', class_='instancename') 
        if subtitles:
            # create a CourseSyllabus section for the title
            title_node = URIRef(CS[quote(title_text.replace(" ", "_"))])
            g.add((title_node, RDF.type, CS.Section))
            g.add((title_node, RDFS.label, Literal(title_text)))
            for subtitle in subtitles:
                subtitle_text = subtitle.text
                # create a CourseSyllabus subSection for the subtitle
                subtitle_node = URIRef(CS[quote(subtitle_text.replace(" ", "_"))])
                g.add((subtitle_node, RDF.type, CS.SubSection))
                g.add((subtitle_node, RDFS.label, Literal(subtitle_text)))
                g.add((title_node, CS.hasSubSection, subtitle_node))
                print('Subtitle:', subtitle_text)
        else:
            print('No subtitle')
            

print(g.serialize(format='turtle'))

