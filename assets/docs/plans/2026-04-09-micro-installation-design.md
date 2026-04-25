# Design: Global Micro Editor Installation

## Objective
Make the `micro` text editor globally accessible across all terminal sessions (PowerShell and Bash) on the Windows system.

## Proposed Changes
1. **Target Directory**: Use `C:\Users\Rob\bin` as a dedicated location for user-specific binaries.
2. **Binary Migration**: Move `micro.exe` from the project root (`D:\download_other\AWS\2026 Cloud Security Architect Roadmap\`) to the target directory.
3. **PATH Configuration**: Update the User environment variable `PATH` to include `C:\Users\Rob\bin`.
4. **Cleanup**: Remove any temporary installation artifacts (like the `micro-2.0.15` folder if it exists).

## Verification Plan
1. Open a new PowerShell/Bash session.
2. Run `micro --version` from a directory other than the current project root.
3. Verify the binary location using `Get-Command micro` or `which micro`.

## Constraints & Considerations
- **Running Process**: If `micro` is currently open, the move operation might fail. The user will be asked to close it if necessary.
- **Permission**: Adding to PATH is a User-level change, which shouldn't require Admin rights in most configurations.
