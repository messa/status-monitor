import fetch from 'node-fetch'

// Inspiration: https://github.com/zeit/micro-proxy/blob/master/index.js

export default async function(req, res) {
  // Note: Websockets support not implemented here
  try {
    const newUrl = 'http://localhost:8080' + req.url
    const fetchOptions = {
      method: req.method,
      // headers: Object.assign({ 'x-forwarded-host': req.headers.host }, req.headers, { host: url.host }),
      headers: {
        cookie: req.headers.cookie,
      },
    }
    if (req.method !== 'GET') {
      fetchOptions.body = req
    }
    const proxyRes = await fetch(newUrl, fetchOptions)

    // Forward status code
    res.statusCode = proxyRes.status

    // Forward headers
    const headers = proxyRes.headers.raw()
    for (const key of Object.keys(headers)) {
      res.setHeader(key, headers[key])
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
