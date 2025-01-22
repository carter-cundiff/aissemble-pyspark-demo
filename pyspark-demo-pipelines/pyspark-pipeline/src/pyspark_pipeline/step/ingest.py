###
# #%L
# PysparkDemo::Pipelines::Pyspark Pipeline
# %%
# Copyright (C) 2021 Booz Allen
# %%
# All Rights Reserved. You may not copy, reproduce, distribute, publish, display,
# execute, modify, create derivative works of, transmit, sell or offer for resale,
# or in any way exploit any part of this solution without Booz Allen Hamilton's
# express written permission.
# #L%
###
from ..generated.step.ingest_base import IngestBase
from krausening.logging import LogManager
from aissemble_core_filestore.file_store_factory import FileStoreFactory
from pyspark.sql.dataframe import DataFrame

import os


class Ingest(IngestBase):
    """
    Performs the business logic for Ingest.

    GENERATED STUB CODE - PLEASE ***DO*** MODIFY

    Originally generated from: templates/data-delivery-pyspark/synchronous.processor.impl.py.vm
    """

    logger = LogManager.get_instance().get_logger("Ingest")
    file_stores = {}

    def __init__(self):
        """
        TODO: Configure file store(s)
        In order for the factory to set up your file store, you will need to set a couple of environment
        variables through whichever deployment tool(s) you are using, and in the environment.py file for your tests.
        For more information: https://boozallen.github.io/aissemble/current/file-storage-details.html
        """
        super().__init__("synchronous", self.get_data_action_descriptive_label())

    def get_data_action_descriptive_label(self) -> str:
        """
        Provides a descriptive label for the action that can be used for logging (e.g., provenance details).
        """
        # TODO: replace with descriptive label
        return "Ingest"

    def execute_step_impl(self) -> None:
        """
        Convert the images to a Spark Dataframe and save them to Delta Lake
        """
        # Path to the directory containing .jpg files
        directory_path = "/opt/spark/work-dir/images/"

        # List to store data as tuples (id, binary_data)
        data = []

        # Iterate through all files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".jpg"):
                file_path = os.path.join(directory_path, filename)

                # Read the .jpg file as binary data
                with open(file_path, "rb") as file:
                    binary_data = file.read()

                # Add the binary data and filename (or any other info) to the data list
                data.append((filename, binary_data))

        # Create a DataFrame from the collected data
        image_df = self.spark.createDataFrame(data, ["filename", "image_data"])

        # Save to delta lake table
        self.save_dataset(image_df)

    def save_dataset(self, dataset: DataFrame) -> None:
        """
        Saves a dataset.
        """
        output_table = "delta_images"
        output_uri = f"s3a://spark-infrastructure/{output_table}/"

        IngestBase.logger.info(f"Saving {self.descriptive_label} To Delta Lake...")

        dataset.write.format("delta").mode("overwrite").save(output_uri)

        # Get the latest version just saved
        latest_version = str(
            self.spark.sql(f"DESCRIBE HISTORY '{output_uri}'").collect()[0]["version"]
        )

        IngestBase.logger.info(
            f"Saved version {latest_version} of {self.descriptive_label} to Delta Lake"
        )
