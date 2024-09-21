import json

movie_info_path = "../../Stage1_1/Result/Movie_info.json"
with open(movie_info_path, 'r', encoding="utf-8") as f_movie_info:
    movie_info = json.load(f_movie_info)

for _id in movie_info:
    movie_info[_id]["Other version name"] = ""
    index = movie_info[_id]["name"].find(' ')
    if index != -1:
        name = movie_info[_id]["name"][: index]
        other_version_name = movie_info[_id]["name"][index + 1:]
        movie_info[_id]["name"] = name
        movie_info[_id]["Other version name"] = other_version_name

with open(movie_info_path, 'w', encoding="utf-8") as f_movie_info:
    json.dump(movie_info, f_movie_info, indent=4, ensure_ascii=False)
