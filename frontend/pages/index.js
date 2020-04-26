import React from 'react'
import Link from 'next/link'
import Layout from '../components/Layout'

function IndexPage() {
  return (
    <Layout>
      <p>
        This page is visible only in dev mode, because in production there is a
        redirect either to{' '}
        <Link href='/login'>
          <a>/login</a>
        </Link>
        {' or to '}
        <Link href='/dashboard'>
          <a>/dashboard</a>
        </Link>
        .
      </p>
    </Layout>
  )
}

export default IndexPage
