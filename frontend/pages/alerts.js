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
      <h1>Project {projectId}: Alerts</h1>
      <p>
        <Link href={{ pathname: '/checks', query: { p: projectId } }}><a>Checks</a></Link>
        {' | '}
        <b>Alerts</b>
      </p>
    </Layout>
  )
}

export default ProjectPage
