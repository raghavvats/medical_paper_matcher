from src.cli.profile_input import ProfileInputCLI

def test_cli():
    cli = ProfileInputCLI()
    
    # Test individual components
    print("Testing physical characteristics input:")
    physical = cli._get_physical_characteristics()
    print(f"Result: {physical}\n")

    print("Testing demographics input:")
    demographics = cli._get_demographics()
    print(f"Result: {demographics}\n")

    # Uncomment to test full profile collection
    # profile = cli.collect_profile()
    # cli.save_profile(profile, "test_profile")

if __name__ == "__main__":
    test_cli() 