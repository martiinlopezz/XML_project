<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes" />

    <xsl:template match="/zoos">
        <html>
            <head>
                <title>Endangered and Vulnerable Animals</title>
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
                <h1>Endangered and Vulnerable Animals</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Animal Name</th>
                            <th>Scientific Name</th>
                            <th>Habitat</th>
                            <th>Diet</th>
                            <th>Status</th>
                            <th>Population in Wild</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Filtra animales por estado de conservación -->
                        <xsl:for-each select="conservation_statistic[status='Endangered' or status='Vulnerable']">
                            <tr>
                                <!-- Buscar detalles del animal relacionado -->
                                <xsl:variable name="animal" select="/zoos/animal[@id=current()/@animalid]" />
                                <td><xsl:value-of select="$animal/name" /></td>
                                <td><xsl:value-of select="$animal/scientific_name" /></td>
                                <td><xsl:value-of select="$animal/habitat" /></td>
                                <td><xsl:value-of select="$animal/diet" /></td>
                                <td><xsl:value-of select="status" /></td>
                                <td><xsl:value-of select="population_in_wild" /></td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
