import React from 'react'
import Link from 'next/link'
import User from './User'

function NavBar() {
  return (
    <div className='NavBar'>
      <div className='mainContainer'>
        <strong className='siteTitle'>
          <Link href='/'><a>Status Monitor</a></Link>
        </strong>

        <User />


      </div>
      <style jsx>{`
        .NavBar {
          padding-top: 12px;
          padding-bottom: 8px;
          border-bottom: 1px dotted #c00;
        }
        .siteTitle a {
          text-decoration: none;
          color: #c00;
        }
      `}</style>
    </div>
  )
}

export default NavBar
