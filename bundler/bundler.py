import re
import os
import argparse
import subprocess

def get_global_node_modules_path():
    try:
        result = subprocess.run(['npm', 'root', '-g'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error locating global node_modules directory: {e}")
    return None

def resolve_imports(file_path, resolved_files=set(), base_dir='', dependency_dir=''):
    if file_path in resolved_files:
        return ''

    resolved_files.add(file_path)

    if not os.path.isabs(file_path):
        file_path = os.path.join(base_dir, file_path)
    
    file_path = os.path.normpath(file_path)

    with open(file_path, 'r') as f:
        content = f.read()

    # Regular expression to find import statements
    import_regex = r'import\s+(?:\{[^}]+\}\s+from\s+)?["\'](.+?)["\'];'
    matches = re.findall(import_regex, content)

    for match in matches:
        if match.startswith('@'):
            stripped_match = re.sub(r'@[0-9\.]+', '', match)
            import_path = os.path.join(dependency_dir, stripped_match)
        else:
            if not os.path.isabs(match):
                import_path = os.path.join(base_dir, match)
            else:
                import_path = match

        import_path = os.path.normpath(import_path)
        imported_content = resolve_imports(import_path, resolved_files, os.path.dirname(import_path), dependency_dir)
        content = re.sub(f'import\s+(?:\{{[^}}]+\}}\s+from\s+)?["\']{re.escape(match)}["\'];', imported_content, content)

    return content

def bundle_solidity_contracts(main_file_path, output_file_path, node_modules_path=None):
    if not node_modules_path:
        node_modules_path = get_global_node_modules_path()
        if not node_modules_path:
            raise FileNotFoundError("Global node_modules directory not found")

    resolved_files = set()
    bundled_content = resolve_imports(main_file_path, resolved_files, base_dir=os.path.dirname(main_file_path), dependency_dir=node_modules_path)


    with open(main_file_path, 'r') as f:
        pragma_file = f.read()

    pragma_match = re.search(r'pragma\s+solidity\s+[^;]+;', pragma_file)
    pragma_statement = pragma_match.group(0) if pragma_match else ''

    bundled_content = re.sub(r'pragma\s+solidity\s+[^;]+;', '', bundled_content)

    final_content = pragma_statement + '\n' + bundled_content

    with open(output_file_path, 'w') as f:
        f.write(final_content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bundle Solidity contracts into a single file.')
    parser.add_argument('main_file', type=str, help='Path to the main contract file.')
    parser.add_argument('output_file', type=str, help='Path to the output bundled file.')
    parser.add_argument('--node-modules-path', type=str, help='Path to the node_modules directory.')

    args = parser.parse_args()
    
    bundle_solidity_contracts(args.main_file, args.output_file, args.node_modules_path)
    print(f'Bundled contract written to {args.output_file}')

