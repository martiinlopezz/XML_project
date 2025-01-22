<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes" />

    <xsl:key name="zooAnimals" match="animal" use="@zooid" />

    <xsl:template match="/zoos">
        <html>
            <head>
                <title>Animals Count by Zoo</title>
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
                <h1>Animals Count by Zoo</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Zoo Name</th>
                            <th>City</th>
                            <th>Location</th>
                            <th>Number of Animals</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Iterar sobre los zoológicos -->
                        <xsl:for-each select="zoo">
                            <tr>
                                <td><xsl:value-of select="name" /></td>
                                <td><xsl:value-of select="city" /></td>
                                <td><xsl:value-of select="@location" /></td>
                                <td>
                                    <xsl:value-of select="count(key('zooAnimals', @id))" />
                                </td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
