import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import Layout from '../components/Layout'

function ProjectPage(props) {
  const router = useRouter()
  const projectId = router.query.p
  return (
    <Layout>
      <p><Link href='/dashboard'><a>List of all projects</a></Link></p>
      <h1>Project {projectId}: Checks</h1>
      <p>
        <b>Checks</b>
        {' | '}
        <Link href={{ pathname: '/alerts', query: { p: projectId } }}><a>Alerts</a></Link>
      </p>
    </Layout>
  )
}

export default ProjectPage
