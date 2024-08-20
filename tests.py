import unittest
import csv
import os
from collections import defaultdict
from src.FlowLogRecords import protocolAssign, loadLookupTable, flowLogs

class TestFlowLogProcessor(unittest.TestCase):

    def setUp(self):
        """Mock files for testing"""
        self.protocol_csv = "test_protocols.csv"
        self.lookup_csv = "test_lookup.csv"
        self.flow_log_txt = "test_flow_log.txt"

        with open(self.protocol_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Decimal", "Keyword", "Protocol", "IPv6 Extension Header", "Reference"])
            writer.writerow(["6", "TCP", "Transmission Control Protocol", "", "[RFC793]"])
            writer.writerow(["17", "UDP", "User Datagram Protocol", "", "[RFC768]"])

        with open(self.lookup_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Port", "Protocol", "Tag"])
            writer.writerow(["49158", "tcp", "sv_P1"])
            writer.writerow(["80", "tcp", "sv_P2"])
            writer.writerow(["68", "udp", "sv_P3"])

        with open(self.flow_log_txt, 'w') as f:
            f.write("2 123456789012 eni-6m7n8o9p 10.0.2.200 198.51.100.4 143 49158 6 18 14000 1620140761 1620140821 ACCEPT OK\n")
            f.write("2 123456789012 eni-1a2b3c4d 192.168.0.1 203.0.113.12 1024 80 6 10 5000 1620140661 1620140721 ACCEPT OK\n")
            f.write("2 123456789012 eni-6e7f8g9h 10.0.2.101 192.0.2.206 25 49180 6 14 12500 1620140761 1620140821 REJECT OK\n")

    def tearDown(self):
        """Remove mock files after tests"""
        os.remove(self.protocol_csv)
        os.remove(self.lookup_csv)
        os.remove(self.flow_log_txt)

    def test_protocolAssign(self):
        """Test protocolAssign function"""
        expected_protocols = {
            "6": "tcp",
            "17": "udp"
        }
        protocols = protocolAssign(self.protocol_csv)
        self.assertEqual(protocols, expected_protocols)

    def test_loadLookupTable(self):
        """Test loadLookupTable function"""
        expected_lookup = {
            (49158, "tcp"): "sv_P1",
            (80, "tcp"): "sv_P2",
            (68, "udp"): "sv_P3"
        }
        lookup_table = loadLookupTable(self.lookup_csv)
        self.assertEqual(lookup_table, expected_lookup)

    def test_flowLogs(self):
        """Test flowLogs function."""
        protocol_table = protocolAssign(self.protocol_csv)
        lookup_table = loadLookupTable(self.lookup_csv)
        output_path = "test_output.csv"

        tag_count, port_protocol_counts = flowLogs(self.flow_log_txt, lookup_table, output_path, protocol_table)

        expected_tag_count = defaultdict(int, {
            "sv_P1": 1,
            "sv_P2": 1,
            "Untagged": 1
        })

        expected_port_protocol_counts = defaultdict(int, {
            (49180, "tcp"): 1,
            (80, "tcp"): 1,
            (49158, "tcp"): 1
        })

        self.assertEqual(tag_count, expected_tag_count)
        self.assertEqual(port_protocol_counts, expected_port_protocol_counts)

        # Remove the files
        os.remove(output_path)

if __name__ == "__main__":
    unittest.main()
