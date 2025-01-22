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
from ..generated.step.transform_base import TransformBase
from krausening.logging import LogManager
from aissemble_core_filestore.file_store_factory import FileStoreFactory

import os


class Transform(TransformBase):
    """
    Performs the business logic for Transform.

    GENERATED STUB CODE - PLEASE ***DO*** MODIFY

    Originally generated from: templates/data-delivery-pyspark/synchronous.processor.impl.py.vm
    """

    logger = LogManager.get_instance().get_logger("Transform")
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
        return "Transform"

    def execute_step_impl(self) -> None:
        """
        Read the versioned data from Delta Lake and convert them to images
        """
        # Path to your Delta Lake table (assuming images are stored as binary data)
        delta_table_path = "s3a://spark-infrastructure/delta_images"

        # Read the Delta Lake table
        df = (
            self.spark.read.format("delta")
            .option("versionAsOf", 0)
            .load(delta_table_path)
        )

        # Specify the output directory to save the images
        output_dir = "/opt/spark/work-dir/output_images/"
        os.makedirs(output_dir, exist_ok=True)

        # Iterate through each row in the DataFrame
        for image_row in df.select("filename", "image_data").collect():
            filename = image_row["filename"]
            binary_image_data = image_row["image_data"]

            # --------------- Transform your image here -----------------------

            # Construct the full output path
            output_image_path = os.path.join(output_dir, filename)

            # Save the binary image data to the file
            with open(output_image_path, "wb") as f:
                f.write(binary_image_data)

            TransformBase.logger.info(f"Image saved as {output_image_path}")
