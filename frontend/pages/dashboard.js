import React from 'react'
import Link from 'next/link'
import Layout from '../components/Layout'
import ErrorMessage from '../components/ErrorMessage'
import useFetch from '../lib/useFetch'

function DashboardPage() {
  return (
    <Layout>
      <h1>Dashboard</h1>
      <p>Projects:</p>
      <ProjectList />
    </Layout>
  )
}

function ProjectList() {
  const [data, error] = useFetch('/api/projects')
  if (error)
    return <ErrorMessage title='Failed to load projects' error={error} />
  if (!data) return null
  const { projects } = data
  return (
    <ul>
      {projects.map(p => (
        <li key={p.id}>
          <Link href={{ pathname: '/checks', query: { p: p.id } }}>
            <a>{p.name}</a>
          </Link>
        </li>
      ))}
    </ul>
  )
}

export default DashboardPage
