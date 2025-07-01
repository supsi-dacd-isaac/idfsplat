# idfsplat

A command-line tool and Python library to extract available EnergyPlus API data for an IDF file.



> [!IMPORTANT]  
> This project depends on the `pyenergyplus` package, which is **only available through an installation of EnergyPlus**. To use this project, you must first install EnergyPlus. You will also need to make your interpreter aware of the included EnergyPlus Python package.

## Installation

After cloning the repository, you can install the package using pip. The package might be uploaded to PyPI in the future, but for now, you can install it directly from the source.
```bash
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Basic usage; the data will be printed to the console (paged)
idfsplat input.idf weather.epw

# Save output to Excel file instead
idfsplat input.idf weather.epw -o output.xlsx

# Get help
idfsplat --help
```

### Python API

```python
from idfsplat.splat import run_splat

# Run the tool programmatically
df = run_splat("input.idf", "weather.epw", output_path="output.xlsx")
print(df)
```

## Requirements

- Python 3.7+
- pandas
- pyenergyplus (comes with EnergyPlus)
- openpyxl (for Excel output)

## What it does

The `idfsplat` tool:

1. Takes an EnergyPlus IDF file and EPW weather file as input
2. Initializes EnergyPlus with these files
3. Lists all the data points available through the EnergyPlus API
4. Optionally saves the results to an Excel file instead of printing to the console

The tool is designed to help developers extract the data available through the EnergyPlus API for a given IDF.

## Output

The tool outputs a DataFrame with the following columns:
- `what`: Description of the API endpoint
- `name`: Name of the endpoint
- `type`: Data type
- `key`: Unique identifier

The Excel output will have the same structure.

## License

MIT License 