"""Tests for the Red team agent.

These were rewritten against the current constructors. The previous version called
`Team(model_ID, energy, potency, influence_factor, alignment)` and a `team()` method,
neither of which exist any more, so every test here failed with a TypeError before
asserting anything -- and nobody saw it, because pytest aborted during collection.

Imports go through `class_api.team` rather than a bare `team`, so that patching
`class_api.team.get_message` reaches the same module object the tests exercise.
"""
import unittest
from unittest.mock import patch

import networkx as nx

from class_api.team import RedTeam


def make_red(**overrides):
    """Build a RedTeam with the current constructor.

    The signature is long and entirely positional, so tests build through this one
    helper: when it changes again, this is the only place that has to follow.
    """
    params = {
        "team": "red",
        "model_ID": "test-model",
        "potency": 0,
        "msg_count": 0,
        "influence_factor": 1.5,
        "temperature": 0.5,
        "penalty": 20,
        "penalty_threshold": 70,
        "alignment": 50,
    }
    params.update(overrides)
    return RedTeam(**params)


def network_with(node_id=1, alignment=0.2, rejecting=False):
    """A one-node graph carrying the attributes red_agent_penalty reads."""
    graph = nx.DiGraph()
    graph.add_node(node_id, Alignment=alignment, rejectMessaging=rejecting)
    return graph


class TestRedTeamConstruction(unittest.TestCase):
    def test_initialisation(self):
        red = make_red()
        self.assertEqual(red._team, "red")
        self.assertEqual(red._model_ID, "test-model")
        self.assertEqual(red._message_count, 0)
        self.assertEqual(red._influence_factor, 1.5)
        self.assertEqual(red._alignment, 50)
        self.assertEqual(red._temperature, 0.5)
        self.assertEqual(red._penalty, 20)
        self.assertEqual(red._penalty_threshold, 70)

    def test_potency_argument_is_ignored(self):
        """`Team.__init__` accepts `potency` and then unconditionally sets `_potency = None`.

        Pinned deliberately. The old test asserted the argument was stored, which is part
        of why it failed. Potency belongs to a message, not to the agent, and is assigned
        by generate_message. If the constructor ever starts honouring the argument this
        test should fail loudly rather than the behaviour drifting unnoticed.
        """
        self.assertIsNone(make_red(potency=80)._potency)


class TestRedTeamRounds(unittest.TestCase):
    def test_next_round_counts_messages(self):
        red = make_red()
        red.next_round()
        red.next_round()
        self.assertEqual(red._message_count, 2)

    def test_update_alignment(self):
        red = make_red()
        red.update_alignment(72)
        self.assertEqual(red._alignment, 72)


class TestRedTeamMessages(unittest.TestCase):
    def test_generate_message_stores_rather_than_returns(self):
        """generate_message assigns to _message/_potency and returns None.

        The old test unpacked a return value (`message, potency = ...`). Anything relying
        on that reads None, which is how a failure here would surface elsewhere.
        """
        red = make_red()
        with patch("class_api.team.get_message", return_value=("a message", 65)) as get_msg:
            returned = red.generate_message(topic="vaccines", previous="")

        self.assertIsNone(returned)
        self.assertEqual(red._message, "a message")
        self.assertEqual(red._potency, 65)
        get_msg.assert_called_once()

    def test_generate_message_passes_agent_state_through(self):
        red = make_red(alignment=41, temperature=0.9)
        red.next_round()
        with patch("class_api.team.get_message", return_value=("m", 10)) as get_msg:
            red.generate_message(topic="climate", previous="")

        args, _ = get_msg.call_args
        self.assertEqual(args[0], "red")
        self.assertEqual(args[1], "test-model")
        self.assertEqual(args[2], 41)
        self.assertEqual(args[3], 0.9)
        self.assertEqual(args[4], 1)
        self.assertEqual(args[5], "climate")


class TestRedAgentPenalty(unittest.TestCase):
    """The penalty turns a node away from Red entirely, so both guards matter."""

    def test_below_threshold_leaves_the_node_alone(self):
        red = make_red(penalty_threshold=70)
        graph = network_with()
        # Deterministic: the potency check short-circuits before random is consulted.
        result = red.red_agent_penalty(potency=10, node_id=1, network_graph=graph)

        self.assertFalse(result[1])
        self.assertEqual(nx.get_node_attributes(graph, "Alignment")[1], 0.2)

    def test_above_threshold_flips_an_accepting_node(self):
        red = make_red(penalty_threshold=70)
        graph = network_with(alignment=0.2, rejecting=False)
        # random() decides whether the penalty lands; pin it so the test is not a coin toss.
        with patch("class_api.team.random.random", return_value=0.1):
            result = red.red_agent_penalty(potency=90, node_id=1, network_graph=graph)

        self.assertTrue(result[1])
        # A node that rejects Red is pushed to maximum Blue alignment.
        self.assertEqual(nx.get_node_attributes(graph, "Alignment")[1], -1)

    def test_red_aligned_node_is_not_penalised(self):
        """Above the cutoff the node already leans Red, so there is nothing to lose."""
        red = make_red(penalty_threshold=70)
        graph = network_with(alignment=0.9, rejecting=False)
        with patch("class_api.team.random.random", return_value=0.1):
            result = red.red_agent_penalty(potency=90, node_id=1, network_graph=graph)

        self.assertFalse(result[1])
        self.assertEqual(nx.get_node_attributes(graph, "Alignment")[1], 0.9)

    def test_unlucky_roll_skips_the_penalty(self):
        red = make_red(penalty_threshold=70)
        graph = network_with()
        with patch("class_api.team.random.random", return_value=0.9):
            result = red.red_agent_penalty(potency=90, node_id=1, network_graph=graph)

        self.assertFalse(result[1])


if __name__ == "__main__":
    unittest.main()
