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
        <xsl:variable name="caseTopCol">
            <xsl:value-of select="concat($TopColId, '/cases')"/>
        </xsl:variable>

<!--copy static ARCHE MD -->
        <rdf:RDF xmlns:acdh="https://vocabs.acdh.oeaw.ac.at/schema#">       
            <!-- <acdh:TopCollection>
                <xsl:attribute name="rdf:about">
                    <xsl:value-of select=".//acdh:TopCollection/@rdf:about"/>
                </xsl:attribute>
                <xsl:copy-of select="$constants"/>
                <xsl:for-each select=".//node()[parent::acdh:TopCollection]">
                    <xsl:copy-of select="."/>
                </xsl:for-each>
            </acdh:TopCollection> -->
            
            
            <!-- <xsl:for-each select=".//node()[parent::acdh:MetaAgents]">
                <xsl:copy-of select="."/>
            </xsl:for-each> -->
            <!-- <xsl:for-each select=".//acdh:Collection">
                <acdh:Collection>
                    <xsl:attribute name="rdf:about"><xsl:value-of select="@rdf:about"/></xsl:attribute>
                    <xsl:copy-of select="$constants"/>
                    <xsl:for-each select=".//node()">
                        <xsl:copy-of select="."/>
                    </xsl:for-each>
                </acdh:Collection>
            </xsl:for-each> -->
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
                    <xsl:copy-of select="$constants"/>
                    <acdh:hasTitle xml:lang="de"><xsl:value-of select=".//tei:titleStmt/tei:title[1]/text()"/></acdh:hasTitle>
                    <acdh:isPartOf rdf:resource="{$caseTopCol}"/>
                    <acdh:hasExtent xml:lang="de"><xsl:value-of select="count(.//tei:sourceDesc//tei:item)"/> Dokumente</acdh:hasExtent>
                    <xsl:for-each select=".//tei:keywords//tei:term/text()">
                        <acdh:hasSubject xml:lang="de"><xsl:value-of select="."/></acdh:hasSubject>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:classCode/text()">
                        <acdh:hasSubject xml:lang="de"><xsl:value-of select="."/></acdh:hasSubject>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:place[@xml:id]">
                        <xsl:variable name="entId">
                            <xsl:choose>
                                <xsl:when test="./tei:idno[contains(./text(), 'geonames')][1]">
                                    <xsl:value-of select="./tei:idno[contains(./text(), 'geonames')][1]/text()"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="concat('https://id.acdh.oeaw.ac.at/pmb/', (substring-after(@xml:id, 'pmb')))"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:variable>
                        <acdh:hasSpatialCoverage>
                            <acdh:Place>
                                <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                                <acdh:hasTitle xml:lang="und"><xsl:value-of select="./tei:placeName[1]/text()"/></acdh:hasTitle>
                            </acdh:Place>
                        </acdh:hasSpatialCoverage>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:person[@xml:id]">
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
                        <acdh:hasActor>
                            <acdh:Person>
                                <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                                <acdh:hasTitle xml:lang="und"><xsl:value-of select=".//tei:forename[1]/text()||' '||.//tei:surname[1]/text()"/></acdh:hasTitle>
                            </acdh:Person>
                        </acdh:hasActor>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:org[@xml:id]">
                        <xsl:variable name="entId">
                            <xsl:value-of select="concat('https://id.acdh.oeaw.ac.at/pmb/', (substring-after(@xml:id, 'pmb')))"/>
                        </xsl:variable>
                        <acdh:hasActor>
                            <acdh:Organisation>
                                <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                                <acdh:hasTitle xml:lang="und"><xsl:value-of select=".//tei:orgName[1]/text()"/></acdh:hasTitle>
                            </acdh:Organisation>
                        </acdh:hasActor>
                    </xsl:for-each>
                </acdh:Collection>
                
<!--                MAKE CASE-TEI-MD-->
                
                <acdh:Resource rdf:about="{$flatId}">
                    <xsl:copy-of select="$constants"/>
                    <!--<acdh:hasPid><xsl:value-of select=".//tei:idno[@type='handle']/text()"/></acdh:hasPid>-->
                    <acdh:hasTitle xml:lang="de">TEI zu: <xsl:value-of select=".//tei:titleStmt/tei:title[1]/text()"/></acdh:hasTitle>
                    <acdh:hasAccessRestriction rdf:resource="https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public"/>
                    <acdh:hasCategory rdf:resource="https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei"/>
                    <!--<acdh:hasLanguage rdf:resource="https://vocabs.acdh.oeaw.ac.at/iso6393/deu"/> can be taken from /tei:TEI/tei:teiHeader/tei:profileDesc/tei:langUsage/tei:language/@ident but need to mapped to arche-lang-vocabs-->
                    <acdh:isPartOf rdf:resource="{$partOf}"/>
                    <acdh:documents rdf:resource="{$partOf}"/>
                    <xsl:for-each select=".//tei:keywords//tei:term/text()">
                        <acdh:hasSubject xml:lang="de"><xsl:value-of select="."/></acdh:hasSubject>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:classCode/text()">
                        <acdh:hasSubject xml:lang="de"><xsl:value-of select="."/></acdh:hasSubject>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:place[@xml:id]">
                        <xsl:variable name="entId">
                            <xsl:choose>
                                <xsl:when test="./tei:idno[contains(./text(), 'geonames')][1]">
                                    <xsl:value-of select="./tei:idno[contains(./text(), 'geonames')][1]/text()"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="concat('https://id.acdh.oeaw.ac.at/pmb/', (substring-after(@xml:id, 'pmb')))"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:variable>
                        <acdh:hasSpatialCoverage>
                            <acdh:Place>
                                <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                                <acdh:hasTitle xml:lang="und"><xsl:value-of select="./tei:placeName[1]/text()"/></acdh:hasTitle>
                            </acdh:Place>
                        </acdh:hasSpatialCoverage>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:person[@xml:id]">
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
                        <acdh:hasActor>
                            <acdh:Person>
                                <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                                <acdh:hasTitle xml:lang="und"><xsl:value-of select=".//tei:forename[1]/text()||' '||.//tei:surname[1]/text()"/></acdh:hasTitle>
                            </acdh:Person>
                        </acdh:hasActor>
                    </xsl:for-each>
                    <xsl:for-each select=".//tei:org[@xml:id]">
                        <xsl:variable name="entId">
                            <xsl:value-of select="concat('https://id.acdh.oeaw.ac.at/pmb/', (substring-after(@xml:id, 'pmb')))"/>
                        </xsl:variable>
                        <acdh:hasActor>
                            <acdh:Organisation>
                                <xsl:attribute name="rdf:about"><xsl:value-of select="$entId"/></xsl:attribute>
                                <acdh:hasTitle xml:lang="und"><xsl:value-of select=".//tei:orgName[1]/text()"/></acdh:hasTitle>
                            </acdh:Organisation>
                        </acdh:hasActor>
                    </xsl:for-each>
                </acdh:Resource>
                
            </xsl:for-each>
        </rdf:RDF>
    </xsl:template>   
</xsl:stylesheet>
