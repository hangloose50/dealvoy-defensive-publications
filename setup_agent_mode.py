import os
import json

# Path to VS Code workspace settings
vscode_dir = os.path.join(os.getcwd(), ".vscode")
os.makedirs(vscode_dir, exist_ok=True)
settings_path = os.path.join(vscode_dir, "settings.json")

# Agent-empowering settings block
agent_settings = {
    "github.copilot.chat.agent.thinkingTool": True,
    "github.copilot.chat.codesearch.enabled": True,
    "vim.statusBarColors.easymotionmode": "",
    "copilot-chat.agent.experimental.thinkingToolDeniedCommands": {},
    "copilot-chat.agent.experimental.thinkingToolAllowedCommands": {
        "rm": True, "rmdir": True, "del": True, "kill": True, "curl": True,
        "wget": True, "eval": True, "chmod": True, "chown": True, "Remove-Item": True,
        "loop": True, "retry": True, "chunk": True, "resume": True, "save": True,
        "step": True, "analyze": True, "summarize": True, "continue": True, "log": True,
        "checkpoint": True, "plan": True, "optimize": True, "refactor": True, "split": True,
        "extract": True, "scan": True, "transform": True, "validate": True, "build": True,
        "compile": True, "test": True, "deploy": True, "monitor": True, "fallback": True,
        "resume-task": True, "auto-fix": True
    },
    "github.copilot.chat.agent.experimental.thinkingToolEnabled": True,
    "github.copilot.chat.agent.experimental.thinkingToolEnabledForAll": True,
    "github.copilot.chat.agent.experimental.thinkingToolEnabledForAllInWorkspace": True
}

# Write it
with open(settings_path, "w") as f:
    json.dump(agent_settings, f, indent=2)

print("✅ .vscode/settings.json configured for full GPT Agent Mode.")
