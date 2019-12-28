import React from 'react'
import Link from 'next/link'

function ProjectMenu({ projectId, activeItem }) {
  return (
    <p>
      <MenuItem
        active={activeItem === 'checks'}
        href={{ pathname: '/checks', query: { p: projectId } }}
        content='Checks'
      />
      {' | '}
      <MenuItem
        active={activeItem === 'alerts'}
        href={{ pathname: '/alerts', query: { p: projectId } }}
        content='Alerts'
      />
    </p>
  )
}

function MenuItem({ active, href, content }) {
  if (active) return <strong>{content}</strong>
  return <Link href={href}><a>{content}</a></Link>
}

export default ProjectMenu
