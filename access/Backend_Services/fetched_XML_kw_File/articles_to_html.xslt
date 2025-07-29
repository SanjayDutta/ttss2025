<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" indent="yes"/>
  <xsl:template match="/">
    <html>
      <head>
        <title>Articles Search Results</title>
        <style>
          table, th, td { border: 1px solid black; border-collapse: collapse; }
          th, td { padding: 8px; }
          .bias-analysis { max-width: 300px; word-wrap: break-word; }
          .url-cell { max-width: 200px; word-wrap: break-word; }
        </style>
      </head>
      <body>
        <h2>Articles Search Results</h2>
        <xsl:for-each select="articles_search_results/metadata">
          <div><b>Search Timestamp:</b> <xsl:value-of select="search_timestamp"/></div>
          <div><b>Keywords Searched:</b> <xsl:value-of select="keywords_searched"/></div>
          <div><b>Total Articles Found:</b> <xsl:value-of select="total_articles_found"/></div>
          <xsl:if test="guardian_analysis">
            <div><b>Guardian AI Analysis:</b> <xsl:value-of select="guardian_analysis"/></div>
          </xsl:if>
          <xsl:if test="breitbart_analysis">
            <div><b>Breitbart AI Analysis:</b> <xsl:value-of select="breitbart_analysis"/></div>
          </xsl:if>
        </xsl:for-each>
        <table>
          <tr>
            <th >Title</th>
            <th>Author</th>
            <th>Source</th>
            <th style="width: 15%;">Date</th>
            <th style="width: 7%;">Bias Score</th>
            <th style="width: 50%;">Bias Analysis</th>
          </tr>
          <xsl:for-each select="articles_search_results/articles/article">
            <tr>
              <td><a href="{url}" target="_blank"><xsl:value-of select="title"/></a></td>
              <td><xsl:value-of select="author"/></td>
              <td><xsl:value-of select="source"/></td>
              <td><xsl:value-of select="date"/></td>
              <td><xsl:value-of select="bias_score"/></td>
              <td class="bias-analysis"><xsl:value-of select="bias_analysis"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
