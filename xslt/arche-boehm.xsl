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
            <xsl:for-each select=".//acdh:Collection">
                <acdh:Collection>
                    <xsl:attribute name="rdf:about"><xsl:value-of select="@rdf:about"/></xsl:attribute>
                    <xsl:copy-of select="$constants"/>
                    <xsl:for-each select=".//node()">
                        <xsl:copy-of select="."/>
                    </xsl:for-each>
                </acdh:Collection>
            </xsl:for-each>
            <xsl:for-each select="collection('../boehm_tei')//tei:TEI">
                <xsl:variable name="colId">
                    <xsl:value-of select="replace(replace(data(@xml:id), '.xml', ''), 'boehm_', '')"/>
                </xsl:variable>
                <xsl:variable name="colUri">
                    <xsl:value-of select="concat('https://id.acdh.oeaw.ac.at/legalkraus/boehm/', $colId)"/>
                </xsl:variable>
                <acdh:Collection rdf:about="{$colUri}">
                    <acdh:isPartOf rdf:resource="https://id.acdh.oeaw.ac.at/legalkraus/boehm"/>
                    <acdh:hasTitle xml:lang="de">TEI und Faksimiles zu: <xsl:value-of select=".//tei:title[1]/text()"/></acdh:hasTitle>
                    <acdh:hasExtent xml:lang="de">1 TEI Dokument und <xsl:value-of select="count(.//tei:div[@type='page'])"/> Bilder (.tif)</acdh:hasExtent>
                    <xsl:copy-of select="$constants"/>
                </acdh:Collection>
                <acdh:Resource rdf:about="{concat($TopColId, '/', data(@xml:id))}">
                    <acdh:isPartOf rdf:resource="{$colUri}"/>
                    <acdh:hasTitle xml:lang="de"><xsl:value-of select=".//tei:title[1]/text()"/></acdh:hasTitle>
                    <xsl:copy-of select="$constants"/>
                    <acdh:hasTitle xml:lang="de"><xsl:value-of select=".//tei:titleStmt/tei:title[1]/text()"/></acdh:hasTitle>
                    <acdh:hasAccessRestriction rdf:resource="https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public"/>
                    <acdh:hasCategory rdf:resource="https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei"/>
                    <acdh:hasLanguage rdf:resource="https://vocabs.acdh.oeaw.ac.at/iso6393/deu"/>
                </acdh:Resource>
                <xsl:for-each select=".//tei:div[@type='page']">
                    <acdh:Resource rdf:about="{concat($colUri, '/', data(@n))}">
                        <acdh:isPartOf rdf:resource="{$colUri}"/>
                        <acdh:hasTitle xml:lang="de"><xsl:value-of select="data(@n)"/></acdh:hasTitle>
                        <acdh:hasAccessRestriction rdf:resource="https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public"/>s
                        <acdh:hasCategory rdf:resource="https://vocabs.acdh.oeaw.ac.at/archecategory/image"/>
                        <xsl:copy-of select="$constants"/>
                    </acdh:Resource>
                </xsl:for-each>
            </xsl:for-each>
        </rdf:RDF>
    </xsl:template>
</xsl:stylesheet>
