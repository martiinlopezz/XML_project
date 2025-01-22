<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes" />

    <xsl:key name="habitatKey" match="animal" use="habitat" />

    <xsl:template match="/zoos">
        <html>
            <head>
                <title>Animals Grouped by Habitat</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h1>Animals Grouped by Habitat</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Habitat</th>
                            <th>Animal Name</th>
                            <th>Species</th>
                            <th>Diet</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Agrupa los animales por hábitat -->
                        <xsl:for-each select="animal[generate-id() = generate-id(key('habitatKey', habitat)[1])]">
                            <tr>
                                <td rowspan="{count(key('habitatKey', habitat))}">
                                    <xsl:value-of select="habitat" />
                                </td>
                                <xsl:for-each select="key('habitatKey', habitat)">
                                    <tr>
                                        <td><xsl:value-of select="name" /></td>
                                        <td><xsl:value-of select="@species" /></td>
                                        <td><xsl:value-of select="diet" /></td>
                                    </tr>
                                </xsl:for-each>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
