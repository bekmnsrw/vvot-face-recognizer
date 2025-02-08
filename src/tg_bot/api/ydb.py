def get_unrecognized_face_id(session):
    query = "SELECT face_id FROM photos WHERE face_name IS NULL AND is_processing = TRUE LIMIT 1"
    unrecognized_face = session.transaction().execute(query)[0].rows

    if unrecognized_face:
        unrecognized_face_id = unrecognized_face[0]["face_id"].decode("utf-8")
        return unrecognized_face_id
    else:
        query = "SELECT face_id FROM photos WHERE face_name IS NULL LIMIT 1"
        unrecognized_face = session.transaction().execute(query)[0].rows
        unrecognized_face_id = unrecognized_face[0]["face_id"].decode("utf-8")
        return unrecognized_face_id

def get_processing_face_id(session):
    query = "SELECT face_id FROM photos WHERE face_name IS NULL AND is_processing = TRUE LIMIT 1"
    processing_face = session.transaction().execute(query)[0].rows

    if processing_face:
        processing_face_id = processing_face[0]["face_id"].decode("utf-8")
        return processing_face_id
    else:
        raise Exception

def set_is_processing(session, face_id, is_processing):
    query = f"UPDATE photos SET is_processing = '{is_processing}' WHERE face_id = '{face_id}'"
    session.transaction().execute(query, commit_tx=True)

def get_all_original_photos_with(session, name):
    query = f"SELECT photo_id FROM photos WHERE face_name = '{name}'"
    all_photos_with = session.transaction().execute(query)[0].rows
    return [row["photo_id"].decode("utf-8") for row in all_photos_with] if all_photos_with else []

def save_name(session, name, face_id):
    query = f"UPDATE photos SET face_name = '{name}' WHERE face_id = '{face_id}'"
    session.transaction().execute(query, commit_tx=True)
