# Hard-Coded Force Deletion Utility

A Python utility for forcefully deleting files and directories with enhanced safety features.

## Features

- Force deletion of files and directories
- Handles locked files
- Bypasses permission issues
- Safety checks and confirmations
- Detailed operation logging
- Rich console output

## Requirements

```
rich
send2trash (optional for safe mode)
```

## Usage

```bash
python __init__.py target_path [--safe-mode]
```

## Safety Features

- Confirmation prompts
- Safe mode option
- Path validation
- System file protection
- Operation logging
- Undo capability (in safe mode)

## Deletion Modes

- Force delete
- Safe delete (moves to recycle bin)
- Recursive deletion
- Pattern-based deletion

## Error Handling

- Permission verification
- Path validation
- System file protection
- Operation logging
- Recovery options

## Additional Features

- Progress tracking
- Detailed logging
- Pattern matching
- Directory scanning
- Recovery options (when available)