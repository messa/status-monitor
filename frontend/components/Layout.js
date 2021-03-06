import React from 'react'
import Head from 'next/head'
import useSWR from 'swr'
import NavBar from './NavBar'

function Layout({ children }) {
  const { data, error } = useSWR('/api/user')
  const { user } = data || {}
  return (
    <div className='Layout'>
      <Head>
        <title>Status Monitor</title>
        <link
          href='https://fonts.googleapis.com/css?family=IBM+Plex+Sans:400,700&display=swap&subset=latin-ext'
          rel='stylesheet'
        />
        <link
          href='https://fonts.googleapis.com/css?family=IBM+Plex+Sans&display=swap&subset=latin-ext'
          rel='stylesheet'
        />
        <style>{globalStyles}</style>
      </Head>
      <NavBar user={user} />
      <div className='mainContent'>{children}</div>
    </div>
  )
}

const globalStyles = `
  *, :after, :before {
    box-sizing: border-box;
  }
  body {
    font-family: IBM Plex Sans, Roboto, sans-serif;
    font-size: 15px;
    margin: 0;
    padding: 0;
  }
  .mainContainer, .mainContent {
    max-width: 1000px;
    margin: 0 auto;
    padding-left: 16px;
    padding-right: 16px;
  }
  .mainContent {
    margin-top: 16px;
    margin-bottom: 16px;
  }
  a {
    color: #00c;
  }
  pre, code {
    font-family: IBM Plex Mono, Roboto Mono, monospace;
  }
  pre {
    font-size: 13px;
  }
  td, th {
    font-size: 16px;
    text-align: left;
    padding: 1px 16px 1px 0;
  }
  h1 {
    font-size: 21px;
    font-weight: 400;
    margin-top: 0;
  }
`

export default Layout
