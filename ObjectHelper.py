class DefaultObject:
    def __str__(self):
        return vars(self).__str__()


