from split_word import Split

if __name__ == "__main__":
    path1 = "./Result/Movie_info.json"
    path2 = "./Dataset/cn_stopwords.txt"
    path3 = "./Dataset/Movie_id.csv"
    path4 = "./Result/Movie_keyword.json"
    movie_test = Split(path3, path1, path2, path4)
    movie_test.get_id_list()
    movie_test.get_full_info()
    movie_test.get_stop_word_list()
    # some info is list
    for id_ in movie_test.full_info.keys():
        movie_test.split_info(movie_test.full_info[id_]['name'])
        for alias_ in movie_test.full_info[id_]['alias']:
            movie_test.split_info(alias_)
        movie_test.split_info(movie_test.full_info[id_]['intro'])
        movie_test.single_id_info.append(movie_test.full_info[id_]['name'])
        for director_ in movie_test.full_info[id_]['director']:
            movie_test.single_id_info.append(director_)
        for character_ in movie_test.full_info[id_]['characters']:
            movie_test.single_id_info.append(character_)
        for playwright_ in movie_test.full_info[id_]['playwright']:
            movie_test.single_id_info.append(playwright_)
        for type_ in movie_test.full_info[id_]['type']:
            movie_test.single_id_info.append(type_)
        for alias_ in movie_test.full_info[id_]['alias']:
            movie_test.single_id_info.append(alias_)
        for tag_ in movie_test.full_info[id_]['tag']:
            movie_test.single_id_info.append(tag_)
        print(movie_test.single_id_info)
        movie_test.combine_single_info(id_)
    movie_test.save_keyword_to_json()