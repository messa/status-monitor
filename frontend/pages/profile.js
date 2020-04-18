import React from 'react'
import Link from 'next/link'
import useSWR from 'swr'
import Layout from '../components/Layout'

const fetcher = url => fetch(url).then(r => r.json())

function ProfilePage() {
  const { data, error } = useSWR('/api/user')
  const { user } = data || {}
  return (
    <Layout>
      <h1>Profile</h1>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </Layout>
  )
}

export default ProfilePage
