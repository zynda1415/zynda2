import data
import pandas as pd


def edit_item(index: int, updated_item: dict) -> None:
    """Update an existing item in the inventory at the specified index."""
    df = data.load_data()
    if index not in df.index:
        raise IndexError("Item index out of range")
    for key, value in updated_item.items():
        if key in df.columns:
            df.at[index, key] = value
    data.save_data(df)


def delete_item(index: int) -> None:
    """Delete an item from the inventory at the specified index."""
    df = data.load_data()
    if index not in df.index:
        raise IndexError("Item index out of range")
    df = df.drop(index).reset_index(drop=True)
    data.save_data(df)
