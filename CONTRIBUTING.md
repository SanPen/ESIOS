# Contributing to ESIOS

Thank you for considering contributing to ESIOS! We appreciate your interest in making this project better.

## Code of Conduct

Before you begin, please make sure to read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We have established this code to ensure a welcoming and inclusive environment for all contributors.

## How Can I Contribute?

You can contribute to ESIOS in various ways, including but not limited to:

- **Reporting Issues:** If you encounter a bug or have a feature request, please open an issue on our [GitHub Issues](https://github.com/SanPen/ESIOS/issues) page.

- **Submitting Pull Requests (PRs):** If you have code or documentation changes to propose, feel free to open a pull request. Make sure your PR includes a clear description and addresses a specific issue or feature.

## Getting Started

If you're new to open-source contribution or you're unsure how to get started, you can follow these general steps:

1. **Fork** the ESIOS repository to your GitHub account.

2. **Clone** your forked repository to your local machine.

   ```bash
   git clone https://github.com/your-username/ESIOS.git
   ```
3. (Optional) - Create a **New Branch**.

   ```bash
    git checkout -b feature/your-feature-name
    ```
4. Install the dev dependencies.
   ```bash
    make init-dev
    ```
5. Make your changes, write code, and/or documentation.
6. Ensure your code follows the project's coding standards and conventions. You can run to check for linting:
   ```bash
    make lint-check
    ```
    And if you want automatic fixing:
   ```bash
    make lint-fix
    ```
    Still some things might have to be checked again.

7. Test your changes thoroughly to verify they work as intended. You can also run

   ```bash
    make test
    ```
8. Commit your changes and push them to your forked repository.
   ```bash
    git commit -m "Add your detailed commit message here"
    git push origin feature/your-feature-name
    ```
9. Create a Pull Request from your fork to the ESIOS repository. Be sure to describe your changes in detail, including references to any relevant issues.
Be sure to have also tests if you write new code. And make sure the linting is correct.

## Code of Conduct

All contributors are expected to adhere to our Code of Conduct. By participating, you are agreeing to uphold the principles outlined in the code.

## Support and Questions

If you have questions or need assistance with your contribution, feel free to reach out on our GitHub Discussions.

## Thank You

Your contributions help make ESIOS better for everyone. We greatly appreciate your time and efforts in helping us improve the project.