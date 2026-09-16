"""Tests for the simulation loop.

These exercise `Simulation.next_round`, not `Simulation.start`. The old test called
`Simulation(red_params, blue_params, node_attributes, node_connections)` and then
`start()`, and could not have passed: the constructor takes built team objects and a
green network, and `start()` is dead code that raises before doing anything useful --
`self._round_num` is only assigned in a commented-out line, and it calls
`generate_message(topic=...)` without the `previous` argument the method requires.

`next_round` is what the Flask `/next_round` endpoint drives, so that is what is
covered here. The LLM call is mocked: these tests must not reach the network, and the
termination rules are what is being checked, not message quality.
"""
import unittest
from unittest.mock import patch

from class_api.simulation import Simulation
from class_api.team import BlueTeam, RedTeam
from class_api.termination import Termination


class FakeGreenNetwork:
    """Stands in for GreenTeam.

    A real GreenTeam needs a populated networkx graph built from spreadsheets. The
    termination rules never consult the network -- they read the teams' own alignment
    and energy -- so a recorder is enough, and it keeps these tests about the loop
    rather than about network propagation.
    """

    def __init__(self, red=0.0, blue=0.0):
        self._red = red
        self._blue = blue
        self.broadcasts = 0
        self.updates = 0

    def broadcast_message(self, *args):
        self.broadcasts += 1

    def update_green_network(self):
        self.updates += 1

    def red_alignment(self):
        return self._red

    def blue_alignment(self):
        return self._blue


def make_red(alignment=10):
    return RedTeam(
        team="red", model_ID="test-model", potency=0, msg_count=0,
        influence_factor=1.5, temperature=0.5, penalty=20,
        penalty_threshold=70, alignment=alignment,
    )


def make_blue(alignment=10, energy=100):
    return BlueTeam(
        team="blue", model_ID="test-model", potency=0, msg_count=0,
        influence_factor=1.2, temperature=0.5, energy=energy,
        max_cost=20, alignment=alignment,
    )


def make_sim(red=None, blue=None, green=None):
    return Simulation(
        red_team=red or make_red(),
        blue_team=blue or make_blue(),
        green_team=green or FakeGreenNetwork(),
        topic="vaccines",
    )


class TestTermination(unittest.TestCase):
    """A round decides the game before any message is generated."""

    def test_blue_out_of_energy_hands_it_to_red(self):
        sim = make_sim(blue=make_blue(energy=0))
        victor, reason = sim.next_round(Termination(round=10, alignment=80))

        self.assertEqual(victor, "red")
        self.assertEqual(reason, "Blue team energy depletion")

    def test_red_majority_wins(self):
        sim = make_sim(red=make_red(alignment=80))
        victor, reason = sim.next_round(Termination(round=10, alignment=80))

        self.assertEqual(victor, "red")
        self.assertEqual(reason, "Majority support for red team")

    def test_blue_majority_wins(self):
        sim = make_sim(blue=make_blue(alignment=85))
        victor, reason = sim.next_round(Termination(round=10, alignment=80))

        self.assertEqual(victor, "blue")
        self.assertEqual(reason, "Majority support for blue team")

    def test_threshold_comes_from_the_termination_object(self):
        """60 wins under a threshold of 60 and does not under the default 80."""
        sim = make_sim(red=make_red(alignment=60))
        self.assertEqual(sim.next_round(Termination(round=10, alignment=60))[0], "red")

        undecided = make_sim(red=make_red(alignment=60))
        with patch("class_api.team.get_message", return_value=("m", 10)):
            self.assertIsNone(undecided.next_round(Termination(round=10, alignment=80))[0])

    def test_a_decided_game_stays_decided(self):
        """Calling again must not restart play or overwrite the recorded reason."""
        sim = make_sim(blue=make_blue(energy=0))
        first = sim.next_round(Termination(round=10, alignment=80))
        second = sim.next_round(Termination(round=10, alignment=80))

        self.assertEqual(first, second)


class TestRoundProgress(unittest.TestCase):
    def test_undecided_round_broadcasts_and_updates_alignments(self):
        green = FakeGreenNetwork(red=0.42, blue=0.31)
        sim = make_sim(green=green)

        with patch("class_api.team.get_message", return_value=("a message", 55)):
            victor, reason = sim.next_round(Termination(round=10, alignment=80))

        self.assertIsNone(victor)
        self.assertIsNone(reason)
        self.assertEqual(green.broadcasts, 1)
        self.assertEqual(green.updates, 1)
        # Alignments are read back off the network and rounded to 2dp.
        self.assertEqual(sim._red_team._alignment, 0.42)
        self.assertEqual(sim._blue_team._alignment, 0.31)

    def test_a_string_potency_is_not_broadcast(self):
        """get_message can return prose instead of a number; the guard exists for that."""
        green = FakeGreenNetwork()
        sim = make_sim(green=green)

        with patch("class_api.team.get_message", return_value=("a message", "not a number")):
            sim.next_round(Termination(round=10, alignment=80))

        self.assertEqual(green.broadcasts, 0)

    def test_switch_teams_alternates(self):
        sim = make_sim()
        self.assertEqual(sim._current_team, "red")
        sim.switch_teams()
        self.assertEqual(sim._current_team, "blue")
        sim.switch_teams()
        self.assertEqual(sim._current_team, "red")

    def test_blue_turn_spends_energy(self):
        green = FakeGreenNetwork()
        sim = make_sim(blue=make_blue(energy=100), green=green)
        sim.switch_teams()

        with patch("class_api.team.get_message", return_value=("a message", 50)):
            sim.next_round(Termination(round=10, alignment=80))

        self.assertLess(sim._blue_team._energy, 100)


class TestTurnData(unittest.TestCase):
    def test_turn_data_reports_the_current_team(self):
        sim = make_sim()
        with patch("class_api.team.get_message", return_value=("a message", 55)):
            sim.next_round(Termination(round=10, alignment=80))

        # GameTurnData exposes public attributes, unlike the underscore-prefixed
        # attributes the team classes use.
        turn = sim.get_turn_data(round_num=1)
        self.assertEqual(turn.turn, 1)
        self.assertEqual(turn.team, "red")
        self.assertEqual(turn.message_chosen, "a message")
        self.assertEqual(turn.potency, 55)


if __name__ == "__main__":
    unittest.main()
