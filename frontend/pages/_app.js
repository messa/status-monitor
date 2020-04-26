import { SWRConfig } from 'swr'

function MyApp({ Component, pageProps }) {
  return (
    <SWRConfig
      value={{
        refreshInterval: 5 * 1000,
        fetcher: (...args) => fetch(...args).then(res => res.json()),
      }}
    >
      <Component {...pageProps} />
    </SWRConfig>
  )
}

export default MyApp
