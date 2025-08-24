#!/usr/bin/env python3
"""
Comprehensive test runner for all Portia plans.
Run this to test all agent plans in sequence.
"""

import sys
import traceback

def run_test(test_name, test_function):
    """Run a single test with error handling."""
    print(f"\n{'='*60}")
    print(f"TESTING: {test_name}")
    print('='*60)
    
    try:
        test_function()
        print(f"✅ {test_name} - PASSED")
        return True
    except Exception as e:
        print(f"❌ {test_name} - FAILED")
        print(f"Error: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Portia Plans Test Suite")
    print("Testing all agent plans...")
    
    # Import test functions
    try:
        from app.tests.research_test import test_run_market_research_plan
        from app.tests.content_test import test_run_content_planning_system
        from app.tests.publishing_test import test_run_publishing_plan
        from app.tests.podcast_test import test_run_podcast_plan
        from app.tests.video_test import test_run_video_plan
    except ImportError as e:
        print(f"❌ Failed to import test modules: {e}")
        return False
    
    # Define tests to run
    tests = [
        ("Research Plans", test_run_market_research_plan),
        ("Content Plans", test_run_content_planning_system),
        ("Publishing Plans", test_run_publishing_plan),
        ("Podcast Plans", test_run_podcast_plan),
        ("Video Plans", test_run_video_plan),
    ]
    
    # Run all tests
    results = []
    for test_name, test_func in tests:
        results.append(run_test(test_name, test_func))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
