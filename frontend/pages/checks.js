import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import Layout from '../components/Layout'
import ErrorMessage from '../components/ErrorMessage'
import ProjectMenu from '../components/ProjectMenu'
import User from '../components/User'
import CheckTable from '../components/CheckTable'
import useFetch from '../lib/useFetch'

function CheckPage(props) {
  const router = useRouter()
  const projectId = router.query.p
  return (
    <Layout>
      <User />
      <p><Link href='/dashboard'><a>List of all projects</a></Link></p>
      {projectId && <ProjectChecks projectId={projectId} />}
    </Layout>
  )
}

function ProjectChecks({ projectId }) {
  const [ data, error ] = useFetch(`/api/project?projectId=${projectId}`)
  if (error) return <ErrorMessage title='Failed to load project' error={error} />
  if (!data) return null
  const { project } = data
  return (
    <>
      <h1>{project.name}</h1>
      <ProjectMenu activeItem='checks' projectId={projectId} />
      <CheckTable projectId={projectId} />
    </>
  )
}

export default CheckPage
