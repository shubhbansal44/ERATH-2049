# from os.path import join
# import json
# import os
# import pygame as pg

# def load_settings():
#     try:
#         saved_file_path = join('Code', 'saved_settings.txt')
#         if os.path.getsize(saved_file_path) > 0:
#             with open(saved_file_path, 'r') as settings:
#                 data = json.load(settings)
#         else:
#             raise json.JSONDecodeError("Empty file", saved_file_path, 0)
#     except (json.JSONDecodeError, FileNotFoundError):
#         default_file_path = join('Code', 'default_settings.txt')
#         with open(default_file_path, 'r') as settings:
#             data = json.load(settings)

#     return data

# data = load_settings()
# print(data)
# os.environ['SDL_VIDEO_CENTERED'] = '1'
# print(pg.display.Info())

res = [[(1536, 864), '#475F77'], [(1280, 800), '#475F77'], [(640, 480), '#475F77']]

# print(str(res[2][1]))

# for i, j in enumerate(res):
#     print(i, j)