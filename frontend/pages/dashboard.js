import React from 'react'
import Link from 'next/link'
import Layout from '../components/Layout'
import ErrorMessage from '../components/ErrorMessage'
import User from '../components/User'
import useFetch from '../lib/useFetch'

function DashboardPage() {
  return (
    <Layout>
      <User />
      <h1>Dashboard</h1>
      <p>Projects:</p>
      <ProjectList />
    </Layout>
  )
}

function ProjectList() {
  const [ data, error ] = useFetch('/api/projects')
  if (error) return <ErrorMessage title='Failed to load projects' error={error} />
  if (!data) return null
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

export default DashboardPage
