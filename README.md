# Bank Statement Parser

Bank Statement Parser is a Python-based tool designed to extract and analyze transaction data from bank statements. It supports various bank statement formats and provides a structured output for financial analysis and record-keeping.

## Features

- **Multi-bank Support**: Parses statements from multiple banks with different formats.
- **Data Extraction**: Extracts transaction details such as date, description, amount, and balance.
- **Output Formats**: Exports parsed data to CSV or JSON for easy integration with other tools.
- **Error Handling**: Identifies and reports inconsistencies or errors in statement formats.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/R3XCran1um/Bank-Statement-Parser.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd Bank-Statement-Parser
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Your Bank Statement**: Ensure your bank statement is in a supported format (e.g., PDF, CSV).

2. **Run the Parser**:

   ```bash
   python parser.py /path/to/your/bank_statement.pdf
   ```

3. **View the Output**: The parsed data will be saved in the `output` directory in your chosen format (CSV or JSON).

## Configuration

You can customize the parser's behavior using the `config.yaml` file. This includes setting the output format, specifying bank-specific parsing rules, and more.
