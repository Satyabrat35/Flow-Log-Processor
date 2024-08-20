from argparse import ArgumentParser
from src.FlowLogRecords import loadLookupTable, flowLogs, protocolAssign

FLOW_LOG_PATH = 'files/flow_log_large.txt'
PROTOCOL_ASSIGNMENT_PATH = 'files/protocol_assignment.csv'
LOOKUP_TABLE_PATH = 'files/lookup_large.csv'

CHUNK_SIZE = 1000

OUTPUT_PATH = 'output_large.csv'

def main():
    parser = ArgumentParser()

    parser.add_argument("-p", "--protocol-file-path", default=PROTOCOL_ASSIGNMENT_PATH,
                        help="Path to protocol assignment file.", metavar="protocol_path")

    parser.add_argument("-f", "--flow-logs-file-path", default=FLOW_LOG_PATH,
                        help="Path to flow logs file to read from.", metavar="flow_logs_path")

    parser.add_argument("-l", "--lookup-file-path", default=LOOKUP_TABLE_PATH,
                        help="Path to lookup file to aggregate logs.", metavar="lookup_path")

    parser.add_argument("-o", "--output-path", default=OUTPUT_PATH,
                        help="Path to output the processed results.", metavar="output_path")

    parser.add_argument("-c", "--chunk-size", default=CHUNK_SIZE, type=int,
                        help="Chunk size for processing large files.", metavar="chunk_size")

    args = parser.parse_args()

    try:
        print(f"[INFO] Loading protocol assignments from {args.protocol_file_path}...")
        protocol_table = protocolAssign(args.protocol_file_path)

        print(f"[INFO] Generating lookup table from {args.lookup_file_path}...")
        lookup_table = loadLookupTable(args.lookup_file_path)

        # Processing flow logs and generating results
        print(f"[INFO] Analyzing and processing flow logs from {args.flow_logs_file_path}...")
        tag_count, port_protocol_counts = flowLogs(args.flow_logs_file_path, lookup_table, args.output_path,
                                                   protocol_table, args.chunk_size)

        print(f"Final Results written to -> {args.output_path}")

    except Exception as e:
        print(f"Error occured - {e}")


if __name__ == "__main__":
    main()