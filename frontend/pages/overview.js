import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import Layout from '../components/Layout'
import ErrorMessage from '../components/ErrorMessage'
import Octicon, { ChevronDown } from '@primer/octicons-react'
import useSWR from 'swr'

const dummyProject = {
  name: '...',
}

function ProjectChooser({ project, path }) {
  const [show, setShow] = useState(false)
  const projectsRes = useSWR(`/api/projects`)
  const { projects } = projectsRes.data || []
  return (
    <span className='ProjectChooser' onClick={() => setShow(!show)}>
      <span className='currentName'>{project.name}</span>
      <Octicon icon={ChevronDown} verticalAlign='middle' />
      {show && (
        <div className='dropDown'>
          {projects.map(p => (
            <Link
              key={p.id}
              href={{ path: path || '/overview', query: { p: p.id } }}
            >
              <a>{p.name}</a>
            </Link>
          ))}
        </div>
      )}
      <style jsx>{`
        .ProjectChooser {
          margin-right: 6px;
          cursor: pointer;
        }
        .ProjectChooser .currentName {
          padding-right: 3px;
        }
        .ProjectChooser :global(.octicon) {
          color: #808080;
        }
        .dropDown {
          position: absolute;
          background-color: #f8f8f8;
          min-width: 160px;
          box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
          z-index: 1;
        }
        .dropDown :global(a) {
          color: black;
          padding: 12px 16px;
          text-decoration: none;
          display: block;
        }
        .dropDown :global(a:hover) {
          background-color: #ddd;
        }
      `}</style>
    </span>
  )
}

function OverviewPage(props) {
  const {
    query: { p: projectId },
  } = useRouter()
  const projectsRes = useSWR(`/api/projects`)
  const { projects } = projectsRes.data || []
  const projectRes = useSWR(`/api/project?projectId=${projectId}`)
  const { project } = projectRes.data || { project: dummyProject }
  return (
    <Layout>
      <h1>
        <ProjectChooser project={project} /> <b>Overview</b>
      </h1>
      <pre>{JSON.stringify(projectId)}</pre>
      <pre>{JSON.stringify(project, null, 2)}</pre>
      <pre>{JSON.stringify(projects, null, 2)}</pre>
    </Layout>
  )
}

export default OverviewPage
