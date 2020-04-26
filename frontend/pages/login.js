import React from 'react'
import Layout from '../components/Layout'

function DashboardPage() {
  return (
    <Layout>
      <h1>Sign in</h1>

      <p>
        <a href='/api/auth/google'>Sign in using Google</a>
      </p>
    </Layout>
  )
}

export default DashboardPage
