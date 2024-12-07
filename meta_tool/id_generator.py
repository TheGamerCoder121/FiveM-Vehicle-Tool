#!/usr/bin/env python3

import random
from typing import Set

class IDGenerator:
    """Generates unique IDs for GTA V meta files."""

    def __init__(self, existing_ids: Set[int] = None):
        self.existing_ids = existing_ids or set()

    def generate_carcols_id(self) -> int:
        """
        Generate a unique random number for carcols ID.

        Returns:
            int: A unique random number
        """
        while True:
            # Generate a random number (wide range for uniqueness)
            new_id = random.randint(10000, 99999)
            if new_id not in self.existing_ids:
                self.existing_ids.add(new_id)
                return new_id

    def generate_modkit_id(self) -> int:
        """
        Generate a unique 2-6 digit number for modkit ID.

        Returns:
            int: A unique number between 10 and 999999
        """
        while True:
            # Generate a random 2-6 digit number
            new_id = random.randint(10, 999999)
            if new_id not in self.existing_ids:
                self.existing_ids.add(new_id)
                return new_id

    def validate_id_availability(self, id_value: int) -> bool:
        """
        Check if an ID is available (not in use).

        Args:
            id_value: The ID to check

        Returns:
            bool: True if the ID is available
        """
        return id_value not in self.existing_ids
