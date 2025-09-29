# Contributing

Thank you for your interest in contributing to Triality! This document provides guidelines and instructions for contributing to this project.

## Ground rules

- Keep PRs surgical. Add tests. Update docs when behavior changes.
- No data that you don't own or can't license. Prefer tiny, reproducible samples.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Conda package manager

### Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd triality
   ```

2. Create and activate the conda environment:
   ```bash
   conda env create -f env/environment.yml
   conda activate triality
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Run tests to verify setup:
   ```bash
   pytest -q
   ```

## Testing

### Test Categories

- **Unit Tests**: `src/dsp/*`, `src/triad/*` (pytest)
- **Reproduction Tests**: `scripts/run-replication.sh` must pass (generates v11 report)

### Running Tests

```bash
# Run all tests
pytest

# Run tests quietly
pytest -q

# Run specific test categories
pytest src/dsp/
pytest src/triad/

# Run reproduction tests
scripts/run-replication.sh
```

## Code Style and Standards

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks will run automatically on commit and include:

- Code formatting (black, isort)
- Linting (flake8, pylint)
- Type checking (mypy)
- Security checks (bandit)

### Code Formatting

- Use `black` for code formatting
- Use `isort` for import sorting
- Follow PEP 8 style guidelines

## Pull Request Process

### Before Submitting

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the ground rules above
3. **Add tests** for new functionality
4. **Update documentation** if behavior changes
5. **Run tests** to ensure everything passes
6. **Run pre-commit hooks** to ensure code quality

### PR Guidelines

- **Keep PRs surgical**: Focus on a single feature or bug fix
- **Write clear commit messages**: Use conventional commit format when possible
- **Add tests**: Include unit tests for new functionality
- **Update docs**: Update relevant documentation for behavior changes
- **Use descriptive titles**: Make it clear what the PR accomplishes
- **Provide context**: Explain the problem and solution in the PR description

### PR Template

When creating a PR, please include:

- **Description**: What changes were made and why
- **Testing**: How the changes were tested
- **Documentation**: Any documentation updates made
- **Breaking Changes**: Any breaking changes (if applicable)

## Data and Licensing

- **No proprietary data**: Do not include data you don't own or can't license
- **Use sample data**: Prefer tiny, reproducible samples for testing
- **Respect licenses**: Ensure all data and dependencies are properly licensed

## Getting Help

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for questions and general discussion
- **Documentation**: Check the project documentation for detailed information

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (Apache License 2.0).

## Code of Conduct

Please note that this project follows a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

Thank you for contributing to Triality!
