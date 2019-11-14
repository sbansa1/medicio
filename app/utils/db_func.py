from app.extensions import db


class ResourceMixin(object):


    def save(self):

        """save the Model instance in the db"""
        """return model instance"""

        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """Deletes a model instance"""

        db.session.delete(self)
        return db.session.commit()
