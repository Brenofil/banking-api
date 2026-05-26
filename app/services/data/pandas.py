from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.constants.date import DateConstants
from app.constants.files import FileConstants
from app.services.base_service import BaseService
import pandas as pd


class PandasService(BaseService):
    """
    Service responsible for handling data transformations with the pandas library

    Args:
        BaseService (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__()

    def df_from_dict(
        self, attribute: str, data: Dict[str, Any] = {}
    ) -> List[pd.DataFrame]:
        """
        Method responsible for extracting any available dataframe from a fiven dictionary structure

        Args:
            attribute (str): the location of the property which contains the dataframe
            data (Dict[str, Any], optional): The dictionary that holds the raw data. Defaults to {}.

        Raises:
            e: _description_

        Returns:
            List[pd.DataFrame]: _description_
        """

        self.logger.info("trying to create DataFrame from given data")

        df_data = data[attribute]

        try:
            dataframes: list[pd.DataFrame] = [
                pd.DataFrame(data["data"])
                for data in (df_data if isinstance(df_data, list) else [df_data])
            ]

            self.logger.debug("Successfully eztracted DataFrame from dict")

            return dataframes
        except Exception as e:
            self.logger.error(f"Unable to create DataFrame due to {str(e)}")
            raise e

    def write_df_as_excel(
        self,
        data: list[pd.DataFrame] = [],
        sheets: list[str] = [],
        filename: Optional[str] = None,
    ) -> None:
        """
        Method responsible for extracting the the content from a dataframe and
        writing as an excel file

        Args:
            df (pd.DataFrame): the dataframe used as data
        """

        total_dataframes: int = len(data)

        if total_dataframes == 0:
            self.logger.warning("No dataframe available to write as xlsx.")
            return

        if total_dataframes != len(sheets):
            self.logger.warning(
                "Dataframes total differs from sheets, some sheets will be named automatically."
            )

        # Generate filename with timestamp
        timestamp: str = datetime.now().strftime(format=DateConstants.TIME_STAMP)

        name: str = "" if filename is None else filename

        base_filename: str = name.rsplit(".", 1)[0]

        excel_filename: str = f"{timestamp}_{base_filename}_tables.xlsx"

        self.logger.info(f"Writting excel file as {str(excel_filename)}")

        excel_path: Path = Path(FileConstants.OUTPUT_EXCEL_DIR) / excel_filename

        for i, df in enumerate(data):
            # get sheet name or force default
            sheet_name: str = f"Sheet {i}"

            try:
                # instantiate xlsx writer
                self.xlsx_writer = pd.ExcelWriter(
                    path=excel_path, date_format=DateConstants.XLSX_FORMAT, mode="w"
                )

                with self.xlsx_writer as excel_writer:
                    df.to_excel(excel_writer, sheet_name=sheet_name)
            except ValueError as error:
                self.logger.error(f"Could not write excel file due to {str(error)}")
                raise error
