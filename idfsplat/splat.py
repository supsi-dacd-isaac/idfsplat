import pandas as pd
import argparse
import sys
import tempfile
import os
import pydoc

from pyenergyplus.api import EnergyPlusAPI


def expand(x):
    return {
        'what': x.what,
        'name': x.name,
        'type': x.type,
        'key': x.key,
    }


def format_dataframe_for_paging(df):
    """Format DataFrame for paged output with a nice header."""
    # Convert DataFrame to string with full display options
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    # Create a formatted output string
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("ENERGYPLUS API ENDPOINTS")
    output_lines.append("=" * 80)
    output_lines.append(f"Total endpoints found: {len(df)}")
    output_lines.append("")
    
    # Add the DataFrame as a string
    df_str = df.to_string(index=False)
    output_lines.append(df_str)
    output_lines.append("")
    output_lines.append("=" * 80)
    
    return "\n".join(output_lines)


def paged_output(content):
    """Display content using the system's pager."""
    try:
        # Use pydoc.pager which automatically detects the best pager
        pydoc.pager(content)
    except Exception:
        # Fallback: print directly if paging fails
        print(content)


def splat(state, api, temp_file_path):

    # get what's available in the API and put it into a DataFrame
    api_endpoints = api.exchange.get_api_data(state)
    api_endpoints_descriptions = [expand(x) for x in api_endpoints]
    descriptions_df = pd.DataFrame(api_endpoints_descriptions)
    
    # save the dataframe to the temporary file
    descriptions_df.to_pickle(temp_file_path)

    # kill the simulation; this will cause an OSError as soon as we return
    api.state_manager.delete_state(state)


def run_splat(idf_path, epw_path, output_path=None):

    # create a temporary file in RAM
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        # set up EnergyPlusAPI with our callback
        api = EnergyPlusAPI()
        state = api.state_manager.new_state()
        args = ["-r",
                "-w", epw_path,
                "-d", "output",
                idf_path
                ]
        tsh = lambda s: splat(s, api, temp_file_path)
        api.runtime.set_console_output_status(state, False)
        api.runtime.callback_begin_system_timestep_before_predictor(state, tsh)

        # launch EnergyPlus and catch the OSError that will be raised at the first step
        try:
            _return_code = api.runtime.run_energyplus(state, args)
        except OSError as _e:
            pass  # OSError is expected as we are killing the simulation in a dirty way for speed

        # load the dataframe from the temporary file
        descriptions_df = pd.read_pickle(temp_file_path)

        # output and return
        if output_path is not None:
            descriptions_df.to_excel(output_path, index=False)

        return descriptions_df
    
    finally:
        # clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Extract metadata of available EnergyPlus API endpoints from an IDF file and weather file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.idf weather.epw
  %(prog)s input.idf weather.epw -o output.xlsx
  %(prog)s --help
        """
    )
    
    parser.add_argument('idf_path', 
                       help='Path to the EnergyPlus IDF file')
    parser.add_argument('epw_path', 
                       help='Path to the EnergyPlus EPW weather file')
    parser.add_argument('-o', '--output', 
                       dest='output_path',
                       help='Output Excel file path (optional)')
    
    args = parser.parse_args()
    
    try:
        df = run_splat(args.idf_path, args.epw_path, args.output_path)
        print(f"Successfully extracted {len(df)} API endpoints")
        if args.output_path:
            print(f"Results saved to: {args.output_path}")
        else:
            # Use paged output for better CLI experience
            formatted_output = format_dataframe_for_paging(df)
            paged_output(formatted_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
