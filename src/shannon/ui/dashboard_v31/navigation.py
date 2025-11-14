"""
Navigation Controller - Handle keyboard navigation between dashboard layers

Pure functional navigation: (key_event, current_state, snapshot) → new_state

Created: 2025-11-14
Part of: V3.1 Wave 1 (Navigation & State)
"""

import dataclasses
from typing import Optional

from .models import DashboardUIState, DashboardSnapshot, KeyEvent, AgentSnapshot


class NavigationController:
    """
    Controls navigation between dashboard layers

    Implements layer-specific keyboard handling with validation.
    Pure function - no side effects, just state transformations.

    Usage:
        controller = NavigationController()

        # User presses Enter
        key = KeyEvent('enter')
        new_state = controller.handle_key(key, current_state, snapshot)

        # new_state reflects navigation (e.g., layer 1 → 2)
    """

    def handle_key(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """
        Handle keyboard event and return new UI state

        Args:
            key: Keyboard event
            state: Current UI state
            snapshot: Current data snapshot (for validation)

        Returns:
            New UI state after applying navigation logic
        """
        # Route to layer-specific handler
        if state.current_layer == 1:
            return self._handle_layer1(key, state, snapshot)
        elif state.current_layer == 2:
            return self._handle_layer2(key, state, snapshot)
        elif state.current_layer == 3:
            return self._handle_layer3(key, state, snapshot)
        elif state.current_layer == 4:
            return self._handle_layer4(key, state, snapshot)

        return state

    def _handle_layer1(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """
        Handle Layer 1 (Session Overview) keyboard events

        Keys:
        - Enter: Navigate to Layer 2 (multi-agent) or Layer 3 (single agent)
        - h: Toggle help
        - q: Handled globally (quit)
        """
        if key.key == 'enter':
            # Multi-agent: go to agent list (Layer 2)
            if len(snapshot.agents) > 1:
                return dataclasses.replace(
                    state,
                    current_layer=2,
                    focused_agent_id=snapshot.agents[0].agent_id,
                    agent_selection_index=0
                )
            # Single agent: skip to agent detail (Layer 3)
            elif len(snapshot.agents) == 1:
                return dataclasses.replace(
                    state,
                    current_layer=3,
                    focused_agent_id=snapshot.agents[0].agent_id
                )
            # No agents: go to detail anyway (for single-process commands like analyze)
            else:
                return dataclasses.replace(state, current_layer=3)

        elif key.key == 'h':
            # Toggle help overlay
            return dataclasses.replace(state, show_help=not state.show_help)

        return state

    def _handle_layer2(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """
        Handle Layer 2 (Agent List) keyboard events

        Keys:
        - Enter: Navigate to Layer 3 for focused agent
        - Esc: Return to Layer 1
        - 1-9: Select agent by number
        - h: Toggle help
        """
        if key.key == 'enter':
            # Navigate to agent detail
            if state.focused_agent_id:
                return dataclasses.replace(state, current_layer=3)

        elif key.key == 'escape':
            # Return to session overview
            return dataclasses.replace(state, current_layer=1)

        elif key.is_number:
            # Select agent by number
            agent_num = int(key.key)
            if 0 < agent_num <= len(snapshot.agents):
                agent = snapshot.agents[agent_num - 1]  # Convert to 0-indexed
                return dataclasses.replace(
                    state,
                    focused_agent_id=agent.agent_id,
                    agent_selection_index=agent_num - 1
                )

        elif key.key == 'h':
            return dataclasses.replace(state, show_help=not state.show_help)

        return state

    def _handle_layer3(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """
        Handle Layer 3 (Agent Detail) keyboard events

        Keys:
        - Enter: Navigate to Layer 4 (message stream)
        - Esc: Return to Layer 2 or Layer 1
        - 1-9: Switch to different agent (stay on Layer 3)
        - t: Toggle tool history panel
        - c: Toggle context panel
        - h: Toggle help
        """
        if key.key == 'enter':
            # Navigate to message stream
            if state.can_navigate_to_layer_4(snapshot):
                return dataclasses.replace(
                    state,
                    current_layer=4,
                    message_scroll_offset=0,
                    message_selection_index=0
                )

        elif key.key == 'escape':
            # Return to agent list (if multi-agent) or session (if single)
            if len(snapshot.agents) > 1:
                return dataclasses.replace(state, current_layer=2)
            else:
                return dataclasses.replace(state, current_layer=1)

        elif key.is_number:
            # Switch to different agent (stay on Layer 3)
            agent_num = int(key.key)
            if 0 < agent_num <= len(snapshot.agents):
                agent = snapshot.agents[agent_num - 1]
                return dataclasses.replace(
                    state,
                    focused_agent_id=agent.agent_id,
                    agent_selection_index=agent_num - 1,
                    message_scroll_offset=0  # Reset scroll for new agent
                )

        elif key.key == 't':
            # Toggle tool history panel
            return dataclasses.replace(
                state,
                show_tool_history=not state.show_tool_history
            )

        elif key.key == 'c':
            # Toggle context panel
            return dataclasses.replace(
                state,
                show_context_panel=not state.show_context_panel
            )

        elif key.key == 'h':
            return dataclasses.replace(state, show_help=not state.show_help)

        return state

    def _handle_layer4(
        self,
        key: KeyEvent,
        state: DashboardUIState,
        snapshot: DashboardSnapshot
    ) -> DashboardUIState:
        """
        Handle Layer 4 (Message Stream) keyboard events

        Keys:
        - ↑/k: Scroll up one message
        - ↓/j: Scroll down one message
        - Page Up: Scroll up 10 messages
        - Page Down: Scroll down 10 messages
        - Home/g: Jump to first message
        - End/G: Jump to last message
        - Enter: Expand selected message
        - Space: Toggle thinking block
        - Esc: Return to Layer 3
        - 1-9: Switch agent (stay on Layer 4)
        - h: Toggle help
        """
        if not snapshot.messages:
            return state

        total_messages = snapshot.messages.total_messages
        max_offset = max(0, total_messages - state.viewport_height)

        if key.key in ('up', 'k'):
            # Scroll up one message
            new_offset = max(0, state.message_scroll_offset - 1)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key in ('down', 'j'):
            # Scroll down one message
            new_offset = min(max_offset, state.message_scroll_offset + 1)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key == 'page_up':
            # Scroll up 10 messages
            new_offset = max(0, state.message_scroll_offset - 10)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key == 'page_down':
            # Scroll down 10 messages
            new_offset = min(max_offset, state.message_scroll_offset + 10)
            return dataclasses.replace(state, message_scroll_offset=new_offset)

        elif key.key in ('home', 'g'):
            # Jump to start
            return dataclasses.replace(state, message_scroll_offset=0)

        elif key.key in ('end', 'G'):
            # Jump to end
            return dataclasses.replace(state, message_scroll_offset=max_offset)

        elif key.key == 'escape':
            # Return to agent detail
            return dataclasses.replace(state, current_layer=3)

        elif key.is_number:
            # Switch to different agent (stay on Layer 4)
            agent_num = int(key.key)
            if 0 < agent_num <= len(snapshot.agents):
                agent = snapshot.agents[agent_num - 1]
                return dataclasses.replace(
                    state,
                    focused_agent_id=agent.agent_id,
                    agent_selection_index=agent_num - 1,
                    message_scroll_offset=0  # Reset scroll for new agent
                )

        elif key.key == 'h':
            return dataclasses.replace(state, show_help=not state.show_help)

        # Enter and Space would be handled for message expansion/thinking toggle
        # (requires mutable message state, would be handled at dashboard level)

        return state
