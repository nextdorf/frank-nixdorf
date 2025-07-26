# Architecture Overview

"The Anything App" is a self-extending agentic AI application that generates functional plugins dynamically using Google Gemini API. The app can understand user requests and create interactive tools that integrate seamlessly into the workspace.

```
┌─────────────────────────────────────────────────────────────────┐
│                     The Anything App                           │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React/TypeScript)                                   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │  Document       │ │  Command Bar    │ │  Plugin Canvas  │   │
│  │  Editor         │ │                 │ │                 │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │  Plugin         │ │  Plugin         │ │  usePluginManager│   │
│  │  Sidebar        │ │  Toolbar        │ │  Hook           │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Backend API (FastAPI/Python)                                  │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │  Text Prompt    │ │  Plugin         │ │  Plugin         │   │
│  │  Endpoint       │ │  Generation     │ │  Management     │   │
│  │                 │ │  Endpoint       │ │  Endpoints      │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
│  ┌─────────────────┐ ┌─────────────────┐                       │
│  │  Gemini         │ │  Plugin         │                       │
│  │  Service        │ │  Service        │                       │
│  └─────────────────┘ └─────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Agent Library (Python)                                        │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │  Intent         │ │  Prompt         │ │  Media          │   │
│  │  Analyzer       │ │  Engineer       │ │  Handlers       │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
│  ┌─────────────────┐                                           │
│  │  Logging &      │                                           │
│  │  Observability  │                                           │
│  └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  External Services                                              │
│  ┌─────────────────┐ ┌─────────────────┐                       │
│  │  Google Gemini  │ │  File System    │                       │
│  │  API            │ │  Storage        │                       │
│  └─────────────────┘ └─────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. **Frontend Interface (React/TypeScript)**
- **Document Editor**: Markdown editor for content creation  
- **Command Bar**: Natural language input interface for user commands
- **Plugin Canvas**: Dynamic rendering area for generated plugins
- **Plugin Management**: Sidebar for plugin activation/deactivation
- **Plugin Toolbar**: Quick access to active plugin functions

### 2. **Backend Core (FastAPI/Python)**
- **Gemini Service**: Handles Google Gemini API integration for text generation
- **Plugin Service**: Manages plugin generation, storage, and retrieval
- **API Endpoints**: RESTful interface for frontend communication
- **CORS Middleware**: Cross-origin resource sharing configuration

### 3. **Agent Library**
- **Intent Analyzer**: Classifies user requests and extracts semantic meaning
- **Prompt Engineer**: Optimizes prompts for Gemini API interaction
- **Media Handlers**: Processes audio and image inputs (AudioHandler, ImageHandler)
- **Logging System**: Comprehensive observability with request tracking

### 4. **Plugin System**
- **Dynamic Generation**: Creates functional React components on-demand
- **Code Storage**: Persistent plugin storage with metadata
- **Runtime Integration**: Hot-loading of generated plugins into UI
- **Hardcoded Fallbacks**: Timer and calculator plugins as examples

### 5. **External Integrations**
- **Google Gemini API**: LLM service for natural language understanding and code generation
- **File System**: Plugin persistence and retrieval
- **Docker Environment**: Containerized deployment setup

## Agentic Behaviors

1. **Planning**: Intent analyzer determines plugin requirements from user input
2. **Tool Calling**: Gemini API generates functional JavaScript/React code
3. **Memory**: Plugin metadata and code stored for reuse and management
4. **Self-Extension**: App dynamically adds new capabilities based on user needs

## Data Flow

1. User enters command → Command Bar
2. Intent analysis → Agent Library  
3. Plugin generation request → Gemini Service
4. Code generation → Google Gemini API
5. Plugin storage → Plugin Service
6. UI integration → Plugin Canvas
7. User interaction → Active plugins
