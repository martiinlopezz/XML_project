package services;

import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;

public class XMLService {
    private Document document; // Aquí guardamos el XML en memoria.
    private String filePath;  // La ruta al archivo XML.

    // Constructor: carga el archivo XML.
    public XMLService(String filePath) {
        this.filePath = filePath;
        loadXML();
    }

    // Cargar el archivo XML
    private void loadXML() {
        try {
            File xmlFile = new File(filePath);
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            document = builder.parse(xmlFile); // Cargamos el archivo.
            document.getDocumentElement().normalize();
            System.out.println("XML cargado correctamente.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Guardar los cambios en el archivo XML
    public void saveXML() {
        try {
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            DOMSource source = new DOMSource(document);
            StreamResult result = new StreamResult(new File(filePath));
            transformer.transform(source, result); // Guardamos el XML.
            System.out.println("XML guardado correctamente.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Document getDocument() {
        return document; // Devolvemos el XML para que otras clases trabajen con él.
    }
}
