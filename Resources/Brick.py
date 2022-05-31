from flask_restful import Resource
from extensions import firestoredb

class BrickResource(Resource):
    def post(selfs):
        # result = []
        # shortucts2 = firestoredb.collection('shortcuts').stream()
        # for doc in shortucts2:
        #     partResult = doc.to_dict()
        #     partResult["document_id"] = doc.id
        #     result.append(partResult)
        # id=result[0]
        # palette=firestoredb.collection(u'shortcuts').document(result[0]['document_id'])
        # palette.update({"name": "Namex"})

        x=firestoredb.collection('shortcuts').document('ss')
        #x.set({"name1":"name1"})
        x.update({"name":"name6"})

