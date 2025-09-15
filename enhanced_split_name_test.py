#!/usr/bin/env python3
"""
Enhanced split_name function with additional edge case handling and comprehensive tests
"""


def split_name_enhanced(full_name: str | None) -> tuple[str, str]:
    """
    Split full name into first_name and last_name with robust edge case handling.

    Args:
        full_name: The full name to split. Can be None, empty, or contain various formats.

    Returns:
        A tuple of (first_name, last_name). Returns ("Unknown", "Unknown") for
        invalid/empty inputs.

    Examples:
        >>> split_name_enhanced("John Smith")
        ('John', 'Smith')
        >>> split_name_enhanced("John Michael Smith")
        ('John', 'Michael Smith')
        >>> split_name_enhanced("Madonna")
        ('Madonna', 'Unknown')
        >>> split_name_enhanced("")
        ('Unknown', 'Unknown')
    """
    # Handle None input
    if full_name is None:
        return "Unknown", "Unknown"

    # Handle empty or whitespace-only strings
    if not full_name or not full_name.strip():
        return "Unknown", "Unknown"

    # Clean and split the name - handles multiple types of whitespace
    cleaned_name = " ".join(
        full_name.split()
    )  # This handles tabs, newlines, multiple spaces
    parts = [part for part in cleaned_name.split() if part and not part.isspace()]

    # Handle case where cleaning resulted in no valid parts
    if not parts:
        return "Unknown", "Unknown"

    # Handle single name
    if len(parts) == 1:
        return parts[0], "Unknown"

    # Handle multiple names: first name + remaining names as last name
    return parts[0], " ".join(parts[1:])


def split_name_current(full_name):
    """Current implementation from api.py"""
    if not full_name or not full_name.strip():
        return "Unknown", "Unknown"

    # Clean and split the name
    parts = [part for part in full_name.strip().split() if part]

    if len(parts) == 1:
        return parts[0], "Unknown"
    else:
        return parts[0], " ".join(parts[1:])


def test_enhanced_vs_current():
    """Test enhanced version against current implementation with additional edge cases"""

    print("ENHANCED vs CURRENT split_name comparison")
    print("=" * 60)

    # Include original test cases plus new edge cases
    test_cases = [
        # Original test cases
        ("John Smith", "John", "Smith", "Normal two names"),
        ("John", "John", "Unknown", "Single name"),
        ("John Michael Smith", "John", "Michael Smith", "Three names"),
        ("John    Smith", "John", "Smith", "Multiple spaces"),
        ("  John Smith  ", "John", "Smith", "Leading/trailing spaces"),
        ("", "Unknown", "Unknown", "Empty string"),
        ("   ", "Unknown", "Unknown", "Only spaces"),
        ("Mary-Jane Watson", "Mary-Jane", "Watson", "Hyphenated first name"),
        ("Alisa Green", "Alisa", "Green", "Two names with no issues"),
        ("Sarah Jane Doe", "Sarah", "Jane Doe", "Three names - first + rest"),
        ("Madonna Black ", "Madonna", "Black", "Two names with trailing space"),
        # New edge cases
        (None, "Unknown", "Unknown", "None input"),
        ("O'Connor Smith", "O'Connor", "Smith", "Apostrophe in name"),
        ("Dr. John Smith", "Dr.", "John Smith", "Title with period"),
        ("José María García", "José", "María García", "Unicode characters"),
        ("John\tSmith", "John", "Smith", "Tab separator"),
        ("John\nSmith", "John", "Smith", "Newline separator"),
        ("  \t  \n  ", "Unknown", "Unknown", "Mixed whitespace only"),
        ("A", "A", "Unknown", "Single character name"),
        ("X Y Z W", "X", "Y Z W", "Four names"),
    ]

    enhanced_failures = 0
    current_failures = 0

    for i, (input_name, expected_first, expected_last, description) in enumerate(
        test_cases, 1
    ):
        print(f"\nTest {i}: {description}")
        print(f"Input: {repr(input_name)}")

        try:
            # Test current function
            if input_name is None:
                # Current function doesn't handle None, so we'll expect it to fail
                try:
                    current_first, current_last = split_name_current(input_name)
                except (AttributeError, TypeError):
                    current_first, current_last = "ERROR", "ERROR"
            else:
                current_first, current_last = split_name_current(input_name)

            # Test enhanced function
            enhanced_first, enhanced_last = split_name_enhanced(input_name)

            print(f"CURRENT:  first='{current_first}', last='{current_last}'")
            print(f"ENHANCED: first='{enhanced_first}', last='{enhanced_last}'")
            print(f"EXPECTED: first='{expected_first}', last='{expected_last}'")

            # Check current function
            current_correct = (
                current_first == expected_first and current_last == expected_last
            )
            if not current_correct:
                current_failures += 1
                print("CURRENT: ❌ FAILED")
            else:
                print("CURRENT: ✅ PASSED")

            # Check enhanced function
            enhanced_correct = (
                enhanced_first == expected_first and enhanced_last == expected_last
            )
            if not enhanced_correct:
                enhanced_failures += 1
                print("ENHANCED: ❌ FAILED")
            else:
                print("ENHANCED: ✅ PASSED")

        except Exception as e:
            print(f"ERROR during testing: {e}")
            current_failures += 1
            enhanced_failures += 1

    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print(
        f"CURRENT Function:  {current_failures}/{len(test_cases)} FAILURES ({((len(test_cases)-current_failures)/len(test_cases)*100):.1f}% success rate)"
    )
    print(
        f"ENHANCED Function: {enhanced_failures}/{len(test_cases)} FAILURES ({((len(test_cases)-enhanced_failures)/len(test_cases)*100):.1f}% success rate)"
    )


if __name__ == "__main__":
    test_enhanced_vs_current()
