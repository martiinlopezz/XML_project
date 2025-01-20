<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>
    <xsl:template match="/">
        <html>
        <head><title>Zoos</title></head>
        <body>
            <h1>Zoos del mundo</h1>
            <table border="1">
                <tr>
                    <th>Nombre</th>
                    <th>Ciudad</th>
                    <th>Fundación</th>
                </tr>
                <xsl:for-each select="//zoo">
                    <tr>
                        <td><xsl:value-of select="name"/></td>
                        <td><xsl:value-of select="city"/></td>
                        <td><xsl:value-of select="foundation"/></td>
                    </tr>
                </xsl:for-each>
            </table>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
