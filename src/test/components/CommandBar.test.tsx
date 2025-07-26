import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import CommandBar from '../../components/CommandBar'

describe('CommandBar Component', () => {
  const mockOnSubmit = vi.fn()

  beforeEach(() => {
    mockOnSubmit.mockClear()
  })

  it('renders input and submit button', () => {
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    expect(screen.getByPlaceholderText(/Type your command/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument()
  })

  it('calls onSubmit when form is submitted', async () => {
    const user = userEvent.setup()
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    const button = screen.getByRole('button', { name: /send/i })
    
    await user.type(input, 'test command')
    await user.click(button)
    
    expect(mockOnSubmit).toHaveBeenCalledWith('test command')
  })

  it('calls onSubmit when Enter key is pressed', async () => {
    const user = userEvent.setup()
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    
    await user.type(input, 'test command')
    await user.keyboard('{Enter}')
    
    expect(mockOnSubmit).toHaveBeenCalledWith('test command')
  })

  it('does not submit empty commands', async () => {
    const user = userEvent.setup()
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    const button = screen.getByRole('button', { name: /send/i })
    await user.click(button)
    
    expect(mockOnSubmit).not.toHaveBeenCalled()
  })

  it('trims whitespace from commands', async () => {
    const user = userEvent.setup()
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    const button = screen.getByRole('button', { name: /send/i })
    
    await user.type(input, '   test command   ')
    await user.click(button)
    
    expect(mockOnSubmit).toHaveBeenCalledWith('test command')
  })

  it('clears input after successful submission', async () => {
    const user = userEvent.setup()
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    const button = screen.getByRole('button', { name: /send/i })
    
    await user.type(input, 'test command')
    await user.click(button)
    
    expect(input).toHaveValue('')
  })

  it('disables form when loading', () => {
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={true} />)
    
    const input = screen.getByPlaceholderText(/Type your command/i)
    const button = screen.getByRole('button', { name: /Processing/i })
    
    expect(input).toBeDisabled()
    expect(button).toBeDisabled()
  })

  it('shows loading state on button', () => {
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={true} />)
    
    const button = screen.getByRole('button', { name: /Processing/i })
    expect(button).toHaveTextContent('Processing...')
  })

  it('shows not implemented alert for voice button', async () => {
    const user = userEvent.setup()
    
    // Mock window.alert
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
    
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    const voiceButton = screen.getByTitle('Voice input (not implemented)')
    await user.click(voiceButton)
    
    expect(alertSpy).toHaveBeenCalledWith('Feature not implemented yet')
    
    alertSpy.mockRestore()
  })

  it('shows not implemented alert for image button', async () => {
    const user = userEvent.setup()
    
    // Mock window.alert
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
    
    render(<CommandBar onSubmit={mockOnSubmit} isLoading={false} />)
    
    const imageButton = screen.getByTitle('Image input (not implemented)')
    await user.click(imageButton)
    
    expect(alertSpy).toHaveBeenCalledWith('Feature not implemented yet')
    
    alertSpy.mockRestore()
  })
})