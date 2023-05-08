from bs4 import BeautifulSoup #is used to parse the input HTML and extracting information
from rdflib import Graph, Namespace, URIRef, Literal #is used to create an RDF graph, adding nodes and triples to it, and serializing it
from rdflib.namespace import RDF, RDFS #same as above
from urllib.parse import quote #is used to encode URL strings

# OERSchema namespace, here you can define any namespace suitable for you
OER = Namespace("http://oerschema.org/LearningComponent/")

# convert the input file to HTML for parsing
with open('consumer_log.txt', 'r') as file:
    text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    html = f'<html><body><pre>{text}</pre></body></html>'

with open('output.html', 'w') as file:
    file.write(html)

# parse the HTML to extract titles and subtitles(those will be used to specify the relation in RDF)
lis = soup.select('div.course-content li')

# create an RDF graph
g = Graph()
g.bind('oer', OER)

for li in lis:
    #the main titles for sections are hidden withing 'hidden sectionname' class in html file
    title = li.find('span', class_='hidden sectionname') 
    if title:
        title_text = title.text
        # create a LearningComponent section for the title 
        title_node = URIRef(OER[quote(title_text.replace(" ", "_"))])
        g.add((title_node, RDF.type, OER.LearningComponent))
        g.add((title_node, RDFS.label, Literal(title_text)))
        #the subtitles for titles are hidden withing 'instancename' class in html file
        subtitles = li.find_all('span', class_='instancename') 
        if subtitles:
            for subtitle in subtitles:
                subtitle_text = subtitle.text
                # create a LearningResource component for the subtitle
                subtitle_node = URIRef(OER[quote(subtitle_text.replace(" ", "_"))])
                g.add((subtitle_node, RDF.type, OER.LearningResource))
                g.add((subtitle_node, RDFS.label, Literal(subtitle_text)))
                g.add((title_node, OER.hasComponent, subtitle_node))

print(g.serialize(format='turtle'))

#in order to have .owl file and see the scheme in Protege 
g.serialize(destination='output.owl', format='xml')

