from typing import Any, Dict, List, Type
import json
import os
from enum import Enum

from src.models.profile import (
    CustomerProfile, PhysicalCharacteristics, Demographics, 
    MedicalHistory, Lifestyle, Sex, Race, Continent,
    PreexistingCondition, PriorCondition, Surgery, 
    Medication, Athleticism, Diet
)

class ProfileInputCLI:
    @staticmethod
    def _get_enum_input(enum_class: Type[Enum], prompt: str) -> str:
        while True:
            print(f"\n{prompt}")
            for i, option in enumerate(enum_class, 1):
                print(f"{i}. {option.value}")
            
            try:
                choice = int(input("\nEnter the number of your choice: "))
                if 1 <= choice <= len(enum_class):
                    return list(enum_class)[choice-1].value
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def _get_multi_enum_input(enum_class: Type[Enum], prompt: str) -> List[str]:
        print(f"\n{prompt}")
        print("Enter numbers separated by commas, or press Enter if none apply.")
        for i, option in enumerate(enum_class, 1):
            print(f"{i}. {option.value}")
        
        while True:
            try:
                choices = input("\nEnter your choices (e.g., 1,3,4): ").strip()
                if not choices:
                    return []
                
                indices = [int(x.strip()) for x in choices.split(",")]
                if all(1 <= idx <= len(enum_class) for idx in indices):
                    return [list(enum_class)[idx-1].value for idx in indices]
                print("Invalid choice(s). Please try again.")
            except ValueError:
                print("Please enter valid numbers separated by commas.")

    def _get_physical_characteristics(self) -> Dict[str, Any]:
        print("\n=== Physical Characteristics ===")
        while True:
            try:
                age = int(input("Enter age (0-120): "))
                weight = float(input("Enter weight in lbs (0-1000): "))
                height = float(input("Enter height in inches (0-120): "))
                sex = self._get_enum_input(Sex, "Select sex:")
                
                return {
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "sex": sex
                }
            except ValueError:
                print("Invalid input. Please try again.")

    def _get_demographics(self) -> Dict[str, Any]:
        print("\n=== Demographics ===")
        return {
            "race": self._get_enum_input(Race, "Select race:"),
            "location": self._get_enum_input(Continent, "Select continent:")
        }

    def _get_medical_history(self) -> Dict[str, Any]:
        print("\n=== Medical History ===")
        return {
            "preexisting_conditions": self._get_multi_enum_input(
                PreexistingCondition, "Select preexisting conditions:"
            ),
            "prior_conditions": self._get_multi_enum_input(
                PriorCondition, "Select prior conditions:"
            ),
            "surgeries": self._get_multi_enum_input(
                Surgery, "Select surgeries:"
            ),
            "active_medications": self._get_multi_enum_input(
                Medication, "Select active medications:"
            )
        }

    def _get_lifestyle(self) -> Dict[str, Any]:
        print("\n=== Lifestyle ===")
        return {
            "athleticism": self._get_enum_input(Athleticism, "Select athleticism level:"),
            "diet": self._get_enum_input(Diet, "Select diet type:")
        }

    def collect_profile(self) -> CustomerProfile:
        """Collect all profile information from user input."""
        print("Welcome to the Customer Profile Input System")
        print("Please provide the following information:")

        profile_data = {
            "physical": self._get_physical_characteristics(),
            "demographics": self._get_demographics(),
            "medical_history": self._get_medical_history(),
            "lifestyle": self._get_lifestyle()
        }

        return CustomerProfile(**profile_data)

    def save_profile(self, profile: CustomerProfile, filename: str) -> None:
        """Save the profile to a JSON file."""
        os.makedirs("data/profiles", exist_ok=True)
        filepath = f"data/profiles/{filename}.json"
        
        with open(filepath, 'w') as f:
            json.dump(profile.dict(), f, indent=2)
        print(f"\nProfile saved to {filepath}")

def main():
    cli = ProfileInputCLI()
    try:
        profile = cli.collect_profile()
        filename = input("\nEnter filename to save profile (without extension): ")
        cli.save_profile(profile, filename)
    except KeyboardInterrupt:
        print("\nProfile collection cancelled.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
