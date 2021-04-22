import face_recognition
from PIL import Image, ImageDraw


def face_rec():
    gal_face_img = face_recognition.load_image_file("img/ivan.jpg")
    gal_face_location = face_recognition.face_locations(gal_face_img)

    justice_league_img = face_recognition.load_image_file("img/ivan3.jpg")
    justice_league_faces_locations = face_recognition.face_locations(justice_league_img)

    # print(gal_face_location)
    # print(justice_league_faces_locations)
    # print(f"Found {len(gal_face_location)} face(s) in this image")
    # print(f"Found {len(justice_league_faces_locations)} face(s) in this image")

    pil_img1 = Image.fromarray(gal_face_img)
    draw1 = ImageDraw.Draw(pil_img1)

    for(top, right, bottom, left) in gal_face_location:
        draw1.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=4)

    del draw1
    pil_img1.save("img/new_ivan.jpg")

    pil_img2 = Image.fromarray(justice_league_img)
    draw2 = ImageDraw.Draw(pil_img2)

    for(top, right, bottom, left) in justice_league_faces_locations:
        draw2.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=4)

    del draw2
    pil_img2.save("img/new_ivan3.jpg")


def extracting_faces(img_path): # вырезать лица
    count = 0
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"img/{count}_face_img.jpg")
        count += 1

    return f"Found {count} face(s) in this photo"


def compare_faces(img1_path, img2_path):
    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]
    # print(img1_encodings)

    img2 = face_recognition.load_image_file(img2_path)
    img2_encodings = face_recognition.face_encodings(img2)

    for face_location in img2_encodings:
        result = face_recognition.compare_faces([img1_encodings], face_location)
        if result[0]:
            print("Доступ открыт")
            return True


def main():
    # face_rec()
    # print(extracting_faces("img/ivan3.jpg"))
    # compare_faces("img/gal1.jpg", "img/gal2.jpg")
    ivan = compare_faces("img/ivan.jpg", "photo/access.png")
    vlad = compare_faces("img/vlad.jpg", "photo/access.png")

    if ivan == True:
        b = "Здравствуй Иван создатель"
        return ivan, b

        return True
    elif vlad == True:
        b = "Привет Влад"
        return vlad, b
    else:
        b = "Я вас не знаю. Доступ запрещен"
        return False, b

if __name__ == '__main__':
    main()