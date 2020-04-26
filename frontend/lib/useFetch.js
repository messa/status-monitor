import fetch from 'isomorphic-unfetch'
import { useState, useEffect } from 'react'

function useFetch(url, options) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(
    function () {
      const fetchData = async function () {
        try {
          const res = await fetch(url, options)
          if (res.status != 200)
            throw new Error(`Received status ${res.status}`)
          const json = await res.json()
          setData(json)
        } catch (error) {
          setError(`${error}; URL: ${url}`)
        }
      }
      fetchData()
      // eslint-disable-next-line react-hooks/exhaustive-deps
    },
    [url]
  )

  return [data, error]
}

export default useFetch
