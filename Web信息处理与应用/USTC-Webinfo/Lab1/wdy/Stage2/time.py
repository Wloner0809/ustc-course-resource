class BookRatingDataset(Dataset):
    def __init__(self, data, user_to_idx, book_to_idx, tag_embedding_dict):
        self.data = data
        self.user_to_idx = user_to_idx
        self.book_to_idx = book_to_idx
        self.tag_embedding_dict = tag_embedding_dict
        self.data['Time'] = self.data['Time'].astype(str)
        self.data['Time'] = self.data['Time'].apply(lambda x: x.split('+')[0].replace('-','').replace('T', '').replace(':', '') if isinstance(x, str) else x)
        self.data['Time'] = self.data['Time'].astype('int64')
        self.time_max = self.data['Time'].max()
        self.time_min = self.data['Time'].min()
        self.data['Time'] = self.data['Time'].apply(lambda x:((x - self.time_min) / (self.time_max - self.time_min) + 1) / 2)
        self.data['Time'] = self.data['Time'].astype('float32')
        
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data.iloc[index]
        user = self.user_to_idx[row['User']]
        book = self.book_to_idx[row['Book']]
        rating = row['Rate'].astype('float32')
        time = row['Time']
        rating = rating * time
        text_embedding = self.tag_embedding_dict.get(row['Book'])
        return user, book, rating, text_embedding