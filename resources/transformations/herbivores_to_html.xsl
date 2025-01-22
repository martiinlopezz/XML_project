<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes" />

    <xsl:template match="/zoos">
        <html>
            <head>
                <title>Herbivorous Animals</title>
            </head>
            <body>
                <h1>List of Herbivorous Animals</h1>
                <ul>
                    <!-- Loop through animals with diet 'Herbivore' -->
                    <xsl:for-each select="animal[diet='Herbivore']">
                        <li>
                            <xsl:value-of select="name" /> - 
                            <xsl:value-of select="scientific_name" />
                        </li>
                    </xsl:for-each>
                </ul>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
