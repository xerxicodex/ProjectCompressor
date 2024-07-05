import os
import argparse
import pathspec
import json
import mimetypes
import fnmatch

def load_gitignore_patterns(gitignore_path):
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as gitignore:
            return pathspec.PathSpec.from_lines('gitwildmatch', gitignore)
    return pathspec.PathSpec.from_lines('gitwildmatch', [])

def should_ignore(file_path, ignore_specs, script_path, additional_ignores):
    if os.path.samefile(file_path, script_path):
        return True
    
    relative_path = os.path.relpath(file_path, os.path.dirname(script_path))
    
    # Check additional ignore patterns
    for pattern in additional_ignores:
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
            return True
    
    for root, spec in reversed(ignore_specs):
        if file_path.startswith(root):
            relative_path = os.path.relpath(file_path, root)
            if spec.match_file(relative_path):
                return True
    return False

def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('text')

def is_image_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('image')

def compress_project(root_dir, output_file, script_path, additional_ignores):
    ignore_specs = [(root_dir, load_gitignore_patterns(os.path.join(root_dir, '.gitignore')))]
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(root_dir):
            # Check for .gitignore in the current directory
            gitignore_path = os.path.join(root, '.gitignore')
            if os.path.exists(gitignore_path):
                ignore_specs.append((root, load_gitignore_patterns(gitignore_path)))
            
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_specs, script_path, additional_ignores)]
            
            for file in files:
                file_path = os.path.join(root, file)
                if not should_ignore(file_path, ignore_specs, script_path, additional_ignores) and file != '.gitignore':
                    relative_path = os.path.relpath(file_path, root_dir)
                    print(f'Processing: {relative_path}')
                    outfile.write(f'// File: {relative_path}\n')
                    
                    if is_image_file(file_path):
                        outfile.write(f'// Image file, path: {relative_path}\n')
                    elif is_text_file(file_path) or file.endswith(('.css', '.html', '.ts', '.tsx', '.py', '.js', '.json')):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                content = infile.read()
                                if file.endswith('.json'):
                                    try:
                                        json_content = json.loads(content)
                                        content = json.dumps(json_content, separators=(',', ':'))
                                    except json.JSONDecodeError:
                                        pass  # If it's not valid JSON, keep the original content
                                outfile.write(content)
                        except UnicodeDecodeError:
                            outfile.write(f'// Binary file, content not included\n')
                    else:
                        outfile.write(f'// Binary file, content not included\n')
                    outfile.write('\n\n')

def main():
    parser = argparse.ArgumentParser(description='Compress project into a single file.')
    parser.add_argument('--in', dest='input_dir', type=str, default=os.getcwd(),
                        help='Input directory path (default: current directory)')
    parser.add_argument('--out', dest='output_file', type=str, default='codebase.txt',
                        help='Output file path (default: codebase.txt in the current directory)')
    parser.add_argument('--ignore', nargs='*', default=['*-lock.json', '.git/'],
                        help='Additional patterns to ignore (default: *-lock.json .git/)')
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    output_file = args.output_file if os.path.isabs(args.output_file) else os.path.join(os.getcwd(), args.output_file)
    script_path = os.path.abspath(__file__)

    compress_project(input_dir, output_file, script_path, args.ignore)
    print(f'Project compressed from {input_dir} to {output_file}')
    print(f'Additional ignore patterns: {args.ignore}')

if __name__ == '__main__':
    main()