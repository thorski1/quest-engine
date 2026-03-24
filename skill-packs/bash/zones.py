"""
zones.py - All zone and challenge data for Terminal Quest
"""

ZONES = {
    "antechamber": {
        "id": "antechamber",
        "name": "The Jack Node",
        "subtitle": "Shell Navigation",
        "color": "cyan",
        "icon": "⚡",
        "commands": ["ls", "cd", "pwd", "mkdir", "rmdir"],
        "challenges": [
            {
                "id": "antech_1",
                "type": "quiz",
                "title": "First Signal",
                "flavor": "The terminal is live. The cursor blinks. Somewhere in this directory is the data you need. What do you run to see what's here?",
                "lesson": (
                    "ls — lists the contents of a directory.\n\n"
                    "Syntax: ls [flags] [directory]\n\n"
                    "Common flags:\n"
                    "  -l   long format (permissions, size, date)\n"
                    "  -a   show hidden files (dotfiles)\n"
                    "  -h   human-readable file sizes\n\n"
                    "Example: ls /home/user    → lists files in /home/user"
                ),
                "question": "What command lists the contents of the current directory?",
                "answers": ["ls"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's a two-letter command.",
                    "Think 'list'. Now abbreviate it.",
                    "The answer is: ls",
                ],
            },
            {
                "id": "antech_2",
                "type": "quiz",
                "title": "Position Confirmed",
                "flavor": "The monitoring system wants to know where you are. You want to know first. What prints your exact location in the filesystem?",
                "lesson": (
                    "pwd — prints the full path of your current working directory.\n\n"
                    "Syntax: pwd\n\n"
                    "Common flags:\n"
                    "  -L   use logical path (follows symlinks, default)\n"
                    "  -P   use physical path (resolves symlinks)\n\n"
                    "Example: pwd    → /home/user/projects"
                ),
                "question": "What command prints your current working directory?",
                "answers": ["pwd"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It stands for 'Print Working Directory'.",
                    "Three letters: P-W-D.",
                    "The answer is: pwd",
                ],
            },
            {
                "id": "antech_3",
                "type": "quiz",
                "title": "Lateral Movement",
                "flavor": "The data isn't in this directory. It never is. One command lets you move through the filesystem without ever touching a mouse.",
                "lesson": (
                    "cd — changes the current working directory.\n\n"
                    "Syntax: cd [directory]\n\n"
                    "Special paths:\n"
                    "  cd ~       go to your home directory\n"
                    "  cd ..      go up one level (parent directory)\n"
                    "  cd -       return to the previous directory\n\n"
                    "Example: cd /etc    → moves into the /etc directory"
                ),
                "question": "What command do you use to change directories?",
                "answers": ["cd"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's 2 letters.",
                    "Think 'Change Directory'.",
                    "The answer is: cd",
                ],
            },
            {
                "id": "antech_4",
                "type": "flag_quiz",
                "title": "Dark Files",
                "flavor": "The corps hide their most sensitive configs as dotfiles — hidden by default, invisible to anyone who doesn't know the flag. What reveals them?",
                "lesson": (
                    "Flags modify how a command behaves. For ls, flags are added after the command name.\n\n"
                    "Hidden files (dotfiles) start with a dot, e.g. .bashrc or .gitignore.\n"
                    "By default, ls does not show them.\n\n"
                    "  -a   show ALL files, including hidden ones\n"
                    "  -A   like -a, but excludes . and ..\n\n"
                    "Example: ls -a    → shows .bashrc, .ssh, and other hidden files"
                ),
                "question": "What flag do you add to 'ls' to show hidden files (dotfiles)?",
                "answers": ["-a", "-la", "-al", "-lah", "-lA", "--all"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It's a single letter flag.",
                    "Think 'all'.",
                    "The answer is: -a (or -la, -al)",
                ],
            },
            {
                "id": "antech_5",
                "type": "live",
                "title": "Allocate Space",
                "flavor": "You need a staging directory. The exfil operation doesn't work without somewhere to stage the data. Create one.",
                "lesson": (
                    "mkdir — creates a new directory.\n\n"
                    "Syntax: mkdir [flags] directory_name\n\n"
                    "Common flags:\n"
                    "  -p   create parent directories as needed (no error if exists)\n"
                    "  -v   verbose — print each directory as it is created\n\n"
                    "Example: mkdir expedition    → creates a directory named 'expedition'"
                ),
                "question": "Create a directory called 'expedition' in the current sandbox directory.",
                "setup": {
                    "files": {},
                    "dirs": [],
                },
                "validation": {
                    "type": "dir_exists",
                    "target": "expedition",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "The command is 'mkdir'.",
                    "Try: mkdir expedition",
                    "The full command is: mkdir expedition",
                ],
            },
            {
                "id": "antech_boss",
                "type": "live",
                "title": "BOSS: Security Sweep",
                "flavor": "The passive monitor flagged an anomaly. You have thirty seconds of cover before the active scan starts. Create the directory structure and disappear.",
                "lesson": (
                    "mkdir -p — creates a full directory path in a single command.\n\n"
                    "Syntax: mkdir -p path/to/nested/directory\n\n"
                    "Without -p, mkdir fails if a parent directory does not exist.\n"
                    "With -p, it creates all missing directories along the path.\n\n"
                    "Example: mkdir -p ruins/inner_chamber    → creates 'ruins' and then 'inner_chamber' inside it"
                ),
                "question": (
                    "The Guardian demands a test of navigation mastery:\n"
                    "Create a directory called 'ruins', then inside it create 'inner_chamber'.\n"
                    "(Hint: there's a flag that lets you create nested directories in one step)"
                ),
                "setup": {
                    "files": {},
                    "dirs": [],
                },
                "validation": {
                    "type": "dir_exists",
                    "target": "ruins/inner_chamber",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need to create a directory inside another directory.",
                    "Try: mkdir -p ruins/inner_chamber",
                    "The full command is: mkdir -p ruins/inner_chamber",
                ],
            },
        ],
    },

    "archive_vaults": {
        "id": "archive_vaults",
        "name": "The Dead Drop Vaults",
        "subtitle": "File Operations",
        "color": "yellow",
        "icon": "📚",
        "commands": ["cat", "cp", "mv", "rm", "touch", "file"],
        "challenges": [
            {
                "id": "arch_1",
                "type": "live",
                "title": "Allocate File",
                "flavor": "Before you write to it, you need to create it. An empty placeholder. The corps' monitoring systems log file creation timestamps — that's useful. Create one.",
                "lesson": (
                    "touch — creates an empty file, or updates a file's timestamps if it already exists.\n\n"
                    "Syntax: touch [flags] filename\n\n"
                    "Common flags:\n"
                    "  -a   update only the access time\n"
                    "  -m   update only the modification time\n\n"
                    "Example: touch scroll.txt    → creates an empty file called scroll.txt"
                ),
                "question": "Create an empty file called 'scroll.txt' in the sandbox.",
                "setup": {"files": {}, "dirs": []},
                "validation": {"type": "file_exists", "target": "scroll.txt"},
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "The command to create empty files is 'touch'.",
                    "Try: touch scroll.txt",
                    "The answer is: touch scroll.txt",
                ],
            },
            {
                "id": "arch_2",
                "type": "live",
                "title": "Extract the Intercept",
                "flavor": "There's a file on this server. You don't have time to open an editor. You need its contents dumped to the terminal. Now.",
                "lesson": (
                    "cat — concatenates and displays file contents to the terminal.\n\n"
                    "Syntax: cat [flags] file(s)\n\n"
                    "Common flags:\n"
                    "  -n   number all output lines\n"
                    "  -A   show non-printing characters (tabs, line endings)\n\n"
                    "Example: cat ancient_text.txt    → prints the contents of ancient_text.txt"
                ),
                "question": "Display the contents of 'ancient_text.txt' to the terminal.",
                "setup": {
                    "files": {"ancient_text.txt": "In the beginning was the command line.\nAnd it was good.\n"},
                    "dirs": [],
                },
                "validation": {
                    "type": "output_contains",
                    "expected": "In the beginning was the command line.",
                },
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "The command is 'cat' — short for concatenate.",
                    "Try: cat ancient_text.txt",
                    "The answer is: cat ancient_text.txt",
                ],
            },
            {
                "id": "arch_3",
                "type": "live",
                "title": "Stage a Copy",
                "flavor": "Never touch the original. Cardinal rule of intrusion work. Copy the file, work on the copy. If anything goes wrong, the original is clean.",
                "lesson": (
                    "cp — copies files or directories from one location to another.\n\n"
                    "Syntax: cp [flags] source destination\n\n"
                    "Common flags:\n"
                    "  -r   recursive (required to copy directories)\n"
                    "  -i   interactive — prompt before overwriting\n"
                    "  -v   verbose — show files as they are copied\n\n"
                    "Example: cp artifact.dat artifact_backup.dat    → creates a copy with a new name"
                ),
                "question": "Copy 'artifact.dat' to a new file called 'artifact_backup.dat'.",
                "setup": {
                    "files": {"artifact.dat": "ARTIFACT DATA: 0xDEADBEEF\n"},
                    "dirs": [],
                },
                "validation": {"type": "file_exists", "target": "artifact_backup.dat"},
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "The copy command is 'cp'.",
                    "Syntax: cp <source> <destination>",
                    "The answer is: cp artifact.dat artifact_backup.dat",
                ],
            },
            {
                "id": "arch_4",
                "type": "live",
                "title": "Cover Your Tracks",
                "flavor": "The file has the wrong name — it'll get flagged in the next audit sweep. Rename it to something that looks like it belongs here.",
                "lesson": (
                    "mv — moves or renames files and directories.\n\n"
                    "Syntax: mv [flags] source destination\n\n"
                    "Common flags:\n"
                    "  -i   interactive — prompt before overwriting\n"
                    "  -v   verbose — show what is being moved\n"
                    "  -n   no-clobber — do not overwrite existing files\n\n"
                    "Example: mv wrongname.txt correctname.txt    → renames the file in place"
                ),
                "question": "Rename 'wrongname.txt' to 'correctname.txt'.",
                "setup": {
                    "files": {"wrongname.txt": "I have the wrong name!\n"},
                    "dirs": [],
                },
                "validation": {"type": "file_exists", "target": "correctname.txt"},
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "In bash, renaming uses the 'mv' (move) command.",
                    "Syntax: mv <old_name> <new_name>",
                    "The answer is: mv wrongname.txt correctname.txt",
                ],
            },
            {
                "id": "arch_5",
                "type": "live",
                "title": "Wipe the Evidence",
                "flavor": "That file is a liability. It links back to you. Delete it — and remember: rm has no undo button. That's the point.",
                "lesson": (
                    "rm — removes (deletes) files or directories. There is no trash — deletion is permanent.\n\n"
                    "Syntax: rm [flags] file(s)\n\n"
                    "Common flags:\n"
                    "  -r   recursive — delete directories and their contents\n"
                    "  -f   force — ignore nonexistent files, no prompts\n"
                    "  -i   interactive — prompt before each deletion\n\n"
                    "Example: rm heresy.txt    → permanently deletes heresy.txt"
                ),
                "question": "Delete the file called 'heresy.txt'.",
                "setup": {
                    "files": {"heresy.txt": "This file should not exist.\n"},
                    "dirs": [],
                },
                "validation": {"type": "file_missing", "target": "heresy.txt"},
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "The remove command is 'rm'.",
                    "Try: rm heresy.txt",
                    "The answer is: rm heresy.txt",
                ],
            },
            {
                "id": "arch_boss",
                "type": "live",
                "title": "BOSS: The Dead Drop Protocol",
                "flavor": "Multi-step extraction. No room for mistakes. The vault's integrity checker runs every ninety seconds. You have one pass to get this right.",
                "lesson": (
                    "Chaining commands — run multiple commands in sequence using && or ;.\n\n"
                    "  cmd1 && cmd2   runs cmd2 only if cmd1 succeeds\n"
                    "  cmd1 ; cmd2    runs cmd2 regardless of cmd1's result\n\n"
                    "This challenge uses mkdir, touch, and cp together:\n\n"
                    "Example: mkdir archive && touch archive/manifest.txt && cp source.dat archive/"
                ),
                "question": (
                    "Multi-step challenge:\n"
                    "1. Create a directory called 'archive'\n"
                    "2. Create a file called 'manifest.txt' inside it\n"
                    "3. Copy 'source.dat' into the archive directory\n\n"
                    "You can use semicolons or && to chain commands."
                ),
                "setup": {
                    "files": {"source.dat": "CLASSIFIED ARCHIVE DATA\n"},
                    "dirs": [],
                },
                "validation": {
                    "type": "multi",
                    "checks": [
                        {"type": "dir_exists", "target": "archive"},
                        {"type": "file_exists", "target": "archive/manifest.txt"},
                        {"type": "file_exists", "target": "archive/source.dat"},
                    ],
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need mkdir, touch, and cp.",
                    "Try: mkdir archive && touch archive/manifest.txt && cp source.dat archive/",
                    "Full command: mkdir archive && touch archive/manifest.txt && cp source.dat archive/",
                ],
            },
        ],
    },

    "oracle_library": {
        "id": "oracle_library",
        "name": "The Signal Broker",
        "subtitle": "Intelligence Extraction",
        "color": "magenta",
        "icon": "📡",
        "commands": ["grep", "find", "sort", "uniq", "wc"],
        "challenges": [
            {
                "id": "oracle_1",
                "type": "quiz",
                "title": "Pattern Match",
                "flavor": "There's signal in this noise. Megabytes of corporate logs and exactly one line that matters. What tool extracts it?",
                "lesson": (
                    "grep — searches for lines matching a pattern in files or piped input.\n\n"
                    "Syntax: grep [flags] pattern [file...]\n\n"
                    "Common flags:\n"
                    "  -i   case-insensitive search\n"
                    "  -r   recursive (search through directories)\n"
                    "  -n   show line numbers\n"
                    "  -v   invert match (show lines that do NOT match)\n\n"
                    "Example: grep 'error' system.log    → prints every line containing 'error'"
                ),
                "question": "What command searches for patterns within files?",
                "answers": ["grep"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It stands for 'Global Regular Expression Print'.",
                    "It's a 4-letter command starting with 'g'.",
                    "The answer is: grep",
                ],
            },
            {
                "id": "oracle_2",
                "type": "live",
                "title": "Extract the Signal",
                "flavor": "The intercept file is full of noise. The word you need is in there three times, buried in hundreds of lines. Pull it out.",
                "lesson": (
                    "grep — filters lines from a file that contain a given word or pattern.\n\n"
                    "Syntax: grep pattern filename\n\n"
                    "Common flags:\n"
                    "  -i   ignore case\n"
                    "  -c   count matching lines instead of printing them\n"
                    "  -l   print only filenames that contain a match\n\n"
                    "Example: grep prophecy scrolls.txt    → prints all lines containing 'prophecy'"
                ),
                "question": "Find all lines containing the word 'prophecy' in 'scrolls.txt'.",
                "setup": {
                    "files": {
                        "scrolls.txt": (
                            "The beginning was the command line.\n"
                            "A prophecy was written in bash.\n"
                            "Many artifacts were found.\n"
                            "The prophecy speaks of a grandmaster.\n"
                            "Regular expressions hold the key.\n"
                        )
                    },
                    "dirs": [],
                },
                "validation": {
                    "type": "output_contains",
                    "expected": "prophecy",
                },
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Use grep to search for a pattern.",
                    "Syntax: grep <pattern> <file>",
                    "The answer is: grep prophecy scrolls.txt",
                ],
            },
            {
                "id": "oracle_3",
                "type": "live",
                "title": "Quantify the Breach",
                "flavor": "The client wants numbers. How many log entries? How many lines compromised? Don't read it — count it.",
                "lesson": (
                    "wc — counts lines, words, and bytes in a file or from piped input.\n\n"
                    "Syntax: wc [flags] [file...]\n\n"
                    "Common flags:\n"
                    "  -l   count lines only\n"
                    "  -w   count words only\n"
                    "  -c   count bytes only\n"
                    "  -m   count characters only\n\n"
                    "Example: wc -l tome.txt    → prints the number of lines in tome.txt"
                ),
                "question": "Count the number of lines in 'tome.txt'.",
                "setup": {
                    "files": {
                        "tome.txt": "line one\nline two\nline three\nline four\nline five\n"
                    },
                    "dirs": [],
                },
                "validation": {
                    "type": "output_contains",
                    "expected": "5",
                },
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "The word-count command is 'wc'. Use the -l flag for lines.",
                    "Try: wc -l tome.txt",
                    "The answer is: wc -l tome.txt",
                ],
            },
            {
                "id": "oracle_4",
                "type": "live",
                "title": "Sort the Feed",
                "flavor": "The data dump came out of order. You need it alphabetical before you can do anything useful with it. Run it through the sorter.",
                "lesson": (
                    "sort — sorts lines of text alphabetically or numerically.\n\n"
                    "Syntax: sort [flags] [file...]\n\n"
                    "Common flags:\n"
                    "  -r   reverse order (Z to A, or largest to smallest)\n"
                    "  -n   numeric sort (treat values as numbers)\n"
                    "  -u   unique — remove duplicate lines after sorting\n\n"
                    "Example: sort chaos.txt    → prints lines of chaos.txt in alphabetical order"
                ),
                "question": "Sort the contents of 'chaos.txt' alphabetically and display them.",
                "setup": {
                    "files": {
                        "chaos.txt": "zebra\napple\nmango\nbanana\nkiwi\n"
                    },
                    "dirs": [],
                },
                "validation": {
                    "type": "output_contains",
                    "expected": "apple",
                },
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "The sort command arranges lines alphabetically.",
                    "Try: sort chaos.txt",
                    "The answer is: sort chaos.txt",
                ],
            },
            {
                "id": "oracle_5",
                "type": "live",
                "title": "Hunt the Log",
                "flavor": "The logs are scattered through subdirectories the way the corps scatter blame — everywhere and nowhere. Hunt them down by extension.",
                "lesson": (
                    "find — walks a directory tree and finds files matching given criteria.\n\n"
                    "Syntax: find [path] [expression]\n\n"
                    "Common flags:\n"
                    "  -name pattern   match by filename (supports wildcards like *.log)\n"
                    "  -type f         match only regular files\n"
                    "  -type d         match only directories\n"
                    "  -mtime -1       modified in the last 1 day\n\n"
                    "Example: find . -name '*.log'    → finds all .log files from the current directory down"
                ),
                "question": "Find all files ending in '.log' in the current directory and subdirectories.",
                "setup": {
                    "files": {
                        "system.log": "LOG: system started\n",
                        "notes.txt": "not a log\n",
                        "subdir/error.log": "LOG: error occurred\n",
                    },
                    "dirs": ["subdir"],
                },
                "validation": {
                    "type": "output_contains",
                    "expected": ".log",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use the 'find' command.",
                    "Syntax: find <path> -name <pattern>",
                    "The answer is: find . -name '*.log'",
                ],
            },
            {
                "id": "oracle_boss",
                "type": "live",
                "title": "BOSS: Deduplicate the Feed",
                "flavor": "The data stream is poisoned with duplicates — a classic corp obfuscation technique. Extract only unique entries, sorted, counted. Clean signal only.",
                "lesson": (
                    "uniq — filters out consecutive duplicate lines. Usually used after sort.\n\n"
                    "Syntax: uniq [flags] [file]\n\n"
                    "Common flags:\n"
                    "  -c   prefix lines with the count of occurrences\n"
                    "  -d   only print duplicate lines\n"
                    "  -u   only print unique (non-duplicate) lines\n\n"
                    "Example: sort data.txt | uniq | wc -l    → counts distinct lines in data.txt"
                ),
                "question": (
                    "The Oracle's challenge:\n"
                    "Find all unique words that appear in 'data.txt',\n"
                    "sort them, and count how many unique lines exist."
                ),
                "setup": {
                    "files": {
                        "data.txt": "alpha\nbeta\nalpha\ngamma\nbeta\ndelta\ngamma\nalpha\n"
                    },
                    "dirs": [],
                },
                "validation": {
                    "type": "output_contains",
                    "expected": "4",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need to chain sort, uniq, and wc -l.",
                    "Use pipes: sort data.txt | uniq | wc -l",
                    "The answer is: sort data.txt | uniq | wc -l",
                ],
            },
        ],
    },

    "pipe_sanctum": {
        "id": "pipe_sanctum",
        "name": "The Pipe Works",
        "subtitle": "Signal Routing",
        "color": "blue",
        "icon": "🔌",
        "commands": ["|", ">", ">>", "<", "tee", "xargs"],
        "challenges": [
            {
                "id": "pipe_1",
                "type": "quiz",
                "title": "The Connector",
                "flavor": "One character. Invented in 1973. The corps have spent fifty years trying to abstract away from it. What routes output from one command into the next?",
                "lesson": (
                    "| (pipe) — sends the output of one command as input to the next command.\n\n"
                    "Syntax: command1 | command2\n\n"
                    "Pipes let you chain tools together so data flows from left to right.\n"
                    "Each command reads from the previous one's output.\n\n"
                    "Example: ls | grep '.txt'    → lists files, then filters for only .txt files"
                ),
                "question": "What symbol is used to pipe the output of one command into another?",
                "answers": ["|", "pipe"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's a single character, found above the backslash on most keyboards.",
                    "It's called the 'pipe' symbol.",
                    "The answer is: |",
                ],
            },
            {
                "id": "pipe_2",
                "type": "live",
                "title": "Route the Signal",
                "flavor": "The directory has noise in it. You need only the text files. Chain ls and grep — don't write to disk, don't open an editor. Just route it.",
                "lesson": (
                    "| (pipe) — connects commands so the output of one feeds directly into the next.\n\n"
                    "Syntax: command1 | command2 | command3 ...\n\n"
                    "You can chain as many commands as needed.\n"
                    "No intermediate files are created — data flows in memory.\n\n"
                    "Example: ls | grep '.txt'    → shows only filenames that contain '.txt'"
                ),
                "question": "List all files in the current directory and pipe the output to 'grep' to filter only '.txt' files.",
                "setup": {
                    "files": {
                        "readme.txt": "read me\n",
                        "data.csv": "data\n",
                        "notes.txt": "notes\n",
                        "binary.bin": "binary\n",
                    },
                    "dirs": [],
                },
                "validation": {
                    "type": "output_contains",
                    "expected": ".txt",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use ls and pipe to grep.",
                    "Try: ls | grep .txt",
                    "The answer is: ls | grep .txt",
                ],
            },
            {
                "id": "pipe_3",
                "type": "live",
                "title": "Write to Disk",
                "flavor": "Terminal output is ephemeral. One scroll and it's gone. Capture it — redirect it into a file so it survives the session.",
                "lesson": (
                    "> (redirect) — writes command output to a file, overwriting any existing content.\n\n"
                    "Syntax: command > filename\n\n"
                    "Related operators:\n"
                    "  >>   append to a file instead of overwriting\n"
                    "  2>   redirect error output (stderr) to a file\n\n"
                    "Example: echo 'EXCAVATED DATA' > output.txt    → creates output.txt with that text"
                ),
                "question": "Write the text 'EXCAVATED DATA' into a file called 'output.txt' using redirection.",
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "file_contains",
                    "target": "output.txt",
                    "expected": "EXCAVATED DATA",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use echo with the > redirection operator.",
                    "Try: echo 'EXCAVATED DATA' > output.txt",
                    "The answer is: echo 'EXCAVATED DATA' > output.txt",
                ],
            },
            {
                "id": "pipe_4",
                "type": "live",
                "title": "Append the Entry",
                "flavor": "> destroys what was there. >> preserves it. You're updating a live log — wrong operator and the entire operation history is gone.",
                "lesson": (
                    ">> (append redirect) — adds output to the end of a file without erasing existing content.\n\n"
                    "Syntax: command >> filename\n\n"
                    "Comparison:\n"
                    "  >    overwrites the file each time (destructive)\n"
                    "  >>   appends to the file (preserves existing content)\n\n"
                    "Example: echo 'SECOND ENTRY' >> log.txt    → adds a line to log.txt without erasing it"
                ),
                "question": "Append the line 'SECOND ENTRY' to 'log.txt' without overwriting it.",
                "setup": {
                    "files": {"log.txt": "FIRST ENTRY\n"},
                    "dirs": [],
                },
                "validation": {
                    "type": "file_contains",
                    "target": "log.txt",
                    "expected": "FIRST ENTRY",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use >> to append instead of overwrite.",
                    "Try: echo 'SECOND ENTRY' >> log.txt",
                    "The answer is: echo 'SECOND ENTRY' >> log.txt",
                ],
            },
            {
                "id": "pipe_5",
                "type": "fill_blank",
                "title": "Split the Stream",
                "flavor": "You need to watch the output AND save it. Not one or the other. One command splits the stream — screen and file simultaneously.",
                "lesson": (
                    "tee — reads from stdin and writes to both stdout (the screen) and a file simultaneously.\n\n"
                    "Syntax: command | tee [flags] filename\n\n"
                    "Common flags:\n"
                    "  -a   append to the file instead of overwriting it\n\n"
                    "Named after the T-shaped pipe fitting that splits flow in two directions.\n\n"
                    "Example: echo 'SACRED TEXT' | tee record.txt    → prints to screen AND saves to record.txt"
                ),
                "question": "Complete this command to both display output AND save it to 'record.txt':\n\necho 'SACRED TEXT' | ___ record.txt",
                "answers": ["tee"],
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "The command is named after a T-shaped pipe fitting.",
                    "It starts with 't'.",
                    "The answer is: tee",
                ],
            },
            {
                "id": "pipe_boss",
                "type": "live",
                "title": "BOSS: The Full Pipeline",
                "flavor": "One command chain. No intermediate files. List, filter, count, save. The monitoring system won't wait for you to figure this out step by step.",
                "lesson": (
                    "Combining pipes and redirection — chain | and > to process and save data in one command.\n\n"
                    "Syntax: cmd1 | cmd2 | cmd3 > output_file\n\n"
                    "Data flows left to right through each pipe.\n"
                    "The final > captures the end result into a file.\n\n"
                    "Example: ls | grep '.txt' | wc -l > count.txt    → counts .txt files and saves the number"
                ),
                "question": (
                    "Build a pipeline that:\n"
                    "1. Lists all files in the sandbox\n"
                    "2. Filters for only .txt files\n"
                    "3. Counts how many there are\n"
                    "4. Saves the count to 'count.txt'"
                ),
                "setup": {
                    "files": {
                        "alpha.txt": "a\n",
                        "beta.txt": "b\n",
                        "gamma.txt": "c\n",
                        "data.bin": "binary\n",
                        "config.cfg": "config\n",
                    },
                    "dirs": [],
                },
                "validation": {
                    "type": "file_exists",
                    "target": "count.txt",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Chain: ls | grep | wc -l and redirect to a file.",
                    "Try: ls | grep '.txt' | wc -l > count.txt",
                    "The answer is: ls | grep '.txt' | wc -l > count.txt",
                ],
            },
        ],
    },

    "process_catacombs": {
        "id": "process_catacombs",
        "name": "The Ghost Stack",
        "subtitle": "Process Control",
        "color": "red",
        "icon": "👾",
        "commands": ["ps", "kill", "jobs", "bg", "fg", "top"],
        "challenges": [
            {
                "id": "proc_1",
                "type": "quiz",
                "title": "Enumerate the Daemons",
                "flavor": "Something on this server is watching for intrusion. You can't kill it if you can't see it. What command shows currently running processes?",
                "lesson": (
                    "ps — displays a snapshot of currently running processes.\n\n"
                    "Syntax: ps [flags]\n\n"
                    "Common flags:\n"
                    "  aux   show all processes for all users in detail (BSD style)\n"
                    "  -ef   show all processes in full format (UNIX style)\n\n"
                    "Each process has a PID (Process ID), which uniquely identifies it.\n\n"
                    "Example: ps    → shows processes running in the current terminal session"
                ),
                "question": "What command shows currently running processes?",
                "answers": ["ps"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It stands for 'process status'.",
                    "It's two letters.",
                    "The answer is: ps",
                ],
            },
            {
                "id": "proc_2",
                "type": "flag_quiz",
                "title": "Full Enumeration",
                "flavor": "The basic ps output only shows your own processes. The ghost processes — the corp's daemons — run under other users. What flags expose everything?",
                "lesson": (
                    "ps flags — control which processes are shown and how much detail is displayed.\n\n"
                    "  a   show processes for all users (not just yours)\n"
                    "  u   user-oriented format (shows username, CPU, memory)\n"
                    "  x   include processes not attached to a terminal\n\n"
                    "Combined: ps aux shows every process on the system in a readable format.\n\n"
                    "Example: ps aux    → full system-wide process list with CPU and memory usage"
                ),
                "question": "What flags do you use with 'ps' to see ALL processes from ALL users in a detailed format?",
                "answers": ["aux", "-aux", "aux", "axu", "-ef", "ef"],
                "xp": 75,
                "difficulty": "medium",
                "hints": [
                    "Two common combinations work: ps aux or ps -ef",
                    "The most common is 'aux'.",
                    "The answer is: aux (making it: ps aux)",
                ],
            },
            {
                "id": "proc_3",
                "type": "quiz",
                "title": "Terminate the Watcher",
                "flavor": "It's watching you. You found its PID. One command ends it — cleanly if you're lucky, hard if you're not. What command sends a kill signal by PID?",
                "lesson": (
                    "kill — sends a signal to a process, typically to terminate it.\n\n"
                    "Syntax: kill [signal] PID\n\n"
                    "Common signals:\n"
                    "  -15  SIGTERM — politely ask the process to stop (default)\n"
                    "  -9   SIGKILL — force-kill immediately, cannot be ignored\n"
                    "  -1   SIGHUP  — reload configuration\n\n"
                    "Example: kill 1234    → sends SIGTERM to process with PID 1234"
                ),
                "question": "What command sends a signal to terminate a process by PID?",
                "answers": ["kill"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It's a very direct command name.",
                    "It starts with 'k'.",
                    "The answer is: kill",
                ],
            },
            {
                "id": "proc_4",
                "type": "quiz",
                "title": "Live Surveillance",
                "flavor": "Static snapshots aren't enough. You need a live feed — all processes, updating every second, CPU usage, memory consumption. One command does this.",
                "lesson": (
                    "top — displays a live, auto-refreshing view of all running processes and system resources.\n\n"
                    "Syntax: top\n\n"
                    "While running:\n"
                    "  q      quit\n"
                    "  k      kill a process (enter its PID when prompted)\n"
                    "  M      sort by memory usage\n"
                    "  P      sort by CPU usage\n\n"
                    "Example: top    → opens an interactive real-time process monitor"
                ),
                "question": "What interactive command gives a real-time view of all system processes?",
                "answers": ["top", "htop"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It shows you what's happening 'at the top'.",
                    "It's three letters.",
                    "The answer is: top",
                ],
            },
            {
                "id": "proc_5",
                "type": "live",
                "title": "Find the Process",
                "flavor": "You know the process name. You need its PID. Enumerate everything and filter. Classic pipeline work. Fast and quiet.",
                "lesson": (
                    "ps aux | grep — combines process listing with pattern matching to find specific processes.\n\n"
                    "Syntax: ps aux | grep process_name\n\n"
                    "ps aux lists all processes; grep filters for lines matching your pattern.\n"
                    "This is one of the most common process-inspection idioms in shell work.\n\n"
                    "Example: ps aux | grep bash    → shows all running bash processes"
                ),
                "question": (
                    "Run 'ps aux' and pipe it to grep to find the 'bash' process.\n"
                    "Show all lines containing 'bash'."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "bash",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use ps aux piped to grep.",
                    "Try: ps aux | grep bash",
                    "The answer is: ps aux | grep bash",
                ],
            },
            {
                "id": "proc_boss",
                "type": "live",
                "title": "BOSS: Ghost PID Extraction",
                "flavor": "The corp's intrusion detection needs your shell's PID to flag you. Save it to disk before it finds you — and hide the evidence in a file only you can find.",
                "lesson": (
                    "$$ — a special bash variable that holds the PID of the current shell process.\n\n"
                    "Special bash variables:\n"
                    "  $$   PID of the current shell\n"
                    "  $!   PID of the last background process\n"
                    "  $?   exit status of the last command\n"
                    "  $0   name of the current script or shell\n\n"
                    "Example: echo $$    → prints the PID of your running bash session"
                ),
                "question": (
                    "The Necromancer demands:\n"
                    "Find your current shell's process ID and save it to 'my_pid.txt'.\n\n"
                    "Hint: bash has a special variable that holds the current shell's PID."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "file_exists",
                    "target": "my_pid.txt",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Use the special $$ variable which contains the current shell's PID.",
                    "Try: echo $$ > my_pid.txt",
                    "The answer is: echo $$ > my_pid.txt",
                ],
            },
        ],
    },

    "permissions_fortress": {
        "id": "permissions_fortress",
        "name": "The Access Grid",
        "subtitle": "Permission Systems",
        "color": "green",
        "icon": "🔒",
        "commands": ["chmod", "chown", "ls -l", "umask"],
        "challenges": [
            {
                "id": "perm_1",
                "type": "quiz",
                "title": "Read the Access String",
                "flavor": "Every file has a ten-character access string. The corps think it's invisible. You need to see it — and know exactly what it means.",
                "lesson": (
                    "ls -l — shows files in long format, including permissions, owner, size, and date.\n\n"
                    "Syntax: ls -l [directory]\n\n"
                    "Permission string format: -rwxr-xr--\n"
                    "  Position 1:   file type (- = file, d = directory, l = symlink)\n"
                    "  Positions 2-4: owner permissions (r=read, w=write, x=execute)\n"
                    "  Positions 5-7: group permissions\n"
                    "  Positions 8-10: other (world) permissions\n\n"
                    "Example: ls -l    → shows permissions, owner, size, and name of each file"
                ),
                "question": "What flag do you add to 'ls' to see detailed permissions for each file?",
                "answers": ["-l", "-la", "-al", "-lh"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's a single letter flag meaning 'long' format.",
                    "It's -l (lowercase L).",
                    "The answer is: -l",
                ],
            },
            {
                "id": "perm_2",
                "type": "quiz",
                "title": "Modify Access",
                "flavor": "The access bits are wrong. The corporate security team misconfigured this file. One command fixes it — or breaks it wider open. Your call.",
                "lesson": (
                    "chmod — changes the permission mode of a file or directory.\n\n"
                    "Syntax: chmod [mode] file\n\n"
                    "Symbolic mode examples:\n"
                    "  u+x   add execute for owner (u=user, g=group, o=other, a=all)\n"
                    "  go-w  remove write from group and others\n"
                    "  a+r   add read for everyone\n\n"
                    "Example: chmod u+x script.sh    → makes script.sh executable by its owner"
                ),
                "question": "What command changes file permissions?",
                "answers": ["chmod"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It stands for 'change mode'.",
                    "It's 5 characters: chmod.",
                    "The answer is: chmod",
                ],
            },
            {
                "id": "perm_3",
                "type": "live",
                "title": "Make It Runnable",
                "flavor": "The exploit script is there. The permissions say it can't execute. The corp's sysadmin forgot to flip the bit. You remember. Fix it.",
                "lesson": (
                    "chmod +x — adds execute permission, allowing a file to be run as a program.\n\n"
                    "Syntax: chmod [who]+x filename\n\n"
                    "  chmod +x file      adds execute for all (owner, group, others)\n"
                    "  chmod u+x file     adds execute for the owner only\n"
                    "  chmod a+x file     same as +x, explicitly all\n\n"
                    "Example: chmod u+x spell.sh    → makes spell.sh runnable by its owner"
                ),
                "question": "Make 'spell.sh' executable by its owner.",
                "setup": {
                    "files": {"spell.sh": "#!/bin/bash\necho 'The spell is cast!'\n"},
                    "dirs": [],
                },
                "validation": {
                    "type": "file_executable",
                    "target": "spell.sh",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use chmod with 'u+x' to add execute permission for the owner.",
                    "Try: chmod u+x spell.sh",
                    "Or: chmod +x spell.sh",
                ],
            },
            {
                "id": "perm_4",
                "type": "fill_blank",
                "title": "Octal Code",
                "flavor": "Symbolic flags are for beginners. Real permission work uses octal notation — three digits that contain more access control information than most corps' entire security dashboards.",
                "lesson": (
                    "chmod numeric mode — sets permissions using a 3-digit octal number (owner, group, others).\n\n"
                    "Each digit is the sum of: 4=read, 2=write, 1=execute\n\n"
                    "  7 = rwx (4+2+1)   full access\n"
                    "  6 = rw-  (4+2)    read and write\n"
                    "  5 = r-x  (4+1)    read and execute\n"
                    "  4 = r--  (4)      read only\n\n"
                    "Example: chmod 754 file    → owner=rwx, group=r-x, others=r--"
                ),
                "question": (
                    "Complete the command to give the owner full permissions (rwx),\n"
                    "group read+execute (r-x), and others read-only (r--):\n\n"
                    "chmod ___ mysecret.txt"
                ),
                "answers": ["754", "0754"],
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "Owner=7 (rwx), Group=5 (r-x), Others=4 (r--)",
                    "Combine the numbers: 754",
                    "The answer is: 754",
                ],
            },
            {
                "id": "perm_5",
                "type": "live",
                "title": "Lockdown Protocol",
                "flavor": "This file contains the extracted credentials. If any other process can read it, the whole operation is blown. Lock it to owner-only access.",
                "lesson": (
                    "chmod 600 — sets a file to be readable and writable by the owner only, with no access for anyone else.\n\n"
                    "Syntax: chmod 600 filename\n\n"
                    "Common secure permission modes:\n"
                    "  600  rw-------  private files (SSH keys, credentials)\n"
                    "  644  rw-r--r--  normal files (readable by all, writable by owner)\n"
                    "  700  rwx------  private executables or directories\n\n"
                    "Example: chmod 600 secrets.txt    → only the owner can read or write secrets.txt"
                ),
                "question": "Set permissions on 'secrets.txt' so ONLY the owner can read it (chmod 600).",
                "setup": {
                    "files": {"secrets.txt": "TOP SECRET SHELL KNOWLEDGE\n"},
                    "dirs": [],
                },
                "validation": {
                    "type": "file_perms",
                    "target": "secrets.txt",
                    "expected_mode": "600",
                },
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "Use chmod with numeric mode 600.",
                    "Try: chmod 600 secrets.txt",
                    "The answer is: chmod 600 secrets.txt",
                ],
            },
            {
                "id": "perm_boss",
                "type": "live",
                "title": "BOSS: Deploy and Secure",
                "flavor": "Create the payload script. Set it executable and world-readable. One chain of commands — because the access audit runs in forty-five seconds.",
                "lesson": (
                    "chmod 755 — the standard permission for executable scripts shared with others.\n\n"
                    "755 means:\n"
                    "  7 (rwx) — owner can read, write, and execute\n"
                    "  5 (r-x) — group can read and execute\n"
                    "  5 (r-x) — others can read and execute\n\n"
                    "This is the typical permission for shell scripts and programs on a system.\n\n"
                    "Example: touch vault.sh && chmod 755 vault.sh    → creates and makes vault.sh world-executable"
                ),
                "question": (
                    "The Warden's challenge:\n"
                    "1. Create a file called 'vault.sh'\n"
                    "2. Make it executable by everyone (chmod 755)\n\n"
                    "Chain both commands together on one line."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "multi",
                    "checks": [
                        {"type": "file_exists", "target": "vault.sh"},
                        {"type": "file_perms", "target": "vault.sh", "expected_mode": "755"},
                    ],
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need touch and then chmod.",
                    "Try: touch vault.sh && chmod 755 vault.sh",
                    "The answer is: touch vault.sh && chmod 755 vault.sh",
                ],
            },
        ],
    },

    "scripting_citadel": {
        "id": "scripting_citadel",
        "name": "The Code Forge",
        "subtitle": "Shell Scripting",
        "color": "yellow",
        "icon": "⚙️",
        "commands": ["variables", "loops", "if/else", "functions"],
        "challenges": [
            {
                "id": "script_1",
                "type": "live",
                "title": "Memory Allocation",
                "flavor": "You're about to use the same string eight times in this script. Sane people store it in a variable. The corps' sysadmins copy-paste it eight times. That's why you're here and they're not.",
                "lesson": (
                    "Variables — store values in the shell so they can be reused.\n\n"
                    "Syntax: VARNAME=value    (no spaces around the = sign)\n\n"
                    "To use a variable, prefix its name with $:\n"
                    "  echo $VARNAME    → prints the variable's value\n\n"
                    "Variable names are case-sensitive. ALL_CAPS is conventional for environment variables.\n\n"
                    "Example: HERO=HackerArchaeologist && echo $HERO    → prints: HackerArchaeologist"
                ),
                "question": "Create a variable called 'HERO' with value 'HackerArchaeologist' and echo it.",
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "HackerArchaeologist",
                },
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Assign with: VARNAME=value (no spaces around =)",
                    "Then use: echo $VARNAME",
                    "Full command: HERO=HackerArchaeologist && echo $HERO",
                ],
            },
            {
                "id": "script_2",
                "type": "live",
                "title": "Conditional Logic",
                "flavor": "Every exploit needs decision logic. If the target is vulnerable, execute. If not, abort cleanly. This is the most fundamental structure in any real script.",
                "lesson": (
                    "if/else — executes commands conditionally based on whether a test is true or false.\n\n"
                    "Syntax: if [ condition ]; then commands; fi\n\n"
                    "Common test operators:\n"
                    "  -gt   greater than (numeric)\n"
                    "  -lt   less than (numeric)\n"
                    "  -eq   equal (numeric)\n"
                    "  =     equal (string)\n\n"
                    "Example: if [ 5 -gt 3 ]; then echo 'YES'; fi    → prints YES because 5 > 3"
                ),
                "question": (
                    "Run a bash one-liner that checks if 5 is greater than 3\n"
                    "and prints 'YES' if true.\n\n"
                    "Try: if [ 5 -gt 3 ]; then echo 'YES'; fi"
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "YES",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use if [ condition ]; then ... fi syntax.",
                    "For greater-than, use -gt.",
                    "Try: if [ 5 -gt 3 ]; then echo 'YES'; fi",
                ],
            },
            {
                "id": "script_3",
                "type": "live",
                "title": "Iteration Protocol",
                "flavor": "Manual repetition is for interns and people who haven't discovered loops. You need to hit forty targets. Writing forty commands individually is not an option.",
                "lesson": (
                    "for loop — repeats a block of commands for each item in a list.\n\n"
                    "Syntax: for variable in list; do commands; done\n\n"
                    "The list can be literal values, a range, or command output:\n"
                    "  for i in 1 2 3       explicit list\n"
                    "  for i in $(seq 1 5)  range using seq\n"
                    "  for f in *.txt       all .txt files\n\n"
                    "Example: for i in 1 2 3; do echo $i; done    → prints 1, 2, 3 on separate lines"
                ),
                "question": "Write a for loop that prints the numbers 1, 2, and 3.",
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "1",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use: for var in values; do commands; done",
                    "Try: for i in 1 2 3; do echo $i; done",
                    "The answer is: for i in 1 2 3; do echo $i; done",
                ],
            },
            {
                "id": "script_4",
                "type": "live",
                "title": "Write the Tool",
                "flavor": "You need this to run repeatedly. A one-liner won't cut it. Write a proper script — shebang, commands, ready to execute. This is how the pros do persistent access.",
                "lesson": (
                    "Bash scripts — text files containing shell commands, run as programs.\n\n"
                    "Every script should start with a shebang line that tells the OS which interpreter to use:\n"
                    "  #!/bin/bash\n\n"
                    "After writing the script, make it executable with chmod +x, then run it with ./script.sh\n\n"
                    "Example: printf '#!/bin/bash\\necho THE QUEST BEGINS\\n' > quest.sh"
                ),
                "question": (
                    "Create a bash script called 'quest.sh' that echoes 'THE QUEST BEGINS'.\n"
                    "It must start with a shebang line (#!/bin/bash)."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "file_contains",
                    "target": "quest.sh",
                    "expected": "#!/bin/bash",
                },
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "Use printf or echo with escape sequences to write the file.",
                    "The shebang line is: #!/bin/bash",
                    "Try: printf '#!/bin/bash\\necho THE QUEST BEGINS\\n' > quest.sh",
                ],
            },
            {
                "id": "script_5",
                "type": "live",
                "title": "Encapsulate the Attack",
                "flavor": "You're calling the same logic from three different places in your script. Functions exist for exactly this reason. Encapsulate it. Call it by name. Write it once.",
                "lesson": (
                    "Functions — named, reusable blocks of commands in bash.\n\n"
                    "Syntax: funcname() { commands; }\n\n"
                    "Define first, then call by name. Functions can accept arguments via $1, $2, etc.\n"
                    "  greet() { echo \"Hello, $1\"; }\n"
                    "  greet World    → prints: Hello, World\n\n"
                    "Example: greet() { echo 'GREETINGS TRAVELER'; }; greet    → calls and runs the function"
                ),
                "question": (
                    "Define a bash function called 'greet' that echoes 'GREETINGS TRAVELER',\n"
                    "then call it."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "GREETINGS TRAVELER",
                },
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "Define with: funcname() { commands; }",
                    "Then call it by name.",
                    "Try: greet() { echo 'GREETINGS TRAVELER'; }; greet",
                ],
            },
            {
                "id": "script_boss",
                "type": "live",
                "title": "BOSS: The Full Tool",
                "flavor": "The corps' countermeasure adapts to single commands. You need a real script — variables, loops, logic. Write it. Deploy it. The monitoring window is closing.",
                "lesson": (
                    "Combining scripting constructs — real scripts use variables, loops, and conditionals together.\n\n"
                    "A typical script structure:\n"
                    "  #!/bin/bash          shebang\n"
                    "  COUNT=3              variable assignment\n"
                    "  for i in $(seq 1 $COUNT); do    loop using the variable\n"
                    "    echo $i            body of loop\n"
                    "  done\n\n"
                    "seq generates a numeric sequence: seq 1 5 → 1 2 3 4 5"
                ),
                "question": (
                    "Create 'masterwork.sh' containing a script that:\n"
                    "- Starts with #!/bin/bash\n"
                    "- Sets a variable COUNT=3\n"
                    "- Uses a for loop with seq to print 1 through $COUNT\n\n"
                    "Use printf to write the script contents to the file."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "file_contains",
                    "target": "masterwork.sh",
                    "expected": "#!/bin/bash",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Create a .sh file with a shebang, variable, and for loop.",
                    "Use printf to write the file with newlines.",
                    "Try: printf '#!/bin/bash\\nCOUNT=3\\nfor i in $(seq 1 $COUNT); do echo $i; done\\n' > masterwork.sh",
                ],
            },
        ],
    },

    "network_nexus": {
        "id": "network_nexus",
        "name": "The Meat Highway",
        "subtitle": "Network Operations",
        "color": "cyan",
        "icon": "🌐",
        "commands": ["curl", "ping", "ssh", "netstat", "wget"],
        "challenges": [
            {
                "id": "net_1",
                "type": "quiz",
                "title": "Host Reachability",
                "flavor": "Before you attempt anything against a remote target, you need to know it's alive. One command sends a probe and listens for the echo.",
                "lesson": (
                    "ping — sends ICMP echo request packets to a host to test if it is reachable.\n\n"
                    "Syntax: ping [flags] hostname_or_IP\n\n"
                    "Common flags:\n"
                    "  -c N   send exactly N packets then stop (without this, ping runs forever)\n"
                    "  -i N   wait N seconds between packets\n"
                    "  -t N   set time-to-live (max hops)\n\n"
                    "Example: ping -c 3 google.com    → sends 3 packets to google.com and reports round-trip time"
                ),
                "question": "What command sends ICMP packets to test if a host is reachable?",
                "answers": ["ping"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It makes a sound when you think about it.",
                    "It's 4 letters: ping.",
                    "The answer is: ping",
                ],
            },
            {
                "id": "net_2",
                "type": "quiz",
                "title": "Data Retrieval",
                "flavor": "The target's API is wide open. No auth, no rate limit, no logging on the public endpoint. One command to pull what you need from any URL.",
                "lesson": (
                    "curl — transfers data to or from a server using URLs. Supports HTTP, HTTPS, FTP, and more.\n\n"
                    "Syntax: curl [flags] URL\n\n"
                    "Common flags:\n"
                    "  -o file   save output to a file instead of printing it\n"
                    "  -s        silent mode (suppress progress and errors)\n"
                    "  -L        follow HTTP redirects\n"
                    "  -X POST   use a specific HTTP method\n\n"
                    "Example: curl https://example.com    → fetches and prints the HTML of the page"
                ),
                "question": "What command transfers data from/to a URL (supports HTTP, FTP, etc.)?",
                "answers": ["curl"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It stands for 'Client URL'.",
                    "It's 4 letters starting with 'c'.",
                    "The answer is: curl",
                ],
            },
            {
                "id": "net_3",
                "type": "quiz",
                "title": "Remote Access",
                "flavor": "The data isn't on this machine. It's on the server. Physical access is not an option. You need a terminal on that box — encrypted, authenticated, silent.",
                "lesson": (
                    "ssh — opens an encrypted remote shell session on another machine over the network.\n\n"
                    "Syntax: ssh [flags] user@hostname\n\n"
                    "Common flags:\n"
                    "  -p PORT   connect on a specific port (default is 22)\n"
                    "  -i file   use a specific private key file for authentication\n"
                    "  -L        local port forwarding (tunnel a remote port to your machine)\n\n"
                    "Example: ssh alice@192.168.1.10    → logs in as user 'alice' on that machine"
                ),
                "question": "What command lets you log into a remote machine securely over the network?",
                "answers": ["ssh"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It stands for 'Secure Shell'.",
                    "It's 3 letters.",
                    "The answer is: ssh",
                ],
            },
            {
                "id": "net_4",
                "type": "flag_quiz",
                "title": "Silent Exfil",
                "flavor": "The progress meter is noise. The error messages are noise. In an automated script, noise kills you. What flag makes curl run clean and quiet?",
                "lesson": (
                    "curl flags — modify how curl behaves when fetching data.\n\n"
                    "Useful flags for scripting:\n"
                    "  -s / --silent    suppress progress meter and error messages\n"
                    "  -o file          write output to a file instead of stdout\n"
                    "  -w format        print custom information after transfer (e.g. HTTP status code)\n"
                    "  -f              fail silently on HTTP errors (non-zero exit code)\n\n"
                    "Example: curl -s https://example.com    → fetches the page with no progress output"
                ),
                "question": "What flag makes curl run silently (suppressing progress and error messages)?",
                "answers": ["-s", "--silent"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "It's a single letter flag.",
                    "Think 'silent'.",
                    "The answer is: -s",
                ],
            },
            {
                "id": "net_5",
                "type": "live",
                "title": "Probe the Endpoint",
                "flavor": "You need the HTTP status code — not the response body, just the status. A 200 means the door is open. A 403 means they know you're coming.",
                "lesson": (
                    "curl -o /dev/null -s -w — a pattern used to check HTTP status codes without saving the response body.\n\n"
                    "  -o /dev/null   discard the response body\n"
                    "  -s             silent (no progress output)\n"
                    "  -w '%{http_code}'   print just the HTTP status code after the request\n\n"
                    "Example: curl -o /dev/null -s -w '%{http_code}' http://httpbin.org/status/200\n"
                    "  → prints: 200"
                ),
                "question": (
                    "Use curl to fetch the HTTP status code from http://httpbin.org/status/200.\n"
                    "Use the -o /dev/null -s -w '%{http_code}' flags to get just the status code.\n\n"
                    "Try: curl -o /dev/null -s -w '%{http_code}' http://httpbin.org/status/200"
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "200",
                },
                "xp": 150,
                "difficulty": "hard",
                "hints": [
                    "Use curl with special output flags.",
                    "Try: curl -o /dev/null -s -w '%{http_code}' http://httpbin.org/status/200",
                    "The answer is: curl -o /dev/null -s -w '%{http_code}' http://httpbin.org/status/200",
                ],
            },
            {
                "id": "net_boss",
                "type": "live",
                "title": "BOSS: Identify the Node",
                "flavor": "The client needs to know what machine you're on. Corporate attribution, network segmentation, asset tracking — it all starts with the hostname. Extract it and save it.",
                "lesson": (
                    "hostname — prints the name of the current machine on the network.\n\n"
                    "Syntax: hostname [flags]\n\n"
                    "Common flags:\n"
                    "  -I   show all IP addresses of the machine\n"
                    "  -f   show the fully qualified domain name (FQDN)\n\n"
                    "Combining with redirection saves the result to a file for later use.\n\n"
                    "Example: hostname > host.txt    → writes your machine's hostname into host.txt"
                ),
                "question": "Save your machine's hostname to 'host.txt'.",
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "file_exists",
                    "target": "host.txt",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "The 'hostname' command prints your machine's name.",
                    "Redirect its output to a file.",
                    "Try: hostname > host.txt",
                ],
            },
        ],
    },

    "grand_terminal": {
        "id": "grand_terminal",
        "name": "The Black Ice Room",
        "subtitle": "Advanced Shell Mastery",
        "color": "magenta",
        "icon": "💀",
        "commands": ["alias", "history", "env", "export", "awk", "sed"],
        "challenges": [
            {
                "id": "grand_1",
                "type": "quiz",
                "title": "Bind the Shortcut",
                "flavor": "You'll type this command four hundred times before the operation is over. Professionals don't repeat themselves. They make aliases.",
                "lesson": (
                    "alias — creates a shortcut name for a longer command or command with flags.\n\n"
                    "Syntax: alias name='command'\n\n"
                    "Common uses:\n"
                    "  alias ll='ls -la'          shorthand for long listing with hidden files\n"
                    "  alias gs='git status'       shorthand for a common git command\n"
                    "  alias ..='cd ..'            navigate up without typing 'cd'\n\n"
                    "Example: alias ll='ls -la'    → typing 'll' now runs 'ls -la'"
                ),
                "question": "What command creates a shortcut (custom name) for another command?",
                "answers": ["alias"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It lets you create a nickname for commands.",
                    "It starts with 'a' and means 'alternative name'.",
                    "The answer is: alias",
                ],
            },
            {
                "id": "grand_2",
                "type": "quiz",
                "title": "Shell Memory",
                "flavor": "What did you run three hours ago? The shell remembers. Every command, every flag, every typo. What retrieves that record?",
                "lesson": (
                    "history — displays a numbered list of previously run commands from the current shell session.\n\n"
                    "Syntax: history [n]\n\n"
                    "Useful tricks:\n"
                    "  history 20       show the last 20 commands\n"
                    "  history | grep ssh    search history for ssh commands\n"
                    "  !!               re-run the last command\n"
                    "  !42              re-run command number 42 from history\n\n"
                    "Example: history    → prints a numbered list of all recent commands"
                ),
                "question": "What command shows your shell's command history?",
                "answers": ["history"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It stores everything you've ever typed.",
                    "It's literally called 'history'.",
                    "The answer is: history",
                ],
            },
            {
                "id": "grand_3",
                "type": "live",
                "title": "Enumerate the Environment",
                "flavor": "The shell is soaked in environment variables — credentials, paths, API keys that sloppy devs exported and forgot about. What command dumps them all?",
                "lesson": (
                    "env — prints all environment variables currently set in the shell.\n\n"
                    "Syntax: env\n\n"
                    "Related command: export sets a variable so child processes inherit it.\n"
                    "  export MY_VAR=hello    → MY_VAR is now available to any program you run\n\n"
                    "Key environment variables:\n"
                    "  PATH    directories searched for executable programs\n"
                    "  HOME    your home directory\n"
                    "  USER    your username\n\n"
                    "Example: env | grep PATH    → shows the current PATH variable"
                ),
                "question": "Display all environment variables and pipe to grep to find 'PATH'.",
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "PATH",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use 'env' to list environment variables.",
                    "Pipe to grep: env | grep PATH",
                    "The answer is: env | grep PATH",
                ],
            },
            {
                "id": "grand_4",
                "type": "live",
                "title": "Rewrite the Stream",
                "flavor": "The log file says 'OLD version detected'. You need it to say 'NEW version detected'. You're not opening an editor — the file has 40,000 lines. Use sed.",
                "lesson": (
                    "sed — a stream editor that reads text line by line and applies transformations.\n\n"
                    "Syntax: sed 'command' [file]   or   command | sed 'command'\n\n"
                    "Most common use — substitution:\n"
                    "  sed 's/old/new/'       replace first occurrence per line\n"
                    "  sed 's/old/new/g'      replace all occurrences per line (global)\n"
                    "  sed -i 's/old/new/g' file    edit the file in-place\n\n"
                    "Example: echo 'OLD way' | sed 's/OLD/NEW/'    → prints: NEW way"
                ),
                "question": (
                    "Use sed to replace 'OLD' with 'NEW' in the output of:\n"
                    "echo 'This is the OLD way'\n\n"
                    "Try: echo 'This is the OLD way' | sed 's/OLD/NEW/'"
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "NEW",
                },
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "sed uses the syntax: sed 's/pattern/replacement/'",
                    "Pipe echo output into sed.",
                    "Try: echo 'This is the OLD way' | sed 's/OLD/NEW/'",
                ],
            },
            {
                "id": "grand_5",
                "type": "live",
                "title": "Field Extraction",
                "flavor": "The dump is whitespace-delimited. You need column two of every row. All forty thousand rows. sed won't do this. grep won't do this. awk will do this in one line.",
                "lesson": (
                    "awk — a powerful text processing tool that splits each line into fields and lets you act on them.\n\n"
                    "Syntax: awk '{action}' [file]   or   command | awk '{action}'\n\n"
                    "Fields are split by whitespace by default. Access them with $1, $2, $3...\n"
                    "  $0   the entire line\n"
                    "  $1   first field, $2 second field, etc.\n"
                    "  NF   number of fields on the current line\n\n"
                    "Example: echo 'alpha beta gamma' | awk '{print $2}'    → prints: beta"
                ),
                "question": (
                    "Use awk to print only the second field (word) from:\n"
                    "echo 'alpha beta gamma'\n\n"
                    "Try: echo 'alpha beta gamma' | awk '{print $2}'"
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "output_contains",
                    "expected": "beta",
                },
                "xp": 125,
                "difficulty": "medium",
                "hints": [
                    "awk uses $1, $2, $3... for fields.",
                    "Print the second field with: awk '{print $2}'",
                    "Try: echo 'alpha beta gamma' | awk '{print $2}'",
                ],
            },
            {
                "id": "grand_boss",
                "type": "live",
                "title": "FINAL BOSS: The Black Ice Sequence",
                "flavor": "The corps' final countermeasure activates. A full pipeline — write, transform, output. This is what separates the people who learned the Shell from the people who own it.",
                "lesson": (
                    "Combining tools — the grandmaster wields echo, sed, and redirection together in one pipeline.\n\n"
                    "This challenge chains three steps:\n"
                    "  1. echo writes text into a file using >\n"
                    "  2. sed reads that file and substitutes text\n"
                    "  3. > saves the transformed output to a new file\n\n"
                    "Example:\n"
                    "echo 'GRANDMASTER' > legacy.txt && sed 's/GRANDMASTER/LEGEND/' legacy.txt > legend.txt"
                ),
                "question": (
                    "The Grand Terminal's final trial:\n\n"
                    "Create a file 'legacy.txt' containing the text 'GRANDMASTER',\n"
                    "then use sed to replace 'GRANDMASTER' with 'LEGEND',\n"
                    "and save the result to 'legend.txt'."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "file_contains",
                    "target": "legend.txt",
                    "expected": "LEGEND",
                },
                "xp": 300,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need echo, sed, and file redirection.",
                    "Chain them: echo ... > legacy.txt && sed ... > legend.txt",
                    "Try: echo 'GRANDMASTER' > legacy.txt && sed 's/GRANDMASTER/LEGEND/' legacy.txt > legend.txt",
                ],
            },
        ],
    },
}

ZONE_ORDER = [
    "antechamber",
    "archive_vaults",
    "oracle_library",
    "pipe_sanctum",
    "process_catacombs",
    "permissions_fortress",
    "scripting_citadel",
    "network_nexus",
    "grand_terminal",
]


def get_zone(zone_id: str) -> dict:
    return ZONES.get(zone_id, {})


def get_all_zones() -> list:
    return [ZONES[z] for z in ZONE_ORDER if z in ZONES]


def get_zone_challenges(zone_id: str) -> list:
    zone = get_zone(zone_id)
    return zone.get("challenges", [])


def get_challenge(zone_id: str, challenge_id: str) -> dict:
    for ch in get_zone_challenges(zone_id):
        if ch["id"] == challenge_id:
            return ch
    return {}


def zone_total_xp(zone_id: str) -> int:
    return sum(ch.get("xp", 0) for ch in get_zone_challenges(zone_id))
