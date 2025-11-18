import pytest

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Custom summary to help students understand results."""
    terminalreporter.write_sep("=", "Assignment Test Summary")
    
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    
    terminalreporter.write_line(f"\n✅ Passed: {passed}")
    terminalreporter.write_line(f"❌ Failed: {failed}")
    terminalreporter.write_line(f"⏭️  Skipped: {skipped}")
    
    if failed == 0 and passed > 0:
        terminalreporter.write_line("\n🎉 Congratulations! All implemented tests pass!")
    elif failed > 0:
        terminalreporter.write_line("\n💡 Review the failure hints above to fix issues.")
        terminalreporter.write_line("   Run individual tests with: pytest test_assignment.py::TestPartA::test_name -v")
