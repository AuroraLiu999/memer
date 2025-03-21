from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['MemeGenSample']
from gridfs import GridFS

fs = GridFS(db)

# 读取图片文件
for i in range(1, 44):
    with open(f'meme{i}.jpg', 'rb') as f:
        image_data = f.read()

# 将图片存入GridFS
    file_id = fs.put(image_data, filename=f'meme{i}.jpg')

print(f"Image stored with file_id: {file_id}")

# 通过file_id读取
output_image = fs.get(file_id).read()

# 保存到本地
with open('output_image.jpg', 'wb') as f:
    f.write(output_image)

    