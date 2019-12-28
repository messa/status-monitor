import React from 'react'
import Link from 'next/link'
import Layout from '../../../components/Layout'

function ProjectPage(props) {
  const { url } = props
  const { project_slug } = url.query
  return (
    <Layout>
      <p><Link href='../../dashboard'><a>List of all projects</a></Link></p>
      <h1>Project {project_slug}: Alerts</h1>
      <p>
        <Link href='./checks'><a>Checks</a></Link>
        {' | '}
        <b>Alerts</b>
      </p>
    <pre>{JSON.stringify(props, null, 2)}</pre>
    </Layout>
  )
}

export default ProjectPage
