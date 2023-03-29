from exceptions.exceptions import ValidationException


class MovieValidator:
    """
    clasa pentru incapsularea algoritmului de validare
    """
    def validate(self, movie):
        errors = []
        try:
            n = int(movie.getId())
            if int(movie.getId()) < 1:
                errors.append('Id-ul trebuie sa fie un numar mai mare decat 0')
        except ValueError:
            errors.append("Id-ul trebuie sa fie un numar")
        if len(movie.getTitlu().split()) < 1:
            errors.append('Titlul are cel putin un cuvant')
        if len(movie.getGen().split(', ')) > 1:
            g = movie.getGen().split(', ')
            for elem in g:
                if elem.lower() not in ['actiune', 'comedie', 'sf', 'romantic', 'thriller', 'family', 'drama']:
                    errors.append('Nu toate genurile se afla in lista acceptata de genuri')
        elif movie.getGen().lower() not in ['actiune', 'comedie', 'sf', 'romantic', 'thriller', 'family', 'drama']:
            errors.append('Genul nu se afla in lista acceptata de genuri')

        if len(errors) > 0:
            error_string = '\n'.join(errors)
            raise ValidationException(error_string)


class ClientValidator:
    """
    clasa pentru incapsularea algoritmului de validare
    """
    def validate(self, client):
        errors = []
        try:
            n = int(client.getId())
            if int(client.getId()) < 1:
                errors.append('Id-ul trebuie sa fie un numar mai mare decat 0')
        except ValueError:
            errors.append("Id-ul trebuie sa fie un numar")
        if len(client.getNume().split()) < 2:
            errors.append('Numele trebuie sa aiba cel putin 2 cuvinte')
        if len(client.getCNP()) != 13:
            errors.append('CNP-ul trebuie sa aiba 13 caractere')
        if len(errors) > 0:
            error_string = '\n'.join(errors)
            raise ValidationException(error_string)

