<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output omit-xml-declaration="yes" indent="yes"/>
<xsl:template match ="/">
<simple_guide>
<xsl:for-each select ="broadcasts/channel">
<channel>
<xsl:attribute name="name"><xsl:value-of select="@name"/>
</xsl:attribute><xsl:for-each select ="broadcast_day/transmission">
<show>
<xsl:attribute name="name"><xsl:value-of select="name"/>
</xsl:attribute><xsl:attribute name="date"><xsl:value-of select="../@date"/>
</xsl:attribute></show>
</xsl:for-each>
</channel>
</xsl:for-each>
</simple_guide>
</xsl:template>
</xsl:stylesheet>
