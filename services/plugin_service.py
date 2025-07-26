import uuid
import json
import os
from typing import List, Optional, Dict
from models.responses import PluginGenerationResponse, PluginMetadata

class PluginService:
  def __init__(self):
    self.plugins_dir = 'generated_plugins'
    self.plugins_registry: Dict[str, PluginGenerationResponse] = {}
    os.makedirs(self.plugins_dir, exist_ok=True)
    self._initialize_hardcoded_plugins()
  
  def _initialize_hardcoded_plugins(self):
    timer_plugin = PluginGenerationResponse(
      pluginId='timer-001',
      code='''
import React, { useState, useEffect } from 'react';

export default function TimerPlugin() {
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    let interval = null;
    if (isActive) {
      interval = setInterval(() => {
        setSeconds(seconds => seconds + 1);
      }, 1000);
    } else if (!isActive && seconds !== 0) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive, seconds]);

  const toggle = () => {
    setIsActive(!isActive);
  };

  const reset = () => {
    setSeconds(0);
    setIsActive(false);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div style={{ padding: '16px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h3>Timer</h3>
      <div style={{ fontSize: '24px', fontFamily: 'monospace', margin: '16px 0' }}>
        {formatTime(seconds)}
      </div>
      <div>
        <button onClick={toggle} style={{ marginRight: '8px' }}>
          {isActive ? 'Pause' : 'Start'}
        </button>
        <button onClick={reset}>Reset</button>
      </div>
    </div>
  );
}
      '''.strip(),
      metadata=PluginMetadata(
        name='Timer',
        description='A simple timer that counts up from zero',
        version='1.0.0',
        type='widget',
        dependencies=['react']
      )
    )
    
    calculator_plugin = PluginGenerationResponse(
      pluginId='calculator-001',
      code='''
import React, { useState } from 'react';

export default function CalculatorPlugin() {
  const [display, setDisplay] = useState('0');
  const [previousValue, setPreviousValue] = useState(null);
  const [operation, setOperation] = useState(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);

  const inputNumber = (num) => {
    if (waitingForOperand) {
      setDisplay(String(num));
      setWaitingForOperand(false);
    } else {
      setDisplay(display === '0' ? String(num) : display + num);
    }
  };

  const inputOperation = (nextOperation) => {
    const inputValue = parseFloat(display);

    if (previousValue === null) {
      setPreviousValue(inputValue);
    } else if (operation) {
      const currentValue = previousValue || 0;
      const newValue = calculate(currentValue, inputValue, operation);

      setDisplay(String(newValue));
      setPreviousValue(newValue);
    }

    setWaitingForOperand(true);
    setOperation(nextOperation);
  };

  const calculate = (firstValue, secondValue, operation) => {
    switch (operation) {
      case '+': return firstValue + secondValue;
      case '-': return firstValue - secondValue;
      case '×': return firstValue * secondValue;
      case '÷': return firstValue / secondValue;
      case '=': return secondValue;
      default: return secondValue;
    }
  };

  const clear = () => {
    setDisplay('0');
    setPreviousValue(null);
    setOperation(null);
    setWaitingForOperand(false);
  };

  return (
    <div style={{ padding: '16px', border: '1px solid #ccc', borderRadius: '8px', maxWidth: '200px' }}>
      <h3>Calculator</h3>
      <div style={{ 
        backgroundColor: '#000', 
        color: '#fff', 
        padding: '8px', 
        textAlign: 'right', 
        marginBottom: '8px',
        fontSize: '18px',
        fontFamily: 'monospace'
      }}>
        {display}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '4px' }}>
        <button onClick={clear} style={{ gridColumn: 'span 2' }}>Clear</button>
        <button onClick={() => inputOperation('÷')}>÷</button>
        <button onClick={() => inputOperation('×')}>×</button>
        
        <button onClick={() => inputNumber(7)}>7</button>
        <button onClick={() => inputNumber(8)}>8</button>
        <button onClick={() => inputNumber(9)}>9</button>
        <button onClick={() => inputOperation('-')}>-</button>
        
        <button onClick={() => inputNumber(4)}>4</button>
        <button onClick={() => inputNumber(5)}>5</button>
        <button onClick={() => inputNumber(6)}>6</button>
        <button onClick={() => inputOperation('+')}>+</button>
        
        <button onClick={() => inputNumber(1)}>1</button>
        <button onClick={() => inputNumber(2)}>2</button>
        <button onClick={() => inputNumber(3)}>3</button>
        <button onClick={() => inputOperation('=')} style={{ gridRow: 'span 2' }}>=</button>
        
        <button onClick={() => inputNumber(0)} style={{ gridColumn: 'span 2' }}>0</button>
        <button onClick={() => inputNumber('.')}>.</button>
      </div>
    </div>
  );
}
      '''.strip(),
      metadata=PluginMetadata(
        name='Calculator',
        description='A basic calculator for arithmetic operations',
        version='1.0.0',
        type='widget',
        dependencies=['react']
      )
    )
    
    self.plugins_registry[timer_plugin.pluginId] = timer_plugin
    self.plugins_registry[calculator_plugin.pluginId] = calculator_plugin

  async def generate_plugin(self, description: str, user_id: Optional[str] = None) -> PluginGenerationResponse:
    description_lower = description.lower()
    
    if 'timer' in description_lower:
      return self.plugins_registry['timer-001']
    elif 'calculator' in description_lower or 'calc' in description_lower:
      return self.plugins_registry['calculator-001']
    else:
      plugin_id = str(uuid.uuid4())
      return PluginGenerationResponse(
        pluginId=plugin_id,
        code='// Plugin generation for custom requests not implemented yet',
        metadata=PluginMetadata(
          name='Custom Plugin',
          description=f'Generated for: {description}',
          version='1.0.0',
          type='component'
        )
      )

  def list_all_plugins(self) -> List[PluginGenerationResponse]:
    return list(self.plugins_registry.values())

  def get_plugin_code(self, plugin_id: str) -> Optional[str]:
    plugin = self.plugins_registry.get(plugin_id)
    return plugin.code if plugin else None

  def save_plugin_to_file(self, plugin_id: str, code: str) -> str:
    file_path = os.path.join(self.plugins_dir, f'{plugin_id}.js')
    with open(file_path, 'w') as f:
      f.write(code)
    return file_path