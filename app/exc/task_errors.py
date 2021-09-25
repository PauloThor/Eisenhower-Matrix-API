class InvalidOptions(Exception):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def msg(importance, urgency):
        return {  "error": {
                "valid_options": {
                    "importance": [
                        1, 2
                    ],
                    "urgency": [
                        1, 2
                    ]
                },
                "received_options": {
                    "importance": importance,
                    "urgency": urgency
                }
            }
        }, 404