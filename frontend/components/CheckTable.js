import React from 'react'
import useFetch from '../lib/useFetch'

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
          </tr>
          {checks.map(check => (
            <tr key={check.id}>
              <td><code>{check.id}</code></td>
              <td><code>{check.url}</code></td>
            </tr>
          ))}
        </table>
      )}
      {/*<pre>{JSON.stringify(checks)}</pre>*/}
    </div>
  )
}

export default CheckTable
