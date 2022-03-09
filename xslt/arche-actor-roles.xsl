<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:acdh="https://vocabs.acdh.oeaw.ac.at/schema#"
    xmlns:lk="https://legalkraus/custom/ns#"
    version="3.0" exclude-result-prefixes="#default">
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
        <xsl:variable name="caseTopCol">
            <xsl:value-of select="concat($TopColId, '/cases')"/>
        </xsl:variable>

        <rdf:RDF xmlns:acdh="https://vocabs.acdh.oeaw.ac.at/schema#" xmlns:lk="https://legalkraus/custom/ns#">       
            
            
<!-- case-collection MD and case-tei-md -->
            <xsl:for-each select="collection('../data/cases_tei')//tei:TEI">
                <xsl:variable name="caseId">
                    <xsl:value-of select="replace(data(@xml:id), '.xml', '')"/>
                </xsl:variable>
                <xsl:variable name="partOf">
                    <xsl:value-of select="concat($TopColId, '/', $caseId)"/>
                </xsl:variable>
                <xsl:variable name="flatId">
                    <xsl:value-of select="concat($TopColId, '/', @xml:id)"/>
                </xsl:variable>
                <xsl:variable name="coverageStartDate">
                    <xsl:value-of select="normalize-space(string-join(data(.//tei:profileDesc/tei:creation/tei:date[1]/@when-iso[1])))"/>
                </xsl:variable>
<!--                MAKE CASE-COL-MD-->
                
                <acdh:Collection rdf:about="{$partOf}">
                    <xsl:for-each select=".//tei:back//tei:person[@xml:id]">
                        <xsl:variable name="entXmlId">
                            <xsl:value-of select="concat('#', data(@xml:id))"/>
                        </xsl:variable>
                        <xsl:variable name="entId">
                            <xsl:choose>
                                <xsl:when test="./tei:idno[@subtype='gnd']">
                                    <xsl:value-of select="./tei:idno[@subtype='gnd']/text()"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="concat('https://id.acdh.oeaw.ac.at/pmb/', (substring-after(@xml:id, 'pmb')))"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:variable>
                        <xsl:variable name="customPropUri">
                            <xsl:value-of select="data(.//ancestor::tei:TEI//tei:particDesc//*[@ref=$entXmlId]/@role)"/>
                        </xsl:variable>
                        <xsl:variable name="customPropId">
                            <xsl:value-of select="lower-case(replace(tokenize($customPropUri, '/')[last()], '.', '', 'q'))"/>
                        </xsl:variable>
                        <xsl:element name="{concat('lk:', $customPropId)}">
                            <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                        </xsl:element>
                    </xsl:for-each>
                    <!--<xsl:for-each select=".//tei:org[@xml:id]">
                        <xsl:variable name="entId">
                            <xsl:value-of select="concat('https://id.acdh.oeaw.ac.at/pmb/', (substring-after(@xml:id, 'pmb')))"/>
                        </xsl:variable>
                        <acdh:hasActor>
                            <acdh:Organisation>
                                <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                                <acdh:hasTitle xml:lang="und"><xsl:value-of select=".//tei:orgName[1]/text()"/></acdh:hasTitle>
                            </acdh:Organisation>
                        </acdh:hasActor>
                    </xsl:for-each>-->
                </acdh:Collection>
            </xsl:for-each>
        </rdf:RDF>
    </xsl:template>   
</xsl:stylesheet>