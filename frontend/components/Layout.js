import React from 'react'
import Head from 'next/head'

function Layout({ children }) {
  return (
    <div className='Layout'>
      <Head>
        <title>Status Monitor</title>
        <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Sans:400,700&display=swap&subset=latin-ext" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Sans&display=swap&subset=latin-ext" rel="stylesheet" />
        <style>{globalStyles}</style>
      </Head>
      <div className='mainContent'>
        {children}
      </div>
    </div>
  )
}

const globalStyles = `
  body {
    font-family: IBM Plex Sans, Roboto, sans-serif;
    font-size: 16px;
    margin: 0;
    padding: 0;
  }
  .mainContent {
    max-width: 1000px;
    margin: 0 auto;
    padding: 16px;
  }
  a {
    color: #00c;
  }
  code {
    font-family: IBM Plex Mono, Roboto Mono, monospace;
  }
  td, th {
    font-size: 16px;
    text-align: left;
    padding: 1px 16px 1px 0;
  }
`

export default Layout
