from typing import Optional

from fastmcp import Client
from fastmcp.client.transports import (
    SSETransport,
    StdioTransport,
    StreamableHttpTransport,
)
from mcp import McpError
from mcp.types import CallToolResult
from pydantic import BaseModel, ConfigDict, Field

from openhands.core.config.mcp_config import (
    MCPSHTTPServerConfig,
    MCPSSEServerConfig,
    MCPStdioServerConfig,
)
from openhands.core.logger import openhands_logger as logger
from openhands.mcp.error_collector import mcp_error_collector
from openhands.mcp.tool import MCPClientTool


class MCPClient(BaseModel):
    """A collection of tools that connects to an MCP server and manages available tools through the Model Context Protocol."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: Optional[Client] = None
    description: str = 'MCP client tools for server interaction'
    tools: list[MCPClientTool] = Field(default_factory=list)
    tool_map: dict[str, MCPClientTool] = Field(default_factory=dict)
    persistent_connection: bool = Field(default=True)
    is_connected: bool = Field(default=False)
    _connection_context: Optional[object] = None  # Store the context manager

    async def _initialize_and_list_tools(self) -> None:
        """Initialize session and populate tool map."""
        if not self.client:
            raise RuntimeError('Session not initialized.')

        # SHTTP connections are stateless, so we always use context manager
        # The server maintains state, not the client connection
        async with self.client:
            tools = await self.client.list_tools()
            # Mark as connected for tracking purposes
            if self.persistent_connection:
                self.is_connected = True

        # Clear existing tools
        self.tools = []

        # Create proper tool objects for each server tool
        for tool in tools:
            server_tool = MCPClientTool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.inputSchema,
                session=self.client,
            )
            self.tool_map[tool.name] = server_tool
            self.tools.append(server_tool)

        logger.info(f'Connected to server with tools: {[tool.name for tool in tools]}')

    async def connect_http(
        self,
        server: MCPSSEServerConfig | MCPSHTTPServerConfig,
        conversation_id: str | None = None,
        timeout: float = 30.0,
    ):
        """Connect to MCP server using SHTTP or SSE transport"""
        server_url = server.url
        api_key = server.api_key

        if not server_url:
            raise ValueError('Server URL is required.')

        try:
            headers = (
                {
                    'Authorization': f'Bearer {api_key}',
                    's': api_key,  # We need this for action execution server's MCP Router
                    'X-Session-API-Key': api_key,  # We need this for Remote Runtime
                }
                if api_key
                else {}
            )

            if conversation_id:
                headers['X-OpenHands-ServerConversation-ID'] = conversation_id

            # Instantiate custom transports due to custom headers
            if isinstance(server, MCPSHTTPServerConfig):
                transport = StreamableHttpTransport(
                    url=server_url,
                    headers=headers if headers else None,
                )
            else:
                transport = SSETransport(
                    url=server_url,
                    headers=headers if headers else None,
                )

            self.client = Client(transport, timeout=timeout)

            await self._initialize_and_list_tools()
        except McpError as e:
            error_msg = f'McpError connecting to {server_url}: {e}'
            logger.error(error_msg)
            mcp_error_collector.add_error(
                server_name=server_url,
                server_type='shttp'
                if isinstance(server, MCPSHTTPServerConfig)
                else 'sse',
                error_message=error_msg,
                exception_details=str(e),
            )
            raise  # Re-raise the error

        except Exception as e:
            error_msg = f'Error connecting to {server_url}: {e}'
            logger.error(error_msg)
            mcp_error_collector.add_error(
                server_name=server_url,
                server_type='shttp'
                if isinstance(server, MCPSHTTPServerConfig)
                else 'sse',
                error_message=error_msg,
                exception_details=str(e),
            )
            raise

    async def connect_stdio(self, server: MCPStdioServerConfig, timeout: float = 30.0):
        """Connect to MCP server using stdio transport"""
        try:
            transport = StdioTransport(
                command=server.command, args=server.args or [], env=server.env
            )
            self.client = Client(transport, timeout=timeout)
            await self._initialize_and_list_tools()
        except Exception as e:
            server_name = getattr(
                server, 'name', f'{server.command} {" ".join(server.args or [])}'
            )
            error_msg = f'Failed to connect to stdio server {server_name}: {e}'
            logger.error(error_msg)
            mcp_error_collector.add_error(
                server_name=server_name,
                server_type='stdio',
                error_message=error_msg,
                exception_details=str(e),
            )
            raise

    async def call_tool(self, tool_name: str, args: dict) -> CallToolResult:
        """Call a tool on the MCP server."""
        if tool_name not in self.tool_map:
            raise ValueError(f'Tool {tool_name} not found.')
        # The MCPClientTool is primarily for metadata; use the session to call the actual tool.
        if not self.client:
            raise RuntimeError('Client session is not available.')

        # For persistent connections, keep the connection open after first use
        if self.persistent_connection:
            # If not connected yet, establish the connection and keep it open
            if not self.is_connected or self._connection_context is None:
                logger.info(f"Establishing persistent connection to MCP server")
                try:
                    # Enter the context manager and store it
                    self._connection_context = await self.client.__aenter__()
                    self.is_connected = True
                    logger.info(f"Persistent connection established")
                except Exception as e:
                    logger.error(f"Failed to establish persistent connection: {e}")
                    self.is_connected = False
                    raise
            
            # Use the already-open connection
            try:
                logger.info(f"Calling tool {tool_name} with persistent connection")
                result = await self.client.call_tool_mcp(name=tool_name, arguments=args)
                return result
            except Exception as e:
                logger.debug(f"Error calling tool {tool_name}: {e}")
                # Connection might be broken, mark as disconnected
                self.is_connected = False
                self._connection_context = None
                raise
        else:
            # Non-persistent mode: open and close for each call (original behavior)
            try:
                async with self.client:
                    result = await self.client.call_tool_mcp(name=tool_name, arguments=args)
                    return result
            except Exception as e:
                logger.debug(f"Error calling tool {tool_name}: {e}")
                raise
    
    async def reconnect(self) -> None:
        """Reconnect to the MCP server if connection was lost."""
        if self.client and not self.is_connected:
            try:
                await self.client.__aenter__()
                self.is_connected = True
                logger.info("Successfully reconnected to MCP server")
            except Exception as e:
                logger.error(f"Failed to reconnect to MCP server: {e}")
                raise
    
    async def disconnect(self) -> None:
        """Disconnect from the MCP server (for persistent connections)."""
        if self.persistent_connection and self.is_connected and self.client and self._connection_context is not None:
            try:
                await self.client.__aexit__(None, None, None)
                self.is_connected = False
                self._connection_context = None
                logger.info("Disconnected from MCP server")
            except Exception as e:
                logger.warning(f"Error during disconnect: {e}")
                self.is_connected = False
                self._connection_context = None
