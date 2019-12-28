import React from 'react'
import Link from 'next/link'
import Layout from '../components/Layout'

function DashboardPage() {
  return (
    <Layout>
      <h1>Dashboard</h1>
      <p>Projects:</p>
      <ul>
        <li><Link href={`/p/foo/checks`}><a>Foo</a></Link></li>
        <li><Link href={`/p/bar/checks`}><a>Bar</a></Link></li>
      </ul>
    </Layout>
  )
}

export default DashboardPage
