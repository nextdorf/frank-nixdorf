import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import App from '../App'

// Mock Monaco Editor
vi.mock('@monaco-editor/react', () => ({
  default: ({ value, onChange }: { value: string; onChange: (value: string) => void }) => (
    <textarea
      data-testid="monaco-editor"
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
    />
  ),
  Editor: ({ value, onChange }: { value: string; onChange: (value: string) => void }) => (
    <textarea
      data-testid="monaco-editor"
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
    />
  )
}))

describe('App Component', () => {
  it('renders the app header', () => {
    render(<App />)
    expect(screen.getByText('The Anything App')).toBeInTheDocument()
  })

  it('renders with initial document content', () => {
    render(<App />)
    const editor = screen.getByTestId('monaco-editor') as HTMLTextAreaElement
    expect(editor.value).toContain('# Welcome to The Anything App')
  })

  it('handles command submission', async () => {
    const user = userEvent.setup()
    render(<App />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    const submitButton = screen.getByRole('button', { name: /send/i })
    
    await user.type(input, 'test command')
    await user.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/Mock AI response for testing/i)).toBeInTheDocument()
    })
  })

  it('shows loading state during command processing', async () => {
    const user = userEvent.setup()
    render(<App />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    const submitButton = screen.getByRole('button', { name: /send/i })
    
    await user.type(input, 'test command')
    await user.click(submitButton)
    
    // Should show loading state briefly
    expect(submitButton).toBeDisabled()
  })

  it('generates plugin for timer command', async () => {
    const user = userEvent.setup()
    render(<App />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    const submitButton = screen.getByRole('button', { name: /send/i })
    
    await user.type(input, 'Add a timer')
    await user.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/Mock AI response for testing/i)).toBeInTheDocument()
    })
    
    // Should have added a plugin to the sidebar
    await waitFor(() => {
      expect(screen.getAllByText('Test Plugin')).toHaveLength(2) // One in sidebar, one in canvas
    })
  })

  it('updates document content when editor changes', async () => {
    const user = userEvent.setup()
    render(<App />)
    
    const editor = screen.getByTestId('monaco-editor')
    await user.clear(editor)
    await user.type(editor, 'New content')
    
    expect(editor).toHaveValue('New content')
  })
})