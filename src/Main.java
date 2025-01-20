package main;

import services.XMLService;
import services.XPathService;
import services.XSLTService;

public class Main {
    public static void main(String[] args) {
        XMLService xmlService = new XMLService("resources/zoo.xml");
        XPathService xPathService = new XPathService(xmlService.getDocument());
        XSLTService xsltService = new XSLTService();

        // Buscar equipos con XPath
        System.out.println("Búsqueda de equipos:");
        xPathService.search("//team/name");

        // Transformar XML a HTML con XSLT
        xsltService.transform("resources/zoo.xml", "resources/transformations/example.xsl", "output/zoos.html");

        xmlService.saveXML();
    }
}
