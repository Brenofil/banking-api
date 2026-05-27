import re
import json
import os
from typing import Dict, List, Union
from typing_extensions import Any
import pandas as pd
from app.utils.logger import get_logger


class MarkdownUtils:

    logger = get_logger("Markdown Utils")

    def _parse_markdown_tables(self, markdown_text: str) -> List[Dict[str, Any]]:
        """
        Parse markdown tables from text and convert to structured format.

        Args:
            markdown_text: Markdown text containing tables

        Returns:
            List[Dict[str, Any]]: List of parsed tables with data, rows, and columns
        """
        tables = []

        # Regex pattern to match markdown tables
        # Matches: header row | separator row | data rows
        table_pattern = r"\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n)+"

        matches = re.finditer(table_pattern, markdown_text)

        for match in matches:
            try:
                table_text = match.group(0)
                lines = [
                    line.strip() for line in table_text.split("\n") if line.strip()
                ]

                if len(lines) < 3:  # Need at least header, separator, and one data row
                    continue

                # Parse header
                header_line = lines[0]
                headers = [cell.strip() for cell in header_line.split("|")[1:-1]]

                # Skip separator line (lines[1])

                # Parse data rows
                data_rows = []
                for line in lines[2:]:
                    cells = [cell.strip() for cell in line.split("|")[1:-1]]
                    if len(cells) == len(headers):
                        data_rows.append(cells)

                if not data_rows:
                    continue

                # Convert to dictionary format (similar to pandas to_dict())
                table_data = {}
                for col_idx, header in enumerate(headers):
                    table_data[header] = {
                        str(row_idx): row[col_idx] if col_idx < len(row) else ""
                        for row_idx, row in enumerate(data_rows)
                    }

                tables.append(
                    {
                        "data": table_data,
                        "rows": len(data_rows),
                        "columns": len(headers),
                    }
                )

            except Exception as e:
                self.logger.warning(f"Failed to parse markdown table: {str(e)}")
                continue

        return tables

    def read_pdf_response_to_dataframes(
        self, response_data: Dict[str, Any]
    ) -> Union[pd.DataFrame, List[pd.DataFrame]]:
        """
        Convert tables from PDF response data to pandas DataFrames.

        This method is designed to work with ProcessorResponse.data from the PDF processor.
        It extracts all tables and converts them to pandas DataFrames for easy data manipulation.

        If all tables have the same columns, returns a single DataFrame.
        If tables have different columns, returns a list of DataFrames.

        Args:
            response_data: Dictionary containing the PDF response data with tables.
                          Expected format: {'tables': [{'data': {...}, 'rows': int, 'columns': int}, ...]}

        Returns:
            Union[pd.DataFrame, List[pd.DataFrame]]:
                - Single DataFrame if all tables have identical columns (concatenated)
                - List of DataFrames if tables have different columns

        Raises:
            ValueError: If the data format is invalid or no tables found

        Example:
            >>> utils = MarkdownUtils()
            >>> # From ProcessorResponse
            >>> dataframes = utils.read_pdf_response_to_dataframes(response.data)
            >>> if isinstance(dataframes, list):
            >>>     print(f"Found {len(dataframes)} tables with different columns")
            >>> else:
            >>>     print(f"Single DataFrame with shape {dataframes.shape}")
        """
        try:
            # Extract tables from the response data
            if "tables" not in response_data:
                raise ValueError("Invalid response data: missing 'tables' field")

            tables = response_data["tables"]

            if not tables:
                raise ValueError("No tables found in the PDF response")

            # Convert each table to a DataFrame
            dataframes = []
            for table in tables:
                if "data" not in table:
                    self.logger.warning(
                        f"Skipping table at index {table.get('index', 'unknown')}: missing 'data' field"
                    )
                    continue

                # Convert the table data to DataFrame
                df = pd.DataFrame(table["data"])
                dataframes.append(df)

            if not dataframes:
                raise ValueError("No valid tables could be converted to DataFrames")

            # Check if all DataFrames have the same columns
            if len(dataframes) == 1:
                self.logger.info("Converted 1 table to DataFrame")
                return dataframes[0]

            # Compare column sets
            first_columns = set(dataframes[0].columns)
            all_same_columns = all(
                set(df.columns) == first_columns for df in dataframes[1:]
            )

            if all_same_columns:
                # Concatenate all DataFrames into one
                combined_df = pd.concat(dataframes, ignore_index=True)
                self.logger.info(
                    f"Converted {len(dataframes)} tables with identical columns to single DataFrame"
                )
                return combined_df
            else:
                # Return list of DataFrames
                self.logger.info(
                    f"Converted {len(dataframes)} tables with different columns to list of DataFrames"
                )
                return dataframes

        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Error converting PDF response to DataFrames: {str(e)}")
            raise
