import React from 'react'
import Link from 'next/link'
import fetch from 'isomorphic-unfetch'
import Layout from '../components/Layout'
import ErrorMessage from '../components/ErrorMessage'
import useFetch from '../lib/useFetch'

function ProjectList() {
  const [ data, error ] = useFetch('/api/projects')
  if (error) {
    return <ErrorMessage title='Failed to load projects' error={error} />
  }
  if (!data) {
    return <p><em>Loading</em></p>
  }
  const { projects } = data
  return (
    <ul>
      {projects.map(p => (
        <li key={p.projectId}>
          <Link href={{ pathname: '/checks', query: { p: p.projectId } }}><a>{p.name}</a></Link>
        </li>
      ))}
    </ul>
  )
}

function DashboardPage() {
  return (
    <Layout>
      <h1>Dashboard</h1>
      <p>Projects:</p>
      <ProjectList />
    </Layout>
  )
}

export default DashboardPage
