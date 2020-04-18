import React from 'react'
import Link from 'next/link'
import classnames from 'classnames'
import Octicon, { Person, SignIn, SignOut } from '@primer/octicons-react'
import User from './User'

function NavBar({ user }) {
  return (
    <div className='NavBar'>
      <div className='mainContainer flexContainer'>

        <div className='siteTitle'>
          <Link href={user ? '/dashboard' : '/home'}><a>Status Monitor</a></Link>
        </div>

        <div className='mainMenu'>
          {user && (
            <>
              <NavBarItem href='/projects' title='Projects' />
              <NavBarItem href='/alerts' title='Alerts' />
              <NavBarItem href='/checks' title='Checks' />
            </>
          )}
        </div>

        <div className='userMenu'>
          {user && (
            <>
              <NavBarItem href='/profile' title='Profile' octicon={Person} right />
              <NavBarItem href='/api/auth/logout' title='Sign out' octicon={SignOut} right rawLink />
            </>
          )}
          {!user && (
            <>
              <NavBarItem href='/login' title='Sign in' octicon={SignIn} right />
            </>
          )}
        </div>

      </div>
      <style jsx global>{`
        .NavBar {
          padding-top: 16px;
          padding-bottom: 12px;
          font-family: IBM Plex Mono, Roboto Mono, monospace;
          font-size: 14px;
          font-weight: 400;
        }

        .NavBar .flexContainer {
          display: flex;
          flex-direction: row;
        }

        .NavBar .flexContainer > .siteTitle {
          flex: 0 0 auto;
        }
        .NavBar .flexContainer > .mainMenu {
          flex: 1 1 auto;
        }
        .NavBar .flexContainer > .userMenu {
          flex: 0 1 auto;
        }

        .NavBar .siteTitle,
        .NavBar .NavBarItem {
          display: inline-block;
          margin-right: 20px;
        }
        .NavBar .NavBarItem.right {
          margin-right: 0;
          margin-left: 20px;
        }

        .NavBar .siteTitle,
        .NavBar .siteTitle a {
          font-weight: 700;
          text-decoration: none;
          color: #c03;
        }

        .NavBar .NavBarItem a,
        .NavBar .NavBarItem a {
          color: #333;
          text-decoration: none;
        }
        .NavBar .NavBarItem a:hover {
          color: #000;
          text-decoration: underline;
        }

      `}</style>
    </div>
  )
}

function NavBarItem({ href, title, right, rawLink, octicon }) {
  let linkContent = title
  if (octicon) {
    linkContent = <><Octicon icon={octicon} />{' '}{linkContent}</>
  }
  let link = rawLink ? <a href={href}>{linkContent}</a> : <Link href={href}><a>{linkContent}</a></Link>
  return (
    <span className={classnames('NavBarItem', { right })}>
      {link}
    </span>
  )
}

export default NavBar
