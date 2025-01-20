package services;

import javax.xml.transform.*;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import java.io.File;

public class XSLTService {
    public void transform(String xmlPath, String xslPath, String outputPath) {
        try {
            TransformerFactory factory = TransformerFactory.newInstance();
            Transformer transformer = factory.newTransformer(new StreamSource(new File(xslPath))); // Carga el archivo XSLT.
            transformer.transform(new StreamSource(new File(xmlPath)), new StreamResult(new File(outputPath))); // Aplica la transformación.
            System.out.println("Transformación completada. Archivo guardado en: " + outputPath);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
