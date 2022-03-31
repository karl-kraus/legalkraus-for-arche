<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:acdh="https://vocabs.acdh.oeaw.ac.at/schema#"
    version="2.0" exclude-result-prefixes="#all">
    <xsl:output encoding="UTF-8" media-type="text/html" method="xhtml" version="1.0" indent="yes" omit-xml-declaration="yes"/>
    
    <xsl:template match="/">
        <xsl:variable name="constants">
            <xsl:for-each select=".//node()[parent::acdh:RepoObject]">
                <xsl:copy-of select="."/>
            </xsl:for-each>
        </xsl:variable>
        <xsl:variable name="TopColId">
            <xsl:value-of select="data(.//acdh:TopCollection/@rdf:about)"/>
        </xsl:variable>
        <rdf:RDF xmlns:acdh="https://vocabs.acdh.oeaw.ac.at/schema#">            
            <xsl:for-each select="collection('../data/indices')//tei:TEI">
                <xsl:variable name="partOf">
                    <xsl:value-of select="concat($TopColId, '/indices')"/>
                </xsl:variable>
                <xsl:variable name="flatId">
                    <xsl:value-of select="concat($TopColId, '/', @xml:id)"/>
                </xsl:variable>
                
                <acdh:Resource rdf:about="{replace($flatId, '.xml', '.json')}">
                    <xsl:copy-of select="$constants"/>
                    <!--<acdh:hasPid><xsl:value-of select=".//tei:idno[@type='handle']/text()"/></acdh:hasPid>-->
                    <acdh:hasTitle xml:lang="de"><xsl:value-of select=".//tei:titleStmt/tei:title[1]/text()"/></acdh:hasTitle>
                    <acdh:hasAccessRestriction rdf:resource="https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public"/>
                    <acdh:hasCategory rdf:resource="https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei"/>
                    <acdh:hasLanguage rdf:resource="https://vocabs.acdh.oeaw.ac.at/iso6393/deu"/>
                    <acdh:isPartOf rdf:resource="{replace($partOf, 'indices', 'utils')}"/>
                </acdh:Resource>
                <!--<acdh:Resource rdf:about="{$flatId}">
                    <xsl:copy-of select="$constants"/>
                    <acdh:hasTitle xml:lang="de">JSON Version von <xsl:value-of select=".//tei:titleStmt/tei:title[1]/text()"/></acdh:hasTitle>
                    <acdh:hasAccessRestriction rdf:resource="https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public"/>
                    <acdh:hasCategory rdf:resource="https://vocabs.acdh.oeaw.ac.at/archecategory/dataset"/>
                    <acdh:hasLanguage rdf:resource="https://vocabs.acdh.oeaw.ac.at/iso6393/deu"/>
                    <acdh:isPartOf rdf:resource="{$partOf}"/>
                </acdh:Resource>-->
            </xsl:for-each>
        </rdf:RDF>
    </xsl:template>   
</xsl:stylesheet>