import React from 'react'

function ErrorMessage({ title, error }) {
  return (
    <div className='ErrorMessage'>
      <strong>{title}:</strong> {error.toString()}
      <style jsx>{`
        .ErrorMessage {
          border: 1px solid red;
          background: #fee;
          padding: 10px;
          color: #600;
        }
      `}</style>
    </div>
  )
}

export default ErrorMessage
