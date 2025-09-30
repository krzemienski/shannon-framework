"""
Production readiness validation tests.

Validates:
- All modules importable
- No TODOs in codebase
- No placeholders or mock implementations
- Syntax validation
- Type hint completeness
"""

import ast
import importlib
import re
from pathlib import Path
from typing import List, Tuple

import pytest


class TestProductionReady:
    """Production readiness validation suite"""

    def test_all_modules_importable(self, src_directory: Path):
        """
        Validate all Python modules can be imported without errors.

        Args:
            src_directory: Path to src directory
        """
        python_files = list(src_directory.rglob('*.py'))
        assert python_files, "No Python files found in src directory"

        import_errors = []
        successful_imports = []

        for py_file in python_files:
            # Skip __init__.py files
            if py_file.name == '__init__.py':
                continue

            # Convert path to module name
            relative_path = py_file.relative_to(src_directory.parent)
            module_name = str(relative_path.with_suffix('')).replace('/', '.')

            try:
                importlib.import_module(module_name)
                successful_imports.append(module_name)
            except Exception as e:
                import_errors.append((module_name, str(e)))

        # Report results
        print(f"\nImport Results:")
        print(f"  Successful: {len(successful_imports)}/{len(python_files)}")
        if import_errors:
            print(f"  Failed: {len(import_errors)}")
            for module, error in import_errors:
                print(f"    - {module}: {error}")

        assert not import_errors, f"Failed to import {len(import_errors)} modules"

    def test_no_todos_in_codebase(self, src_directory: Path):
        """
        Validate no TODO comments exist in production code.

        Args:
            src_directory: Path to src directory
        """
        python_files = list(src_directory.rglob('*.py'))
        assert python_files, "No Python files found"

        todo_pattern = re.compile(r'#\s*TODO|#\s*FIXME|#\s*XXX', re.IGNORECASE)
        files_with_todos = []

        for py_file in python_files:
            content = py_file.read_text()
            matches = todo_pattern.finditer(content)

            todos_in_file = []
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = content.split('\n')[line_num - 1].strip()
                todos_in_file.append((line_num, line_content))

            if todos_in_file:
                files_with_todos.append((py_file, todos_in_file))

        # Report results
        if files_with_todos:
            print(f"\nTODOs found in {len(files_with_todos)} files:")
            for py_file, todos in files_with_todos:
                print(f"\n  {py_file.relative_to(src_directory)}:")
                for line_num, line_content in todos:
                    print(f"    Line {line_num}: {line_content}")

        assert not files_with_todos, f"Found TODOs in {len(files_with_todos)} files"

    def test_no_placeholders_in_code(self, src_directory: Path):
        """
        Validate no placeholder implementations exist.

        Checks for:
        - pass statements in function bodies
        - raise NotImplementedError
        - ... (Ellipsis) as placeholder

        Args:
            src_directory: Path to src directory
        """
        python_files = list(src_directory.rglob('*.py'))
        files_with_placeholders = []

        for py_file in python_files:
            content = py_file.read_text()

            try:
                tree = ast.parse(content)
                placeholders = self._find_placeholders(tree, py_file)

                if placeholders:
                    files_with_placeholders.append((py_file, placeholders))

            except SyntaxError as e:
                pytest.fail(f"Syntax error in {py_file}: {e}")

        # Report results
        if files_with_placeholders:
            print(f"\nPlaceholders found in {len(files_with_placeholders)} files:")
            for py_file, placeholders in files_with_placeholders:
                print(f"\n  {py_file.relative_to(src_directory)}:")
                for func_name, issue in placeholders:
                    print(f"    {func_name}: {issue}")

        assert not files_with_placeholders, \
            f"Found placeholders in {len(files_with_placeholders)} files"

    def test_syntax_validation(self, src_directory: Path):
        """
        Validate all Python files have valid syntax.

        Args:
            src_directory: Path to src directory
        """
        python_files = list(src_directory.rglob('*.py'))
        syntax_errors = []

        for py_file in python_files:
            try:
                content = py_file.read_text()
                ast.parse(content)
            except SyntaxError as e:
                syntax_errors.append((py_file, str(e)))

        # Report results
        if syntax_errors:
            print(f"\nSyntax errors in {len(syntax_errors)} files:")
            for py_file, error in syntax_errors:
                print(f"  {py_file.relative_to(src_directory)}: {error}")

        assert not syntax_errors, f"Syntax errors in {len(syntax_errors)} files"

    def test_type_hints_completeness(self, src_directory: Path):
        """
        Validate type hint coverage for public functions.

        Args:
            src_directory: Path to src directory
        """
        python_files = list(src_directory.rglob('*.py'))
        functions_without_hints = []
        total_functions = 0
        functions_with_hints = 0

        for py_file in python_files:
            content = py_file.read_text()

            try:
                tree = ast.parse(content)
                missing = self._check_type_hints(tree, py_file)

                for func_name, location in missing:
                    functions_without_hints.append((py_file, func_name, location))
                    total_functions += 1

                # Count functions with hints
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if not node.name.startswith('_'):
                            total_functions += 1
                            if node.returns or any(arg.annotation for arg in node.args.args):
                                functions_with_hints += 1

            except SyntaxError:
                continue

        # Calculate coverage
        coverage = (functions_with_hints / total_functions * 100) if total_functions > 0 else 100

        print(f"\nType Hint Coverage:")
        print(f"  Functions with hints: {functions_with_hints}/{total_functions}")
        print(f"  Coverage: {coverage:.1f}%")

        if functions_without_hints:
            print(f"\n  Missing hints in {len(functions_without_hints)} functions:")
            for py_file, func_name, location in functions_without_hints[:10]:
                print(f"    {py_file.relative_to(src_directory)} - {func_name} (line {location})")

        # Require at least 80% coverage
        assert coverage >= 80.0, \
            f"Type hint coverage {coverage:.1f}% below 80% threshold"

    def test_no_mock_implementations(self, src_directory: Path):
        """
        Validate no mock or fake implementations exist.

        Checks for common mock patterns:
        - Classes with 'Mock' in name
        - Functions returning empty dict/list
        - Stub implementations

        Args:
            src_directory: Path to src directory
        """
        python_files = list(src_directory.rglob('*.py'))
        mock_implementations = []

        mock_patterns = [
            (re.compile(r'class\s+\w*Mock\w*'), "Mock class"),
            (re.compile(r'class\s+\w*Fake\w*'), "Fake class"),
            (re.compile(r'class\s+\w*Stub\w*'), "Stub class"),
            (re.compile(r'return\s+\{\}.*#.*mock'), "Mock return"),
            (re.compile(r'return\s+\[\].*#.*mock'), "Mock return"),
        ]

        for py_file in python_files:
            content = py_file.read_text()

            for pattern, description in mock_patterns:
                matches = pattern.finditer(content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    mock_implementations.append((py_file, line_num, description))

        # Report results
        if mock_implementations:
            print(f"\nMock implementations found in {len(mock_implementations)} locations:")
            for py_file, line_num, description in mock_implementations:
                print(f"  {py_file.relative_to(src_directory)} line {line_num}: {description}")

        assert not mock_implementations, \
            f"Found {len(mock_implementations)} mock implementations"

    # Helper methods

    def _find_placeholders(self, tree: ast.AST, py_file: Path) -> List[Tuple[str, str]]:
        """Find placeholder implementations in AST"""
        placeholders = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip abstract methods
                if any(isinstance(d, ast.Name) and d.id == 'abstractmethod'
                      for d in node.decorator_list):
                    continue

                # Check for placeholder patterns
                if not node.body:
                    continue

                first_stmt = node.body[0]

                # Check for pass statement
                if isinstance(first_stmt, ast.Pass):
                    placeholders.append((node.name, "Empty function with 'pass'"))

                # Check for NotImplementedError
                elif isinstance(first_stmt, ast.Raise):
                    if isinstance(first_stmt.exc, ast.Call):
                        if isinstance(first_stmt.exc.func, ast.Name):
                            if first_stmt.exc.func.id == 'NotImplementedError':
                                placeholders.append((node.name, "Raises NotImplementedError"))

                # Check for Ellipsis
                elif isinstance(first_stmt, ast.Expr):
                    if isinstance(first_stmt.value, ast.Constant):
                        if first_stmt.value.value is ...:
                            placeholders.append((node.name, "Ellipsis placeholder"))

        return placeholders

    def _check_type_hints(self, tree: ast.AST, py_file: Path) -> List[Tuple[str, int]]:
        """Check for missing type hints in public functions"""
        missing_hints = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private functions
                if node.name.startswith('_'):
                    continue

                # Skip __init__ and __post_init__
                if node.name in ('__init__', '__post_init__'):
                    continue

                # Check for return annotation
                has_return_hint = node.returns is not None

                # Check for parameter annotations
                has_param_hints = all(
                    arg.annotation is not None
                    for arg in node.args.args
                    if arg.arg != 'self' and arg.arg != 'cls'
                )

                if not (has_return_hint and has_param_hints):
                    missing_hints.append((node.name, node.lineno))

        return missing_hints