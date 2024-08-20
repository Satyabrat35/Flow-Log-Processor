import csv
from collections import defaultdict
import os

def protocolAssign(path):
    """
        Reads a CSV file containing protocol assignments and returns a dictionary mapping protocol numbers to protocol names

        Args:
            path (str): Path to the CSV file containing protocol assignments

        Returns:
            dict: A dictionary where keys are protocol numbers (as strings) and values are protocol names (in lowercase)

        Raises:
            FileNotFoundError: If the specified file is not found
            RuntimeError: For any other errors that occur while reading the file
        """
    protocols = {}
    try:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)

            # Read each record and populate the values
            for row in reader:
                if not row:
                    continue
                protocols[row[0]] = row[1].lower()

            return protocols
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {path} was not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the protocol file: {e}")

def loadLookupTable(path):
    """
    Loads a CSV file containing lookup table data and returns a dictionary mapping (destination port, protocol) tuples to tags

    Args:
        path (str): Path to the CSV file containing the lookup table

    Returns:
        dict: A dictionary where keys are tuples (destination port, protocol) and values are tags

    Raises:
        FileNotFoundError: If the specified file is not found
        RuntimeError: For any other errors that occur while reading the file
    """

    lookup_records = {}
    try:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            # Skip first line - header
            next(reader)

            # Process each row in the CSV file
            for row in reader:
                if not row:
                    continue

                if len(row) != 3:
                    print(f"Lookup table does not have 3 elements: {row}")
                    print("Moving to next record ...")
                    continue

                dstport, protocol, tag = row[0].strip(), row[1].strip().lower(), row[2].strip()
                try:
                    dstport = int(dstport)
                except ValueError:
                    print(f"Invalid destination port value: {dstport}. Skipping record...")
                    continue

                key = (dstport, protocol)
                lookup_records[key] = tag

        return lookup_records

    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {path} was not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the lookup table: {e}")


def flowLogs(path, lookup_table, output_path, protocol_table, chunk_size=10000):
    """
    Processes a flow log file, aggregates tag counts and port/protocol combination counts, and writes the results to a CSV file

    Args:
        path (str): Path to the flow log file
        lookup_table (dict): A dictionary mapping (destination port, protocol) tuples to tags
        output_path (str): Path to the CSV file where the output will be written
        protocol_table (dict): A dictionary mapping protocol numbers to protocol names
        chunk_size (int): The number of lines to read at a time from the flow log file

        Returns:
            tuple: Two dictionaries:
                - tag_count: A dictionary where keys are tags and values are counts
                - port_protocol_counts: A dictionary where keys are (port, protocol) tuples and values are counts

        Raises:
            FileNotFoundError: If the specified file is not found
            RuntimeError: For any other errors that occur while processing the file
        """
    tag_count = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    try:
        with open(path, 'r') as lines:
            # Read file in chunks due to large size
            # Adjust based on available memory
            chunk_size = chunk_size

            while True:
                chunk = lines.readlines(chunk_size)
                if not chunk:
                    break
                for line in chunk:
                    fields = line.split()

                    # Check for field values
                    if len(fields) < 14:
                        print(f"Not enough fields in flow log file: {line}")
                        print("Moving to next record ...")

                    # Version 2 check
                    if fields[0] != '2':
                        continue

                    dstport = int(fields[6])
                    protocol = protocol_table[fields[7]]

                    key = (dstport, protocol)
                    tag = lookup_table.get(key, "Untagged")

                    tag_count[tag] += 1
                    port_protocol_counts[key] += 1

        # Write to the output file
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write header for the tag counts section
            writer.writerow(["Tag Counts:"])
            writer.writerow(["Tag", "Count"])

            # Write tag count data
            for tag, count in tag_count.items():
                writer.writerow([tag, count])

            writer.writerow([])

            # Write header for the port/protocol combination section
            writer.writerow(["Port/Protocol Combination Counts:"])
            writer.writerow(["Port", "Protocol", "Count"])

            # Write port/protocol combination data
            for (port, protocol), count in port_protocol_counts.items():
                writer.writerow([port, protocol, count])

        return tag_count, port_protocol_counts

    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {path} was not found.")
    except Exception as e:
        raise RuntimeError(f"Error while processing flow log file '{path}': {e}")







