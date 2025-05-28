# System Patterns - AI Website Builder Architecture

## Overall Architecture

### High-Level System Design

```
Frontend (React + Tailwind) ↔ Backend API (FastAPI) ↔ CrewAI Orchestrator ↔ AI Agents ↔ MCP Servers
                                        ↓
                                 Generated React Projects
```

### Core Components

#### 1. Frontend Layer (React + Tailwind)

- **User Interface**: Project specification forms and natural language input
- **Component Preview**: Real-time preview of generated components
- **Project Management**: Download, version control, and iteration management
- **Progress Tracking**: Visual feedback on agent collaboration progress

#### 2. Backend API Layer (FastAPI)

- **Request Processing**: Handle project generation requests
- **Status Management**: Track and report generation progress
- **File Operations**: Manage generated project files and assets
- **Error Handling**: Graceful error recovery and user feedback

#### 3. CrewAI Orchestration Layer

- **Agent Coordination**: Manage collaboration between specialized agents
- **Task Distribution**: Assign appropriate tasks to each agent
- **Process Management**: Ensure proper workflow execution
- **Quality Control**: Validate outputs and ensure consistency

#### 4. AI Agent Layer

- **Product Manager Agent**: Requirements analysis and project planning
- **UI/UX Designer Agent**: Design systems and component architecture
- **Software Engineer Agent**: Code generation and implementation

#### 5. MCP Server Integration

- **Filesystem Server**: File operations for component generation
- **Memory Server**: Context persistence and pattern storage
- **Fetch Server**: External content and inspiration gathering
- **Sequential Thinking**: Complex problem-solving workflows

## Agent Collaboration Patterns

### Sequential Workflow Pattern

```
User Input → Product Manager → UI/UX Designer → Software Engineer → Output
```

### Iterative Refinement Pattern

```
Initial Generation → User Feedback → Agent Collaboration → Refined Output → Repeat
```

### Parallel Processing Pattern

```
Requirements Analysis (PM) ↘
                           → Integration → Final Output
Design Planning (UX)      ↗
```

## Data Flow Architecture

### Request Processing Flow

1. **User Input**: Natural language description of desired application
2. **Natural Language Processing**: Parse and extract requirements from user description
3. **Agent Assignment**: Distribute tasks based on agent capabilities and application type
4. **Collaboration**: Agents work together with shared context to build simple React applications
5. **Generation**: Create React components using ShadCN/UI and basic state management
6. **Validation**: Quality checks and best practice verification for simple applications
7. **Output**: Complete simple React project ready for download

### Context Management

- **Shared Memory**: All agents access common project context
- **Agent-Specific Context**: Each agent maintains specialized knowledge
- **Persistent Storage**: Project history and user preferences
- **Real-time Updates**: Live synchronization during collaboration

## Component Generation Patterns

### React Component Structure

```typescript
// Generated component template with ShadCN integration
import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ComponentProps } from './types';

interface Props extends ComponentProps {
  // Agent-generated prop definitions
}

export const GeneratedComponent: React.FC<Props> = ({ ...props }) => {
  // Agent-generated implementation using ShadCN components
  return (
    <Card className="agent-generated-tailwind-classes">
      <CardHeader>
        <CardTitle>Agent-generated title</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Agent-generated JSX with ShadCN components */}
        <Button variant="default">Agent-generated button</Button>
      </CardContent>
    </Card>
  );
};

export default GeneratedComponent;
```

### File Organization Pattern

```
generated-project/
├── src/
│   ├── components/
│   │   ├── ui/           # Base UI components
│   │   ├── layout/       # Layout components
│   │   └── features/     # Feature-specific components
│   ├── pages/            # Page components
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utility functions
│   └── types/            # TypeScript definitions
├── public/               # Static assets
├── package.json          # Dependencies and scripts
└── README.md            # Generated documentation
```

## Integration Patterns

### MCP Server Communication

```python
# Pattern for MCP server integration
async def use_mcp_capability(server_name: str, tool_name: str, params: dict):
    try:
        result = await mcp_client.call_tool(server_name, tool_name, params)
        return result
    except Exception as e:
        # Graceful fallback handling
        return fallback_implementation(params)
```

### Agent Communication Protocol

```python
# Pattern for agent collaboration
class AgentMessage:
    sender: str
    recipient: str
    message_type: str
    content: dict
    context: dict

# Agents communicate through structured messages
async def agent_collaborate(message: AgentMessage):
    # Process message and generate response
    response = await process_agent_message(message)
    return response
```

## Error Handling Patterns

### Graceful Degradation

- **Primary Path**: Full agent collaboration with MCP enhancement
- **Fallback Path**: Basic generation without MCP servers
- **Emergency Path**: Template-based generation

### Error Recovery Strategies

1. **Retry Logic**: Automatic retry with exponential backoff
2. **Alternative Approaches**: Switch to different generation strategies
3. **User Notification**: Clear error messages with suggested actions
4. **Partial Success**: Deliver what can be generated successfully

## Security Patterns

### API Key Management

- Environment variable isolation
- Secure key rotation capabilities
- Rate limiting and usage monitoring

### Generated Code Safety

- Input sanitization and validation
- Code injection prevention
- Safe dependency management

## Performance Patterns

### Caching Strategies

- **Component Templates**: Cache common component patterns
- **Agent Responses**: Cache similar requirement analyses
- **MCP Results**: Cache external API responses

### Optimization Techniques

- **Parallel Processing**: Run independent agent tasks concurrently
- **Lazy Loading**: Load MCP servers on demand
- **Resource Pooling**: Reuse expensive resources across requests

## Extensibility Patterns

### Plugin Architecture

- **Agent Plugins**: Add new specialized agents
- **MCP Extensions**: Integrate additional MCP servers
- **Template Plugins**: Add new project templates
- **Export Plugins**: Support different output formats

### Configuration Management

- **Agent Behavior**: Configurable agent personalities and approaches
- **Generation Rules**: Customizable code generation patterns
- **Quality Standards**: Adjustable quality and complexity thresholds
