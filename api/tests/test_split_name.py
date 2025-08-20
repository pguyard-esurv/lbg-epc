#!/usr/bin/env python3
"""
Test suite for the split_name functions to find the bugs
"""

def split_name_old(full_name):
    """Old buggy implementation"""
    parts = full_name.split(" ")
    if len(parts) == 1:
        return "", parts[0]
    return " ".join(parts[:-1]), parts[-1]

def split_name_new(full_name):
    """Split full name into first_name and last_name"""
    if not full_name or not full_name.strip():
        return "Unknown", "Unknown"
    
    # Clean and split the name
    parts = [part for part in full_name.strip().split() if part]
    
    if len(parts) == 1:
        return parts[0], "Unknown"
    else:
        return parts[0], " ".join(parts[1:])

def test_split_name_comparison():
    """Test cases comparing old vs new implementations"""
    
    print("COMPARISON: OLD vs NEW split_name functions")
    print("=" * 60)
    
    test_cases = [
        # (input, expected_first, expected_last, description)
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
    ]
    
    old_bugs_found = 0
    new_bugs_found = 0
    
    for i, (input_name, expected_first, expected_last, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"Input: '{input_name}'")
        
        try:
            # Test old function
            old_first, old_last = split_name_old(input_name)
            print(f"OLD:      first='{old_first}', last='{old_last}'")
            
            # Test new function
            new_first, new_last = split_name_new(input_name)
            print(f"NEW:      first='{new_first}', last='{new_last}'")
            
            print(f"EXPECTED: first='{expected_first}', last='{expected_last}'")
            
            # Check old function
            old_correct = (old_first == expected_first and old_last == expected_last)
            if not old_correct:
                old_bugs_found += 1
                print("OLD: ❌ FAILED")
                
                # Explain the specific bug
                if input_name == "John" and old_first == "" and old_last == "John":
                    print("   🐛 BUG: Single name goes to last_name, first_name is empty!")
                elif "   " in input_name and old_first != expected_first:
                    print("   🐛 BUG: Multiple spaces create issues!")
                elif input_name == "John Michael Smith" and old_first == "John Michael":
                    print("   🐛 BUG: Wrong splitting - all names except last go to first!")
            else:
                print("OLD: ✅ PASSED")
            
            # Check new function
            new_correct = (new_first == expected_first and new_last == expected_last)
            if not new_correct:
                new_bugs_found += 1
                print("NEW: ❌ FAILED")
            else:
                print("NEW: ✅ PASSED")
                
        except Exception as e:
            print(f"ERROR: {e}")
            old_bugs_found += 1
            new_bugs_found += 1
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print(f"OLD Function: {old_bugs_found}/{len(test_cases)} BUGS FOUND ({((len(test_cases)-old_bugs_found)/len(test_cases)*100):.1f}% success rate)")
    print(f"NEW Function: {new_bugs_found}/{len(test_cases)} BUGS FOUND ({((len(test_cases)-new_bugs_found)/len(test_cases)*100):.1f}% success rate)")

if __name__ == "__main__":
    test_split_name_comparison()