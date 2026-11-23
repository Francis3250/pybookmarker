# NAME Wentai Yan
# EMAIL wentaiy@uci.edu

"""
Dog feeding simulation program.

This module implements a virtual dog adoption and feeding system with
different breeds.
"""

from abc import ABC, abstractmethod
import random
import time


class Appetite:
    """Constants for different appetite levels."""

    LOW = 3
    MEDIUM = 4
    HIGH = 5


class Dog(ABC):
    """Abstract base class representing a dog with basic behaviors."""

    def __init__(self, name, age, appetite) -> None:
        """
        Initialize a dog with basic attributes.

        Args:
            name (str): The dog's name
            age (int): The dog's age in years
            appetite (int): The dog's appetite level
        """
        self.hunger_clock = 0
        self._name = name
        self._age = age
        self.appetite = appetite

    @abstractmethod
    def breed(self):
        """Return the breed name of the dog."""
        ...

    def name(self):
        """Return the dog's name."""
        return self._name

    def age(self):
        """Return the dog's age."""
        return self._age

    def hungry(self, notify_callback: callable, interval: float = 2.0):
        """
        Monitor hunger status automatically.

        Once determined "hungry", calls notify_callback(self).

        Args:
            notify_callback (callable): Callback function to be called when
                triggered, should accept a single parameter (this Dog
                instance).
            interval (float): Sleep seconds between each loop to avoid high
                CPU usage.
        """
        while True:
            # Check if hunger should be triggered
            if self.hunger_clock > self.appetite:
                # 50% chance of being truly hungry
                if random.getrandbits(1):
                    notify_callback(self)
                    # Reset after eating/feeding
                    self.hunger_clock = 0
                    # Continue to next round after reset to avoid immediately
                    # entering else branch
                    time.sleep(interval)
                    continue
            else:
                self.hunger_clock += 1

            time.sleep(interval)

    def feed(self):
        """Reset the hunger timer."""
        self.hunger_clock = 0


class GermanShepherd(Dog):
    """Represents a German Shepherd dog breed."""

    def __init__(self, name, age):
        """
        Initialize a German Shepherd.

        Args:
            name (str): The dog's name
            age (int): The dog's age in years
        """
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        """Return the breed name."""
        return "German Shepherd"


class GoldenRetriever(Dog):
    """Represents a Golden Retriever dog breed."""

    def __init__(self, name, age):
        """
        Initialize a Golden Retriever.

        Args:
            name (str): The dog's name
            age (int): The dog's age in years
        """
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        """Return the breed name."""
        return "Golden Retriever"


class AnatolianShepherd(Dog):
    """Represents an Anatolian Shepherd dog breed."""

    def __init__(self, name, age):
        """
        Initialize an Anatolian Shepherd.

        Args:
            name (str): The dog's name
            age (int): The dog's age in years
        """
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        """Return the breed name."""
        return "Anatolian Shepherd"


def feed_dog(d: Dog):
    """
    Handle feeding interaction with the dog.

    Args:
        d (Dog): The dog instance that needs feeding
    """
    print(f"\n{d.name()} is hungry! 🍖")
    action = input("Feed now?  (y)es / (q)uit : \n").lower().strip()

    if action == "y":
        d.feed()
        print("Nom nom... All good!\n")
    elif action == "q":
        print("Goodbye! 👋")
        exit(0)
    else:
        print("Skipped feeding this time.\n")


if __name__ == "__main__":
    # Interactive dog selection
    breeds = {
        "1": GermanShepherd,
        "2": GoldenRetriever,
        "3": AnatolianShepherd,
    }

    choice = input(
        "Which breed would you like?\n"
        "  1. German Shepherd\n"
        "  2. Golden Retriever\n"
        "  3. Anatolian Shepherd\n"
        ": "
    ).strip()

    if choice not in breeds:
        print("Invalid choice. Exiting.")
        exit(1)

    name = input("Dog's name: ").strip() or "Buddy"
    age = int(input("Dog's age: ").strip() or "3")

    dog = breeds[choice](name, age)
    print(f"\nGreat! You adopted a {dog.breed()} named {dog.name()}.\n")

    # Start monitoring (blocking loop)
    dog.hungry(feed_dog)
