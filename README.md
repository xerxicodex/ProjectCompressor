# ProjectCompressor

ProjectCompressor is a Python script designed to compress an entire project into a single file. This is particularly useful for providing codebase context to AI systems, making it easier to process and understand large codebases.

## Features
- Compresses all text-based files (e.g., `.py`, `.js`, `.json`, `.css`, `.html`, `.ts`, `.tsx`) into a single file.
- Skips binary files and large images to keep the output manageable.
- Utilizes `.gitignore` patterns to exclude unnecessary files and directories.
- Allows for additional ignore patterns through command-line arguments.

## Why Use ProjectCompressor?

When working with AI systems that require context from an entire codebase, it can be cumbersome to provide multiple files and directories. ProjectCompressor simplifies this by consolidating all relevant files into one, making it easier to input into an AI system. This is especially beneficial for tasks like code analysis, automated refactoring, or training code-based models.

## Usage

### Prerequisites
- Python 3.x

### Installation
Clone the repository:
```bash
git clone https://github.com/your-username/ProjectCompressor.git
cd ProjectCompressor
```

### Running the Script
Use the script with the following command:

```bash
python compress_project.py --in <input_directory> --out <output_file> --ignore <additional_patterns>
```

### Command-Line Arguments
--in: Input directory path (default: current directory).
--out: Output file path (default: codebase.txt in the current directory).
--ignore: Additional patterns to ignore (default: *-lock.json .git/).

### Example
Compress the current directory into a file named codebase.txt, ignoring node_modules and .git directories:

```bash
python compress_project.py --in . --out codebase.txt --ignore node_modules .git
```

## Detailed Information
### How It Works
* Loading Ignore Patterns: The script reads .gitignore files to determine which files and directories should be excluded.
* File Filtering: It checks each file against the ignore patterns and additional user-defined patterns.
* File Processing: Text files are read and their content is included in the output file. Binary files and images are skipped.
* Output Generation: The processed files are written to the output file, each preceded by a comment indicating the file path.

### Main Purpose
The primary goal of ProjectCompressor is to generate a single, comprehensive file from a project's codebase. This file can then be used as input for AI systems, providing them with the necessary context to perform various tasks effectively.

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

### License
This project is licensed under the MIT License.
