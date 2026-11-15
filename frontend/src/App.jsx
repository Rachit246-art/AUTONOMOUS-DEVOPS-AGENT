import { useState, useRef, useEffect } from 'react'
import {
  ArrowUp,
  Sun,
  Moon,
  Copy,
  Check
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { getChatUrl } from './config'
import './App.css'

function CodeBlock({ children, className }) {
  const [copied, setCopied] = useState(false)

  const language = className
    ? className.replace('language-', '')
    : ''

  const codeText = String(children).replace(/\n$/, '')

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(codeText)
      setCopied(true)
      setTimeout(() => setCopied(false), 1800)
    } catch (error) {
      console.error('Copy failed:', error)
    }
  }

  return (
    <div className="code-container">
      <div className="code-header">
        <span className="code-lang">{language || 'code'}</span>

        <button
          className="copy-btn"
          onClick={handleCopy}
          aria-label="Copy code"
        >
          {copied ? <Check size={13} /> : <Copy size={13} />}
          <span>{copied ? 'Copied!' : 'Copy code'}</span>
        </button>
      </div>

      <pre className="code-pre">
        <code>{codeText}</code>
      </pre>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([])
  const [prompt, setPrompt] = useState('')
  const [theme, setTheme] = useState('light')
  const [isLoading, setIsLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState(null)

  const textareaRef = useRef(null)
  const messagesEndRef = useRef(null)

  const hasMessages = messages.length > 0

  // Apply selected theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  // Automatically scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth'
    })
  }, [messages, isLoading])

  // Handle input changes
  const handleInputChange = (e) => {
    setPrompt(e.target.value)

    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'

      textareaRef.current.style.height =
        `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }

  // Toggle light and dark theme
  const toggleTheme = () => {
    setTheme((prev) =>
      prev === 'dark' ? 'light' : 'dark'
    )
  }

  // Send message to FastAPI backend
  const handleSendPrompt = async () => {
    const textToSend = prompt.trim()

    if (!textToSend || isLoading) return

    setErrorMsg(null)

    const userMessage = {
      id: `u-${Date.now()}`,
      sender: 'user',
      text: textToSend
    }

    setMessages((prev) => [...prev, userMessage])

    setPrompt('')

    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }

    setIsLoading(true)

    try {
      // Get backend API URL
      const apiUrl = getChatUrl()

      console.log('Sending request to:', apiUrl)

      // Send request to FastAPI
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error_message: textToSend
        })
      })

      // Read backend response
      const data = await response.json()

      console.log('Backend response:', data)

      // Handle HTTP errors
      if (!response.ok) {
        throw new Error(
          data.detail ||
          data.message ||
          `Server returned HTTP ${response.status}`
        )
      }

      // Extract actual RAG-generated solution
      const assistantText = data.solution

      if (!assistantText) {
        throw new Error(
          'Backend response does not contain a solution.'
        )
      }

      // Create assistant message with RAG metadata
      const assistantMessage = {
        id: `a-${Date.now()}`,
        sender: 'assistant',
        text: assistantText,
        sources: data.sources || [],
        retrievedChunks: data.retrieved_chunks || 0,
        incidentId: data.id
      }

      setMessages((prev) => [
        ...prev,
        assistantMessage
      ])

    } catch (err) {
      console.error('API Error:', err)

      setErrorMsg(err.message)

      const errorBubble = {
        id: `err-${Date.now()}`,
        sender: 'assistant',
        text:
          `**Backend Error:** ${err.message}\n\n` +
          'Please check your backend server and API logs.'
      }

      setMessages((prev) => [
        ...prev,
        errorBubble
      ])

    } finally {
      setIsLoading(false)
    }
  }

  // Send message using Enter key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendPrompt()
    }
  }

  // Reusable chat input component
  const renderPromptBox = (isCentered = false) => (
    <div className={`input-section ${isCentered ? 'centered' : ''}`}>

      <div className="input-container">

        <textarea
          ref={textareaRef}
          className="prompt-textarea"
          rows={1}
          placeholder="Ask a question or describe an issue..."
          value={prompt}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
        />

        <button
          type="button"
          className="send-btn"
          disabled={!prompt.trim() || isLoading}
          onClick={handleSendPrompt}
          aria-label="Send message"
        >
          <ArrowUp size={18} strokeWidth={2.4} />
        </button>

      </div>

      {errorMsg && (
        <div className="error-note">
          {errorMsg}
        </div>
      )}

      <div className="input-footer-note">
        RAG Assistant provides context-grounded responses from your knowledge base.
      </div>

    </div>
  )

  return (
    <div className="app-container">

      <main className="main-wrapper">

        {/* Header */}
        <header className="top-bar">

          <div className="model-title">
            RAG Assistant
          </div>

          <button
            className="theme-toggle-header"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === 'dark'
              ? <Sun size={17} />
              : <Moon size={17} />
            }

            <span>
              {theme === 'dark' ? 'Light' : 'Dark'}
            </span>

          </button>

        </header>

        {/* Initial Chat Screen */}
        {!hasMessages ? (

          <div className="center-front-screen">

            <h1 className="front-headline">
              What can I help with?
            </h1>

            {renderPromptBox(true)}

          </div>

        ) : (

          <>

            {/* Chat Messages */}
            <div className="chat-container">

              <div className="chat-messages">

                {messages.map((msg) => (

                  <div
                    key={msg.id}
                    className={`message-row ${msg.sender}`}
                  >

                    <div className="message-bubble">

                      {msg.sender === 'assistant' ? (

                        <div className="markdown-body">

                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              code({
                                inline,
                                className,
                                children,
                                ...props
                              }) {
                                if (!inline && className) {
                                  return (
                                    <CodeBlock className={className}>
                                      {children}
                                    </CodeBlock>
                                  )
                                }

                                return (
                                  <code
                                    className="inline-code"
                                    {...props}
                                  >
                                    {children}
                                  </code>
                                )
                              }
                            }}
                          >
                            {msg.text}
                          </ReactMarkdown>

                          {/* RAG Source Information */}
                          {msg.sources && msg.sources.length > 0 && (

                            <div className="rag-source-info">

                              <div>
                                <strong>Knowledge Sources:</strong>

                                <ul>
                                  {msg.sources.map((source, index) => (
                                    <li key={index}>
                                      {source}
                                    </li>
                                  ))}
                                </ul>
                              </div>

                              <div>
                                <strong>Retrieved Chunks:</strong>{' '}
                                {msg.retrievedChunks}
                              </div>

                              {msg.incidentId && (
                                <div>
                                  <strong>Incident ID:</strong>{' '}
                                  {msg.incidentId}
                                </div>
                              )}

                            </div>

                          )}

                        </div>

                      ) : (

                        <div className="user-text">
                          {msg.text}
                        </div>

                      )}

                    </div>

                  </div>

                ))}

                {/* Loading Animation */}
                {isLoading && (

                  <div className="message-row assistant">

                    <div className="message-bubble">

                      <div className="typing-dots">
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                      </div>

                    </div>

                  </div>

                )}

                <div ref={messagesEndRef} />

              </div>

            </div>

            {/* Bottom Chat Input */}
            {renderPromptBox(false)}

          </>

        )}

      </main>

    </div>
  )
}