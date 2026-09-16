"""Tests for building the Green node network.

The old version of this file looked for NodeAttributes.xlsx and NodeConnections.xlsx
beside itself and expected a network_output.json in the same directory. Neither is
true of this module: the spreadsheets ship in clash-of-llms/public/documents/, and
`create_node_network` writes round_0.json under a round_data/ directory resolved from
the current working directory. It was written against the near-duplicate copy in
excel_api/create_node_network/, which does write network_output.json.

Because the output path is built from os.getcwd(), these tests chdir into a tmp
directory rather than writing into the repository.
"""
import json
import os

import pytest

from create_node_network.create_network import create_node_network
from excel_api.import_excel import import_node_attributes, import_node_connections

DOCUMENTS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "public", "documents"
)


@pytest.fixture(name="network_input")
def fixture_network_input():
    """The spreadsheets the application ships as its defaults."""
    attributes = import_node_attributes(os.path.join(DOCUMENTS, "NodeAttributes.xlsx"))
    connections = import_node_connections(os.path.join(DOCUMENTS, "NodeConnections.xlsx"))
    return attributes, connections


@pytest.fixture(name="round_zero")
def fixture_round_zero(tmp_path, monkeypatch, network_input):
    """Build the network with cwd pointed at a tmp directory, and return the JSON."""
    monkeypatch.chdir(tmp_path)
    attributes, connections = network_input
    graph = create_node_network(attributes, connections)

    path = tmp_path / "flask_app" / "create_node_network" / "round_data" / "round_0.json"
    return graph, path


def test_writes_round_zero(round_zero):
    _, path = round_zero
    assert path.exists(), "round_0.json was not created"


def test_json_uses_the_links_key(round_zero):
    """The frontend reads networkData.links (src/services/graphDataService.js).

    networkx 3.6 changed node_link_data's default key from "links" to "edges" without a
    deprecation warning, which would empty the graph in the browser with no error on
    either side. The call sites pass edges="links" explicitly; this is the regression
    test for that.
    """
    _, path = round_zero
    data = json.loads(path.read_text(encoding="utf-8"))

    assert "links" in data, f'expected a "links" key, got {sorted(data)}'
    assert "edges" not in data


def test_every_node_is_written(round_zero, network_input):
    graph, path = round_zero
    attributes, _ = network_input
    data = json.loads(path.read_text(encoding="utf-8"))

    assert len(data["nodes"]) == len(attributes)
    assert graph.number_of_nodes() == len(attributes)


def test_nodes_carry_the_attributes_the_simulation_reads(round_zero):
    """Alignment drives propagation and rejectMessaging gates the Red penalty.

    Both are read by name elsewhere, so a node missing either fails at a distance.
    """
    graph, _ = round_zero

    for node_id, attrs in graph.nodes(data=True):
        assert "Alignment" in attrs, f"node {node_id} has no Alignment"
        assert "rejectMessaging" in attrs, f"node {node_id} has no rejectMessaging"
        assert attrs["rejectMessaging"] is False


def test_graph_is_directed(round_zero):
    """Influence runs one way along an edge; an undirected graph would double it."""
    graph, _ = round_zero
    assert graph.is_directed()
