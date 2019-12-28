import fetch from 'isomorphic-unfetch'

export default async function(req, res) {
  try {
    const fetchRes = await fetch('http://localhost:8080/api/projects')
    const data = await fetchRes.json()
    res.status(200).json(data)
  } catch (err) {
    res.status(500).json({ error: err.toString() })
  }
}
