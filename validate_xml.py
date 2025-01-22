from lxml import etree

# Rutas de los archivos
xml_path = "resources/zoo.xml"
xsd_path = "resources/validation_xsd/zoo.xsd"

try:
    # Cargar el XML y el XSD
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        xml_tree = etree.parse(xml_file)
    
    with open(xsd_path, 'r', encoding='utf-8') as xsd_file:
        xsd_doc = etree.parse(xsd_file)
        schema = etree.XMLSchema(xsd_doc)

    # Validar el XML
    schema.assertValid(xml_tree)
    print("The file is valid against the XSD.")

except etree.DocumentInvalid as e:  
    print("The XML file is not valid.")
    print(e)
except Exception as e:
    print(f"Error: {e}")
