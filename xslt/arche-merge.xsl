<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:acdh="https://vocabs.acdh.oeaw.ac.at/schema#"
    version="2.0" exclude-result-prefixes="#all">
    <xsl:output encoding="UTF-8" media-type="application/xml" method="xml" version="1.0" indent="yes" omit-xml-declaration="yes"/>
    
    <xsl:template match="/">
        
        
        <rdf:RDF xmlns:acdh="https://vocabs.acdh.oeaw.ac.at/schema#">            
            <xsl:for-each-group select=".//acdh:Resource" group-by="data(./acdh:isPartOf/@rdf:resource)">
                <acdh:Collection rdf:about="{current-grouping-key()}">
                    <xsl:for-each select="distinct-values(current-group()//acdh:hasSpatialCoverage/acdh:*/@rdf:about)">
                        <acdh:hasSpatialCoverage rdf:resource="{.}"/>
                    </xsl:for-each>
                    <xsl:for-each select="distinct-values(current-group()//acdh:hasActor/acdh:*/@rdf:about)">
                        <acdh:hasActor rdf:resource="{.}"/>
                    </xsl:for-each>
                    <xsl:for-each select="distinct-values(current-group()//acdh:hasSubject/text())">
                        <acdh:hasSubject xml:lang="de"><xsl:value-of select="."/></acdh:hasSubject>
                    </xsl:for-each>
                </acdh:Collection>
            </xsl:for-each-group>
        </rdf:RDF>
    </xsl:template>   
</xsl:stylesheet>
