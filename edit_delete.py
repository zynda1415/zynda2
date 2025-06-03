import data

def edit_item(index, updated_item):
    df = data.load_data()
    df.loc[index] = updated_item
    data.save_data(df)

def delete_item(index):
    df = data.load_data()
    df = df.drop(index).reset_index(drop=True)
    data.save_data(df)
