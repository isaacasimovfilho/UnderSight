/**
 * Component Tests
 */

import { describe, test, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'

// Simple button component for testing
function TestButton({ 
  children, 
  onClick, 
  disabled = false,
  variant = 'primary' 
}: { 
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary' | 'danger'
}) {
  const baseStyle = "px-4 py-2 rounded font-medium transition-colors"
  const variants = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    danger: "bg-red-500 text-white hover:bg-red-600"
  }
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variants[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      data-testid="test-button"
    >
      {children}
    </button>
  )
}

// Simple card component
function TestCard({ 
  title, 
  children,
  className = "" 
}: { 
  title: string
  children: React.ReactNode
  className?: string
}) {
  return (
    <div className={`border rounded-lg p-4 ${className}`} data-testid="test-card">
      <h2 className="text-xl font-bold mb-2">{title}</h2>
      <div>{children}</div>
    </div>
  )
}

// Simple input component
function TestInput({
  value,
  onChange,
  placeholder = "",
  type = "text",
  label = ""
}: {
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  placeholder?: string
  type?: string
  label?: string
}) {
  return (
    <div className="flex flex-col gap-1">
      {label && <label className="text-sm font-medium">{label}</label>}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="border rounded px-3 py-2"
        data-testid="test-input"
      />
    </div>
  )
}

describe('TestButton Component', () => {
  test('renders children correctly', () => {
    render(<TestButton>Click Me</TestButton>)
    expect(screen.getByTestId('test-button')).toHaveTextContent('Click Me')
  })

  test('calls onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<TestButton onClick={handleClick}>Click Me</TestButton>)
    
    fireEvent.click(screen.getByTestId('test-button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  test('does not call onClick when disabled', () => {
    const handleClick = vi.fn()
    render(<TestButton onClick={handleClick} disabled>Click Me</TestButton>)
    
    fireEvent.click(screen.getByTestId('test-button'))
    expect(handleClick).not.toHaveBeenCalled()
  })

  test('renders with primary variant', () => {
    render(<TestButton variant="primary">Primary</TestButton>)
    const button = screen.getByTestId('test-button')
    expect(button).toHaveClass('bg-blue-500')
  })

  test('renders with danger variant', () => {
    render(<TestButton variant="danger">Danger</TestButton>)
    const button = screen.getByTestId('test-button')
    expect(button).toHaveClass('bg-red-500')
  })
})

describe('TestCard Component', () => {
  test('renders title correctly', () => {
    render(<TestCard title="Test Title">Content</TestCard>)
    expect(screen.getByText('Test Title')).toBeInTheDocument()
  })

  test('renders children content', () => {
    render(<TestCard title="Title"><p>Child content</p></TestCard>)
    expect(screen.getByText('Child content')).toBeInTheDocument()
  })
})

describe('TestInput Component', () => {
  test('renders value correctly', () => {
    render(
      <TestInput 
        value="test value" 
        onChange={() => {}} 
        placeholder="Enter text"
      />
    )
    expect(screen.getByTestId('test-input')).toHaveValue('test value')
  })

  test('renders placeholder', () => {
    render(
      <TestInput 
        value="" 
        onChange={() => {}} 
        placeholder="Enter text"
      />
    )
    expect(screen.getByTestId('test-input')).toHaveAttribute('placeholder', 'Enter text')
  })

  test('renders label', () => {
    render(
      <TestInput 
        value="" 
        onChange={() => {}} 
        label="Username"
      />
    )
    expect(screen.getByText('Username')).toBeInTheDocument()
  })

  test('calls onChange when value changes', () => {
    const handleChange = vi.fn()
    render(
      <TestInput 
        value="" 
        onChange={handleChange} 
      />
    )
    
    fireEvent.change(screen.getByTestId('test-input'), { target: { value: 'new value' } })
    expect(handleChange).toHaveBeenCalled()
  })
})
