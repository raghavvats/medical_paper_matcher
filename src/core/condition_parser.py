from typing import Dict, List, Union, Set

class ConditionParser:
    def __init__(self):
        self.operators = {'AND', 'OR'}
        
    def parse_conditions(self, conditions: str, profile: Dict, ideal_profile: Dict) -> bool:
        """
        Parse and evaluate conditions against a profile.
        
        Args:
            conditions: String representing the condition logic (e.g., "(Race OR Age) AND preexisting_conditions")
            profile: Dictionary containing the actual profile characteristics
            ideal_profile: Dictionary containing the desired characteristics
            
        Returns:
            bool: True if profile matches conditions, False otherwise
        """
        # Handle empty or None conditions
        if not conditions:
            return True
            
        # Remove extra whitespace and parentheses
        conditions = conditions.strip()
        
        # Handle simple single condition
        if conditions.upper() not in self.operators and '(' not in conditions:
            return self._evaluate_single_condition(conditions, profile, ideal_profile)
            
        # Handle compound conditions
        return self._evaluate_compound_conditions(conditions, profile, ideal_profile)
    
    def _evaluate_single_condition(self, condition: str, profile: Dict, ideal_profile: Dict) -> bool:
        """
        Evaluate a single condition against profile characteristics.
        
        Args:
            condition: String representing a single characteristic to check
            profile: Dictionary containing the actual profile characteristics
            ideal_profile: Dictionary containing the desired characteristics
            
        Returns:
            bool: True if condition is met, False otherwise
        """
        condition = condition.strip()
        print(f"\nEvaluating single condition: {condition}")
        
        # Get nested value if it exists
        def get_nested_value(d: Dict, key: str):
            # First try direct access
            if key in d:
                return d[key]
            
            # Then try each section
            for section in ['physical', 'demographics', 'medical_history', 'lifestyle']:
                if section in d:
                    if isinstance(d[section], dict):
                        if key in d[section]:
                            return d[section][key]
                        # For medical_history, check lists
                        if section == 'medical_history' and key in ['preexisting_conditions', 'prior_conditions', 'surgeries', 'active_medications']:
                            return d[section].get(key, [])
            return None
        
        profile_value = get_nested_value(profile, condition)
        ideal_value = get_nested_value(ideal_profile, condition)
        
        print(f"Profile value: {profile_value}")
        print(f"Ideal value: {ideal_value}")
        
        if profile_value is None or ideal_value is None:
            print(f"One of the values is None")
            return False
            
        # Handle age ranges
        if condition == 'age' and isinstance(ideal_value, list) and len(ideal_value) == 2:
            result = ideal_value[0] <= profile_value <= ideal_value[1]
            print(f"Age range check: {ideal_value[0]} <= {profile_value} <= {ideal_value[1]} = {result}")
            return result
            
        # Handle list/set type values (e.g., preexisting_conditions)
        if isinstance(profile_value, (list, set)) and isinstance(ideal_value, (list, set)):
            if not ideal_value:  # If ideal value is empty list, accept any value
                print("Empty ideal list - accepting any value")
                return True
            
            # Convert both to sets for intersection
            profile_set = set(profile_value)
            ideal_set = set(ideal_value)
            
            # Normal set intersection
            result = bool(profile_set & ideal_set)
            print(f"Set intersection: {profile_set} & {ideal_set} = {result}")
            return result
            
        # Handle empty constraints
        if isinstance(ideal_value, list) and not ideal_value:
            print("Empty constraint - accepting any value")
            return True
            
        # Handle single value comparison
        result = profile_value == ideal_value
        print(f"Direct comparison: {profile_value} == {ideal_value} = {result}")
        return result
    
    def _evaluate_compound_conditions(self, conditions: str, profile: Dict, ideal_profile: Dict) -> bool:
        """
        Evaluate compound conditions with AND/OR operators.
        
        Args:
            conditions: String representing compound conditions
            profile: Dictionary containing the actual profile characteristics
            ideal_profile: Dictionary containing the desired characteristics
            
        Returns:
            bool: True if conditions are met, False otherwise
        """
        # Handle parentheses groups
        while '(' in conditions:
            innermost = self._find_innermost_parentheses(conditions)
            if not innermost:
                break
                
            result = self._evaluate_simple_expression(innermost, profile, ideal_profile)
            conditions = conditions.replace(f"({innermost})", str(result))
            
        return self._evaluate_simple_expression(conditions, profile, ideal_profile)
    
    def _find_innermost_parentheses(self, expression: str) -> str:
        """
        Find the contents of the innermost parentheses in an expression.
        
        Args:
            expression: String containing nested parentheses
            
        Returns:
            str: Contents of innermost parentheses
        """
        start = expression.rfind('(')
        if start == -1:
            return ''
            
        end = expression.find(')', start)
        if end == -1:
            return ''
            
        return expression[start + 1:end]
    
    def _evaluate_simple_expression(self, expression: str, profile: Dict, ideal_profile: Dict) -> bool:
        """
        Evaluate a simple expression without parentheses.
        
        Args:
            expression: String representing a simple expression (e.g., "Race OR Age")
            profile: Dictionary containing the actual profile characteristics
            ideal_profile: Dictionary containing the desired characteristics
            
        Returns:
            bool: True if expression evaluates to True, False otherwise
        """
        expression = expression.strip()
        
        # Handle literal boolean values from previous evaluations
        if expression.lower() == 'true':
            return True
        if expression.lower() == 'false':
            return False
            
        parts = expression.split()
        
        # Process OR conditions
        if 'OR' in parts:
            conditions = [p for p in parts if p != 'OR']
            return any(self._evaluate_single_condition(cond, profile, ideal_profile) 
                      for cond in conditions)
        
        # Process AND conditions
        if 'AND' in parts:
            conditions = [p for p in parts if p != 'AND']
            return all(self._evaluate_single_condition(cond, profile, ideal_profile) 
                      for cond in conditions)
        
        # Single condition
        return self._evaluate_single_condition(expression, profile, ideal_profile)
