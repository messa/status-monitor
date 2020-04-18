import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import Layout from '../components/Layout'
import ErrorMessage from '../components/ErrorMessage'
import useFetch from '../lib/useFetch'

function AlertPage(props) {
  const router = useRouter()
  const projectId = router.query.p
  return (
    <Layout>
      {projectId && <ProjectAlerts projectId={projectId} />}
    </Layout>
  )
}

function ProjectAlerts({ projectId }) {
  const [ data, error ] = useFetch(`/api/project?projectId=${projectId}`)
  if (error) return <ErrorMessage title='Failed to load project' error={error} />
  if (!data) return null
  const { project } = data
  return (
    <>
      <h1>{project.name}</h1>
    </>
  )
}

export default AlertPage
