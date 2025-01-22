from lxml import etree

# Configuración de rutas para las transformaciones
transformations2 = [
    {
        "xslt_path": "resources/transformations/zoos_to_html.xsl",
        "output_path": "resources/transformations/zoos_to_html.html",
        "description": "Transformación general a HTML"
    },
    {
        "xslt_path": "resources/transformations/herbivores_to_html.xsl",
        "output_path": "resources/transformations/herbivores_to_html.html",
        "description": "Transformación de animales herbívoros a HTML"
    },
    {
    "xslt_path": "resources/transformations/animals_by_habitat.xsl",
    "output_path": "resources/transformations/animals_by_habitat.html",
    "description": "Transformación de animales agrupados por hábitat a HTML"
    },
    {
    "xslt_path": "resources/transformations/endangered_animals.xsl",
    "output_path": "resources/transformations/endangered_animals.html",
    "description": "Reporte de animales en peligro de extinción"
    },
    {
    "xslt_path": "resources/transformations/animals_count_by_zoo.xsl",
    "output_path": "resources/transformations/animals_count_by_zoo.html",
    "description": "Conteo de animales por zoológico"
    }



]

xml_path = "resources/zoo.xml"  # Ruta del archivo XML

try:
    # Cargar el archivo XML
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        xml_tree = etree.parse(xml_file)

    # Iterar sobre las transformaciones
    for transform_config in transformations2:
        xslt_path = transform_config["xslt_path"]
        output_path = transform_config["output_path"]
        description = transform_config["description"]

        # Cargar el archivo XSLT
        with open(xslt_path, 'r', encoding='utf-8') as xslt_file:
            xslt_tree = etree.parse(xslt_file)

        # Aplicar la transformación XSLT
        transform = etree.XSLT(xslt_tree)
        result = transform(xml_tree)

        # Guardar el resultado en un archivo de salida
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(str(result))

        print(f"{description} completada. Archivo generado: {output_path}")

except Exception as e:
    print(f"Error al aplicar las transformaciones: {e}")
