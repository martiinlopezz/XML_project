package services;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathFactory;

public class XPathService {
    private Document document; // Recibe el XML cargado en memoria.

    public XPathService(Document document) {
        this.document = document;
    }

    // Método para buscar información con XPath
    public void search(String expression) {
        try {
            XPath xPath = XPathFactory.newInstance().newXPath();
            XPathExpression xPathExpression = xPath.compile(expression); // Prepara la expresión XPath.
            NodeList nodes = (NodeList) xPathExpression.evaluate(document, XPathConstants.NODESET);

            System.out.println("Resultados de la búsqueda:");
            for (int i = 0; i < nodes.getLength(); i++) {
                System.out.println(nodes.item(i).getTextContent()); // Imprime los resultados.
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
