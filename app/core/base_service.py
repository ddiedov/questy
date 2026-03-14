class BaseService:

    def __init__(self, repository, model, create_model, update_model):

        self.repo = repository
        self.model = model
        self.create_model = create_model
        self.update_model = update_model


    def list(self):

        rows = self.repo.list()

        return [self.model(**row) for row in rows]


    def get(self, id: int):

        row = self.repo.get(id)

        if not row:
            return None

        return self.model(**row)


    def create(self, data):

        row = self.repo.create(data.model_dump())

        if not row:
            return None

        return self.model(**row[0])


    def update(self, id: int, data):

        row = self.repo.update(id, data.model_dump())

        if not row:
            return None

        return self.model(**row[0])