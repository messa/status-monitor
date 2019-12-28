import React from 'react'
import Link from 'next/link'
import Layout from '../../../components/Layout'

function ProjectPage(props) {
  const { url } = props
  const { project_slug } = url.query
  return (
    <Layout>
      <p><Link href='../../dashboard'><a>List of all projects</a></Link></p>
      <h1>Project {project_slug}: Checks</h1>
      <p>
        <b>Checks</b>
        {' | '}
        <Link href='./alerts'><a>Alerts</a></Link>
      </p>

    <pre>{JSON.stringify(props, null, 2)}</pre>
    </Layout>
  )
}

export default ProjectPage
