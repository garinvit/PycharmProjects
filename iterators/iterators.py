import json
import hashlib

with open('countries.json') as file:
    COUNTRIES = json.load(file)


class WikiCountries:

    def __init__(self):
        self.url = 'https://en.wikipedia.org/wiki/'
        self.iter_countries = COUNTRIES.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        country = self.iter_countries.__next__()['name']['official']
        country_link = f"{country} : {self.url + country.replace(' ', '_')}\n"
        with open('country-wiki.txt', 'a') as f:
            f.write(country_link)
        return {country: country_link}


def hash_line(fp):
    with open(fp) as file:
        while True:
            encode_line = file.readline().encode()
            if not encode_line:
                break
            line_md5 = hashlib.md5(encode_line)
            yield line_md5.hexdigest()


def main():
    list(WikiCountries())
    for line in hash_line('country-wiki.txt'):
        print(line)


if __name__ == '__main__':
    main()
