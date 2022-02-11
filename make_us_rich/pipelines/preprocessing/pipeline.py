from kedro.pipeline import Pipeline, node

from .nodes import (
    create_sequences,
    extract_features_from_dataset, 
    scale_data,
    split_data,
    split_train_and_val_sequences,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=extract_features_from_dataset,
                inputs="fetched_market_chart",
                outputs="extracted_features",
                name="features_extraction_node",
            ),
            node(
                func=split_data,
                inputs="extracted_features",
                outputs=["splitted_train_data", "splitted_test_data"],
                name="splitting_data_node",
            ),
            node(
                func=scale_data,
                inputs=["splitted_train_data", "splitted_test_data", "params:dir_path"],
                outputs=["scaled_train_data", "scaled_test_data"],
                name="scaling_data_node",
            ),
            node(
                func=create_sequences,
                inputs=["scaled_train_data", "params:target_column","params:sequence_length"],
                outputs="sequences_train_data",
                name="create_sequences_for_train_node",
            ),
            node(
                func=split_train_and_val_sequences,
                inputs=["sequences_train_data", "params:val_size"],
                outputs=["train_sequences", "val_sequences"],
                name="split_train_and_val_sequences_node",
            ),
            node(
                func=create_sequences,
                inputs=["scaled_test_data", "params:target_column","params:sequence_length"],
                outputs="test_sequences",
                name="create_sequences_for_test_node",
            ),
        ]
    )
