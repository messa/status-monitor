import fetch from 'node-fetch'

// Inspiration: https://github.com/zeit/micro-proxy/blob/master/index.js

export default async function(req, res) {
  // Note: Websockets support not implemented here
  try {
    const backendUrl = 'http://localhost:8080'
    const newUrl = backendUrl + req.url
    const fetchOptions = {
      method: req.method,
      // headers: Object.assign({ 'x-forwarded-host': req.headers.host }, req.headers, { host: url.host }),
      headers: {
        'cookie': req.headers.cookie,
        'host': req.headers.host,
      },
      redirect: 'manual',
    }
    if (req.method !== 'GET') {
      fetchOptions.body = req
    }
    console.debug(`API proxy: ${fetchOptions.method} ${newUrl}`)
    const proxyRes = await fetch(newUrl, fetchOptions)

    // Forward status code
    res.statusCode = proxyRes.status
    console.debug(`Proxy response status: ${proxyRes.status}`)

    // Forward headers
    const headers = proxyRes.headers.raw()
    for (const key of Object.keys(headers)) {
      if (key === 'alt-svc' || key === 'connection') continue
      let value = new String(headers[key])
      if (key === 'location' && value.startsWith(backendUrl)) {
        const newValue = value.slice(backendUrl.length)
        console.debug(`Stripping backend URL from ${key}: ${value} -> ${newValue}`)
        value = newValue
      }
      console.debug(`Proxy response header: ${key}: ${value}`)
      res.setHeader(key, value)
    }

    // Stream the proxy response
    proxyRes.body.pipe(res)
    proxyRes.body.on('error', (err) => {
      console.error(`Error on proxying url: ${newUrl}`)
      console.error(err.stack)
      res.end()
    })

    req.on('abort', () => {
      proxyRes.body.destroy()
    })
  } catch (err) {
    res.status(500).json({ proxyError: err.toString() })
  }
}
