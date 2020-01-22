import React from 'react'
import useFetch from '../lib/useFetch'
import ErrorMessage from './ErrorMessage'

function CheckTable({ projectId }) {
  const [ data, error ] = useFetch(`/api/checks?projectId=${projectId}`)
  if (error) return <ErrorMessage title='Failed to load checks' error={error} />
  if (!data || !data.checks) return null
  const { checks } = data
  return (
    <div className='CheckTable'>
      {checks.length === 0 ? <p>No checks.</p> : (
        <table>
          <tr>
            <th>Id</th>
            <th>URL</th>
            <th>Status</th>
            <th>Last check date</th>
          </tr>
          {checks.map(check => {
            return (
              <tr key={check.id}>
                <td><code>{check.id}</code></td>
                <td><code>{check.url}</code></td>
                <td><code>{check.last_check_color || '-'}</code></td>
                <td><code>{check.last_check_date || '-'}</code></td>
              </tr>
            )
          })}
        </table>
      )}
      {/*<pre>{JSON.stringify(checks)}</pre>*/}
    </div>
  )
}

export default CheckTable
