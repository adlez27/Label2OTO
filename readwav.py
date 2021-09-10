import xmltodict
import json

testfile = "test/vcv/ささしさすさんさ-ocen"

file_contents = ''
with open(testfile + ".wav", 'rb') as file:
    try:
        file_contents = file.read().split(b'_PMX')[1]
    except:
        print('Please use ocenaudio to set markers.')
        exit()

file_contents = file_contents[file_contents.index(b'<'):file_contents.rindex(b'>')+1]

with open(testfile + '.xml', 'w', encoding='utf-8') as outfile:
    outfile.write(file_contents.decode())

namespaces = {
    "rdf": None,
    "xmp": None,
    "xmpDM": None
}
converted = xmltodict.parse(file_contents, namespaces=namespaces)['x:xmpmeta']['RDF']['Description']['Tracks']['Bag']['li']['markers']['Seq']['li']

for item in converted:
    print(item['name'])

with open(testfile + '.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(converted, indent=4))