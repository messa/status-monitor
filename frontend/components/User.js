import React from 'react'
import useFetch from '../lib/useFetch'
import ErrorMessage from './ErrorMessage'

function User() {
  return '42'
  /*
  const [ data, error ] = useFetch('/api/user')
  if (error) return <ErrorMessage title='Failed to load user' error={error} />
  if (!data || !data.user) return <br />
  const { user } = data
  return (
    <div className='User'>
      Logged in as {user.name} ({user.email})
      {' '}
      <a href='/api/auth/logout'>Log out</a>
    </div>
  )
  */
}

export default User
