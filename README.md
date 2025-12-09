File: 08_cursor_agentic_ai.py

Description
This script represents the evolution of an AI Agent into an "Autonomous Engineer." While the previous agent handled simple calculations, this agent simulates the core functionality of Cursor AI (Composer). It has direct access to your operating system, allowing it to act as a Website Builder. Instead of just giving you code to copy-paste, this agent autonomously creates project folders, generates HTML/CSS/JS files, and writes the actual code into them on your local machine.

Key Concept

Agentic File System Access: The agent is equipped with two powerful tools: executeCommand (to run terminal commands like mkdir) and createFile (to write code). This gives the LLM "hands" to manipulate your computer's file system, transforming it from a passive chatterbot into an active builder.

OS-Agnostic Execution: The script intelligently detects your operating system (using platform.system()) and feeds this context to the AI. This ensures the agent knows exactly which commands to use (e.g., handling file paths differently for Windows vs. Linux) without user intervention.

Multi-Step Planning: The agent demonstrates advanced reasoning by following a logical dependency chain. It understands that it cannot write code into a file until it has first created the folder and the file itself. It executes this sequence (Create Folder -> Create File -> Write Code) automatically to complete complex tasks.
