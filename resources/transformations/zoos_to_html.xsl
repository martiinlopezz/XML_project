<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes" />

    <!-- Root template -->
    <xsl:template match="/zoos">
        <html>
            <head>
                <title>Zoos and Animals</title>
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
                <h1>List of Zoos and Animals</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Zoo Name</th>
                            <th>City</th>
                            <th>Foundation Year</th>
                            <th>Location</th>
                            <th>Animals</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Loop through zoos -->
                        <xsl:for-each select="zoo">
                            <tr>
                                <td><xsl:value-of select="name" /></td>
                                <td><xsl:value-of select="city" /></td>
                                <td><xsl:value-of select="foundation" /></td>
                                <td><xsl:value-of select="@location" /></td>
                                <td>
                                    <ul>
                                        <!-- Loop through animals associated with the zoo -->
                                        <xsl:for-each select="/zoos/animal[@zooid=current()/@id]">
                                            <li>
                                                <xsl:value-of select="name" />
                                                (<xsl:value-of select="@species" />, Diet: <xsl:value-of select="diet" />)
                                            </li>
                                        </xsl:for-each>
                                    </ul>
                                </td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
