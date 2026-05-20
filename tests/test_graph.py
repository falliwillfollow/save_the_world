from __future__ import annotations

import unittest

from ciac.graph import DependencyCycleError, dependency_order


class GraphTests(unittest.TestCase):
    def test_dependency_order_places_dependencies_first(self) -> None:
        patterns = {
            "a": {"dependencies": []},
            "b": {"dependencies": [{"id": "a", "kind": "pattern"}]},
            "c": {"dependencies": [{"id": "b", "kind": "pattern"}]},
        }
        self.assertEqual(dependency_order(patterns, ["c", "b", "a"]), ["a", "b", "c"])

    def test_dependency_cycle_is_rejected(self) -> None:
        patterns = {
            "a": {"dependencies": [{"id": "b", "kind": "pattern"}]},
            "b": {"dependencies": [{"id": "a", "kind": "pattern"}]},
        }
        with self.assertRaises(DependencyCycleError):
            dependency_order(patterns, ["a", "b"])


if __name__ == "__main__":
    unittest.main()

