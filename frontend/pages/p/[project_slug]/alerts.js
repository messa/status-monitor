import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import Layout from '../../../components/Layout'

function ProjectPage(props) {
  const router = useRouter()
  const { project_slug } = router.query
  return (
    <Layout>
      <p><Link href='../../dashboard'><a>List of all projects</a></Link></p>
      <h1>Project {project_slug}: Alerts</h1>
      <p>
        <Link href='./checks'><a>Checks</a></Link>
        {' | '}
        <b>Alerts</b>
      </p>
    </Layout>
  )
}

export default ProjectPage
